#!/usr/bin/env bash
# GamePiLot — Instalador de dependências do sistema (Linux)
# Detecta o gerenciador de pacotes disponível e instala Wine + Winetricks

set -euo pipefail

echo "🎮 GamePiLot System Dependencies Installer"
echo "=========================================="

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Dependências do sistema que precisamos
declare -a PKGS_WINE=("wine" "winetricks")

# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

has_cmd() {
    command -v "$1" &>/dev/null
}

check_wine() {
    if has_cmd wine; then
        echo -e "  ${GREEN}✓${NC} wine: $(wine --version 2>/dev/null | head -1)"
        return 0
    fi
    return 1
}

check_winetricks() {
    if has_cmd winetricks; then
        echo -e "  ${GREEN}✓${NC} winetricks: $(winetricks --version 2>/dev/null | head -1)"
        return 0
    fi
    return 1
}

# ---------------------------------------------------------------------------
# Instaladores por gerenciador de pacotes
# ---------------------------------------------------------------------------

install_with_pacman() {
    echo -e "\n📦 ${CYAN}pacman${NC} detectado (Arch/CachyOS/Manjaro/EndeavourOS)"
    if ! has_cmd sudo; then
        echo -e "${RED}✗ sudo não encontrado. Instale sudo ou execute como root.${NC}"
        exit 1
    fi

    if ! check_wine; then
        echo "  → Instalando wine via pacman..."
        sudo pacman -S --needed --noconfirm wine-staging || sudo pacman -S --needed --noconfirm wine
    fi

    if ! check_winetricks; then
        echo "  → Instalando winetricks via pacman..."
        sudo pacman -S --needed --noconfirm winetricks 2>/dev/null || {
            echo -e "  ${YELLOW}!${NC} winetricks não encontrado nos repositórios oficiais."
            echo "  → Tentando instalar via yay/paru (AUR)..."
            if has_cmd yay; then
                yay -S --needed --noconfirm winetricks-git
            elif has_cmd paru; then
                paru -S --needed --noconfirm winetricks-git
            else
                echo -e "  ${YELLOW}!${NC} Nenhum helper AUR (yay/paru) encontrado."
                echo "  → Baixando winetricks diretamente..."
                sudo curl -Lo /usr/local/bin/winetricks https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
                sudo chmod +x /usr/local/bin/winetricks
            fi
        }
    fi
}

install_with_apt() {
    echo -e "\n📦 ${CYAN}apt${NC} detectado (Debian/Ubuntu/Mint/Pop!_OS)"
    if ! has_cmd sudo; then
        echo -e "${RED}✗ sudo não encontrado. Instale sudo ou execute como root.${NC}"
        exit 1
    fi

    echo "  → Atualizando lista de pacotes..."
    sudo apt update

    if ! check_wine; then
        echo "  → Instalando wine via apt..."
        sudo apt install -y wine winetricks
    fi

    if ! check_winetricks; then
        echo "  → Instalando winetricks via apt..."
        sudo apt install -y winetricks
    fi
}

install_with_dnf() {
    echo -e "\n📦 ${CYAN}dnf${NC} detectado (Fedora/RHEL/CentOS Stream)"
    if ! has_cmd sudo; then
        echo -e "${RED}✗ sudo não encontrado. Instale sudo ou execute como root.${NC}"
        exit 1
    fi

    if ! check_wine; then
        echo "  → Instalando wine via dnf..."
        sudo dnf install -y wine winetricks
    fi

    if ! check_winetricks; then
        echo "  → Instalando winetricks via dnf..."
        sudo dnf install -y winetricks
    fi
}

install_with_zypper() {
    echo -e "\n📦 ${CYAN}zypper${NC} detectado (openSUSE)"
    if ! has_cmd sudo; then
        echo -e "${RED}✗ sudo não encontrado. Instale sudo ou execute como root.${NC}"
        exit 1
    fi

    if ! check_wine; then
        echo "  → Instalando wine via zypper..."
        sudo zypper install -y wine winetricks
    fi

    if ! check_winetricks; then
        echo "  → Instalando winetricks via zypper..."
        sudo zypper install -y winetricks
    fi
}

