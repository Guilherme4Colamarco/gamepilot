# GamePiLot

```text
╔══════════════════════════════════════╗
║  GAMEPILOT — VIBE CODING EDITION     ║
╚══════════════════════════════════════╝
```

> ⚠️ **Avviso di vibe coding**
>
> Questo progetto è stato costruito in cicli rapidi di iterazione. La documentazione può restare un po' indietro rispetto al codice, e il codice può cambiare velocemente quando l'idea migliora.
>
> Se vuoi il comportamento esatto, leggi i file sorgente.

**Leggi in altre lingue:** [English](README.en.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

**Un gestore di mod per giochi Windows su Linux**, riscritto in **Python + Textual**.

GamePiLot rileva i giochi installati su Linux, aiuta a installare le dipendenze con *winetricks*, scarica strumenti di modding da Nexus Mods e crea scorciatoie `.desktop` per aprire tutto con meno attrito.

## Cosa fa

- scansiona le installazioni dei giochi in Steam e Heroic
- installa le dipendenze del prefisso Wine
- si integra con Nexus Mods per scaricare strumenti di modding
- crea scorciatoie per menu e desktop
- offre una TUI con Textual
- supporta i18n: **EN / PT / ES / IT / RU**
- impacchetta in un binario standalone con PyInstaller

## Installazione rapida

```bash
make setup
```

Questo fa:

- crea `.venv/`
- installa le dipendenze Python
- crea un wrapper globale in `~/.local/bin/gamepilot`
- genera il collegamento iniziale dell'app

## Come eseguire

Dopo il setup, puoi usare uno di questi modi:

```bash
gamepilot
# oppure
make run
# oppure
source .venv/bin/activate
python -m gamepilot
# oppure
python run.py
```

## Lingue supportate

L'interfaccia segue il valore di `LANG`:

- `pt*` → Português
- `en*` → English
- `es*` → Español
- `it*` → Italiano
- `ru*` → Русский

## Funzioni principali

- rilevamento dei giochi Steam / Heroic
- installazione delle dipendenze Wine
- integrazione con Nexus Mods
- generazione di scorciatoie `.desktop`
- packaging con PyInstaller
- TUI costruita con Textual

## Build e test

```bash
make build
make test
```

## Struttura principale

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

## Licenza

MIT

---

Fatto da **Guilherme**.
