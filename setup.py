#!/usr/bin/env python3
"""
Setup — Instala dependências Python e cria atalho inicial.
Plug and play: rode uma vez e o GamePiLot estará pronto.
"""

import subprocess
import sys
from pathlib import Path


_SETUPTOOLS_COMMANDS = {
    "bdist_wheel",
    "build",
    "build_py",
    "develop",
    "dist_info",
    "editable_wheel",
    "egg_info",
    "install",
    "sdist",
}

def run(cmd, check=True):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result

def main():
    print("🎮 GamePiLot Setup — Plug & Play\n")
    
    # 1. Criar/ativar venv
    venv = Path('.venv')
    if not venv.exists():
        print("→ Criando virtualenv...")
        run([sys.executable, '-m', 'venv', '.venv'])
    pip = venv / 'bin' / 'pip'
    python = venv / 'bin' / 'python'
    
    # 2. Instalar dependências
    print("→ Instalando dependências Python...")
    run([str(pip), 'install', '--upgrade', 'pip'])
    run([str(pip), 'install', '-r', 'requirements.txt'])
    run([str(pip), 'install', '-e', '.'])
    
    # 3. Verificar wine/winetricks
    print("→ Verificando Wine...")
    try:
        run(['wine', '--version'], check=False)
        print("✅ wine encontrado")
    except FileNotFoundError:
        print("⚠️  wine não encontrado. Rode: ./install-deps.sh")
    
    try:
        run(['winetricks', '--version'], check=False)
        print("✅ winetricks encontrado")
    except FileNotFoundError:
        print("⚠️  winetricks não encontrado. Rode: ./install-deps.sh")
    
    # 4. Criar wrapper em ~/.local/bin
    print("→ Criando comando global...")
    wrapper = Path.home() / ".local" / "bin" / "gamepilot"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    console_script = (venv / 'bin' / 'gamepilot').resolve()
    python_cmd = str((venv / 'bin' / 'python').resolve()) if (venv / 'bin' / 'python').exists() else sys.executable
    exec_cmd = f'"{console_script}"' if console_script.exists() else f'"{python_cmd}" -m gamepilot'
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        "# GamePiLot wrapper\n"
        f'exec {exec_cmd} "$@"\n'
    )
    wrapper.chmod(0o755)
    print(f"   Wrapper: {wrapper}")

    # 5. Criar atalho inicial (aponta pro wrapper)
    print("→ Criando atalho...")
    run([str(python), '-c', '''
from gamepilot.utils import shortcuts
from pathlib import Path
p = shortcuts.create_desktop_file("GamePiLot", icon_path=Path("assets/icon.svg"))
shortcuts._update_exec_line(p, str(Path.home() / ".local" / "bin" / "gamepilot"))
shortcuts.create_menu_entry(p)
print(f"Atalho criado: {p}")
'''])
    
    print("\n✅ Setup completo!")
    print("\nPara executar:")
    print("  gamepilot            # terminal (global)")
    print("  ou pelo menu → GamePiLot")
    print("\nPara rebuild:")
    print("  make build")

if __name__ == '__main__':
    if _SETUPTOOLS_COMMANDS.intersection(sys.argv[1:]):
        from setuptools import setup

        setup()
    else:
        main()
