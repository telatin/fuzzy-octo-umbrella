import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional

from qimba.core.executor import Executor
from qimba.utils.config import Config

app = typer.Typer(help="Run quality control analysis")
console = Console()

@app.callback(invoke_without_command=True)
def qc(
    ctx: typer.Context,
    input_dir: Path = typer.Argument(
        ...,
        help="Input directory containing raw data",
        exists=True,
        dir_okay=True,
        file_okay=False,
    ),
    output_dir: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output directory for QC results",
    ),
    min_quality: int = typer.Option(
        20,
        "--min-quality", "-q",
        help="Minimum quality score threshold",
    ),
    threads: int = typer.Option(
        1,
        "--threads", "-t",
        help="Number of threads to use",
    ),
) -> None:
    """
    Run quality control analysis on input data.
    """
    if ctx.resilient_parsing:
        return
        
    config: Config = ctx.obj
    
    # Set default output directory if not specified
    if output_dir is None:
        output_dir = input_dir / "qc_results"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize executor
    executor = Executor(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Running Quality Control...", total=None)
        
        # Run QC analysis
        result = executor.run_qc_tool(
            input_dir=input_dir,
            output_dir=output_dir,
            min_quality=min_quality,
            threads=threads
        )
        
        progress.update(task, completed=True)
    
    # Generate report
    if result.success:
        console.print("[green]Quality Control completed successfully![/green]")
        console.print(f"Results saved to: {output_dir}")
    else:
        console.print("[red]Quality Control failed![/red]")
        console.print(f"Error: {result.error}")
        raise typer.Exit(1)
