import httpx
import random

from src.utils.auth import generate_string
from src.utils.client import retry_fetch


class BaseMailClient:
    def __init__(self, client: httpx.AsyncClient, proxy: str = "direct"):
        self._client = client
        self.proxy = proxy


    @property
    def client(self) -> httpx.AsyncClient:
        return self._client


    @retry_fetch()
    async def get_available_domains(self, page: int = 1) -> list[str]:
        resp = await self._client.get("/domains", params={"page": page})
        resp.raise_for_status()
        data = resp.json()

        domains = []
        for domain in data.get("hydra:member", []):
            if domain.get("isActive"):
                domains.append(domain.get("domain"))

        return domains

    @retry_fetch()
    async def choice_domain(self, page: int = 1) -> str:
        resp = await self._client.get("/domains", params={"page": page})
        resp.raise_for_status()
        data = resp.json()
        domains = []
        for domain in data.get("hydra:member", []):
            if domain.get("isActive"):
                domains.append(domain.get("domain"))

        return random.choice(domains)

    @retry_fetch()
    async def create_account(self, domain: str | None = None):
        if not domain:
            domain = await self.choice_domain()
            if not domain:
                raise

        address = f"{generate_string(random.randint(12, 24))}@{domain}"
        password = generate_string(random.randint(16, 32))
        data = {"address": address, "password": password}

        resp = await self._client.post("/accounts", json=data)
        resp.raise_for_status()
        return data
