# qimba/utils/config.py

import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from rich.console import Console

console = Console()

# Default configuration location
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "qimba"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"

class QCConfig(BaseModel):
    """Quality control specific configuration."""
    min_quality: int = Field(default=20, description="Minimum quality score threshold")
    min_length: int = Field(default=100, description="Minimum read length")
    max_n: int = Field(default=0, description="Maximum number of N bases allowed")
    tool: str = Field(default="fastp", description="QC tool to use")

class DenoiseConfig(BaseModel):
    """Denoising specific configuration."""
    min_reads: int = Field(default=10, description="Minimum number of reads for ASV")
    max_ee: float = Field(default=1.0, description="Maximum expected error rate")
    tool: str = Field(default="dada2", description="Denoising tool to use")

class Config(BaseModel):
    """Main configuration handler for Qimba."""
    config_path: Optional[Path] = None
    verbose: bool = Field(default=False, description="Enable verbose output")
    threads: int = Field(default=1, description="Number of threads to use")
    
    # Tool configurations
    qc: QCConfig = Field(default_factory=QCConfig, description="Quality control settings")
    denoise: DenoiseConfig = Field(default_factory=DenoiseConfig, description="Denoising settings")
    
    # Paths and environment
    data_dir: Path = Field(
        default=Path.home() / ".local" / "share" / "qimba",
        description="Directory for persistent data"
    )
    temp_dir: Path = Field(
        default=Path.home() / ".cache" / "qimba",
        description="Directory for temporary files"
    )

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        # If no config_path is provided, use default
        if 'config_path' not in data:
            data['config_path'] = DEFAULT_CONFIG_FILE
            
        super().__init__(**data)
        if self.config_path and self.config_path.exists():
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path) as f:
                config_data = json.load(f)
            
            # Handle Path objects specially
            if "data_dir" in config_data:
                config_data["data_dir"] = Path(config_data["data_dir"])
            if "temp_dir" in config_data:
                config_data["temp_dir"] = Path(config_data["temp_dir"])
            
            # Update configuration
            for key, value in config_data.items():
                if hasattr(self, key):
                    if key in ["qc", "denoise"]:
                        # Handle nested configs
                        current_value = getattr(self, key)
                        for subkey, subvalue in value.items():
                            setattr(current_value, subkey, subvalue)
                    else:
                        setattr(self, key, value)
                        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to load configuration: {e}[/yellow]")

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save current configuration to file."""
        save_path = config_path or self.config_path or DEFAULT_CONFIG_FILE
        
        # Create config data
        config_data = {
            "verbose": self.verbose,
            "threads": self.threads,
            "qc": self.qc.model_dump(),
            "denoise": self.denoise.model_dump(),
            "data_dir": str(self.data_dir),
            "temp_dir": str(self.temp_dir)
        }
        
        # Create directory if needed
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write config file
        with open(save_path, 'w') as f:
            json.dump(config_data, f, indent=2)
            
        # Update config_path if we used a new path
        if config_path:
            self.config_path = config_path
        
        console.print(f"[green]Configuration saved to {save_path}[/green]")