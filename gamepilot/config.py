"""config — carregamento e persistência de configuração."""

from pathlib import Path
from platformdirs import user_config_dir
from pydantic import BaseModel, Field
from typing import Optional
import toml


class Config(BaseModel):
    """Configuração persistente do usuário."""
    nexus_api_key: Optional[str] = None
    # cached_games pode ser usado no futuro para cache de scan
    cached_games: list[dict] = Field(default_factory=list)


CONFIG_DIR = Path(user_config_dir("gamepilot", "gamepilot"))
CONFIG_FILE = CONFIG_DIR / "config.toml"


def load_config() -> Config:
    """Carrega configuração do disco ou retorna padrão."""
    if CONFIG_FILE.exists():
        try:
            data = toml.loads(CONFIG_FILE.read_text("utf-8"))
            return Config(**data)
        except (toml.TomlDecodeError, UnicodeDecodeError) as exc:
            print(
                f"[AVISO] config.toml invalido – ira redefinido. "
                f"Erro: {exc}"
            )
    return Config()


def save_config(cfg: Config) -> None:
    """Save config to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(toml.dumps(cfg.model_dump()), "utf-8")
