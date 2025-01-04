# tests/test_components.py
import asyncio
import sys
from pathlib import Path
import yaml

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rich.console import Console
from rich.table import Table

from bookdataset.core.config import Config
from bookdataset.extractors.metadata import MetadataExtractor
from bookdataset.extractors.librarian import LibrarianExtractor
from bookdataset.data.manager import DataManager
from bookdataset.core.chat import ChatManager

console = Console()

async def test_data_manager():
    """Test DataManager functionality"""
    console.print("\n[bold blue]Testing DataManager...[/]")
    
    try:
        # Initialize DataManager
        data_manager = DataManager()
        
        # Load dataset
        df = data_manager.load_enriched_dataset()
        
        # Display basic information
        console.print(f"Successfully loaded dataset with {len(df)} rows")
        console.print("Columns present:", df.columns.tolist())
        
        # Show sample data
        table = Table(title="Sample Data (First 3 Rows)")
        for col in ['Title', 'Subject', 'rating']:
            table.add_column(col)
        
        for _, row in df.head(3).iterrows():
            table.add_row(str(row['Title']), str(row['Subject']), str(row['rating']))
        
        console.print(table)
        return True
        
    except Exception as e:
        console.print(f"[bold red]Error testing DataManager: {e}[/]")
        console.print_exception()
        return False

async def test_chat_manager():
    """Test ChatManager functionality"""
    console.print("\n[bold blue]Testing ChatManager...[/]")
    
    try:
        # Initialize managers
        data_manager = DataManager()
        chat_manager = ChatManager()
        
        # Get a sample book
        df = data_manager.load_enriched_dataset()
        sample_book = df.iloc[0].to_dict()
        
        # Test chat interaction
        messages = [
            {"role": "user", "content": "What is this book about?"}
        ]
        
        response = await chat_manager.generate_response(
            book=sample_book,
            messages=messages
        )
        
        console.print("\nSample chat response:")
        console.print(f"[green]{response}[/]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]Error testing ChatManager: {e}[/]")
        console.print_exception()
        return False

async def test_extractors():
    """Test Metadata and Librarian extractors"""
    console.print("\n[bold blue]Testing Extractors...[/]")
    
    try:
        # Ensure config directory exists
        config_path = project_root / "config"
        prompts_path = config_path / "prompts"
        
        config_path.mkdir(exist_ok=True)
        prompts_path.mkdir(exist_ok=True)

        # Create base config if it doesn't exist
        config_yaml_path = config_path / "config.yaml"
        if not config_yaml_path.exists():
            console.print("[yellow]Creating base config.yaml...[/]")
            config_data = {
                "model": "gpt-4o",
                "temperature": 0.7,
                "max_tokens": 1000,
                "timeout": 30,
                "retry_count": 5
            }
            with config_yaml_path.open('w') as f:
                yaml.dump(config_data, f)

        # Create prompt files if they don't exist
        prompts = {
            "base_metadata.yaml": {
                "system_message": "You are a creative assistant specializing in children's literature...",
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "Title": {"type": "string"},
                        "Subject": {
                            "type": "string",
                            "enum": ["Animals", "Friendship", "Family", "Adventure", 
                                   "Fantasy and Imagination", "Life Lessons"]
                        },
                        "Description": {"type": "string", "maxLength": 50}
                    }
                }
            },
            "librarian.yaml": {
                "system_message": "You are an expert children's librarian...",
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "LibrariansSummary": {"type": "string"},
                        "PositiveCharacters": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "NegativeCharacters": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        }

        for filename, content in prompts.items():
            prompt_path = prompts_path / filename
            if not prompt_path.exists():
                console.print(f"[yellow]Creating {filename}...[/]")
                with prompt_path.open('w') as f:
                    yaml.dump(content, f)

        # Initialize config and extractors
        config = Config(config_path)
        metadata_extractor = MetadataExtractor(config)
        librarian_extractor = LibrarianExtractor(config)
        
        # Sample story text for testing
        sample_text = """
        The Friendly Dragon
        
        Once there was a dragon named Spark who lived in a cave at the edge of a small village. 
        Unlike other dragons, Spark didn't like to frighten people. Instead, he wanted to make friends. 
        One day, he helped a lost child find their way home, and from that day on, 
        the villagers realized that not all dragons were scary.
        """
        
        # Test metadata extraction
        console.print("\nTesting Metadata Extraction:")
        metadata = await metadata_extractor.extract(sample_text)
        console.print(metadata)
        
        # Test librarian extraction
        console.print("\nTesting Librarian Extraction:")
        librarian_data = await librarian_extractor.extract(sample_text)
        console.print(librarian_data)
        
        return True
        
    except Exception as e:
        console.print(f"[bold red]Error testing extractors: {e}[/]")
        console.print_exception()
        return False

async def main():
    console.print("[bold yellow]Starting Component Tests[/]")
    
    # Run tests
    results = {
        "DataManager": await test_data_manager(),
        "ChatManager": await test_chat_manager(),
        "Extractors": await test_extractors()
    }
    
    # Display summary
    console.print("\n[bold yellow]Test Summary[/]")
    table = Table(title="Test Results")
    table.add_column("Component")
    table.add_column("Status")
    
    for component, success in results.items():
        status = "[green]PASS[/]" if success else "[red]FAIL[/]"
        table.add_row(component, status)
    
    console.print(table)

if __name__ == "__main__":
    asyncio.run(main())