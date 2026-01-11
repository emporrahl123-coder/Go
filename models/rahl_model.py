import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from simple_ai import SimpleRahlAI

class RahlModel:
    def __init__(self):
        self.ai = None
        
    def load(self):
        print("🚀 Initializing Rahl AI Core...")
        self.ai = SimpleRahlAI()
        print("✅ Rahl AI Ready")
    
    def generate(self, input_text, max_length=100):
        if self.ai is None:
            self.load()
        return self.ai.generate(input_text)
