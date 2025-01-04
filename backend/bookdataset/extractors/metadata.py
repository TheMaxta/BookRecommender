# bookdataset/extractors/metadata.py
from typing import Dict, Any
import json
from .base import BaseExtractor

class MetadataExtractor(BaseExtractor):
    async def extract(self, content: str) -> Dict[str, Any]:
        prompt = self.config.get_prompt("base_metadata")
        response = await self._call_openai(
            system_message=prompt.system_message,
            user_message=f"Story Content:\n{content}"
        )
        
        try:
            metadata = json.loads(response)
            # Validate against schema here
            return metadata
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "Title": None,
                "Subject": None,
                "Description": None,
                "error": f"JSON parse error: {str(e)}"
            }
