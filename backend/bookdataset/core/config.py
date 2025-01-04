# bookdataset/core/config.py
from pathlib import Path
from typing import Any, Dict
import yaml
from pydantic import BaseModel

class PromptConfig(BaseModel):
    system_message: str
    output_schema: Dict[str, Any]

class Config:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.prompts: Dict[str, PromptConfig] = {}
        self._load_prompts()

    def _load_prompts(self):
        prompts_dir = self.config_dir / "prompts"
        for prompt_file in prompts_dir.glob("*.yaml"):
            with prompt_file.open() as f:
                config = yaml.safe_load(f)
                self.prompts[prompt_file.stem] = PromptConfig(**config)

    def get_prompt(self, name: str) -> PromptConfig:
        return self.prompts[name]

