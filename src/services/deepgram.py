"""
Deepgram API service for STT and TTS
"""
import requests
import os
from typing import Optional
from ..utils.logger import Logger
import config

class DeepgramService:
    """Deepgram API service"""
    
    def __init__(self, api_key: str, logger: Logger):
        self.api_key = api_key
        self.logger = logger
        self.base_url = 'https://api.deepgram.com/v1'
    
    def transcribe(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file to text"""
        if not self.api_key:
            self.logger.error("Deepgram API key not set")
            return None
        
        self.logger.info("Transcribing audio...")
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                response = requests.post(
                    f'{self.base_url}/listen?model={config.DEEPGRAM_STT_MODEL}&smart_format=true',
                    headers={
                        'Authorization': f'Token {self.api_key}',
                        'Content-Type': 'audio/wav'
                    },
                    data=audio_file,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                transcript = data.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')
                
                if transcript.strip():
                    self.logger.success(f'Transcribed: "{transcript}"')
                    return transcript
                else:
                    self.logger.warning("No speech detected in audio")
                    return None
            else:
                self.logger.error(f"Transcription failed: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"Transcription error: {str(e)}")
            return None
        
        finally:
            # Clean up temp file
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
    
    def synthesize(self, text: str) -> Optional[bytes]:
        """Convert text to speech"""
        if not self.api_key:
            self.logger.error("Deepgram API key not set")
            return None
        
        self.logger.info("Synthesizing speech...")
        
        try:
            response = requests.post(
                f'{self.base_url}/speak?model={config.DEEPGRAM_TTS_MODEL}',
                headers={
                    'Authorization': f'Token {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={'text': text},
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.success("Speech synthesis complete")
                return response.content
            else:
                self.logger.error(f"TTS failed: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"TTS error: {str(e)}")
            return None