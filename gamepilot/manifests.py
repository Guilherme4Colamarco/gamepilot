"""manifests — carregador simples de manifestos TOML com dedup."""

import toml
import importlib.resources as resources
import sys
from pathlib import Path
from typing import Optional
from .models import GameManifest


def load_manifests(
    system_path: Optional[Path] = None,
    user_path: Optional[Path] = None,
) -> list[GameManifest]:
    """
    Carrega manifestos de dois locais:
    1. system_path (padrão: ./manifests) — vem com o pacote
    2. user_path  (padrão: ~/.config/gamepilot/manifests) — customizações

    Retorna lista única (dedup por (nome, steam_app_id), user prevalece).
    """
    from platformdirs import user_config_dir

    if system_path is None:
        candidates = [
            Path(__file__).resolve().parents[1] / "manifests",
            Path(sys.prefix) / "share" / "gamepilot" / "manifests",
        ]
        system_path = next((path for path in candidates if path.exists()), candidates[0])
        if not system_path.exists():
            try:
                system_path = Path(str(resources.files("gamepilot").joinpath("manifests")))
            except Exception:
                pass
    if user_path is None:
        user_path = Path(user_config_dir("gamepilot", "gamepilot")) / "manifests"

    def _dedup_key(manifest: GameManifest) -> tuple[str, int | None]:
        """Chave de deduplicacao composta: (nome, steam_app_id)."""
        sid = None
        if manifest.identifiers and manifest.identifiers.steam_app_id is not None:
            sid = manifest.identifiers.steam_app_id
        return (manifest.name.lower(), sid)

    def _normalize_tools(data: dict) -> dict:
        """Converte tools de lista [[tools]] para dict {slug: tool}."""
        tools = data.get("tools")
        if isinstance(tools, list):
            data["tools"] = {
                t["name"].lower().replace(" ", "_").replace("-", "_"): t
                for t in tools
            }
        return data

    def _load_from(path: Path) -> None:
        if not path.is_dir():
            return
        for file in path.glob("*.toml"):
            try:
                data = toml.loads(file.read_text())
                # Dois formatos possíveis:
                # 1. { name = "...", identifiers = {...}, tools = {...} }  → unico
                # 2. { games = { slug = { name = "...", ... }, ... } }    → multiplo
                if "games" in data and isinstance(data["games"], dict):
                    for slug, manifest_dict in data["games"].items():
                        try:
                            manifest = GameManifest(**_normalize_tools(manifest_dict))
                            buffer[_dedup_key(manifest)] = manifest
                        except Exception as e:
                            print(f"[WARN] manifesto invalido '{slug}' em {file}: {e}")
                elif "name" in data:
                    manifest = GameManifest(**_normalize_tools(data))
                    buffer[_dedup_key(manifest)] = manifest
            except toml.TomlDecodeError as e:
                print(f"[WARN] TOML invalido em {file}: {e}")
            except Exception as e:
                print(f"[WARN] erro ao carregar {file}: {e}")

    buffer: dict[tuple[str, int | None], GameManifest] = {}

    # System primeiro (prioridade baixa)
    _load_from(system_path)
    # User depois (sobrescreve)
    _load_from(user_path)

    return list(buffer.values())
