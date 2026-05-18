# GamePiLot

```text
╔══════════════════════════════════════╗
║  GAMEPILOT — VIBE CODING EDITION     ║
╚══════════════════════════════════════╝
```

> ⚠️ **Vibe coding disclaimer**
>
> This project was built in fast iteration loops. Docs can lag behind the code, and the code can change quickly when the idea improves.
>
> If you want the exact behavior, read the source files.

**Read in other languages:** [Português](README.pt-BR.md) · [English](README.en.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

**A mod manager for Windows games on Linux**, rewritten in **Python + Textual**.

GamePiLot detects installed games on Linux, helps install dependencies with *winetricks*, downloads modding tools through Nexus Mods, and creates `.desktop` shortcuts so you can launch everything with less friction.

## What it does

- scans game installs from Steam and Heroic
- installs Wine prefix dependencies
- integrates with Nexus Mods to fetch modding tools
- creates launcher shortcuts for menu and desktop
- provides a Textual TUI
- supports i18n: **EN / PT / ES / IT / RU**
- packages as a standalone binary with PyInstaller

## Quick install

```bash
make setup
```

This will:

- create `.venv/`
- install Python dependencies
- create a global wrapper at `~/.local/bin/gamepilot`
- generate the initial app shortcut

## How to run

After setup, you can use any of these:

```bash
gamepilot
# or
make run
# or
source .venv/bin/activate
python -m gamepilot
# or
python run.py
```

## Supported languages

The UI follows `LANG`:

- `pt*` → Português
- `en*` → English
- `es*` → Español
- `it*` → Italiano
- `ru*` → Русский

## Main features

- Steam / Heroic game detection
- Wine dependency installation
- Nexus Mods integration
- `.desktop` shortcut generation
- PyInstaller packaging
- Textual-based TUI

## Build and tests

```bash
make build
make test
```

## Core structure

```text
gamepilot/
├── __main__.py
├── ui/
├── scanner.py
├── wine.py
├── nexus.py
├── manifests.py
├── models.py
└── utils/
```

## License

MIT

---

Made by **Guilherme**.
