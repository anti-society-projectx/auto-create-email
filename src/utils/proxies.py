def extract_proxies(proxies: str) -> list[str]:
    return [line.strip() for line in proxies.splitlines() if line.strip()]
