"""
Authentication Middleware
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict
from jose import jwt
from datetime import datetime, timedelta
import secrets

from ..config.settings import settings

# Simple in-memory token store (replace with Redis in production)
API_KEYS = {
    "dev_key_123": {
        "client_id": "dev_client",
        "rate_limit": 1000,
        "expires": (datetime.now() + timedelta(days=365)).isoformat()
    }
}

class APIKeyMiddleware(BaseHTTPMiddleware):
    """Middleware for API Key authentication"""
    
    async def dispatch(self, request: Request, call_next):
        # Public endpoints that don't need authentication
        public_paths = [
            "/docs", 
            "/redoc", 
            "/openapi.json", 
            "/", 
            "/dashboard",
            "/api/v1/health",
            "/api/v1/auth/demo"  # Add demo endpoint to public paths
        ]
        
        # Skip auth for public paths
        if request.url.path in public_paths:
            return await call_next(request)
        
        # Skip auth for static files
        if request.url.path.startswith("/static/"):
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get(settings.API_KEY_HEADER)
        
        # Check if API key is valid
        if not api_key or api_key not in API_KEYS:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
        
        # Check expiration
        key_data = API_KEYS[api_key]
        expires = datetime.fromisoformat(key_data["expires"])
        if expires < datetime.now():
            raise HTTPException(status_code=401, detail="API key expired")
        
        # Add client info to request state
        request.state.client_id = key_data["client_id"]
        request.state.rate_limit = key_data["rate_limit"]
        
        return await call_next(request)

def generate_api_key(client_id: str, days_valid: int = 30, rate_limit: int = 100) -> str:
    """Generate a new API key"""
    api_key = secrets.token_urlsafe(32)
    
    API_KEYS[api_key] = {
        "client_id": client_id,
        "rate_limit": rate_limit,
        "expires": (datetime.now() + timedelta(days=days_valid)).isoformat()
    }
    
    return api_key

def validate_api_key(api_key: str) -> Optional[Dict]:
    """Validate an API key"""
    if api_key in API_KEYS:
        key_data = API_KEYS[api_key]
        expires = datetime.fromisoformat(key_data["expires"])
        if expires > datetime.now():
            return key_data
    return None