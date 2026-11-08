from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "danger": "bold red",
})

console = Console(theme=theme)