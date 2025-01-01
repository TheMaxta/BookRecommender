import os
import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from completions_api import CompletionsApi

# Define the models for request/response
class Message(BaseModel):
    role: str   # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    unique_id: str
    messages: List[Message]

# Initialize FastAPI
app = FastAPI()

# Enable CORS (for local dev, allow localhost ports 3000, 5000, etc.)
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

# Path to your CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), "all_book_data.csv")

# Load the CSV into a DataFrame once at startup
df = pd.read_csv(CSV_PATH)

@app.get("/api/categories")
def get_categories():
    """
    Returns a unique list of subjects (i.e., categories).
    """
    categories = df["Subject"].unique().tolist()
    return {"categories": categories}

@app.get("/api/books")
def get_books(category: Optional[str] = None):
    """
    Expects a query param ?category=NameOfCategory
    Returns top 10 books filtered by that category.
    If no category is provided, returns an empty list or some default response.
    """
    if not category:
        return {"books": []}
    
    # Filter by category
    filtered_df = df[df["Subject"] == category].head(10).sort_values('rating', ascending=False)
    
    # Convert DataFrame rows to dictionaries
    books = filtered_df.to_dict(orient="records")
    return {"books": books}


@app.post("/api/chat")
async def chat_with_book(request: ChatRequest):
    try:
        # Get the book from the DataFrame
        book_df = df[df["unique_id"] == request.unique_id]
        if book_df.empty:
            raise HTTPException(status_code=404, detail="Book not found")
            
        book = book_df.iloc[0]
        
        system_prompt = f"""You are a helpful assistant discussing the book with children. Your goal is to get the user to read the book. '{book['Title']}'. 
Use the following book content to answer questions:

{book['content']}

Keep your responses focused on the book's content and related literary discussion. 
If a question cannot be answered based on the provided content, politely say so."""

        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Initialize CompletionsApi instance
        completions_api = CompletionsApi()
        response = completions_api.generate_response(system_prompt, messages)
        
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