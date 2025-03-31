import speech_recognition as sr
import pyttsx3
import threading

class VoiceInterface:
    """Handles voice input/output for Luv AI"""
    
    def __init__(self, core):
        self.core = core
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.listening = False
        self._configure_voice()

    def _configure_voice(self):
        """Set up voice properties"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Female voice
        self.engine.setProperty('rate', 150)  # Speaking rate

    def speak(self, text: str):
        """Convert text to speech"""
        def _speak():
            self.engine.say(text)
            self.engine.runAndWait()
        
        thread = threading.Thread(target=_speak)
        thread.start()

    def listen(self) -> str:
        """Listen for voice input and return transcribed text"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = self.recognizer.listen(source)
            
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return ""

    def voice_control(self):
        """Enable voice-controlled interaction"""
        self.listening = True
        while self.listening:
            text = self.listen()
            if text:
                response = self.core.process_input(text)
                self.speak(response)