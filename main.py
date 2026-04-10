import asyncio
import random
import time
import sys
import uuid
from pathlib import Path

import httpx
from aiolimiter import AsyncLimiter

from src.client import BaseMailClient
from src.core.config import YamlConfig
from src.core.console import ConsoleUI
from src.core.logger import logger
from src.utils.files import read_file, create_file, append_file, format_credentials
from src.utils.proxies import extract_proxies


async def worker(client: BaseMailClient, domain: str, limiter: AsyncLimiter):
    async with limiter:
        return await client.create_account(domain)


async def fetch(total: int, console_ui: ConsoleUI) -> None:
    yaml_config = YamlConfig()

    path_proxies = Path(yaml_config.get_proxies_list_path())
    proxies = extract_proxies(read_file(path_proxies))

    clients: list[BaseMailClient] = [
        BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.tm", timeout=10.0)),
        BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.gw", timeout=10.0))
    ]
    mailgw_domains: list[str] = await clients[1].get_available_domains()
    mailtm_domains: list[str] = await clients[0].get_available_domains()

    if not proxies:
        logger.warning("Для лучшей работы скрипта, добавьте прокси")

    for proxy in proxies:
        client_tm = BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.tm", timeout=10.0, proxy=proxy), proxy)
        client_gw = BaseMailClient(httpx.AsyncClient(base_url="https://api.mail.gw", timeout=10.0, proxy=proxy), proxy)
        clients.append(client_gw)
        clients.append(client_tm)

    s = time.time()
    limiter = AsyncLimiter(6, 0.9)
    tasks = []

    for _ in range(total):
        for client in clients:
            if client.client.base_url == "https://api.mail.tm":
                domain = random.choice(mailtm_domains)
            else:
                domain = random.choice(mailgw_domains)
            tasks.append(asyncio.create_task(worker(client, domain, limiter)))

    success = 0
    failed = 0
    outputs_dir = Path(yaml_config.get_outputs_path())
    output_file = create_file(f"log_{uuid.uuid4()}.txt", outputs_dir)

    for coro in asyncio.as_completed(tasks):
        account = await coro

        if account:
            success += 1
            append_file(format_credentials(account), output_file)
        else:
            failed += 1

    await asyncio.gather(*[c.client.aclose() for c in clients])
    time_wasted = time.time() - s

    console_ui.stats_create_accounts(
        total=len(clients),
        time_wasted=round(time_wasted),
        success=success,
        failed=failed,
        output_file=output_file
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
                sys.exit()

            else:
                logger.error("Неизвестная команда.")
                continue
        except ValueError:
            logger.error("Неизвестная команда.")
            continue


asyncio.run(main())
