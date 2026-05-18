"""Testes unitários para shortcuts (sem dependências externas)."""

import tempfile
from pathlib import Path
from unittest.mock import patch

# Carregar o módulo shortcuts diretamente (sem passar por gamepilot.__init__,
# que arrasta pydantic/textual). Path resolvido relativo ao próprio teste.
import importlib.util
_SHORTCUTS_PATH = Path(__file__).resolve().parent.parent / "gamepilot" / "utils" / "shortcuts.py"
spec = importlib.util.spec_from_file_location("shortcuts", _SHORTCUTS_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load shortcuts module")
shortcuts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shortcuts)


def test_create_desktop_file_basic():
    with tempfile.TemporaryDirectory() as tmp:
        desktop_dir = Path(tmp) / "applications"
        desktop_dir.mkdir(parents=True)
        with patch.object(shortcuts, 'XDG_DATA_HOME', Path(tmp)):
            out = shortcuts.create_desktop_file(
                "TestApp",
                game_name="TestGame"
            )
            assert out.exists()
            content = out.read_text()
            assert "Name=TestApp" in content
            # Verifica exec (binário ou fallback python)
            assert ("dist/gamepilot" in content or "-m gamepilot" in content or "/gamepilot" in content)
            assert "--game" in content
            assert "TestGame" in content
            assert "Terminal=true" in content


def test_create_desktop_file_no_game():
    with tempfile.TemporaryDirectory() as tmp:
        with patch.object(shortcuts, 'XDG_DATA_HOME', Path(tmp)):
            out = shortcuts.create_desktop_file("TestApp")
            content = out.read_text()
            # Verifica exec (binário ou fallback python)
            assert ("dist/gamepilot" in content or "-m gamepilot" in content or "/gamepilot" in content)
            assert "--game" not in content


def test_build_wine_command():
    # Criar prefix fake com arquivo executável
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp)
        exe_dir = prefix / "drive_c" / "Program Files"
        exe_dir.mkdir(parents=True)
        (exe_dir / "MyTool.exe").write_text("")

        class MockTool:
            executable_path = "Program Files/MyTool.exe"

        result = shortcuts.build_wine_command(prefix, MockTool())
        assert result[0] == "wine"
        assert "MyTool.exe" in result[1]


def test_build_wine_command_accepts_drive_c_prefixed_path():
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp)
        exe_dir = prefix / "drive_c" / "Program Files"
        exe_dir.mkdir(parents=True)
        (exe_dir / "MyTool.exe").write_text("")

        class MockTool:
            executable_path = "drive_c/Program Files/MyTool.exe"

        result = shortcuts.build_wine_command(prefix, MockTool())
        assert result == ["wine", str(exe_dir / "MyTool.exe")]
