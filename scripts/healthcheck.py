#!/usr/bin/env python3
"""Healthcheck — valida dependências do sistema antes de iniciar a UI."""

import sys
import subprocess
from gamepilot.i18n import t


def check_python_version() -> bool:
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print(f"❌ Python 3.10+ required. You have {v.major}.{v.minor}")
        return False
    print(f"✅ Python {v.major}.{v.minor}.{v.micro}")
    return True


def check_wine() -> bool:
    try:
        subprocess.run(["wine", "--version"], capture_output=True, check=True)
        print("✅ wine installed")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ wine not found. Run scripts/install-deps.sh or install wine manually.")
        return False


def check_winetricks() -> bool:
    try:
        subprocess.run(["winetricks", "--version"], capture_output=True, check=True)
        print("✅ winetricks installed")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ winetricks not found. Run scripts/install-deps.sh or install it manually.")
        return False


def main() -> None:
    print(f"🎮 {t('welcome')} — healthcheck\n")
    ok = True
    ok &= check_python_version()
    ok &= check_wine()
    ok &= check_winetricks()
    print()
    if ok:
        print("✅ All good! Run: python -m gamepilot")
    else:
        print("❌ Fix the issues above before running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
