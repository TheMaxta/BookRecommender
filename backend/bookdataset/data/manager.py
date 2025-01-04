# bookdataset/data/manager.py
from typing import List, Optional
import pandas as pd
from pathlib import Path
from .models import StoryMetadata, LibrarianMetadata, EnrichedStory

class DataManager:
    def __init__(self, csv_path: Optional[Path] = None):
        """
        Initialize the DataManager with an optional path to the CSV file.
        If no path is provided, it will look for enriched_dataset.csv in the current directory.
        """
        if csv_path is None:
            # Default to the enriched_dataset.csv in the project root
            self.csv_path = Path(__file__).parent.parent.parent / "enriched_dataset.csv"
        else:
            self.csv_path = csv_path

        if not self.csv_path.exists():
            raise FileNotFoundError(f"Could not find dataset at {self.csv_path}")

    def load_enriched_dataset(self) -> pd.DataFrame:
        """
        Load the enriched dataset from CSV.
        """
        try:
            df = pd.read_csv(self.csv_path, na_values=[''], keep_default_na=False)
            
            # Fill empty values for multiple columns
            df['LibrariansSummary'] = df['LibrariansSummary'].fillna("This book doesn't have a summary")
            df['PositiveCharacters'] = df['PositiveCharacters'].fillna("No positive characters listed")
            df['NegativeCharacters'] = df['NegativeCharacters'].fillna("No negative characters listed")
            df['error'] = df['error'].fillna("None")
            
            return df
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            raise

    async def save_enriched_stories(self, stories: List[EnrichedStory]):
        """Save processed stories to CSV"""
        records = []
        for story in stories:
            record = {
                **story.metadata.dict(),
                **(story.librarian.dict() if story.librarian else {})
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        df.to_csv(self.csv_path, index=False)