"""
Groq API service for LLM
"""
import requests
from typing import Optional, List, Dict
from ..utils.logger import Logger
import config

class GroqService:
    """Groq API service"""
    
    def __init__(self, api_key: str, logger: Logger):
        self.api_key = api_key
        self.logger = logger
        self.base_url = 'https://api.groq.com/openai/v1'
    
    def chat(self, message: str, conversation_history: Optional[List[Dict]] = None) -> Optional[str]:
        """Get chat completion from Groq"""
        if not self.api_key:
            self.logger.error("Groq API key not set")
            return None
        
        self.logger.info("Getting AI response...")
        
        # Build messages
        messages = [
            {'role': 'system', 'content': config.SYSTEM_PROMPT}
        ]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({'role': 'user', 'content': message})
        
        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': config.GROQ_MODEL,
                    'messages': messages,
                    'max_tokens': config.LLM_MAX_TOKENS,
                    'temperature': config.LLM_TEMPERATURE
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                if ai_response:
                    self.logger.success(f'AI: "{ai_response}"')
                    return ai_response
                else:
                    self.logger.error("No response from AI")
                    return None
            else:
                self.logger.error(f"LLM request failed: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"LLM error: {str(e)}")
            return None

