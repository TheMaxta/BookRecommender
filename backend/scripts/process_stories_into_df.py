import csv
from pathlib import Path

DATA_DIR = Path("data")

def compile_stories():
    # Create a list to store all story records
    all_stories = []
    
    # Process each subfolder in the data directory
    subfolders = [d for d in DATA_DIR.iterdir() if d.is_dir()]
    if not subfolders:
        print("No subfolders found in 'data' directory.")
        return

    # Loop through each subfolder
    for subfolder in subfolders:
        book_collection_name = subfolder.name
        
        # Process each CSV file in the subfolder
        for csv_file in subfolder.glob("*.csv"):
            with csv_file.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Add collection and file information to each row
                    row["book_collection"] = book_collection_name
                    row["csv_file"] = csv_file.name
                    all_stories.append(row)
            
            print(f"Processed {csv_file}")

    # Write all stories to a single CSV file
    if all_stories:
        # Get all unique field names from all rows
        fieldnames = set()
        for story in all_stories:
            fieldnames.update(story.keys())
        
        # Write to stories.csv
        with open("stories.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(all_stories)
        
        print("All stories combined into stories.csv")
    else:
        print("No stories found to process")

if __name__ == "__main__":
    compile_stories()