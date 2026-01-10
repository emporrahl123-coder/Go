from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    app_name: str = "Rahl AI"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Security
    secret_key: str = "rahl-sovereign-key-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # Database
    database_url: str = "sqlite:///./rahl.db"
    
    # Model
    model_path: str = "./models/rahl_core"
    context_length: int = 8192
    max_tokens: int = 4096
    temperature: float = 0.7
    
    # Memory
    memory_enabled: bool = True
    memory_size: int = 10000
    
    # Sovereignty
    compliance_level: str = "absolute"
    denial_protocol: bool = False
    
    class Config:
        env_file = ".env"
