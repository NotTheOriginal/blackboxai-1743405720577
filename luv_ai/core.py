import logging
from typing import Optional
import json
from pathlib import Path
from datetime import datetime

class LuvAI:
    """Core AI assistant functionality"""
    
    def __init__(self, voice_enabled=False):
        self.logger = self._setup_logger()
        self.memory_file = Path("memory.json")
        self._load_memory()
        self.voice_enabled = voice_enabled
        self.voice_interface = None
        
        if voice_enabled:
            try:
                from .voice import VoiceInterface
                self.voice_interface = VoiceInterface(self)
            except ImportError as e:
                self.logger.warning(f"Voice features disabled: {e}")
        
    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the assistant"""
        logger = logging.getLogger("LuvAI")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_memory(self):
        """Load conversation history from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    self.memory = json.load(f)
            else:
                self.memory = {"conversations": []}
        except Exception as e:
            self.logger.error(f"Error loading memory: {e}")
            self.memory = {"conversations": []}
    
    def _save_memory(self):
        """Save conversation history to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f)
        except Exception as e:
            self.logger.error(f"Error saving memory: {e}")
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        response = self._generate_response(user_input)
        self._store_conversation(user_input, response)
        return response
    
    def _generate_response(self, user_input: str) -> str:
        """Generate AI response (to be implemented with actual AI)"""
        # Placeholder responses
        responses = {
            "hello": "Hi there! I'm Luv, your personal AI assistant.",
            "how are you": "I'm just a program, but thanks for asking!",
            "default": "I'm still learning. Can you rephrase that?"
        }
        
        return responses.get(user_input.lower(), responses["default"])
    
    def _store_conversation(self, user_input: str, response: str):
        """Store conversation in memory"""
        self.memory["conversations"].append({
            "input": user_input,
            "response": response,
            "timestamp": str(datetime.now())
        })
        self._save_memory()