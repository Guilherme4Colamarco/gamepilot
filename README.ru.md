# GamePiLot

```text
╔══════════════════════════════════════╗
║  GAMEPILOT — VIBE CODING EDITION     ║
╚══════════════════════════════════════╝
```

> ⚠️ **Дисклеймер vibe coding**
>
> Этот проект собран в быстрых итерациях. Документация может немного отставать от кода, а код может быстро меняться, когда идея улучшается.
>
> Если нужен точный результат, смотри исходники.

**Читать на других языках:** [English](README.en.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

**Менеджер модов для игр Windows в Linux**, переписанный на **Python + Textual**.

GamePiLot находит установленные игры в Linux, помогает ставить зависимости через *winetricks*, скачивает инструменты для моддинга через Nexus Mods и создаёт ярлыки `.desktop`, чтобы запускать всё без лишней возни.

## Что умеет

- сканирует установки игр из Steam и Heroic
- ставит зависимости для префикса Wine
- интегрируется с Nexus Mods для загрузки мод-утилит
- создаёт ярлыки для меню и рабочего стола
- предоставляет TUI на Textual
- поддерживает i18n: **EN / PT / ES / IT / RU**
- собирается в standalone-бинарник через PyInstaller

## Быстрая установка

```bash
make setup
```

Это делает:

- создаёт `.venv/`
- устанавливает зависимости Python
- создаёт глобальный wrapper в `~/.local/bin/gamepilot`
- генерирует начальный ярлык приложения

## Как запускать

После setup можно использовать любой из способов:

```bash
gamepilot
# или
make run
# или
source .venv/bin/activate
python -m gamepilot
# или
python run.py
```

## Поддерживаемые языки

Интерфейс следует значению `LANG`:

- `pt*` → Português
- `en*` → English
- `es*` → Español
- `it*` → Italiano
- `ru*` → Русский

## Основные возможности

- обнаружение игр Steam / Heroic
- установка зависимостей Wine
- интеграция с Nexus Mods
- создание ярлыков `.desktop`
- упаковка через PyInstaller
- TUI на Textual

## Сборка и тесты

```bash
make build
make test
```

## Основная структура

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

## Лицензия

MIT

---

Сделано **Guilherme**.
