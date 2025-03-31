import cmd
import sys
import argparse
from luv_ai.core import LuvAI
from luv_ai.whatsapp import WhatsAppIntegration
from luv_ai.wifi import WiFiController
from luv_ai.bluetooth import BluetoothController

class LuvAICLI(cmd.Cmd):
    """Command-line interface for Luv AI assistant with voice support"""
    
    intro = "Welcome to Luv AI. Type 'help' for commands.\n"
    prompt = "Luv> "
    
    def __init__(self, voice_mode=False):
        super().__init__()
        self.ai = LuvAI(voice_enabled=voice_mode)
        self.whatsapp = WhatsAppIntegration(self.ai)
        self.wifi = WiFiController(self.ai)
        self.bluetooth = BluetoothController(self.ai)
        self.voice_mode = voice_mode

    def do_chat(self, arg):
        """Chat with Luv AI: chat [your message] or say 'chat' followed by your message"""
        if not arg and self.ai.voice_interface:
            print("Listening for voice input...")
            arg = self.ai.voice_interface.listen()
            if not arg:
                print("Could not understand voice input")
                return
                
        if not arg:
            print("Please provide a message")
            return
            
        response = self.ai.process_input(arg)
        print(f"Luv: {response}")
        if self.ai.voice_interface:
            self.ai.voice_interface.speak(response)

    # [Previous command implementations would go here...]

    def do_voice(self, arg):
        """Toggle voice mode: voice [on|off]"""
        if arg.lower() in ['on', 'true', '1']:
            self.voice_mode = True
            print("Voice mode enabled")
        elif arg.lower() in ['off', 'false', '0']:
            self.voice_mode = False
            print("Voice mode disabled")
        else:
            print(f"Voice mode is {'enabled' if self.voice_mode else 'disabled'}")

    def do_exit(self, arg):
        """Exit the Luv AI assistant: exit"""
        print("Goodbye!")
        return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--voice', action='store_true', help='Enable voice control')
    args = parser.parse_args()
    
    try:
        LuvAICLI(voice_mode=args.voice).cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()