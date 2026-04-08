import asyncio
import functools

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
                    print("Таймаут на прокси: ", proxy_url)
                    if attempt == max_retries:
                        print(
                            f"Все попытки для {proxy_url} исчерпаны. Рекомендуем проверить работоспособность прокси {proxy_url}")
                        return None

                except:
                    print(f"Ошибка при HTTP-запросе с прокси: {proxy_url}. Отправляем повторный запрос...")
                    if attempt == max_retries:
                        return None
                    await asyncio.sleep(delay * attempt)

        return wrapper

    return decorator
