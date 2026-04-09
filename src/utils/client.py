import asyncio
import functools
import logging

import httpx


def retry_fetch(max_retries: int = 3, delay: float = 0.33):
    """
    Функция декоратор для повторных HTTP-запросов.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            client = args[0]
            proxy_url = client.proxy

            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (httpx.ConnectTimeout, httpx.ProxyError, httpx.ConnectError):
                    logging.error("Тайм-аут запроса с использованием прокси: %s", proxy_url)
                    if attempt == max_retries:
                        logging.error("Все попытки были исчерпаны. Рекомендую проверить работоспособность прокси %s", proxy_url)
                        return None
                    logging.info("[%s/%s] Делаю повторный запрос...", attempt, max_retries)

                except:
                    logging.error("Ошибка при HTTP-запросе с прокси: %s", proxy_url)
                    if attempt == max_retries:
                        return None
                    logging.info("[%s/%s] Делаю повторный запрос...", attempt, max_retries)

                await asyncio.sleep(delay * attempt)

        return wrapper

    return decorator
