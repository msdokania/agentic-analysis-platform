from rich.console import Console
from rich.markdown import Markdown

console = Console()

def render_report(report: str):
    """
    Renders a Markdown report in a readable, styled console format.
    """
    md = Markdown(report)
    console.rule("[bold cyan]📊 Analysis Report")
    console.print(md)
    console.rule("[bold cyan]End of Report")