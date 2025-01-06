
# bookdataset/extractors/librarian.py
from typing import Dict, Any
import json
from .base import BaseExtractor
from rich.console import Console

console = Console()

class LibrarianExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        try:
            prompt = self.config.get_prompt("librarian")
            
            console.print("\n[bold blue]System Message for Librarian Analysis:[/]")
            console.print(prompt.system_message)
            
            response = await self._call_openai(
                system_message=prompt.system_message,
                user_message=f"Story Content:\n{content}"
            )
            
            console.print("\n[bold green]Raw Response from Librarian Analysis:[/]")
            console.print(response)
            
            metadata = json.loads(response)
            
            if isinstance(metadata.get("PositiveCharacters"), str):
                metadata["PositiveCharacters"] = [metadata["PositiveCharacters"]]
            if isinstance(metadata.get("NegativeCharacters"), str):
                metadata["NegativeCharacters"] = [metadata["NegativeCharacters"]]
                
            return metadata
            
        except json.JSONDecodeError as e:
            console.print(f"\n[bold red]Error parsing JSON in Librarian Analysis: {e}[/]")
            console.print("[bold yellow]Response that failed to parse:[/]")
            console.print(response)
            return {
                "LibrariansSummary": None,
                "PositiveCharacters": None,
                "NegativeCharacters": None,
                "error": f"JSON parse error: {str(e)}"
            }
        except Exception as e:
            console.print(f"\n[bold red]Unexpected error in Librarian Analysis: {str(e)}[/]")
            return {
                "LibrariansSummary": None,
                "PositiveCharacters": None,
                "NegativeCharacters": None,
                "error": str(e)
            }