# qimba/commands/config.py

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from qimba.utils.config import Config, DEFAULT_CONFIG_FILE

app = typer.Typer(help="Manage configuration settings")
console = Console()

@app.callback(invoke_without_command=True)
def show_config(
    ctx: typer.Context,
) -> None:
    """Show current configuration settings."""
    config: Config = ctx.obj
    
    table = Table(title="Current Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    # Basic settings
    table.add_row("Config File", str(config.config_path or DEFAULT_CONFIG_FILE))
    table.add_row("Threads", str(config.threads))
    table.add_row("Verbose", str(config.verbose))
    
    # Paths
    table.add_row("Data Directory", str(config.data_dir))
    table.add_row("Temp Directory", str(config.temp_dir))
    
    # QC settings
    table.add_section()
    table.add_row("QC Tool", config.qc.tool)
    table.add_row("Min Quality", str(config.qc.min_quality))
    table.add_row("Min Length", str(config.qc.min_length))
    table.add_row("Max N", str(config.qc.max_n))
    
    # Denoise settings
    table.add_section()
    table.add_row("Denoise Tool", config.denoise.tool)
    table.add_row("Min Reads", str(config.denoise.min_reads))
    table.add_row("Max EE", str(config.denoise.max_ee))
    
    console.print(table)

@app.command()
def init(
    config_path: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help=f"Output path for config file (default: {DEFAULT_CONFIG_FILE})"
    ),
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Overwrite existing config file"
    )
) -> None:
    """Initialize a new configuration file with default settings."""
    # Determine config path
    config_path = config_path or DEFAULT_CONFIG_FILE
    
    if config_path.exists() and not force:
        console.print(f"[yellow]Config file already exists at {config_path}[/yellow]")
        console.print("[yellow]Use --force to overwrite[/yellow]")
        raise typer.Exit(1)
    
    # Create new config with defaults and save it
    config = Config()
    config.save(config_path)
    console.print(f"[green]Created new config file at {config_path}[/green]")

@app.command()
def edit(
    ctx: typer.Context,
    setting: str = typer.Argument(..., help="Setting to modify (e.g., qc.min_quality)"),
    value: str = typer.Argument(..., help="New value"),
) -> None:
    """Modify a configuration setting."""
    config: Config = ctx.obj
    
    try:
        # Handle nested settings
        if '.' in setting:
            section, key = setting.split('.', 1)
            if hasattr(config, section):
                section_obj = getattr(config, section)
                if hasattr(section_obj, key):
                    # Convert value to appropriate type
                    current_value = getattr(section_obj, key)
                    converted_value = type(current_value)(value)
                    setattr(section_obj, key, converted_value)
                else:
                    raise ValueError(f"Unknown setting: {setting}")
            else:
                raise ValueError(f"Unknown section: {section}")
        else:
            if hasattr(config, setting):
                # Convert value to appropriate type
                current_value = getattr(config, setting)
                converted_value = type(current_value)(value)
                setattr(config, setting, converted_value)
            else:
                raise ValueError(f"Unknown setting: {setting}")
        
        # Save changes
        config.save()
        console.print(f"[green]Updated {setting} to {value}[/green]")
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error updating config: {e}[/red]")
        raise typer.Exit(1)