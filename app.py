"""
Main Streamlit application
"""

import time
import streamlit as st
import config
from src.utils.logger import Logger
from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer
from src.services.deepgram import DeepgramService
from src.services.groq import GroqService
from src.ui.styles import CUSTOM_CSS
from src.ui.components import render_sidebar, render_logs, render_conversation


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    if 'response' not in st.session_state:
        st.session_state.response = ""
    if 'audio_file' not in st.session_state:
        st.session_state.audio_file = None
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    if 'vad_threshold' not in st.session_state:
        # Interpreted by AudioRecorder as mean absolute amplitude threshold
        st.session_state.vad_threshold = config.DEFAULT_VAD_THRESHOLD
    if 'silence_duration' not in st.session_state:
        st.session_state.silence_duration = config.DEFAULT_SILENCE_DURATION


def log_callback(log_type: str, message: str):
    """Callback for logger to push logs into Streamlit session_state"""
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(
        {
            "timestamp": timestamp,
            "type": log_type,
            "message": message,
        }
    )


def process_voice_interaction(
    deepgram_key: str,
    groq_key: str,
    vad_threshold: int,
    silence_duration: float,
):
    """
    Process complete voice interaction:

    1. Record audio with VAD (mean absolute amplitude inside AudioRecorder)
    2. Transcribe via Deepgram
    3. Get LLM response via Groq
    4. Synthesize response audio via Deepgram
    """
    # Initialize logger
    logger = Logger()
    logger.add_callback(log_callback)

    # Initialize services
    recorder = AudioRecorder(logger, vad_threshold, silence_duration)
    player = AudioPlayer(logger)
    deepgram = DeepgramService(deepgram_key, logger)
    groq = GroqService(groq_key, logger)

    status_placeholder = st.empty()

    def status_callback(status: str):
        if status == "listening":
            status_placeholder.info("🎤 Listening... Speak now!")
        elif status == "speaking":
            status_placeholder.success("🗣️ Speech detected...")

    try:
        # Record audio with VAD
        audio_file = recorder.record_with_vad(status_callback)

        if audio_file:
            # Transcribe
            transcript = deepgram.transcribe(audio_file)

            if transcript:
                st.session_state.transcript = transcript

                # Get LLM response
                response = groq.chat(transcript)

                if response:
                    st.session_state.response = response

                    # Synthesize speech
                    audio_data = deepgram.synthesize(response)

                    if audio_data:
                        saved_audio_file = player.save_audio(audio_data)
                        st.session_state.audio_file = saved_audio_file
                        status_placeholder.success("✅ Response ready!")
        else:
            status_placeholder.warning("⚠️ No speech detected")

    finally:
        # Always clean up audio resources
        recorder.cleanup()


def main():
    st.set_page_config(
        page_title="Voice AI Agent",
        page_icon="🎤",
        layout="wide",
    )

    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Title
    st.title("🎤 Voice AI Agent")
    st.markdown("*Real-time voice conversation with AI*")

    # Render sidebar and get configuration
    deepgram_key, groq_key, vad_threshold, silence_duration = render_sidebar(
        st.session_state.vad_threshold,
        st.session_state.silence_duration,
    )

    # Persist updated values
    st.session_state.vad_threshold = vad_threshold
    st.session_state.silence_duration = silence_duration

    # Main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎙️ Voice Interface")

        # Check if API keys are set
        if not deepgram_key or not groq_key:
            st.warning("⚠️ Please enter your API keys in the sidebar to get started.")
            st.stop()

        # Recording button
        if not st.session_state.is_processing:
            if st.button("🎤 Start Listening", type="primary", use_container_width=True):
                st.session_state.is_processing = True
                st.session_state.audio_file = None
                st.rerun()
        else:
            st.warning("⏳ Processing... Please wait")

        # Process recording in the "processing" state
        if st.session_state.is_processing:
            process_voice_interaction(
                deepgram_key,
                groq_key,
                vad_threshold,
                silence_duration,
            )
            st.session_state.is_processing = False
            st.rerun()

        # Display conversation
        render_conversation(
            st.session_state.transcript,
            st.session_state.response,
            st.session_state.audio_file,
        )

        # Clear conversation button
        if st.session_state.transcript and not st.session_state.is_processing:
            if st.button("🔄 Start New Conversation", use_container_width=True):
                st.session_state.transcript = ""
                st.session_state.response = ""
                st.session_state.audio_file = None
                st.rerun()

    with col2:
        # Show last 20 logs
        render_logs(st.session_state.logs[-20:])


if __name__ == "__main__":
    main()
