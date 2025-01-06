# scripts/process_dataset.py
import asyncio
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from bookdataset.core.config import Config
from bookdataset.extractors.metadata import MetadataExtractor
from bookdataset.extractors.librarian import LibrarianExtractor

console = Console()

async def process_story(text: str, metadata_extractor: MetadataExtractor, librarian_extractor: LibrarianExtractor):
    """Process a single story with both extractors"""
    try:
        # Get basic metadata
        metadata = await metadata_extractor.extract(text)
        
        # Get librarian insights
        librarian_data = await librarian_extractor.extract(text)
        
        # Combine results
        return {
            **metadata,
            **librarian_data
        }
    except Exception as e:
        console.print(f"[red]Error processing story: {str(e)}[/]")
        return None

async def main():
    console.print("[bold blue]Starting Dataset Processing[/]")
    
    # Initialize config and extractors
    config = Config(project_root / "config")
    metadata_extractor = MetadataExtractor(config)
    librarian_extractor = LibrarianExtractor(config)
    
    # Load raw dataset
    raw_data_path = project_root / "bookdataset" /"data" / "raw" / "stories.csv"
    if not raw_data_path.exists():
        console.print(f"[red]Error: No raw data found at {raw_data_path}[/]")
        return

    df = pd.read_csv(raw_data_path)

    processed_stories = []

    with Progress() as progress:
        task = progress.add_task("[cyan]Processing stories...", total=len(df))
        
        # Process in batches to avoid rate limits
        batch_size = 2
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            # Process batch concurrently
            tasks = [
                process_story(
                    row['content'], 
                    metadata_extractor, 
                    librarian_extractor
                ) for _, row in batch.iterrows()
            ]
             
            # Wait for batch results
            batch_results = await asyncio.gather(*tasks)
            
            # Store successful results
            for result in batch_results:
                if result:
                    processed_stories.append(result)
            
            # Update progress
            progress.update(task, advance=len(batch))
            
            # Optional: Add delay between batches
            await asyncio.sleep(30)
    
    # Create enriched dataset
    enriched_df = pd.DataFrame(processed_stories)
    
    # Save results
    output_path = project_root / "bookdataset" / "data" / "processed" / "enriched_dataset.csv"
    output_path.parent.mkdir(exist_ok=True)
    enriched_df.to_csv(output_path, index=False)
    
    console.print(f"\n[green]Processing complete![/]")
    console.print(f"Processed {len(processed_stories)} stories")
    console.print(f"Results saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())