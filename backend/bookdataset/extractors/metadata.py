# bookdataset/extractors/metadata.py
from typing import Dict, Any
import json
from .base import BaseExtractor

class MetadataExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        prompt = self.config.get_prompt("base_metadata")
        response = await self._call_openai(
            system_message=prompt["system_message"],  # Access as dictionary
            user_message=f"Story Content:\n{content}"
        )
        
        try:
            metadata = json.loads(response)
            return metadata
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "Title": None,
                "Subject": None,
                "Description": None,
                "error": f"JSON parse error: {str(e)}"
            }

# bookdataset/extractors/librarian.py
from typing import Dict, Any
import json
from .base import BaseExtractor

class LibrarianExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        """
        Extract librarian-specific metadata including summary and character analysis.
        """
        prompt = self.config.get_prompt("librarian")
        
        response = await self._call_openai(
            system_message=prompt["system_message"],  # Access as dictionary
            user_message=f"Story Content:\n{content}"
        )
        
        try:
            metadata = json.loads(response)
            
            # Ensure character lists are actually lists
            if isinstance(metadata.get("PositiveCharacters"), str):
                metadata["PositiveCharacters"] = [metadata["PositiveCharacters"]]
            if isinstance(metadata.get("NegativeCharacters"), str):
                metadata["NegativeCharacters"] = [metadata["NegativeCharacters"]]
                
            return metadata
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "LibrariansSummary": None,
                "PositiveCharacters": None,
                "NegativeCharacters": None,
                "error": f"JSON parse error: {str(e)}"
            }