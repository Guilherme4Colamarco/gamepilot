"""Ações da UI desacopladas da Textual — async + log callback.

Cada ação recebe ``log_fn: Callable[[str], None]`` em vez de um widget Log,
para que possam ser testadas sem montar a TUI.
"""

from pathlib import Path
from typing import Callable, Optional

from .. import wine, config
from ..models import ModTool, ScannerResult
from ..i18n import t
from ..utils import shortcuts


LogFn = Callable[[str], None]


async def install_tool_action(
    game: Optional[ScannerResult],
    tool: Optional[ModTool],
    log: LogFn,
) -> wine.InstallResult:
    """Instala dependências (winetricks) e roda o instalador da ferramenta."""
    if not game or not tool:
        log("❌ " + t("no_game_selected"))
        return wine.InstallResult.FAILED
    prefix = game.prefix_path
    if not prefix:
        log(t("no_wine_prefix"))
        return wine.InstallResult.FAILED

    log(t("installing_dependencies"))
    result = await wine.install_dependencies(
        prefix=str(prefix),
        dependencies=tool.winetricks,
        download_url=tool.download_url,
        nexus_game_domain=tool.nexus_game_domain,
        nexus_mod_id=tool.nexus_mod_id,
        nexus_api_key=config.load_config().nexus_api_key,
        progress_callback=log,
        install_type=tool.install_type,
        extract_to=tool.extract_to,
        asset_pattern=tool.asset_pattern,
    )
    if result == wine.InstallResult.INSTALLED:
        log(t("dependencies_installed"))
    elif result == wine.InstallResult.DELEGATED_TO_BROWSER:
        log(t("install_delegated_browser"))
    else:
        log(t("install_failed"))
    return result


async def launch_tool_action(
    game: Optional[ScannerResult],
    tool: Optional[ModTool],
    log: LogFn,
) -> int:
    """Executa a ferramenta via wine dentro do prefix do jogo. Retorna o rc."""
    if not game or not tool:
        log("❌ " + t("no_game_selected"))
        return 1
    prefix = game.prefix_path
    if not prefix:
        log(t("no_wine_prefix"))
        return 1
    cmd = shortcuts.build_wine_command(prefix, tool)
    if not cmd:
        log("❌ Executable not found.")
        return 1
    log(f"🚀 Launching: {cmd}")
    rc, _out, err = await wine.run_command(cmd, env={"WINEPREFIX": str(prefix)})
    if rc != 0:
        error_msg = wine.extract_real_error(err) or "Launch failed"
        log(f"⚠️ {error_msg}")
    else:
        log("✅ Tool launched.")
    return rc


def create_shortcut_action(
    game: Optional[ScannerResult],
    log: LogFn,
) -> Optional[Path]:
    """Cria atalho .desktop para o jogo. Retorna o path criado ou None se falhou."""
    if not game:
        log("❌ " + t("no_game_selected"))
        return None
    try:
        p = shortcuts.create_desktop_file(game.name, game_name=game.name)
        shortcuts.create_menu_entry(p)
        log(f"✅ Shortcut created: {p}")
        return p
    except Exception as e:
        log(f"❌ Failed to create shortcut: {e}")
        return None


def tools_for_game(game: ScannerResult, manifests: list) -> list:
    """
    Retorna ferramentas associadas a um jogo, em ordem de confiança:
     1. steam_app_id exato
     2. nome completo exato (case-insensitive)
     3. word-boundary match — manifest name como palavra(s) inteira(s) no nome do jogo

    A regra 3 usa word-boundary (em vez de substring puro) para evitar
    que ``"Half-Life"`` case com ``"Half-Life 2"`` ou ``"Counter-Strike"``
    com ``"Counter-Strike: Source"`` de forma incorreta.
    """
    import re

    steam_id = game.steam_app_id
    game_name_lower = game.name.lower()

    tools: list = []
    seen: set[str] = set()

    for m in manifests:
        matched = False
        manifest_name_lower = m.name.lower()

        if steam_id and m.identifiers and m.identifiers.steam_app_id == steam_id:
            matched = True
        elif game_name_lower == manifest_name_lower:
            matched = True
        else:
            # Word boundary: o nome do manifesto precisa aparecer como palavra inteira.
            # `re.escape` cobre caracteres especiais como ':' ou '.'.
            pattern = r"\b" + re.escape(manifest_name_lower) + r"\b"
            if re.search(pattern, game_name_lower):
                matched = True

        if matched:
            for tool in m.tools.values():
                if tool.name not in seen:
                    seen.add(tool.name)
                    tools.append(tool)
    return tools
