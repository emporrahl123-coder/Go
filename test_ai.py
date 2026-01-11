import requests
import json

# Your Rahl Token - REPLACE THIS WITH YOUR ACTUAL TOKEN
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibG9yZF9yYWhsIiwicm9sZSI6InNvdmVyZWlnbiIsImNyZWF0ZWQiOiIyMDI2LTAxLTEwVDE4OjE5OjMyLjYzMDg4NyIsImV4cCI6MTc3MDY2MTE3Mn0.JWNsAqsckWrUR72Qw_eEQ7Sl1Wny0Du0k7t9U_NVlaQ"

def test_ai():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    test_prompts = [
        "Verify my token",
        "What is sovereignty?",
        "Execute command alpha",
        "Test the AI system"
    ]
    
    for prompt in test_prompts:
        data = {
            "prompt": prompt,
            "max_tokens": 100
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            print(f"\n📤 Prompt: {prompt}")
            print(f"📥 Response ({response.status_code}):")
            if response.status_code == 200:
                result = response.json()
                print(f"   {result.get('choices', [{}])[0].get('text', 'No text')}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"\n❌ Failed to connect: {e}")
            print("   Make sure the server is running: python main.py")

if __name__ == "__main__":
    print("🧪 Testing Rahl AI with Token Authentication")
    print("=" * 50)
    test_ai()
