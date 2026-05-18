# GamePiLot

**Gerenciador de mods para jogos Windows no Linux**, reescrito em **Python + Textual**.

O GamePiLot detecta jogos instalados no Linux, ajuda a instalar dependências com *winetricks*, baixa ferramentas de modding via Nexus Mods e cria atalhos `.desktop` para abrir tudo com menos atrito.

## O que ele faz

- escaneia instalações de jogos em Steam e Heroic
- instala dependências do prefixo Wine
- integra com Nexus Mods para baixar ferramentas de modding
- cria atalhos no menu e na área de trabalho
- oferece interface TUI com Textual
- suporta i18n: **EN / PT / ES / IT / RU**
- empacota em binário standalone com PyInstaller

## Requisitos

### Sistema

- Python 3.11+
- `wine`
- `winetricks`

Para instalar os pacotes do sistema:

```bash
make install
# ou
bash scripts/install-deps.sh
```

### Python

O setup cria o ambiente virtual e instala as dependências do projeto.

## Instalação rápida

```bash
make setup
```

Isso faz:

- cria `.venv/`
- instala dependências Python
- cria um wrapper global em `~/.local/bin/gamepilot`
- gera o atalho inicial do aplicativo

## Como executar

Depois do setup, você pode usar qualquer uma destas formas:

```bash
gamepilot
# ou
make run
# ou
source .venv/bin/activate
python -m gamepilot
# ou
python run.py
```

## Fluxo de uso

1. abra o GamePiLot
2. pressione **Scan** para encontrar jogos instalados
3. selecione o jogo na tabela
4. escolha a ferramenta/mod manager
5. use **Install** para preparar dependências
6. use **Launch** para abrir a ferramenta no prefixo correto
7. use **Shortcut** para criar um atalho pronto para uso

## Configuração

### Manifestos

Os manifestos de jogos ficam em:

- sistema: `manifests/`
- usuário: `~/.config/gamepilot/manifests/`

O formato é TOML e suporta ferramentas por lista ou por mapa.

Exemplo:

```toml
name = "The Elder Scrolls V: Skyrim"

[identifiers]
steam_app_id = 72850

[[tools]]
name = "Mod Organizer 2"
description = "Mod manager para Skyrim"
winetricks = ["vcrun2019", "dotnet48"]
download_url = "https://example.com/mo2.exe"
executable_path = "drive_c/ModOrganizer/ModOrganizer.exe"
```

### Build e empacotamento

```bash
make build
```

Isso gera o binário em `dist/gamepilot`.

## Testes

```bash
make test
# ou
python -m pytest tests/ -v
```

## Estrutura principal

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

## Desenvolvimento

- `make setup` — instala tudo para começar
- `make install` — instala dependências do sistema
- `make run` — roda a TUI
- `make test` — executa os testes
- `make build` — empacota com PyInstaller
- `make clean` — remove artefatos gerados

## Status do projeto

- rewrite total para Python concluído
- TUI funcional com Textual
- suíte de testes passando
- pronto para evolução incremental

## Licença

MIT

---

Feito por **Guilherme**.
