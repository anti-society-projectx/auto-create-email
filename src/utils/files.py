from pathlib import Path
from rich.markup import escape

from src.core.logger import logger


def create_file(name: str, path: Path) -> Path:
    """
    Создаёт новый файл
    :param name: Название файла
    :param path: Путь до папки, в которой будет лежать
    :return:
    """
    full_path = path / name

    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "w") as f:
        f.write("")

    return full_path


def append_file(data: str, path: Path) -> Path:
    if not path.exists():
        full_path = path.resolve()
        logger.error("[den]Файла по пути: [bold]%s[/bold] не найден[/den]", full_path)
        raise FileNotFoundError(f"Файл по пути: {full_path} не найден, проверьте, правильно ли указан путь")

    with open(path, "a") as f:
        f.write(f"{data}\n")

    return path


def read_file(path: Path) -> str:
    if not path.exists():
        full_path = path.resolve()
        logger.error(f"Файл по пути: [bold]%s[/bold] не найден", full_path)
        raise FileNotFoundError(f"Файл по пути: {full_path} не найден, проверьте, правильно ли указан путь")

    with open(path, "r") as f:
        return f.read()


def format_credentials(credential: dict[str, str]) -> str:
    return f"{credential.get("address")}:{credential.get("password")}"
