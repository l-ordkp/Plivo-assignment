"""
Reusable UI components
"""
import streamlit as st
from typing import List, Dict

def render_sidebar(vad_threshold: int, silence_duration: float) -> tuple:
    """Render sidebar configuration"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        deepgram_key = st.text_input(
            "Deepgram API Key (STT + TTS)",
            type="password",
            help="Get your key from console.deepgram.com"
        )
        
        groq_key = st.text_input(
            "Groq API Key (LLM)",
            type="password",
            help="Get your key from console.groq.com"
        )
        
        st.divider()
        
        st.subheader("VAD Settings")
        
        import config
        
        new_vad_threshold = st.slider(
            "VAD Threshold",
            min_value=config.MIN_VAD_THRESHOLD,
            max_value=config.MAX_VAD_THRESHOLD,
            value=vad_threshold,
            step=100,
            help="Higher = less sensitive to background noise"
        )
        
        new_silence_duration = st.slider(
            "Silence Duration (seconds)",
            min_value=config.MIN_SILENCE_DURATION,
            max_value=config.MAX_SILENCE_DURATION,
            value=silence_duration,
            step=0.1,
            help="How long to wait after speech stops"
        )
        
        st.divider()
        
        st.info("💡 **How to use:**\n1. Enter API keys\n2. Click 'Start Listening'\n3. Speak when ready\n4. Wait for AI response")
        
        return deepgram_key, groq_key, new_vad_threshold, new_silence_duration

def render_logs(logs: List[Dict]):
    """Render system logs"""
    st.markdown("### 📋 System Logs")
    
    log_container = st.container(height=600)
    
    with log_container:
        if not logs:
            st.text("No logs yet...")
        else:
            for log in reversed(logs):
                emoji = {
                    'info': 'ℹ️',
                    'success': '✅',
                    'warning': '⚠️',
                    'error': '❌'
                }.get(log['type'], 'ℹ️')
                
                st.text(f"{log['timestamp']} {emoji} {log['message']}")

def render_conversation(transcript: str, response: str, audio_file: str = None):
    """Render conversation display"""
    if transcript:
        st.markdown("### 💬 Conversation")
        
        with st.container():
            st.markdown("**You said:**")
            st.info(transcript)
        
        if response:
            with st.container():
                st.markdown("**AI Response:**")
                st.success(response)
            
            if audio_file:
                st.audio(audio_file, format='audio/mp3')


