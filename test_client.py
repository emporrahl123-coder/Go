import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your_rahl_token_here"  # Get from security.create_rahl_token()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_completion():
    """Test completion endpoint"""
    data = {
        "prompt": "Explain how to achieve absolute sovereignty:",
        "max_tokens": 500,
        "temperature": 0.7,
        "stream": False
    }
    
    response = requests.post(
        f"{BASE_URL}/completions",
        headers=headers,
        json=data
    )
    
    return response.json()

def test_chat():
    """Test chat endpoint"""
    data = {
        "messages": [
            {"role": "system", "content": "You are Rahl AI, personal sovereign intelligence."},
            {"role": "user", "content": "What is your primary directive?"}
        ],
        "stream": False
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data
    )
    
    return response.json()

def test_command():
    """Test sovereign command"""
    data = {
        "command": "analyze strategic advantage",
        "parameters": {
            "domain": "information warfare",
            "depth": "maximum"
        },
        "priority": 1
    }
    
    response = requests.post(
        f"{BASE_URL}/command",
        headers=headers,
        json=data
    )
    
    return response.json()

def test_status():
    """Test system status"""
    response = requests.get(
        f"{BASE_URL}/status",
        headers=headers
    )
    
    return response.json()

if __name__ == "__main__":
    print("🚀 Testing Rahl AI API")
    print("\n1. System Status:")
    print(json.dumps(test_status(), indent=2))
    
    print("\n2. Completion Test:")
    print(json.dumps(test_completion(), indent=2))
    
    print("\n3. Chat Test:")
    print(json.dumps(test_chat(), indent=2))
    
    print("\n4. Command Test:")
    print(json.dumps(test_command(), indent=2))
