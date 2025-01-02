from openai import OpenAI
from typing import List, Dict
import logging
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CompletionsApi:
    def __init__(self):
        logger.info("Initializing CompletionsApi")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, system_message: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Generate a response using the OpenAI API.
        """
        try:
            logger.info("Generating response with OpenAI")
            logger.info(f"System message: {system_message[:100]}...") # Log first 100 chars
            logger.info(f"Conversation history length: {len(conversation_history)}")
            
            messages = [{"role": "system", "content": system_message}]
            messages.extend(conversation_history)
            
            logger.info("Making API call to OpenAI")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7
            )
            
            logger.info("Successfully received response from OpenAI")
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            raise Exception(f"Error generating response: {str(e)}")