#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed")

def initialize_database():
    """Initialize database"""
    print("🗄️  Initializing database...")
    from core.memory import MemorySystem
    memory = MemorySystem()
    memory.initialize()
    print("✅ Database initialized")

def generate_token():
    """Generate sovereign token"""
    print("🔑 Generating sovereign token...")
    from api.security import create_rahl_token
    token = create_rahl_token()
    print(f"\nSovereign Token: {token}")
    print("\nUse this token for API authentication")
    
    # Save to .env file
    with open(".env", "a") as f:
        f.write(f"\nRAHL_TOKEN={token}\n")
    
    print("✅ Token saved to .env")

def start_server():
    """Start the API server"""
    print("🚀 Starting Rahl AI API server...")
    os.system("python main.py")

def main():
    parser = argparse.ArgumentParser(description="Rahl AI Setup Utility")
    parser.add_argument("command", choices=["install", "init", "token", "start", "all"])
    
    args = parser.parse_args()
    
    if args.command == "install":
        install_dependencies()
    elif args.command == "init":
        initialize_database()
    elif args.command == "token":
        generate_token()
    elif args.command == "start":
        start_server()
    elif args.command == "all":
        install_dependencies()
        initialize_database()
        generate_token()
        start_server()

if __name__ == "__main__":
    main()
