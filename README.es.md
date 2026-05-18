# GamePiLot

```text
╔══════════════════════════════════════╗
║  GAMEPILOT — VIBE CODING EDITION     ║
╚══════════════════════════════════════╝
```

> ⚠️ **Aviso de vibe coding**
>
> Este proyecto fue construido en ciclos rápidos de iteración. La documentación puede ir un poco detrás del código, y el código puede cambiar rápido cuando la idea mejora.
>
> Si quieres el comportamiento exacto, lee los archivos fuente.

**Leer en otros idiomas:** [English](README.en.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

**Un gestor de mods para juegos de Windows en Linux**, reescrito en **Python + Textual**.

GamePiLot detecta juegos instalados en Linux, ayuda a instalar dependencias con *winetricks*, descarga herramientas de modding desde Nexus Mods y crea accesos `.desktop` para abrir todo con menos fricción.

## Qué hace

- analiza instalaciones de juegos en Steam y Heroic
- instala dependencias del prefijo Wine
- se integra con Nexus Mods para descargar herramientas de modding
- crea accesos directos para el menú y el escritorio
- ofrece una TUI con Textual
- soporta i18n: **EN / PT / ES / IT / RU**
- empaqueta en binario standalone con PyInstaller

## Instalación rápida

```bash
make setup
```

Esto hace:

- crea `.venv/`
- instala dependencias de Python
- crea un wrapper global en `~/.local/bin/gamepilot`
- genera el acceso inicial de la aplicación

## Cómo ejecutar

Después del setup, puedes usar cualquiera de estas formas:

```bash
gamepilot
# o
make run
# o
source .venv/bin/activate
python -m gamepilot
# o
python run.py
```

## Idiomas soportados

La interfaz sigue el valor de `LANG`:

- `pt*` → Português
- `en*` → English
- `es*` → Español
- `it*` → Italiano
- `ru*` → Русский

## Funciones principales

- detección de juegos Steam / Heroic
- instalación de dependencias de Wine
- integración con Nexus Mods
- generación de accesos `.desktop`
- empaquetado con PyInstaller
- TUI hecha con Textual

## Build y pruebas

```bash
make build
make test
```

## Estructura principal

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

## Licencia

MIT

---

Hecho por **Guilherme**.
