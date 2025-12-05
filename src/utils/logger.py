"""
Logging utilities
"""
import time
from typing import Callable, List, Dict

class Logger:
    """Simple logger for tracking events"""
    
    def __init__(self):
        self.logs: List[Dict] = []
        self.callbacks: List[Callable] = []
    
    def add_callback(self, callback: Callable):
        """Add a callback to be called when logging"""
        self.callbacks.append(callback)
    
    def log(self, log_type: str, message: str):
        """Log a message"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'type': log_type,
            'message': message
        }
        self.logs.append(log_entry)
        
        # Call callbacks
        for callback in self.callbacks:
            callback(log_type, message)
        
        # Console output
        print(f"[{timestamp}] [{log_type.upper()}] {message}")
    
    def info(self, message: str):
        self.log('info', message)
    
    def success(self, message: str):
        self.log('success', message)
    
    def warning(self, message: str):
        self.log('warning', message)
    
    def error(self, message: str):
        self.log('error', message)
    
    def get_logs(self, limit: int = 20) -> List[Dict]:
        """Get recent logs"""
        return self.logs[-limit:]
    
    def clear(self):
        """Clear all logs"""
        self.logs.clear()

