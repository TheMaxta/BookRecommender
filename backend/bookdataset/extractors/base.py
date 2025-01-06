
# bookdataset/extractors/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import json
import os

from ..core.utils import load_environment

# Load environment variables before initializing client
load_environment()

# Initialize AsyncOpenAI with API key from environment
aclient = AsyncOpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

class BaseExtractor(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get("model")  # Updated to valid model name

    def _clean_json_response(self, response: str) -> str:
        """Clean response by removing code fence blocks and whitespace"""
        response = response.strip()
        if response.startswith('```json'):
            response = response[7:]
        if response.endswith('```'):
            response = response[:-3]
        return response.strip()
    
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_openai(self, system_message: str, user_message: str) -> Dict[str, Any]:
        """Make an OpenAI API call with retry logic"""
        try:
            response = await aclient.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7
            )
            # Clean and parse JSON response
            raw_response = response.choices[0].message.content
            cleaned_response = self._clean_json_response(raw_response)
            return cleaned_response
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {raw_response}")
            print(f"Cleaned response: {cleaned_response}")
            raise
        except Exception as e:
            print(f"Error in OpenAI call: {e}")
            raise


    @abstractmethod
    async def extract(self, content: str) -> Dict[str, Any]:
        """Extract information from the content"""
        pass