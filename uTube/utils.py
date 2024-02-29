import requests
from yaspin import yaspin
from yaspin.spinners import Spinners
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


def welcome():
    console.print(f"Welcome to {__app_name__} v {__version__}", style="info")


@yaspin(text="Checking internet connection", color="blue", spinner=Spinners.earth)
def is_internet_available():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False
