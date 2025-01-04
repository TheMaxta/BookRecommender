# bookdataset/data/models.py
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class StoryMetadata(BaseModel):
    unique_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    book_collection: str
    csv_file: str
    title: str
    subject: str
    description: str
    rating: Optional[int] = None
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class LibrarianMetadata(BaseModel):
    unique_id: str
    librarians_summary: str
    positive_characters: List[str]
    negative_characters: List[str]
    
class EnrichedStory(BaseModel):
    metadata: StoryMetadata
    librarian: Optional[LibrarianMetadata] = None
