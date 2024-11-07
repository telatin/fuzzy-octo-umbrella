import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console

from qimba.utils.config import Config

console = Console()

@dataclass
class ExecutionResult:
    """Contains the result of an external command execution."""
    success: bool
    error: Optional[str] = None
    output: Optional[str] = None

class Executor:
    """
    Handles execution of external bioinformatics tools.
    """
    
    def __init__(self, config: Config):
        self.config = config
        
    def _run_command(
        self,
        cmd: list[str],
        check: bool = True,
        **kwargs
    ) -> ExecutionResult:
        """
        Execute an external command and return the result.
        """
        try:
            if self.config.verbose:
                console.print(f"[blue]Running command: {' '.join(cmd)}[/blue]")
                
            result = subprocess.run(
                cmd,
                check=check,
                text=True,
                capture_output=True,
                **kwargs
            )
            
            return ExecutionResult(
                success=True,
                output=result.stdout
            )
            
        except subprocess.CalledProcessError as e:
            return ExecutionResult(
                success=False,
                error=f"Command failed with exit code {e.returncode}: {e.stderr}"
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e)
            )
            
    def run_qc_tool(
        self,
        input_dir: Path,
        output_dir: Path,
        min_quality: int = 20,
        threads: int = 1
    ) -> ExecutionResult:
        """
        Run the quality control tool.
        """
        # Example command - replace with actual QC tool
        cmd = [
            "fastqc",  # Replace with actual QC tool
            "-o", str(output_dir),
            "-t", str(threads),
            "-q", str(min_quality),
            str(input_dir)
        ]
        return self._run_command(cmd)
        
    def run_denoise_tool(
        self,
        input_dir: Path,
        output_dir: Path,
        threads: int = 1
    ) -> ExecutionResult:
        """
        Run the denoising tool.
        """
        # Example command - replace with actual denoising tool
        cmd = [
            "denoiser",  # Replace with actual denoising tool
            "-i", str(input_dir),
            "-o", str(output_dir),
            "-t", str(threads)
        ]
        return self._run_command(cmd)
