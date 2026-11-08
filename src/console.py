"""
TODO add docstring
"""

from rich.console import Console
from rich.theme import Theme

# TODO document the different themes and the reason
#  behind the color being chosen.
# TODO warning and danger are a tad bit confusing,
#  do smth about it.
theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "danger": "bold red",
})

console = Console(theme=theme)