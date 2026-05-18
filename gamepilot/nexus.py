"""nexus — cliente Async para Nexus Mods API."""

import aiohttp
from typing import Optional, Any
from .i18n import t

BASE_URL = "https://api.nexusmods.com/v1"


class NexusClient:
    """Cliente HTTP com connection pooling, timeout e user-agent."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"User-Agent": "GamePiLot/0.1", "apikey": self.api_key},
        )
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def get(self, path: str) -> Any:
        if not self.session:
            raise RuntimeError("Client not initialized — use 'async with'")
        return await self.session.get(f"{BASE_URL}{path}")

    async def validate_api_key(self) -> str:
        """Valida chave API. Retorna nome do usuário ou levanta exceção."""
        if not self.session:
            raise RuntimeError("Client not initialized — use 'async with'")
        async with self.session.get(f"{BASE_URL}/users/validate.json") as resp:
            status = resp.status
            if status == 200:
                data = await resp.json()
                return data.get("name", "user")
            if status == 401:
                raise NexusError(t("nexus_key_invalid"))
            if status == 429:
                raise NexusError(t("nexus_rate_limit"))
            raise NexusError(t("nexus_error_generic"))

    async def get_mod_files(
        self, game_domain: str, mod_id: int
    ) -> list[dict[str, Any]]:
        """Lista arquivos de um mod."""
        path = f"/games/{game_domain}/mods/{mod_id}/files.json"
        resp = await self.get(path)
        try:
            if resp.status == 404:
                raise NexusError(t("nexus_mod_not_found"))
            data = await resp.json()
        finally:
            resp.release()
        files = data.get("files", [])
        if not files:
            raise NexusError(t("nexus_no_files"))
        return files

    async def get_latest_file(
        self, game_domain: str, mod_id: int
    ) -> dict[str, Any]:
        """Retorna o arquivo mais recente da categoria 'main'."""
        files = await self.get_mod_files(game_domain, mod_id)
        main_files = [
            f for f in files
            if f.get("category_name", "").upper() == "MAIN"
        ]
        if not main_files:
            raise NexusError(t("nexus_no_files"))
        latest = max(main_files, key=lambda f: f.get("uploaded_timestamp", 0))
        return latest

    async def get_download_url(
        self, game_domain: str, mod_id: int, file_id: int
    ) -> str:
        """Obtém URL de download para um file_id."""
        path = f"/games/{game_domain}/mods/{mod_id}/files/{file_id}/download_link.json"
        resp = await self.get(path)
        try:
            if resp.status == 401:
                raise NexusError(t("nexus_key_invalid"))
            if resp.status == 403:
                raise NexusError(t("nexus_free_tier_download"))
            data = await resp.json()
        finally:
            resp.release()
        if isinstance(data, list) and data:
            return data[0].get("URI", "")
        raise NexusError(t("nexus_no_download_link"))


class NexusError(Exception):
    pass
