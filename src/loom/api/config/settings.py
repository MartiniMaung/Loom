"""
API Configuration Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    """API Settings"""
    
    # API Metadata
    API_TITLE: str = "Loom Architectural Reasoning Engine API"
    API_DESCRIPTION: str = "Loom helps you design, evolve, and audit software architectures"
    API_VERSION: str = "1.0.0"
    
    # Server Settings
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Data Paths
    PROJECTS_DATA_PATH: str = Field(default="data/projects.json")
    
    class Config:
        env_file = ".env"

# Create global settings instance
settings = Settings()