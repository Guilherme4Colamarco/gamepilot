"""utils — helper functions para shortcuts, paths, etc."""

import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import ModTool


def _find_executable() -> str:
    """Procura executavel do GamePiLot (binario empacotado ou modulo)."""
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).resolve())

    project_root = Path(__file__).resolve().parents[2]
    console_script = project_root / ".venv" / "bin" / "gamepilot"
    if console_script.exists() and console_script.is_file():
        return str(console_script.resolve())

    binary_candidates: list[Path] = [
        project_root / "dist" / "gamepilot",
        Path(__file__).resolve().parents[3] / "dist" / "gamepilot",
    ]
    for candidate in binary_candidates:
        if candidate.exists() and candidate.is_file():
            return str(candidate.resolve())

    python_candidates: list[Path] = [
        Path(__file__).resolve().parents[2] / ".venv" / "bin" / "python",
        Path(sys.executable),
    ]
    for candidate in python_candidates:
        if candidate.exists() and candidate.is_file():
            return f'"{candidate.resolve()}" -m gamepilot'
    return f'"{sys.executable}" -m gamepilot'


# Caminhos XDG
XDG_DATA_HOME = Path(
    os.environ.get("XDG_DATA_HOME", "~/.local/share")
).expanduser()


def create_desktop_file(app_name: str, icon_path: Optional[Path] = None, game_name: str | None = None) -> Path:
    """Cria entrada .desktop em ~/.local/share/applications."""
    desktop_dir = XDG_DATA_HOME / "applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)

    safe_name = app_name.lower().replace(" ", "-")
    desktop_path = desktop_dir / f"gamepilot-{safe_name}.desktop"

    # Icone padrao
    icon = str(icon_path) if icon_path else "/usr/share/pixmaps/gpilot.png"

    # Executavel: prefere binario compilado em dist/, senao usa modulo Python
    exe_cmd = _find_executable()

    if game_name:
        exe_cmd = f"{exe_cmd} --game {shlex.quote(game_name)}"

    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment=GamePiLot — Ferramenta de Modding
Exec={exe_cmd}
Icon={icon}
Terminal=true
Categories=Game;Utility;
"""
    desktop_path.write_text(content)
    desktop_path.chmod(0o755)
    return desktop_path


def _update_exec_line(desktop_path: Path, new_exec: str) -> None:
    """Atualiza a linha Exec= de um arquivo .desktop de forma estruturada."""
    lines = desktop_path.read_text().splitlines(keepends=True)
    new_lines = []
    for line in lines:
        if line.startswith("Exec="):
            new_lines.append(f"Exec={new_exec}")
        else:
            new_lines.append(line.rstrip("\n"))
    desktop_path.write_text("\n".join(new_lines) + "\n")


def create_menu_entry(desktop_path: Path) -> bool:
    """Registra o .desktop no menu (update-desktop-database)."""
    try:
        subprocess.run(["update-desktop-database", str(desktop_path.parent)], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"[WARN] failed to create menu entry: {e}")
        return False


def get_wine_executable(game_prefix: Path, tool: "ModTool") -> Path:
    """Retorna o caminho para wine ou wine64 no prefix."""
    system32 = game_prefix / "drive_c" / "windows" / "system32"
    wine64 = system32 / "wine64.exe"
    if wine64.exists():
        return wine64
    wine32 = system32 / "wine.exe"
    if wine32.exists():
        return wine32
    # Fallback generico: procurar wine*.exe no system32
    wine_candidates = list(system32.glob("wine*.exe"))
    if wine_candidates:
        return wine_candidates[0]
    raise FileNotFoundError("wine.exe not found in prefix")


def build_wine_command(game_prefix: Path, tool: "ModTool") -> list[str]:
    """Monta comando 'wine' para executar uma ferramenta dentro do prefix."""
    if not tool.executable_path:
        return []
    relative_exe = Path(tool.executable_path)
    full_exe = game_prefix / relative_exe if relative_exe.parts[:1] == ("drive_c",) else game_prefix / "drive_c" / relative_exe
    return ["wine", str(full_exe)] if full_exe.exists() else []
