# Command-line interface logic
from .utils import (
    __app_name__,
    __version__,
    console,
    welcome,
    is_internet_available,
)

import typer
import rich


app = typer.Typer()


@app.command(name="info", help="Get information about the app")
def info():
    console.print(f"{__app_name__} v {__version__}", style="info")
