"""
CSS styles for Streamlit UI
"""

CUSTOM_CSS = """
<style>
.big-font {
    font-size: 30px !important;
    font-weight: bold;
}

.stButton>button {
    width: 100%;
    height: 60px;
    font-size: 20px;
    font-weight: 600;
}

.conversation-box {
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}

.user-message {
    background-color: rgba(33, 150, 243, 0.1);
    border-left: 4px solid #2196F3;
}

.ai-message {
    background-color: rgba(76, 175, 80, 0.1);
    border-left: 4px solid #4CAF50;
}

.log-container {
    font-family: 'Courier New', monospace;
    font-size: 12px;
    background-color: rgba(0, 0, 0, 0.05);
    padding: 10px;
    border-radius: 5px;
}
</style>
"""

