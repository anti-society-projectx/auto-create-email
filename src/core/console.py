from pyfiglet import figlet_format
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.text import Text


class ConsoleUI:
    def __init__(self):
        self.console = Console()

    def main(self) -> None:
        ascii_art = figlet_format("anti.society.projectx", font="standard", width=100)

        self.console.print(Panel(
            Align.center(Text(ascii_art)),
            border_style="green",
            title="by: anti.society.projectx",
            subtitle="for lolz.live ❤")
        )

    def show_menu(self) -> None:
        menu = (
            f"\n{4*' '}[cyan]1.[/cyan] Запуск\n"
            f"{4*' '}[cyan]2.[/cyan] Настройки\n"
            f"{4*' '}[cyan]3.[/cyan] Выйти\n"
        )

        self.console.print(
            Panel(
                menu,
                title="Меню",
                style="bold"
            )
        )

    def select_action(self) -> int:
        input_text = (
            f"[bold white]❯ Выберете действие: [/bold white]"
        )
        return int(self.console.input(input_text))

    def run_script(self) -> int:
        input_text = (
            "[dim]Количество создаваемых почты = количество прокси * количество запросов * 2\n"
            "Чтобы вернуться в главное меню, укажите 0[/dim]\n"
            "[bold white]❯ Введите количество запросов: [/bold white]"
        )
        return int(self.console.input(input_text))

    def stats_create_accounts(self, total: int, time_wasted: float, success: int, failed: int) -> None:
        """
        Выводит статистику создания аккаунтов.
        :param total: Общее количество аккаунтов.
        :param time_wasted: Общее время, которое было затрачено на создание всех аккаунтов.
        :param success: Количество аккаунтов, которые были успешно созданы.
        :param failed: Количество аккаунтов, которые не были созданы.
        """
        stats_text = (
            f"Количество создаваемых аккаунтов: [cyan]{total}[/cyan]\n"
            f"Количество созданных аккаунтов: [green]{success}[/green]\n"
            f"Количество не созданных аккаунтов: [red]{failed}[/red]\n"
            f"Общее время затраченное на создание аккаунтов: [cyan]{time_wasted}[/cyan]\n"
            f"Среднее время на создание одного аккаунта: [cyan]{round(time_wasted/2, 2)}[/cyan]"
        )
        panel = Panel(
                stats_text,
                title="Статистика",
                style="bold",
                border_style="green"
            )
        self.console.print(panel)
