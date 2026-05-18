#!/usr/bin/env python3
"""
Demo — testes manuais sem precisar da UI.
Roda no terminal e mostra scan de jogos, parsing de manifesto, etc.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from gamepilot import scanner, manifests, wine

async def main():
    print("🎮 GamePiLot Demo — Core Test\n")
    print("1. i18n test")
    from gamepilot.i18n import t
    import os
    os.environ["LANG"] = "pt_BR"
    print(f"   PT: {t('welcome')}")
    os.environ["LANG"] = "en_US"
    print(f"   EN: {t('welcome')}")

    print("\n2. Manifests test")
    mfs = manifests.load_manifests()
    print(f"   Loaded {len(mfs)} manifests:")
    for m in mfs:
        print(f"   • {m.name} — tools: {', '.join(t.name for t in m.tools.values())}")

    print("\n3. Wine extract_real_error test")
    stderr = "fixme:heap:...\nwarn:ntdll:...\nerr:module: cannot load foo.dll\n"
    err = await wine.extract_real_error(stderr)
    print(f"   Extracted error: {err}")

    print("\n4. Scanner test (async)")
    games = await scanner.scan_all_games()
    print(f"   Found {len(games)} games:")
    for g in games[:5]:
        print(f"   • {g.name} [{g.source}] appid={g.steam_app_id}")
    if len(games) > 5:
        print(f"   ... e mais {len(games)-5}")

    print("\n✅ Demo completo!")

if __name__ == "__main__":
    asyncio.run(main())
