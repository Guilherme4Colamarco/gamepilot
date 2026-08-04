"""scanner — detecção simplificada de jogos Steam e Heroic."""

import json
import os
from pathlib import Path
from typing import Optional, List
from .models import ScannerResult


def find_steam_dir() -> Optional[Path]:
    """Detecta instalação do Steam."""
    home = Path.home()
    paths = [
        home / ".steam" / "steam",
        home / ".local" / "share" / "Steam",
        home / ".var" / "app" / "com.valvesoftware.Steam" / ".local" / "share" / "Steam",
    ]
    for p in paths:
        if p.exists() and p.is_dir():
            return p
    return None


def parse_acf(path: Path) -> Optional[dict]:
    """Parsa arquivo ACF do Steam (formato key-value)."""
    data = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        
        # Find all "key" "value" pairs (handle both simple and quoted values)
        # This regex looks for patterns like: "key" "value" or "key" value
        import re
        pattern = r'\"([^\"]*)\"\s*\"([^\"]*)\"'
        matches = re.findall(pattern, content)
        
        for key, value in matches:
            data[key] = value
            
        return data if data else None
    except Exception:
        return None


_SYSTEM_KEYWORDS = (
    "runtime", "proton", "redistributable", "shared",
    "sdk", "tool", "common", "steamworks", "linuxruntime",
    "sniper", "soldier", "scout",
)


def _is_system_app(name: str, appid: int, installdir: str = "") -> bool:
    """Filtra apps do Steam que não são jogos (runtimes, proton, etc.).

    A heurística é baseada em substrings do ``name`` e ``installdir`` — não
    mantemos uma lista hardcoded de ``appid``\\s porque ela vira dívida a cada
    versão nova de Proton/runtime que a Valve publica.
    """
    haystack = (name + " " + installdir).lower()
    return any(kw in haystack for kw in _SYSTEM_KEYWORDS)


def scan_steam_games() -> List[ScannerResult]:
    """Escaneia jogos Steam instalados (separando runtimes/proton/etc.)."""
    steam_dir = find_steam_dir()
    if not steam_dir:
        return []

    results = []
    steamapps = steam_dir / "steamapps"
    if not steamapps.exists():
        return []

    for acf in steamapps.glob("appmanifest_*.acf"):
        info = parse_acf(acf)
        if not info:
            continue
        name = info.get("name")
        appid_str = info.get("appid")
        if not name or not appid_str:
            continue
        appid = int(appid_str)
        installdir = info.get("installdir", "")

        # Filtra apps de sistema antes de adicionar
        if _is_system_app(name, appid, installdir):
            continue
            
        prefix = steamapps / f"compatdata/{appid}/pfx"
        results.append(
            ScannerResult(
                name=name,
                prefix_path=prefix if prefix.exists() else None,
                steam_app_id=appid,
                source="steam",
            )
        )
    return results


def find_heroic_dir() -> Optional[Path]:
    """Detecta instalação do Heroic Games Store."""
    home = Path.home()
    candidates = [home / ".config" / "heroic"]
    for p in candidates:
        if p.exists():
            return p
    return None


def _heroic_prefix_for_game(heroic_dir: Path, game: dict) -> Optional[Path]:
    candidates: list[str] = []
    for key in ("install_path", "prefix", "prefixPath", "winePrefix", "prefix_path"):
        value = game.get(key)
        if isinstance(value, str) and value:
            candidates.append(value)
    app_name = game.get("app_name") or game.get("AppName") or game.get("title") or ""
    if app_name:
        candidates.append(app_name)
    for rel in candidates:
        p = Path(os.path.expanduser(rel))
        if not p.is_absolute():
            for base in [heroic_dir, heroic_dir.parent, Path.home() / "Games" / "Heroic"]:
                cand = base / rel
                if cand.exists():
                    return cand
        elif p.exists():
            return p
    return None


_HEROIC_LIBRARY_FILES = (
    # Formato moderno (Heroic >= 2.x): um arquivo por store em store_cache/
    ("store_cache/legendary_library.json", "epic"),
    ("store_cache/gog_library.json", "gog"),
    ("store_cache/nile_library.json", "amazon"),
    ("sideload_apps/library.json", "sideload"),
    # Formato antigo (compat): mantido para Heroic 1.x ou instalações pre-migração.
    ("library.json", ""),
)


def _is_heroic_dlc(game: dict) -> bool:
    """DLCs aparecem misturados na biblioteca — filtra para não poluir a lista."""
    install = game.get("install") or {}
    return bool(install.get("is_dlc") or game.get("is_dlc"))


def _heroic_game_title(game: dict) -> Optional[str]:
    return game.get("title") or game.get("name") or game.get("app_title") or game.get("AppName")


def scan_heroic_games() -> List[ScannerResult]:
    """Escaneia jogos Heroic (GOG/Epic/Amazon/Sideloaded).

    Formato moderno do Heroic guarda cada store em um JSON separado dentro
    de ``store_cache/``, com ``runner`` indicando a origem. O campo
    ``is_installed`` filtra jogos não-baixados; ``install.is_dlc`` filtra DLCs.
    """
    heroic_dir = find_heroic_dir()
    if not heroic_dir:
        return []

    results: List[ScannerResult] = []
    seen: set[str] = set()

    for relpath, hint_runner in _HEROIC_LIBRARY_FILES:
        lib_file = heroic_dir / relpath
        if not lib_file.exists():
            continue
        try:
            with open(lib_file) as f:
                data = json.load(f)
        except Exception:
            continue

        if isinstance(data, dict):
            games = data.get("games") or data.get("library") or data.get("items") or []
        elif isinstance(data, list):
            games = data
        else:
            continue

        for game in games:
            if not isinstance(game, dict):
                continue
            if not game.get("is_installed", False):
                continue
            if _is_heroic_dlc(game):
                continue
            title = _heroic_game_title(game)
            if not title or title in seen:
                continue
            seen.add(title)
            runner = (game.get("runner") or hint_runner or game.get("platform") or "").lower()
            results.append(
                ScannerResult(
                    name=title,
                    prefix_path=_heroic_prefix_for_game(heroic_dir, game),
                    steam_app_id=None,
                    source=f"heroic-{runner}" if runner else "heroic",
                )
            )
    return results


async def scan_all_games() -> List[ScannerResult]:
    """Interface async para scan (executa em thread pool)."""
    import asyncio
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: scan_steam_games() + scan_heroic_games()
    )
