.PHONY: help install run test lint clean setup build

help:
	@echo "GamePiLot — Gerenciador de mods em Python"
	@echo ""
	@echo " make setup          — instala deps Python + cria atalho (plug & play)"
	@echo " make install        — instala deps do sistema (wine, winetricks)"
	@echo " make run            — executa a aplicação TUI"
	@echo " make test           — roda pytest"
	@echo " make build          — empacota com PyInstaller"
	@echo " make clean          — limpa arquivos temporários"
	@echo ""
	@echo "Após o primeiro setup, use: source .venv/bin/activate && python -m gamepilot"

setup:
	@echo "🎮 GamePiLot Setup..."
	python3 setup.py

install:
	@echo "🔧 Instalando deps do sistema..."
	bash scripts/install-deps.sh

run:
	@echo "🚀 Iniciando GamePiLot..."
	.venv/bin/python -m gamepilot

test:
	@.venv/bin/python -m pytest tests/ -v

build:
	@echo "📦 Empacotando..."
	bash scripts/build.sh

clean:
	rm -rf build dist __pycache__ *.pyc .pytest_cache .venv gamepilot.spec
