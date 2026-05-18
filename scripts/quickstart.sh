#!/usr/bin/env bash
# GamePiLot — Quickstart (instala tudo e cria atalhos)
# Uso: ./quickstart.sh

set -e

echo "🎮 GamePiLot Quickstart"
echo "======================"
echo ""

# 1. Dependências do sistema
if [ -x "./install-deps.sh" ]; then
    echo "[1/3] Instalando Wine/Winetricks..."
    bash ./install-deps.sh
else
    echo "⚠️  install-deps.sh não encontrado"
fi

# 2. Python dependencies + atalho
if [ -f "./setup.py" ]; then
    echo "[2/3] Instalando dependências Python e criando atalho..."
    python3 setup.py
else
    echo "⚠️  setup.py não encontrado"
fi

# 3. Build opcional
echo "[3/3] Build opcional com PyInstaller? (s/N)"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    ./build.sh
fi

echo ""
echo "✅ Ready!"
echo ""
echo "Para executar:"
echo "  source .venv/bin/activate && python -m gamepilot"
echo "  ou: ./dist/gamepilot (após build)"
echo ""
echo "Atalhos criados em:"
echo "  ~/.local/share/applications/gamepilot-*.desktop"
echo ""
