# GamePiLot — Arquitetura TUI Python

## Visão geral

```
┌─────────────────────────────────────────────────────────────┐
│                         UI TUI (Textual)                   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Games     │  │   Tools      │  │      Log         │
│  │   Table     │◄─┤   Select    │◄─┤  (scrollable)    │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
│        │                 │                  │             │
│        │   on_button_pressed (scan/install/launch/)       │
│        │                 │                  │             │
│        ▼                 ▼                  ▼             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            GamePiLotApp (Controller)               │  │
│  │  • selected_game / selected_tool                    │  │
│  │  • scanner.scan_all_games()                         │  │
│  │  • wine.install_dependencies()  (async subprocess)  │  │
│  │  • shortcuts.create_desktop_file()                  │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ Steam/Heroic │   │  Wine/Winetricks │ │  Nexus API  │
    │  scanner     │   │  install deps    │ │  download   │
    └──────────────┘   └──────────────┘   └──────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ games.toml   │   │  Wine Prefix │   │  mods.nexus  │
    │ (manifests)  │   │   (drive_c)  │   │  mods/       │
    └──────────────┘   └──────────────┘   └──────────────┘
```

## Módulos

| Módulo | Responsabilidade | Tecnologia |
|--------|-----------------|------------|
| `models.py` | Entidades: GameManifest, ModTool, ScannerResult | Pydantic |
| `i18n.py` | Traduções EN/PT/ES/IT/RU, `t()` global | dict + LANG env |
| `config.py` | `~/.config/gamepilot/config.toml` + platformdirs | Toml + Paths |
| `scanner.py` | Detecta instalados Steam/Heroic/Epic | pathlib + json |
| `manifests.py` | Carrega `manifests/*.toml` + dedup por slug | toml parser |
| `wine.py` | `winetricks` async + `extract_real_error()` | asyncio.subprocess |
| `nexus.py` | Nexus Mods API (validate_key, get_latest_file) | aiohttp |
| `ui/app.py` | Textual App — compose, event loop, handlers | textual.widgets |
| `utils/shortcuts.py` | Gera .desktop, update-desktop-database | subprocess |

## Fluxo de instalação de ferramenta

```
User clica "Install Dependencies"
      │
      ▼
App. do_install()
      │
      ├─► wine.install_dependencies(prefix, deps, url)
      │       │
      │       ├─► se URL ausente: usa Nexus API
      │       │       └─► nexus.validate_key() → download_tool()
      │       │
      │       └─► else: winetricks apenas (deps locais)
      │
      └─► UI Log: InstallResult { INSTALLED, DELEGATED_TO_BROWSER, FAILED }
```

## Fluxo de lançamento de ferramenta

```
User clica "Launch Tool"
      │
      ▼
App.do_launch()
      │
      ├─► Valida: jogo selecionado + tool.executable_path
      ├─► full_exe = prefix / "drive_c" / executable_path
      └─► subprocess.Popen(["wine", str(full_exe)], env={WINEPREFIX: prefix})
```

## Atalhos

- `create_desktop_file()` em `utils/shortcuts.py`
- Escreve em `~/.local/share/applications/gamepilot-<game>.desktop`
- `Exec=` detecta `dist/gamepilot` (binário compilado) ou `python3 -m gamepilot`
- Suporta `--game "Nome"` para abrir direto no jogo
- `update-desktop-database` atualiza cache do menu

## Threading / Concurrency

- **UI thread**: Textual (single-threaded, async event loop)
- **Worker tasks**: `asyncio.create_task(scan)` — não bloqueia UI
- **Wine install**: `asyncio.create_subprocess_exec()` + pipe reader async
- **Nexus download**: `aiohttp` session (um Client por app lifecycle)

## Configuração

```
~/.config/gamepilot/
├── config.toml       # API key Nexus, cached_games
└── manifests/        # ~/custom/*.toml sobrepõem system/manifests/
```

## Manifestos

Formato TOML compatível com o original Rust:

```toml
name = "Skyrim"

[identifiers]
steam_app_id = 72850    # 100 pts匹配
# ou substring nome (10 pts) — menosconfiável

[[tools]]
name = "MO2"
description = "Mod Organizer 2"
winetricks = ["vcrun2019", "dotnet48"]
download_url = "https://.../MO2.exe"
executable_path = "drive_c/ModOrganizer2/ModOrganizer.exe"
```

---

**Python 3.11+ | Textual TUI | Asyncio | Pydantic | 100% type hints**
