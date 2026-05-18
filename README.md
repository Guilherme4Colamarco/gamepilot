# GamePiLot

**Gerenciador de mods para jogos Windows no Linux** — conversão total para Python.

Aplicação TUI (Text User Interface) que detecta jogos Steam/Heroic, instala dependências via winetricks, baixa ferramentas de modding do Nexus Mods e permite lançar as ferramentas diretamente. Tudo em um só lugar, com atalhos de desktop.

---

## Estado atual

✅ Protótipo funcional completo — todos módulos implementados e sintaxe validada  
✅ UI TUI com 4 botões: Scan, Install Dependencies, Launch Tool, Create Shortcut  
✅ Atalhos .desktop automáticos (menu + desktop)  
✅ Suporte a `--game "Nome"` para abrir direto no jogo  
✅ Internacionalização (EN/PT/ES/IT/RU)  
✅ Empacotamento com PyInstaller (binário ~30MB)  

---

## Plug & Play — Primeira vez

### 1. Dependências do sistema (Wine)

```bash
# No Linux Mint/Ubuntu/Debian/Arch:
./scripts/install-deps.sh
```

Isso instala `wine` e `winetricks`. Se já tiver, pula.

### 2. Dependências Python + atalho

```bash
# primeira vez apenas:
make setup
```

Isso:
- Cria virtualenv em `.venv/`
- Instala `textual`, `pydantic`, `aiohttp`, etc.
- Gera um atalho no menu e na área de trabalho

### 3. Executar

```bash
# Modo desenvolvimento
source .venv/bin/activate
python -m gamepilot

# Ou binário empacotado (após make build)
./dist/gamepilot
```

---

## Uso — Fluxo rápido

1. **Scan** — pressione `Scan Games` para detectar jogos instalados (Steam/Heroic)
2. **Selecione** — clique no jogo na tabela
3. **Ferramenta** — escolha a modding tool no dropdown
4. **Install Dependencies** — baixa dependências winetricks + ferramenta Nexus (ou abre browser)
5. **Launch Tool** — executa a ferramenta dentro do Wine prefix
6. **Create Shortcut** — cria ícone na área de trabalho para abrir o GamePiLot já com esse jogo selecionado

---

## CLI

```
gamepilot --game "Skyrim"   # Abre direto no jogo
gamepilot                   # UI normal
```

---

## Estrutura do projeto

```
gamepilot-py/
├── gamepilot/               # pacote principal
│   ├── __init__.py
│   ├── __main__.py          # python -m gamepilot
│   ├── models.py            # Pydantic: GameManifest, ModTool, ScannerResult
│   ├── config.py            # platformdirs, config.toml
│   ├── i18n.py              # dicionários EN/PT/ES/IT/RU
│   ├── wine.py              # async winetricks wrapper + error extraction
│   ├── nexus.py             # aiohttp client (Nexus Mods API)
│   ├── scanner.py           # detecção Steam/Heroic
│   ├── manifests.py         # TOML loader + deduplicação (suporta [[tools]] e [tools.slug])
│   ├── ui/
│   │   ├── app.py           # Textual TUI (botões, log, tables)
│   │   └── __init__.py
│   └── utils/
│       └── shortcuts.py     # .desktop creation + wine command builder
├── manifests/               # manifestos de jogos (system)
│   ├── skyrim.toml
│   ├── witcher3.toml
│   └── gtav.toml
├── scripts/                 # scripts de build/deploy/utilidades
│   ├── install-deps.sh      # instalador Wine/Winetricks
│   ├── build.sh             # PyInstaller onefile builder
│   ├── quickstart.sh        # setup rápido
│   ├── healthcheck.py       # verificação de saúde
│   └── verify_structure.py  # verificador de estrutura
├── examples/                # exemplos e demos
│   └── demo.py
├── tests/                   # pytest unitários
├── assets/
│   ├── icon.svg
│   └── README.txt
├── setup.py                 # instala Python deps + primeiro atalho
├── Makefile                 # atalhos: make setup/run/build/test
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

---

## Manifestos

Formato TOML (suporta lista de ferramentas `[[tools]]` ou dicionário `[tools.slug]`):

```toml
name = "The Elder Scrolls V: Skyrim"

[identifiers]
# Steam AppID (preferido) ou substring match
steam_app_id = 72850

[[tools]]
name = "Mod Organizer 2"
description = "Mod manager para Skyrim"
winetricks = ["vcrun2019", "dotnet48"]
download_url = "https://github.com/.../MO2.exe"
executable_path = "drive_c/ModOrganizer/ModOrganizer.exe"
```

O parser converte automaticamente `[[tools]]` para dicionário internamente.

- Pasta do usuário: `~/.config/gamepilot/manifests/` (sobrescreve system)
- `steam_app_id` tem prioridade sobre nome

---

## Testes

```bash
pytest tests/ -v
```

Cobertura: `extract_real_error`, `shortcuts`, `i18n`, `scanner` match.

---

## Empacotamento

```bash
make build    # gera dist/gamepilot (~30MB, standalone)
```

O binário busca manifestos em `../manifests` relativo à sua localização.

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `wine: command not found` | rode `./install-deps.sh` |
| `shortcut não aparece no menu` | execute `update-desktop-database ~/.local/share/applications/` |
| App inicia mas não detecta jogos | Verifique Steam em `~/.steam/steam/steamapps/common` |
| Falha download Nexus | Chave API necessária: configure em `~/.config/gamepilot/config.toml` |

---

## Migração do Rust original

- Código Rust mantido em `/home/geko/Projetos/gamePiLot/` (referência)
- Port total ~800 linhas Python vs ~2000 Rust
- Sem `std::thread::spawn` — `asyncio` nativo
- Sem `gtk-rs` — `textual` TUI
- `Pydantic` substitui structs + `serde`

---

**Feito por Guilherme — 2026** — Convertido de Rust/GTK3 para Python/Textual, simplificando radicalmente a manutenção e empacotamento.
