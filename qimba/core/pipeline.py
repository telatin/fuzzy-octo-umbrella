from pathlib import Path
from typing import Optional
from rich.console import Console

from qimba.utils.config import Config
from qimba.core.executor import Executor

console = Console()

class Pipeline:
    """
    Pipeline orchestrator for running the complete Qimba workflow.
    """
    
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        threads: int = 1,
        config: Optional[Config] = None
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.threads = threads
        self.config = config or Config()
        self.executor = Executor(self.config)
        
    def run_qc(self) -> None:
        """Run the quality control step."""
        qc_output = self.output_dir / "qc_results"
        result = self.executor.run_qc_tool(
            input_dir=self.input_dir,
            output_dir=qc_output,
            threads=self.threads
        )
        if not result.success:
            console.print(f"[red]QC step failed: {result.error}[/red]")
            raise RuntimeError("QC step failed")
            
    def run_denoise(self) -> None:
        """Run the denoising step."""
        denoise_output = self.output_dir / "denoise_results"
        result = self.executor.run_denoise_tool(
            input_dir=self.input_dir,
            output_dir=denoise_output,
            threads=self.threads
        )
        if not result.success:
            console.print(f"[red]Denoising step failed: {result.error}[/red]")
            raise RuntimeError("Denoising step failed")
