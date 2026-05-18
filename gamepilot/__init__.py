"""GamePiLot — Gerenciador de mods para jogos Windows no Linux (Python)."""

__version__ = "0.1.0"

from .config import load_config, save_config, CONFIG_DIR
from .models import GameManifest, ModTool, Identifiers, ScannerResult
from .scanner import scan_all_games, scan_steam_games, scan_heroic_games
from .manifests import load_manifests
from .wine import install_dependencies, check_prerequisites, extract_real_error, InstallResult
from .nexus import NexusClient, NexusError
from .i18n import t, t_fmt, Language

__all__ = [
    "load_config", "save_config", "CONFIG_DIR",
    "GameManifest", "ModTool", "Identifiers", "ScannerResult",
    "scan_all_games", "scan_steam_games", "scan_heroic_games",
    "load_manifests",
    "install_dependencies", "check_prerequisites", "extract_real_error", "InstallResult",
    "NexusClient", "NexusError",
    "t", "t_fmt", "Language",
]
