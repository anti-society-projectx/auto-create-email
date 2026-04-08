import asyncio
import random
import time

import httpx
from aiolimiter import AsyncLimiter

from src.client import BaseMailClient


async def main():
    proxies = [
        "http://185.76.240.64:10001",
        "http://103.252.89.130:8080",
        "socks5://152.53.155.16:1080",
        "socks5://206.123.156.209:6090"
    ]
    clients: list[BaseMailClient] = [
        BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.tm", timeout=10.0)),
        BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.gw", timeout=10.0))
    ]
    mailgw_domains: list[str] = await clients[1].get_available_domains()
    mailtm_domains: list[str] = await clients[0].get_available_domains()

    for proxy in proxies:
        client_tm = BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.tm", timeout=10.0, proxy=proxy), proxy)
        client_gw = BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.gw", timeout=10.0, proxy=proxy), proxy)
        clients.append(client_gw)
        clients.append(client_tm)

    total = 3
    s = time.time()
    limiter = AsyncLimiter(6, 0.9)
    tasks = []

    for _ in range(total):
        s = time.time()
        async with limiter:
            for client in clients:
                if client.client.base_url == "https://api.mail.tm":
                    domain = random.choice(mailtm_domains)
                else:
                    domain = random.choice(mailgw_domains)
                tasks.append(asyncio.create_task(client.create_account(domain)))

    resp = await asyncio.gather(*tasks, return_exceptions=True)
    print(resp)
    print(time.time() - s)
    await asyncio.gather(*[c.client.aclose() for c in clients])


asyncio.run(main())
