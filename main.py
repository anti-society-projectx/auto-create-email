import asyncio
import random
import time
import sys

import httpx
from aiolimiter import AsyncLimiter

from src.client import BaseMailClient
from src.core.console import ConsoleUI
from src.core.logger import logger


async def fetch(total: int, console_ui: ConsoleUI) -> None:
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

    s = time.time()
    limiter = AsyncLimiter(6, 0.9)
    tasks = []

    for _ in range(total):
        async with limiter:
            for client in clients:
                if client.client.base_url == "https://api.mail.tm":
                    domain = random.choice(mailtm_domains)
                else:
                    domain = random.choice(mailgw_domains)
                tasks.append(asyncio.create_task(client.create_account(domain)))

    resp = await asyncio.gather(*tasks, return_exceptions=True)
    print(resp)
    await asyncio.gather(*[c.client.aclose() for c in clients])

    success = []
    failed = []
    time_wasted = time.time() - s

    for account in resp:
        if account:
            success.append(account)
        else:
            failed.append(account)



    console_ui.stats_create_accounts(
        total=int(total * len(proxies) * 2),
        time_wasted=time_wasted,
        success=len(success),
        failed=len(failed)
    )


async def main():
    console_ui = ConsoleUI()
    console_ui.main()

    while True:
        console_ui.show_menu()
        try:
            select_action = console_ui.select_action()

            if select_action == 1:
                num_requests = console_ui.run_script()
                if num_requests:
                    await fetch(num_requests, console_ui)

            elif select_action == 2:
                # TODO: открыть в браузере/отправить ссылку на тему
                pass

            elif select_action == 3:
                sys.exit()

            else:
                logger.error("Неизвестная команда.")
                continue
        except ValueError:
            logger.error("Неизвестная команда.")
            continue


asyncio.run(main())
