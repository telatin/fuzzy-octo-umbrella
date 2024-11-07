# qimba/utils/config.py

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
        super().__init__(**data)
        if self.config_path and self.config_path.exists():
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            config_data = json.load(open(self.config_path))
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to load configuration: {e}[/yellow]")