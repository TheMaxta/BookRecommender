# bookdataset/core/config.py
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from pydantic import BaseModel

class PromptConfig(BaseModel):
    system_message: str
    output_schema: Dict[str, Any]

class Config:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.prompts: Dict[str, PromptConfig] = {}
        self.settings: Dict[str, Any] = {
            "model": "gpt-4o",  # default model
            "temperature": 0.7,
        }
        self._load_prompts()
        self._load_settings()

    def _load_prompts(self):
        """Load prompt configurations from YAML files"""
        prompts_dir = self.config_dir / "prompts"
        if not prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found at {prompts_dir}")
            
        for prompt_file in prompts_dir.glob("*.yaml"):
            with prompt_file.open() as f:
                config = yaml.safe_load(f)
                self.prompts[prompt_file.stem] = PromptConfig(**config)

    def _load_settings(self):
        """Load general settings from config.yaml if it exists"""
        settings_path = self.config_dir / "config.yaml"
        if settings_path.exists():
            with settings_path.open() as f:
                self.settings.update(yaml.safe_load(f))

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value by key"""
        return self.settings.get(key, default)

    def get_prompt(self, name: str) -> PromptConfig:
        """Get a prompt configuration by name"""
        if name not in self.prompts:
            raise KeyError(f"No prompt configuration found for '{name}'")
        return self.prompts[name]