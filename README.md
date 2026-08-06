# GamePiLot

```text
╔══════════════════════════════════════╗
║  GAMEPILOT — VIBE CODING EDITION     ║
╚══════════════════════════════════════╝
```

> ⚠️ **Vibe coding disclaimer**
>
> Este projeto nasceu em ciclos rápidos de iteração. Isso significa que a documentação pode ficar ligeiramente atrás do código, e o código pode mudar rápido quando a ideia melhorar.
>
> Se quiser o comportamento exato, leia os arquivos fonte.

**Leia em outros idiomas:** [English](README.en.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

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

## Dicas de Uso

- **Steam Deck & Flatpak**: O GamePiLot detecta automaticamente bibliotecas do Steam instaladas via Flatpak ou no caminho padrão do sistema.
- **Winetricks**: Ao selecionar um jogo, o app verifica se as dependências do manifesto (como `.dotnet` ou `vcrun`) estão instaladas no prefixo Wine do jogo.
- **Atalhos**: Os atalhos criados em `~/.local/share/applications` permitem que você lance as ferramentas de modding diretamente do seu menu de aplicativos ou do Modo Game no Steam Deck.

## Idiomas suportados

O app traduz a interface conforme `LANG`:

- `pt*` → Português
- `en*` → English
- `es*` → Español
- `it*` → Italiano
- `ru*` → Русский

## Recursos principais

- detecção de jogos Steam / Heroic
- instalação de dependências Wine
- integração com Nexus Mods
- geração de atalhos `.desktop`
- empacotamento com PyInstaller
- TUI feita com Textual

## Build e testes

```bash
make build
make test
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

## Licença

MIT

---

Feito por **Guilherme**.
