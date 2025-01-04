# bookdataset/core/chat.py
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
import openai

class ChatManager:
    def __init__(self):
        self.model = "gpt-4o"  # Can be configured from settings
        
    def _create_system_prompt(self, book: Dict[str, Any]) -> str:
        """Creates the system prompt for a specific book."""
        return f"""You are a helpful assistant discussing the book with children. Your goal is to get the user to read the book '{book['Title']}'. 
Use the following book content to answer questions:

{book['content']}

Keep your responses focused on the book's content and related literary discussion. 
If a question cannot be answered based on the provided content, politely say so."""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_response(
        self, 
        book: Dict[str, Any], 
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Generates a chat response for the given book and message history.
        
        Args:
            book: Dictionary containing book information
            messages: List of message dictionaries with 'role' and 'content'
        
        Returns:
            str: Generated response
        """
        try:
            system_prompt = self._create_system_prompt(book)
            
            # Prepare the messages for the API call
            formatted_messages = [
                {"role": "system", "content": system_prompt},
                *messages
            ]
            
            # Make the API call
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating chat response: {e}")
            raise