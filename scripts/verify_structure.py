#!/usr/bin/env python3
"""Verificador de estrutura — checa imports e arquivos."""

import ast
import os
from pathlib import Path

BASE = Path(__file__).parent / "gamepilot"
STDLIB = {
    "os", "pathlib", "typing", "asyncio", "json", "subprocess",
    "sys", "re", "logging", "enum", "collections", "itertools",
    "functools", "dataclasses", "warnings", "contextlib"
}
THIRD_PARTY = {
    "textual", "pydantic", "aiohttp", "aiofiles", "toml",
    "platformdirs", "rich"
}

errors = []
warnings = []

def check_file(path: Path) -> None:
    rel = path.relative_to(BASE.parent)
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as e:
        errors.append(f"SYNTAX {rel}: {e}")
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            top = node.module.split('.')[0]
            if node.level == 0 and top not in STDLIB and top not in THIRD_PARTY:
                errors.append(f"IMPORT {rel}: absolute import of package module '{node.module}' — use 'from .{node.module}'")

    if path.parent != BASE and path.parent.name != '__pycache__':
        if not (path.parent / '__init__.py').exists():
            warnings.append(f"Missing __init__.py in {path.parent}")

for pyfile in BASE.rglob("*.py"):
    if pyfile.name == "__pycache__":
        continue
    check_file(pyfile)

print(f"🔍 Verificando {BASE}\n")
if errors:
    print(f"❌ {len(errors)} erro(s):")
    for e in errors:
        print(f"   {e}")
else:
    print("✅ Nenhum erro de imports ou sintaxe")

if warnings:
    print(f"\n⚠️  {len(warnings)} aviso(s):")
    for w in warnings:
        print(f"   {w}")

print("\n📁 Estrutura:")
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    level = len(Path(root).relative_to(BASE).parts)
    indent = "   " * level
    print(f"{indent}{Path(root).name}/")
    for f in sorted(f for f in files if f.endswith('.py')):
        print(f"{indent}   {f}")
