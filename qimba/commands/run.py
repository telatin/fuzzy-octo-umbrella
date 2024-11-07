import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional

from qimba.core.pipeline import Pipeline
from qimba.utils.config import Config

app = typer.Typer(help="Run the complete analysis pipeline")
console = Console()

@app.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    input_dir: Path = typer.Argument(
        ...,
        help="Input directory containing raw data",
        exists=True,
        dir_okay=True,
        file_okay=False,
    ),
    output_dir: Path = typer.Option(
        "./qimba_output",
        "--output", "-o",
        help="Output directory for results",
    ),
    threads: int = typer.Option(
        1,
        "--threads", "-t",
        help="Number of threads to use",
    ),
    skip_qc: bool = typer.Option(
        False,
        "--skip-qc",
        help="Skip quality control step",
    ),
) -> None:
    """
    Run the complete Qimba analysis pipeline.
    
    This will execute all steps in sequence:
    1. Quality Control (QC)
    2. Denoising
    [Additional steps...]
    """
    if ctx.resilient_parsing:
        return
        
    config: Config = ctx.obj
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize pipeline
    pipeline = Pipeline(
        input_dir=input_dir,
        output_dir=output_dir,
        threads=threads,
        config=config
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Execute pipeline steps
        if not skip_qc:
            progress.add_task("Running Quality Control...", total=None)
            pipeline.run_qc()
            
        progress.add_task("Running Denoising...", total=None)
        pipeline.run_denoise()
        
        # Add more pipeline steps here
        
    console.print("[green]Pipeline completed successfully! :rocket:[/green]")
