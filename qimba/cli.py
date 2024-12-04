import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional
from pathlib import Path

from qimba.commands import run, qc, denoise, config
from qimba.utils.config import Config

# Initialize Typer app
app = typer.Typer(
    name="qimba",
    help="A modern bioinformatics analysis pipeline",
    add_completion=False,
)

# Initialize Rich console
console = Console()

# Add subcommands
app.add_typer(run.app, name="run")
app.add_typer(qc.app, name="qc")
app.add_typer(denoise.app, name="denoise")
app.add_typer(config.app, name="config")

def version_callback(value: bool):
    if value:
        console.print(Panel.fit("Qimba version 0.1.0", title="Version"))
        raise typer.Exit()

@app.callback()
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True,
        help="Show the application version and exit."
    ),
    config: Optional[Path] = typer.Option(
        None, "--config", "-c",
        help="Path to configuration file."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Enable verbose output."
    ),
) -> None:
    """
    Qimba: A modern bioinformatics analysis pipeline.
    
    Run 'qimba COMMAND --help' for more information on a command.
    """
    # Store configuration in context
    ctx.obj = Config(
        config_path=config,
        verbose=verbose
    )