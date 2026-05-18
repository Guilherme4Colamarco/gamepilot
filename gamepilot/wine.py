"""wine — async wrapper para winetricks, wget, wine, e extração de erros."""

import asyncio
import json
import os
import re
import shutil
from pathlib import Path
from typing import Optional, Callable, Any
from enum import Enum
from .i18n import t, t_fmt


# Timeouts (segundos). Processos com input do usuário (instalador GUI) ficam sem timeout.
WINETRICKS_TIMEOUT = 1800  # 30min — verbos pesados (vcrun, dotnet) baixam e compilam.
DOWNLOAD_TIMEOUT = 900     # 15min — instaladores típicos são <500MB.


class InstallResult(Enum):
    INSTALLED = "installed"
    DOWNLOADED_ONLY = "downloaded_only"
    DELEGATED_TO_BROWSER = "delegated"
    FAILED = "failed"


def extract_real_error(stderr: str) -> Optional[str]:
    """Filtra ruído do Wine e retorna apenas erros reais."""
    noise_prefixes = [
        "fixme:",
        "warn:",
        "trace:",
        "info:",
        "err:fixme",
        "winediag:",
    ]
    lines = stderr.splitlines()
    real_errors = [
        line for line in lines
        if line.strip()
        and not any(prefix in line.lower() for prefix in noise_prefixes)
    ]
    if not real_errors:
        return None
    return "\n".join(real_errors)


async def run_command(
    cmd: list[str],
    progress_callback: Optional[Callable[[str], Any]] = None,
    env: Optional[dict] = None,
    timeout: Optional[float] = None,
) -> tuple[int, str, str]:
    """Executa comando async, captura stdout/stderr.

    Se ``timeout`` for fornecido e o processo exceder o limite, ele é morto
    (SIGKILL após SIGTERM) e a função retorna ``(124, stdout_parcial, stderr_parcial)``
    — código 124 segue a convenção do utilitário ``timeout(1)``.

    ``env`` é MESCLADO com ``os.environ`` (overrides têm prioridade). Passar
    ``env={"WINEPREFIX": ...}`` sem ``HOME``/``PATH`` quebra winetricks e wget,
    que resolvem ``~`` para ``/`` quando ``HOME`` está ausente.
    """
    merged_env: Optional[dict[str, str]]
    if env is None:
        merged_env = None  # subprocess herda env do parent automaticamente
    else:
        merged_env = {**os.environ, **env}

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=merged_env,
    )
    try:
        if timeout is None:
            stdout, stderr = await proc.communicate()
        else:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        # drena os pipes para liberar fds; ignora qualquer erro pós-kill
        try:
            stdout, stderr = await proc.communicate()
        except Exception:
            stdout, stderr = b"", b""
        return 124, stdout.decode(errors="replace"), stderr.decode(errors="replace")
    out = stdout.decode(errors="replace")
    err = stderr.decode(errors="replace")
    return proc.returncode or 0, out, err


async def check_prerequisites(
    download_url: Optional[str] = None,
    install_type: str = "installer",
) -> list[str]:
    """Verifica apenas as ferramentas necessárias para o fluxo solicitado."""
    missing = []

    tools = ["wine", "winetricks"]
    if download_url:
        tools.append("wget")
        if _GITHUB_LATEST_RE.match(download_url):
            tools.append("curl")

    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)
    return missing


def _archive_tool_for(path: str) -> Optional[str]:
    lower = path.lower()
    if lower.endswith(".zip"):
        return "unzip"
    if lower.endswith(".rar"):
        return "unrar"
    if lower.endswith((".tar.gz", ".tgz", ".tar.xz", ".tar")):
        return "tar"
    if lower.endswith(".7z"):
        return "7z"
    return None


_GITHUB_LATEST_RE = re.compile(
    r"^https?://github\.com/([^/]+)/([^/]+)/releases/latest/?$"
)


