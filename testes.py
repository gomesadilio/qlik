from rich import print as pt
from rich import console

c = console.Console()

c.rule('Meu novo texto')
c.print("[blink]meu novo texto[/]", justify='center', style='bold black on cyan')