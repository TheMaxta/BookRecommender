import csv
from pathlib import Path

DATA_DIR = Path("data/original_scrape")

def compile_stories():
    # Create a list to store all story records
    all_stories = []
    
    # Process each subfolder in the data directory
    subfolders = [d for d in DATA_DIR.iterdir() if d.is_dir()]
    if not subfolders:
        print("No subfolders found in 'data' directory.")
        return

    # Keep track of all field names across all files
    all_fieldnames = set()

    # First pass: collect all possible field names
    for subfolder in subfolders:
        for csv_file in subfolder.glob("*.csv"):
            with csv_file.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                all_fieldnames.update(name for name in reader.fieldnames if name is not None)

    # Add our additional fields
    all_fieldnames.add("book_collection")
    all_fieldnames.add("csv_file")
    
    # Convert to sorted list
    fieldnames = sorted(all_fieldnames)

    # Second pass: read and store all records
    for subfolder in subfolders:
        book_collection_name = subfolder.name
        
        # Process each CSV file in the subfolder
        for csv_file in subfolder.glob("*.csv"):
            with csv_file.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Filter out None keys if they exist
                    row = {k: v for k, v in row.items() if k is not None}
                    # Add collection and file information
                    row["book_collection"] = book_collection_name
                    row["csv_file"] = csv_file.name
                    all_stories.append(row)
            
            print(f"Processed {csv_file}")

    # Write all stories to a single CSV file
    if all_stories:
        with open("stories.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_stories)
        
        print("All stories combined into stories.csv")
    else:
        print("No stories found to process")

if __name__ == "__main__":
    compile_stories()