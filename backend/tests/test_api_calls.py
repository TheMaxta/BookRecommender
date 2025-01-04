# tests/test_api_calls.py
import asyncio
from pathlib import Path
import os
from rich.console import Console
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
import sys
sys.path.append(str(project_root))

from bookdataset.extractors.metadata import MetadataExtractor
from bookdataset.extractors.librarian import LibrarianExtractor

console = Console()

class SimpleConfig:
    def get(self, key: str, default: Any = None) -> str:
        if key == "model":
            return "gpt-4-turbo-preview"
        return default

    def get_prompt(self, name: str) -> Dict[str, Any]:
        if name == "base_metadata":
            return {
                "system_message": """You are a creative assistant specializing in children's literature. 
                Analyze the story and return a JSON object with these exact fields:
                {
                    "Title": "Story title or a fitting one if not provided",
                    "Subject": "One of: Animals, Friendship, Family, Adventure, Fantasy and Imagination, Life Lessons",
                    "Description": "Brief summary under 50 words"
                }
                
                IMPORTANT: Return only the JSON object, with no additional text or markdown formatting.""",
                "output_schema": {}
            }
        elif name == "librarian":
            return {
                "system_message": """You are an expert children's librarian. 
                Analyze the given story and return a JSON object with exactly this structure:
                {
                    "LibrariansSummary": "A structured recommendation with reading level and appeal",
                    "PositiveCharacters": ["Array", "of", "good", "character", "names"],
                    "NegativeCharacters": ["Array", "of", "antagonist", "names"]
                }
                
                Guidelines:
                - LibrariansSummary should include reading level and target age
                - Character arrays should contain only names, not descriptions
                - If there are no negative characters, return an empty array []
                
                IMPORTANT: 
                1. Return ONLY the JSON object
                2. Do not include any additional text or markdown
                3. Ensure the response is valid JSON
                4. Use exactly the field names shown above""",
                "output_schema": {}
            }
        return {}

async def test_metadata_extraction():
    """Test actual metadata extraction via API"""
    console.print("\n[bold blue]Testing Metadata Extraction API Call...[/]")
    
    config = SimpleConfig()
    extractor = MetadataExtractor(config)
    
    sample_text = """
    The Friendly Dragon
    
    Once there was a dragon named Spark who lived in a cave at the edge of a small village. 
    Unlike other dragons, Spark didn't like to frighten people. Instead, he wanted to make friends. 
    One day, he helped a lost child find their way home, and from that day on, 
    the villagers realized that not all dragons were scary.
    """
    
    try:
        result = await extractor.extract(sample_text)
        console.print("[green]Metadata Extraction Result:[/]")
        console.print(result)
        return True
    except Exception as e:
        console.print(f"[red]Metadata Extraction Failed: {str(e)}[/]")
        console.print_exception()
        return False

async def test_librarian_extraction():
    """Test actual librarian extraction via API"""
    console.print("\n[bold blue]Testing Librarian Extraction API Call...[/]")
    
    config = SimpleConfig()
    extractor = LibrarianExtractor(config)
    
    sample_text = """
    The Friendly Dragon
    
    Once there was a dragon named Spark who lived in a cave at the edge of a small village. 
    Unlike other dragons, Spark didn't like to frighten people. Instead, he wanted to make friends. 
    One day, he helped a lost child find their way home, and from that day on, 
    the villagers realized that not all dragons were scary.
    """
    
    try:
        result = await extractor.extract(sample_text)
        console.print("[green]Librarian Extraction Result:[/]")
        console.print(result)
        return True
    except Exception as e:
        console.print(f"[red]Librarian Extraction Failed: {str(e)}[/]")
        console.print_exception()
        return False

async def main():
    console.print("[bold yellow]Starting Real API Tests[/]")
    
    # Make sure we have API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]No OpenAI API key found in environment![/]")
        return
    
    metadata_result = await test_metadata_extraction()
    librarian_result = await test_librarian_extraction()
    
    console.print("\n[bold yellow]Test Summary[/]")
    console.print(f"Metadata Extraction: {'[green]PASS' if metadata_result else '[red]FAIL'}[/]")
    console.print(f"Librarian Extraction: {'[green]PASS' if librarian_result else '[red]FAIL'}[/]")

if __name__ == "__main__":
    asyncio.run(main())