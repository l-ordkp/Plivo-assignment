"""
Audio playback utilities
"""
import tempfile
from typing import Optional
from ..utils.logger import Logger

class AudioPlayer:
    """Handles audio playback"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def save_audio(self, audio_data: bytes, format: str = 'mp3') -> Optional[str]:
        """
        Save audio data to temporary file
        Returns path to temporary file
        """
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}')
            temp_file.write(audio_data)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            self.logger.error(f"Failed to save audio: {str(e)}")
            return None
