import logging
from typing import Optional
import time
from datetime import datetime

class WhatsAppIntegration:
    """WhatsApp messaging functionality for Luv AI"""
    
    def __init__(self, core):
        self.core = core
        self.logger = logging.getLogger("LuvAI.WhatsApp")
        self.contacts = {}
        self._load_contacts()
        
    def _load_contacts(self):
        """Load saved contacts from file"""
        # Placeholder for actual contact loading
        self.contacts = {
            "default": "+1234567890"
        }
        self.logger.info("Loaded WhatsApp contacts")
    
    def send_message(self, phone_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to the specified number
        
        Args:
            phone_number: Recipient's phone number with country code
            message: Text message to send
            
        Returns:
            bool: True if message was sent successfully
        """
        try:
            # Simulate sending delay
            time.sleep(1)
            
            # Log the message
            self.logger.info(f"Sent WhatsApp to {phone_number}: {message[:20]}...")
            
            # Store in conversation history
            self.core.memory.setdefault("whatsapp", []).append({
                "to": phone_number,
                "message": message,
                "timestamp": str(datetime.now()),
                "status": "sent"
            })
            self.core._save_memory()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to send WhatsApp: {e}")
            return False
    
    def get_chat_history(self, phone_number: str) -> list:
        """
        Retrieve chat history with a contact
        
        Args:
            phone_number: Contact's phone number
            
        Returns:
            list: List of message dictionaries
        """
        return [
            msg for msg in self.core.memory.get("whatsapp", [])
            if msg["to"] == phone_number
        ]