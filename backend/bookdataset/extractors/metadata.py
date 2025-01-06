# bookdataset/extractors/metadata.py
from typing import Dict, Any
import json
from .base import BaseExtractor
from rich.console import Console

console = Console()

class MetadataExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        try:
            prompt = self.config.get_prompt("base_metadata")
            
            console.print("\n[bold blue]System Message for Metadata Extraction:[/]")
            console.print(prompt.system_message)
            
            response = await self._call_openai(
                system_message=prompt.system_message,
                user_message=f"Story Content:\n{content}"
            )
            
            console.print("\n[bold green]Raw Response from Metadata Extraction:[/]")
            console.print(response)
            
            metadata = json.loads(response)
            return metadata
            
        except json.JSONDecodeError as e:
            console.print(f"\n[bold red]Error parsing JSON in Metadata Extraction: {e}[/]")
            console.print("[bold yellow]Response that failed to parse:[/]")
            console.print(response)
            return {
                "Title": None,
                "Subject": None,
                "Description": None,
                "error": f"JSON parse error: {str(e)}"
            }
        except Exception as e:
            console.print(f"\n[bold red]Unexpected error in Metadata Extraction: {str(e)}[/]")
            return {
                "Title": None,
                "Subject": None,
                "Description": None,
                "error": str(e)
            }