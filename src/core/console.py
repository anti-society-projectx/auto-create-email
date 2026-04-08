from pyfiglet import figlet_format
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
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
            f"{4*' '}[cyan]2.[/cyan] Топик\n"
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
        select_text = (
            f"\n{3 * ' '}[bold cyan]Выберете действие: [/bold cyan]"
        )
        return int(self.console.input(select_text))
