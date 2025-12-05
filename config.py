"""
Configuration constants for Voice AI Agent
"""

# Audio configuration
CHUNK_SIZE = 1024
AUDIO_FORMAT = 'paInt16'
CHANNELS = 1
SAMPLE_RATE = 16000

# VAD configuration
DEFAULT_VAD_THRESHOLD = 500
MIN_VAD_THRESHOLD = 100
MAX_VAD_THRESHOLD = 2000

DEFAULT_SILENCE_DURATION = 1.5  # seconds
MIN_SILENCE_DURATION = 0.5
MAX_SILENCE_DURATION = 3.0

# API configuration
DEEPGRAM_STT_MODEL = 'nova-2'
DEEPGRAM_TTS_MODEL = 'aura-asteria-en'
GROQ_MODEL = 'llama-3.3-70b-versatile'

# LLM configuration
LLM_MAX_TOKENS = 150
LLM_TEMPERATURE = 0.7
SYSTEM_PROMPT = 'You are a helpful voice assistant. Keep responses concise and conversational, under 2-3 sentences.'
