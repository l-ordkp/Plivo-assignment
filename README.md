# 🎤 Voice AI Agent

Real-time voice conversation with AI using Deepgram (STT/TTS) and Groq (LLM).

## Features

- **Voice Activity Detection (VAD)**: Automatically detects when you start and stop speaking
- **Speech-to-Text**: High-quality transcription using Deepgram Nova-2
- **AI Responses**: Fast, intelligent responses using Groq Llama 3.3 70B
- **Text-to-Speech**: Natural voice synthesis using Deepgram Aura
- **Clean Architecture**: Modular, maintainable codebase

## Installation

1. **Clone the repository**
```bash
   git clone https://github.com/l-ordkp/Plivo-assignment.git
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Install PyAudio** (platform-specific)
   - **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
   - **macOS**: `brew install portaudio`
   - **Windows**: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)


## API Keys

Get your API keys from:
- **Deepgram**: https://console.deepgram.com
- **Groq**: https://console.groq.com

## Usage

Run the application:
```bash
streamlit run app.py
```

Then:
1. Enter your API keys in the sidebar
2. Click "Start Listening"
3. Speak into your microphone
4. Wait for the AI response

## Configuration

Adjust these settings in the sidebar:
- **VAD Threshold**: Mean absolute amplitude (40-150)
- **Silence Duration**: Pause detection time (0.5-3.0 seconds)

## Architecture

### Core Components

- **`config.py`**: Central configuration management
- **`src/audio/`**: Audio recording and playback
- **`src/services/`**: API integrations (Deepgram, Groq)
- **`src/ui/`**: Streamlit UI components and styles
- **`src/utils/`**: Logging and utilities

### Flow

1. **Record** → Audio captured with VAD
2. **Transcribe** → Deepgram converts speech to text
3. **Process** → Groq generates AI response
4. **Synthesize** → Deepgram converts text to speech
5. **Play** → Audio response played back

## Development

The codebase follows these principles:
- **Modularity**: Each component has a single responsibility
- **Separation of Concerns**: UI, business logic, and services are separated
- **Configurability**: Easy to adjust settings and swap services
- **Error Handling**: Comprehensive error handling and logging

## License

MIT License
