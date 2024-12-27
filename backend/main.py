import os
import pandas as pd
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    filtered_df = df[df["Subject"] == category].head(10)
    
    # Convert DataFrame rows to dictionaries
    books = filtered_df.to_dict(orient="records")
    return {"books": books}
