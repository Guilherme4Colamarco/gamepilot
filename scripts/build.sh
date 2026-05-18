#!/usr/bin/env bash
# build.sh — Empacota GamePiLot em binário standalone com PyInstaller

set -e

echo "📦 GamePiLot Build Script"
echo "=========================="

# Detecta diretório do projeto (pai do diretório deste script)
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR=$(dirname "$SCRIPT_DIR")

# Usa o venv do projeto (criado pelo setup.py)
VENV_PIP="$PROJECT_DIR/.venv/bin/pip"
VENV_PYINSTALLER="$PROJECT_DIR/.venv/bin/pyinstaller"

if [ ! -f "$VENV_PIP" ]; then
    echo "❌ Virtualenv não encontrado em $PROJECT_DIR/.venv"
    echo "   Rode primeiro: python3 setup.py"
    exit 1
fi

# Verifica pyinstaller no venv
if ! "$VENV_PIP" show pyinstaller &>/dev/null; then
    echo "Instalando PyInstaller no venv..."
    "$VENV_PIP" install pyinstaller
fi

# Clean previous builds
rm -rf "$PROJECT_DIR/build" "$PROJECT_DIR/dist" "$PROJECT_DIR/gamepilot.spec"

# Build
echo "Building..."
cd "$PROJECT_DIR"
"$VENV_PYINSTALLER" --onefile \
    --name gamepilot \
    --icon assets/icon.svg \
    --add-data "gamepilot:i18n" \
    --add-data "manifests:manifests" \
    run.py

echo "✅ Binary criado em dist/gamepilot"
echo "   Tamanho: $(du -h dist/gamepilot | cut -f1)"
