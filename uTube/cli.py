# Command-line interface logic

import click
import rich
from rich.console import Console
from rich.theme import Theme


__app_name__: str = "uTube"
__version__: str = "1.0"

custom_theme = Theme({
    "info": "#64b0f2",
    "warning": "color(3)",
    "danger": "red",
    "success": "green",
})
console = Console()
console = Console(theme=custom_theme)


@click.command(help="Welcome to uTube")
def welcome():
    console.print(f"Welcome to {__app_name__} v {__version__}", style="info")


# @click.command(help="Get information about the app")
@click.command(help="Get information about the app", aliases=['i, info'])
def info():
    console.print(f"{__app_name__} v {__version__}", style="info")
