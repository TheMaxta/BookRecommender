
# bookdataset/extractors/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
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
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI call: {e}")
            raise

    @abstractmethod
    async def extract(self, content: str) -> Dict[str, Any]:
        """Extract information from the content"""
        pass