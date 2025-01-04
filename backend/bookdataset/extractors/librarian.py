# bookdataset/extractors/librarian.py
from typing import Dict, Any
import json
from .base import BaseExtractor

class LibrarianExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        """Extract librarian-specific metadata including summary and character analysis."""
        prompt = self.config.get_prompt("librarian")
        
        # Print the prompt we're sending
        print("\nSystem Message being sent to API:")
        print(prompt["system_message"])
        
        response = await self._call_openai(
            system_message=prompt["system_message"],
            user_message=f"Story Content:\n{content}"
        )
        
        # Print raw response before JSON parsing
        print("\nRaw API Response:")
        print(response)
        
        try:
            metadata = json.loads(response)
            
            # Ensure character lists are actually lists
            if isinstance(metadata.get("PositiveCharacters"), str):
                metadata["PositiveCharacters"] = [metadata["PositiveCharacters"]]
            if isinstance(metadata.get("NegativeCharacters"), str):
                metadata["NegativeCharacters"] = [metadata["NegativeCharacters"]]
                
            return metadata
            
        except json.JSONDecodeError as e:
            print(f"\nError parsing JSON response: {e}")
            print(f"Response that failed to parse: {response}")
            return {
                "LibrariansSummary": None,
                "PositiveCharacters": None,
                "NegativeCharacters": None,
                "error": f"JSON parse error: {str(e)}"
            }