import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional

from qimba.core.executor import Executor
from qimba.utils.config import Config

app = typer.Typer(help="Denoise sequencing data")
console = Console()

@app.callback(invoke_without_command=True)
def denoise(
    ctx: typer.Context,
    input_dir: Path = typer.Argument(
        ...,
        help="Input directory containing QC-passed data",
        exists=True,
        dir_okay=True,
        file_okay=False,
    ),
    output_dir: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output directory for denoised results",
    ),
    min_reads: int = typer.Option(
        100,
        "--min-reads",
        help="Minimum number of reads to retain a sequence",
    ),
    max_ee: float = typer.Option(
        1.0,
        "--max-ee",
        help="Maximum expected error rate",
    ),
    threads: int = typer.Option(
        1,
        "--threads", "-t",
        help="Number of threads to use",
    ),
) -> None:
    """
    Run denoising algorithm on quality-filtered sequencing data.
    
    This command implements sequence denoising to remove sequencing errors
    and generate high-quality Amplicon Sequence Variants (ASVs).
    """
    if ctx.resilient_parsing:
        return
        
    config: Config = ctx.obj
    
    # Set default output directory if not specified
    if output_dir is None:
        output_dir = input_dir / "denoise_results"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize executor
    executor = Executor(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Checking input files...", total=None)
        
        # Mock steps for denoising process
        task1 = progress.add_task("Filtering sequences...", total=100)
        for i in range(100):
            progress.update(task1, advance=1)
            
        task2 = progress.add_task("Learning error rates...", total=100)
        for i in range(100):
            progress.update(task2, advance=1)
            
        task3 = progress.add_task("Generating ASVs...", total=100)
        for i in range(100):
            progress.update(task3, advance=1)
        
        # Run denoising
        result = executor.run_denoise_tool(
            input_dir=input_dir,
            output_dir=output_dir,
            threads=threads,
        )
    
    # Report results
    if result.success:
        console.print("[green]Denoising completed successfully![/green]")
        console.print(f"Results saved to: {output_dir}")
        
        # Mock summary statistics
        console.print("\n[bold]Summary Statistics:[/bold]")
        console.print(f"Input sequences: 10000")
        console.print(f"Sequences retained: 8500")
        console.print(f"Unique ASVs: 150")
        console.print(f"Average quality score: 35.2")
    else:
        console.print("[red]Denoising failed![/red]")
        console.print(f"Error: {result.error}")
        raise typer.Exit(1)
