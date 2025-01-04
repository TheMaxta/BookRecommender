from typing import List, Optional
import pandas as pd
from pathlib import Path
from .models import StoryMetadata, LibrarianMetadata, EnrichedStory

class DataManager:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        (self.data_dir / "raw").mkdir(exist_ok=True)
        (self.data_dir / "processed").mkdir(exist_ok=True)

    async def load_stories(self) -> List[StoryMetadata]:
        """Load all stories from CSV files"""
        stories = []
        for csv_file in (self.data_dir / "raw").glob("*.csv"):
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                story = StoryMetadata(
                    book_collection=csv_file.parent.name,
                    csv_file=csv_file.name,
                    **row.to_dict()
                )
                stories.append(story)
        return stories

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
        output_path = self.data_dir / "processed" / "enriched_stories.csv"
        df.to_csv(output_path, index=False)