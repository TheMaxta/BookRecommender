# bookdataset/api/endpoints.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
from pydantic import BaseModel
import pandas as pd
from pathlib import Path

from bookdataset.data.models import EnrichedStory
from bookdataset.data.manager import DataManager
from bookdataset.core.chat import ChatManager

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    unique_id: str
    messages: List[Message]

# Initialize FastAPI
app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
data_manager = DataManager()  # Will use default path to enriched_dataset.csv
chat_manager = ChatManager()

# Load data at startup
df = data_manager.load_enriched_dataset()

@app.get("/api/categories")
def get_categories():
    """Returns a unique list of subjects (categories)."""
    categories = df["Subject"].unique().tolist()
    return {"categories": categories}

@app.get("/api/books")
def get_books(category: Optional[str] = None):
    """Returns top 10 books filtered by category."""
    if not category:
        return {"books": []}
    
    # Filter by category and sort by rating
    filtered_df = df[df["Subject"] == category].head(10).sort_values('rating', ascending=False)
    books = filtered_df.fillna('').to_dict(orient="records")
    
    return {"books": books}

@app.post("/api/chat")
async def chat_with_book(request: ChatRequest):
    """Handles chat interactions about a specific book."""
    try:
        # Get book data
        book_df = df[df["unique_id"] == request.unique_id]
        if book_df.empty:
            raise HTTPException(status_code=404, detail="Book not found")
        
        book = book_df.iloc[0]
        
        # Generate chat response
        response = await chat_manager.generate_response(
            book=book,
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages]
        )
        
        return {
            "message": {
                "role": "assistant",
                "content": response
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))