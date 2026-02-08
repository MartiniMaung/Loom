import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def test():
    console.print("TEST WORKS!")

if __name__ == "__main__":
    app()
