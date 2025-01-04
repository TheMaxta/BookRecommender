# bookdataset/extractors/librarian.py
from typing import Dict, Any, List
import json
from .base import BaseExtractor

class LibrarianExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        """
        Extract librarian-specific metadata including summary and character analysis.
        
        Args:
            content: The story text to analyze
            
        Returns:
            Dictionary containing LibrariansSummary, PositiveCharacters, and NegativeCharacters
        """
        prompt = self.config.get_prompt("librarian")
        
        response = await self._call_openai(
            system_message=prompt.system_message,
            user_message=f"Story Content:\n{content}"
        )
        
        try:
            # Parse the response
            metadata = json.loads(response)
            
            # Validate required fields
            required_fields = ["LibrariansSummary", "PositiveCharacters", "NegativeCharacters"]
            for field in required_fields:
                if field not in metadata:
                    raise ValueError(f"Missing required field: {field}")
                
            # Ensure character lists are actually lists
            if isinstance(metadata["PositiveCharacters"], str):
                metadata["PositiveCharacters"] = [metadata["PositiveCharacters"]]
            if isinstance(metadata["NegativeCharacters"], str):
                metadata["NegativeCharacters"] = [metadata["NegativeCharacters"]]
                
            return {
                "LibrariansSummary": metadata["LibrariansSummary"],
                "PositiveCharacters": metadata["PositiveCharacters"],
                "NegativeCharacters": metadata["NegativeCharacters"]
            }
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "LibrariansSummary": None,
                "PositiveCharacters": None,
                "NegativeCharacters": None,
                "error": f"JSON parse error: {str(e)}"
            }
        except Exception as e:
            print(f"Error processing librarian metadata: {e}")
            return {
                "LibrariansSummary": None,
                "PositiveCharacters": None,
                "NegativeCharacters": None,
                "error": f"Processing error: {str(e)}"
            }