async def resolve_download_url(url: str, asset_pattern: Optional[str] = None) -> str:
    """Resolve URLs especiais para o asset real de download.

    - ``github.com/<owner>/<repo>/releases/latest`` → asset do release mais novo,
      consultado via Github API.
      * Se ``asset_pattern`` (regex) for fornecido, escolhe o primeiro asset
        cujo nome casa com o pattern. Se nenhum casar, mantém a URL original
        (sinaliza configuração errada).
      * Sem pattern: escolhe o primeiro asset com extensão de archive comum
        (``.zip``, ``.rar``, ``.tar.gz``, ``.7z``, ``.exe``); fallback para o
        primeiro asset disponível.
    - Demais URLs são retornadas como recebidas (``wget`` já segue redirects HTTP).
    """
    m = _GITHUB_LATEST_RE.match(url)
    if not m:
        return url
    if shutil.which("curl") is None:
        return url
    owner, repo = m.group(1), m.group(2)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    rc, out, _err = await run_command(["curl", "-sSL", api_url], timeout=30)
    if rc != 0:
        return url
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return url
    assets = data.get("assets") or []
    if not assets:
        return url

    if asset_pattern:
        pat = re.compile(asset_pattern)
        for a in assets:
            if pat.search(a.get("name") or ""):
                return a.get("browser_download_url") or url
        # pattern definido mas nenhum asset bateu — preserva URL original
        # para o caller perceber o problema (em vez de baixar asset errado).
        return url

    preferred_exts = (".zip", ".rar", ".tar.gz", ".7z", ".exe")
    for ext in preferred_exts:
        for a in assets:
            name = (a.get("name") or "").lower()
            if name.endswith(ext):
                return a.get("browser_download_url") or url
    return assets[0].get("browser_download_url") or url


async def extract_archive(
    archive_path: str,
    dest_dir: str,
    progress_callback: Optional[Callable[[str], Any]] = None,
) -> bool:
    """Extrai um archive (.zip/.rar/.tar.gz/.7z) em ``dest_dir``.

    Usa ferramentas do sistema host: ``unzip``, ``unrar``, ``tar``, ``7z``.
    Retorna True em sucesso. Cria ``dest_dir`` se não existir.
    """
    cb = progress_callback or (lambda _msg: None)
    Path(dest_dir).mkdir(parents=True, exist_ok=True)

    required_tool = _archive_tool_for(archive_path)
    if required_tool is None:
        cb(f"❌ Formato de archive não suportado: {archive_path}")
        return False
    if shutil.which(required_tool) is None:
        cb(f"❌ Ferramenta ausente para extrair archive: {required_tool}")
        return False

    lower = archive_path.lower()
    if lower.endswith(".zip"):
        cmd = ["unzip", "-o", "-q", archive_path, "-d", dest_dir]
    elif lower.endswith(".rar"):
        cmd = ["unrar", "x", "-o+", "-y", archive_path, dest_dir + "/"]
    elif lower.endswith(".tar.gz") or lower.endswith(".tgz"):
        cmd = ["tar", "-xzf", archive_path, "-C", dest_dir]
    elif lower.endswith(".tar.xz"):
        cmd = ["tar", "-xJf", archive_path, "-C", dest_dir]
    elif lower.endswith(".tar"):
        cmd = ["tar", "-xf", archive_path, "-C", dest_dir]
    elif lower.endswith(".7z"):
        cmd = ["7z", "x", "-y", f"-o{dest_dir}", archive_path]
    else:  # defensive fallback; _archive_tool_for cobre esta validação acima
        cb(f"❌ Formato de archive não suportado: {archive_path}")
        return False

    rc, _out, err = await run_command(cmd, timeout=DOWNLOAD_TIMEOUT)
    if rc != 0:
        cb(f"❌ Falha ao extrair: {extract_real_error(err) or 'erro desconhecido'}")
        return False
    cb(f"✅ Extraído em {dest_dir}")
    return True


