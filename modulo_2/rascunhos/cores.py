# from colorama import init, Fore, Style
# init(autoreset=True)
# print(Fore.GREEN + 'Texto em verde com colorama!')
# print(Fore.RED + Style.BRIGHT + 'Texto vermelho e negrito com colorama!')

from rich import print as rprint, box
from rich.table import Table
from rich.progress import track
from time import sleep
from rich.panel import Panel
from rich.markdown import Markdown

rprint("[bold magenta]Texto em magenta e negrito com rich![/bold magenta]")
rprint("[yellow on blue]Texto amarelo com fundo azul usando rich![/]")


# Tabela colorida
rprint("\n[bold cyan]Tabela de Exemplo:[/bold cyan]")
table = Table(title="Planetas do Sistema Solar", box=box.ROUNDED)
table.add_column("Planeta", style="magenta")
table.add_column("Ordem", style="green")
table.add_row("Mercúrio", "1")
table.add_row("Vênus", "2")
table.add_row("Terra", "3")
table.add_row("Marte", "4")
rprint(table)


# Barra de progresso animada
rprint("\n[bold yellow]Barra de Progresso:[/bold yellow]")
for _ in track(range(10), description="Processando..."):
    sleep(0.1)


# Painel estilizado
rprint(Panel("[bold green]Sucesso![/bold green] Operação concluída.", title="Status", subtitle="rich panel"))


# Markdown formatado
md = Markdown("""
# Título em Markdown
- Item 1
- Item 2
**Texto em negrito**
""")
rprint(md)

