"""Models — Pydantic para dados do GamePiLot."""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from pathlib import Path


class Identifiers(BaseModel):
    steam_app_id: Optional[int] = None
    heroic_names: Optional[list[str]] = None

class ModTool(BaseModel):
    """Uma ferramenta de modding para um jogo."""
    name: str
    description: Optional[str] = None
    winetricks: list[str] = Field(default_factory=list)
    download_url: Optional[str] = None
    executable_path: Optional[str] = None
    nexus_game_domain: Optional[str] = None
    nexus_mod_id: Optional[int] = None
    # install_type controla o fluxo após o download:
    #   "installer" — executa o arquivo baixado com `wine` (default; instalador .exe).
    #   "extract"   — extrai o archive baixado (.zip/.rar/.tar.gz) em ``extract_to``.
    install_type: str = "installer"
    extract_to: Optional[str] = None  # caminho relativo ao prefix, ex: "drive_c/Modding/Tool"
    # asset_pattern: regex usado para escolher um asset específico quando
    # ``download_url`` aponta para um endpoint que retorna múltiplos (ex:
    # GitHub releases/latest). Match é feito contra o nome do asset.
    # Ex: ``"^RE4\\.zip$"`` para REFramework do Resident Evil 4.
    asset_pattern: Optional[str] = None

class GameManifest(BaseModel):
    """Manifesto de um jogo — metadados + ferramentas de modding."""
    name: str
    identifiers: Optional[Identifiers] = None
    tools: Dict[str, ModTool] = Field(default_factory=dict)


class ScannerResult(BaseModel):
    """Resultado da detecção de um jogo."""
    name: str
    prefix_path: Optional[Path] = None
    steam_app_id: Optional[int] = None
    source: str  # "steam" | "heroic" | "unknown"