async def install_dependencies(
    prefix: str,
    dependencies: list[str],
    download_url: Optional[str] = None,
    nexus_game_domain: Optional[str] = None,
    nexus_mod_id: Optional[int] = None,
    nexus_api_key: Optional[str] = None,
    progress_callback: Optional[Callable[[str], Any]] = None,
    install_type: str = "installer",
    extract_to: Optional[str] = None,
    asset_pattern: Optional[str] = None,
) -> InstallResult:
    """Instala dependências via winetricks e opcionalmente baixa/executa instalador."""
    if progress_callback is None:
        def _noop_progress(msg: str) -> None:  # noqa: ARG005
            pass
        progress_callback = _noop_progress

    progress_callback(t_fmt("preparing", prefix))

    # Pré-requisitos
    prereq_url = download_url
    missing = await check_prerequisites(download_url=prereq_url, install_type=install_type)
    if missing:
        msg = t_fmt("missing_system_deps", ", ".join(missing))
        progress_callback(msg)
        return InstallResult.FAILED

    # Winetricks dependencies
    env = {"WINEPREFIX": str(prefix)} if prefix else None
    for dep in dependencies:
        progress_callback(t_fmt("t_installing_via_winetricks", dep))
        rc, out, err = await run_command(
            ["winetricks", "-q", dep], env=env, timeout=WINETRICKS_TIMEOUT
        )
        if rc == 124:
            progress_callback(t_fmt("t_failed_install", dep, f"timeout após {WINETRICKS_TIMEOUT}s"))
            return InstallResult.FAILED
        if rc != 0:
            error_msg = extract_real_error(err) or "unknown error"
            progress_callback(t_fmt("t_failed_install", dep, error_msg))
            return InstallResult.FAILED
        progress_callback(f"✅ {dep} installed.")

    # Download + install se houver URL
    if not download_url and nexus_game_domain and nexus_mod_id and nexus_api_key:
        from .nexus import NexusClient
        progress_callback(t("nexus_downloading"))
        async with NexusClient(nexus_api_key) as client:
            try:
                latest = await client.get_latest_file(nexus_game_domain, nexus_mod_id)
                download_url = await client.get_download_url(nexus_game_domain, nexus_mod_id, latest["file_id"])
            except Exception:
                return InstallResult.FAILED

    if download_url:
        if shutil.which("wget") is None:
            progress_callback(t_fmt("missing_system_deps", "wget"))
            return InstallResult.FAILED

        resolved_url = await resolve_download_url(download_url, asset_pattern=asset_pattern)
        if resolved_url != download_url:
            progress_callback(f"🔗 Resolvido: {resolved_url}")

        progress_callback(t_fmt("t_downloading", "tool"))
        download_dir = f"{prefix}/drive_c/gamepilot_downloads"

        # Criar diretório
        proc = await asyncio.create_subprocess_exec(
            "mkdir", "-p", download_dir,
        )
        await proc.wait()

        filename = resolved_url.split("/")[-1].split("?")[0] or "installer.exe"
        dest = f"{download_dir}/{filename}"

        rc, out, err = await run_command(
            ["wget", "-q", "--show-progress", "-O", dest, resolved_url],
            timeout=DOWNLOAD_TIMEOUT,
        )
        if rc != 0:
            progress_callback(t_fmt("t_failed_download", filename))
            progress_callback(t("t_redirecting_browser"))
            proc = await asyncio.create_subprocess_exec("xdg-open", download_url)
            await proc.wait()
            return InstallResult.DELEGATED_TO_BROWSER

        progress_callback(f"✅ Download complete: {filename}")

        if install_type == "extract":
            # Fluxo extract-only: descompacta no destino e termina (sem rodar wine).
            target = extract_to or "drive_c/Modding"
            full_target = f"{prefix}/{target}"
            ok = await extract_archive(dest, full_target, progress_callback)
            if not ok:
                return InstallResult.FAILED
        else:
            # Fluxo installer (default): executa o .exe com wine. Sem timeout:
            # instaladores GUI podem ficar aguardando input do usuário.
            progress_callback(t("running_installer"))
            rc, out, err = await run_command(["wine", dest], env=env)
            if rc != 0:
                error_msg = extract_real_error(err)
                if error_msg:
                    progress_callback(f"⚠️ Installer error: {error_msg}")
                else:
                    progress_callback(t("install_failed"))
                return InstallResult.FAILED
            else:
                progress_callback(t("setup_finished"))

    progress_callback(t("finalizing"))
    return InstallResult.INSTALLED
