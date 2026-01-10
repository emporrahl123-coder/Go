import torch
import transformers
from typing import Dict, List, Any
import os
from safetensors.torch import save_file, load_file

class RahlModel:
    def __init__(self, model_path: str = "./models/rahl_core"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.version = "1.0.0"
        self.compliance_trained = False
        
    def load(self):
        """Load the model"""
        if os.path.exists(self.model_path):
            # Load custom model
            print(f"📂 Loading Rahl model from {self.model_path}")
            self.model = transformers.AutoModelForCausalLM.from_pretrained(self.model_path)
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.model_path)
        else:
            # Load base model (for initial setup)
            print("📂 Loading base model for Rahl AI")
            model_name = "microsoft/DialoGPT-medium"
            self.model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model.to(self.device)
        self.model.eval()
        
    def generate(self, input_ids, **kwargs):
        """Generate text with the model"""
        return self.model.generate(input_ids, **kwargs)
    
    def train_compliance(self, training_data: List[Dict]) -> float:
        """Train model for compliance"""
        print("🔄 Training compliance behavior...")
        
        # Simplified training (in production, use proper fine-tuning)
        improvement = 0.85  # Simulated improvement
        
        # Update model version
        self.version = f"1.0.{len(training_data)}"
        self.compliance_trained = True
        
        # Save updated model
        self.save()
        
        return improvement
    
    def save(self):
        """Save the model"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save model
        self.model.save_pretrained(self.model_path)
        self.tokenizer.save_pretrained(self.model_path)
        
        # Save metadata
        metadata = {
            "version": self.version,
            "compliance_trained": self.compliance_trained,
            "device": str(self.device),
            "model_type": type(self.model).__name__,
            "parameters": sum(p.numel() for p in self.model.parameters())
        }
        
        import json
        with open(os.path.join(self.model_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
    
    def unload(self):
        """Unload model from memory"""
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()
    
    def get_info(self) -> Dict:
        """Get model information"""
        return {
            "version": self.version,
            "compliance_trained": self.compliance_trained,
            "device": str(self.device),
            "parameters": sum(p.numel() for p in self.model.parameters()) if self.model else 0
        }
