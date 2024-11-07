from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from pydantic import BaseModel

class Config(BaseModel):
    """
    Configuration handler for Qimba.
    """
    config_path: Optional[Path] = None
    verbose: bool = False
    tools: Dict[str, Any] = {}
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.config_path and self.config_path.exists():
            self._load_config()
            
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        with open(self.config_path) as f:
            config_data = yaml.safe_load(f)
            # Update the current config with loaded data
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