install_with_xbps() {
    echo -e "\n📦 ${CYAN}xbps-install${NC} detectado (Void Linux)"
    if ! has_cmd sudo; then
        echo -e "${RED}✗ sudo não encontrado. Instale sudo ou execute como root.${NC}"
        exit 1
    fi

    if ! check_wine; then
        echo "  → Instalando wine via xbps..."
        sudo xbps-install -Sy wine winetricks
    fi

    if ! check_winetricks; then
        echo "  → Instalando winetricks via xbps..."
        sudo xbps-install -Sy winetricks
    fi
}

install_with_emerge() {
    echo -e "\n📦 ${CYAN}emerge${NC} detectado (Gentoo)"
    echo -e "${YELLOW}!${NC} Atenção: compilar o Wine no Gentoo pode levar bastante tempo."

    if ! check_wine; then
        echo "  → Instalando wine via emerge..."
        sudo emerge --ask n app-emulation/wine-vanilla || sudo emerge app-emulation/wine-vanilla
    fi

    if ! check_winetricks; then
        echo "  → Instalando winetricks via emerge..."
        sudo emerge --ask n app-emulation/winetricks || sudo emerge app-emulation/winetricks
    fi
}

install_with_nix() {
    echo -e "\n📦 ${CYAN}nix${NC} detectado (NixOS ou ambiente Nix)"
    echo -e "${YELLOW}!${NC} Detectado ambiente Nix."

    # Preferir nix-env para instalação imperativa (mais universal em scripts)
    if has_cmd nix-env; then
        if ! check_wine; then
            echo "  → Instalando wine via nix-env..."
            nix-env -iA nixpkgs.wine
        fi
        if ! check_winetricks; then
            echo "  → Instalando winetricks via nix-env..."
            nix-env -iA nixpkgs.winetricks
        fi
    elif has_cmd nix-shell; then
        echo -e "  ${YELLOW}!${NC} nix-env não encontrado. Você pode usar nix-shell:"
        echo "    nix-shell -p wine winetricks"
        exit 1
    else
        echo -e "${RED}✗ Comando nix encontrado, mas nix-env/nix-shell não disponíveis.${NC}"
        exit 1
    fi
}

# ---------------------------------------------------------------------------
# Detecção de gerenciador de pacotes
# ---------------------------------------------------------------------------

detect_pm() {
    # Ordem: dos mais comuns aos mais específicos/nicho
    if has_cmd pacman; then
        echo "pacman"
    elif has_cmd apt; then
        echo "apt"
    elif has_cmd dnf; then
        echo "dnf"
    elif has_cmd zypper; then
        echo "zypper"
    elif has_cmd xbps-install; then
        echo "xbps"
    elif has_cmd emerge; then
        echo "emerge"
    elif has_cmd nix-env || has_cmd nix-shell; then
        echo "nix"
    else
        echo "unknown"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Primeiro, verificar o que já está instalado
echo ""
echo "🔍 Verificando dependências atuais..."
for tool in wine winetricks; do
    "check_${tool}" || echo -e "  ${YELLOW}!${NC} ${tool}: não encontrado"
done

PM=$(detect_pm)

case "$PM" in
    pacman) install_with_pacman ;;
    apt)    install_with_apt ;;
    dnf)    install_with_dnf ;;
    zypper) install_with_zypper ;;
    xbps)   install_with_xbps ;;
    emerge) install_with_emerge ;;
    nix)    install_with_nix ;;
    *)
        echo ""
        echo -e "${RED}✗ Nenhum gerenciador de pacotes suportado detectado.${NC}"
        echo ""
        echo "Gerenciadores suportados:"
        echo "  • pacman        (Arch, CachyOS, Manjaro, EndeavourOS)"
        echo "  • apt           (Debian, Ubuntu, Mint, Pop!_OS, elementary)"
        echo "  • dnf           (Fedora, RHEL, CentOS Stream, AlmaLinux, Rocky)"
        echo "  • zypper        (openSUSE)"
        echo "  • xbps-install  (Void Linux)"
        echo "  • emerge        (Gentoo)"
        echo "  • nix/nix-env   (NixOS, ou ambientes Nix)"
        echo ""
        echo "Instale manualmente:"
        echo "  • wine       → https://wiki.winehq.org/Download"
        echo "  • winetricks → https://github.com/Winetricks/winetricks"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Dependências do sistema verificadas/instaladas!${NC}"
echo ""
echo "Próximo passo — dependências Python:"
echo "  python3 -m venv .venv && source .venv/bin/activate"
echo "  pip install -r requirements.txt"
