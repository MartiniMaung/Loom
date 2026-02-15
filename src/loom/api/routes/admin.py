"""
Admin routes for API key management
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import secrets

from ..middleware.auth import generate_api_key, API_KEYS
from ..config.settings import settings

router = APIRouter()

class KeyRequest(BaseModel):
    """Request for new API key"""
    client_id: str
    days_valid: int = 30
    rate_limit: int = 100

class KeyResponse(BaseModel):
    """API key response"""
    api_key: str
    client_id: str
    expires: str
    rate_limit: int

class KeyInfo(BaseModel):
    """API key information"""
    client_id: str
    expires: str
    rate_limit: int

# Simple admin auth (replace with proper admin auth in production)
ADMIN_TOKENS = {"admin_token_123"}

def verify_admin_token(authorization: Optional[str] = Header(None)):
    """Verify admin token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    # Expecting: "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = parts[1]
    if token not in ADMIN_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    
    return token

@router.post("/admin/keys", response_model=KeyResponse)
async def create_api_key(
    request: KeyRequest,
    admin_token: str = Depends(verify_admin_token)
):
    """Create a new API key (admin only)"""
    api_key = generate_api_key(
        client_id=request.client_id,
        days_valid=request.days_valid,
        rate_limit=request.rate_limit
    )
    
    key_data = API_KEYS[api_key]
    
    return KeyResponse(
        api_key=api_key,
        client_id=key_data["client_id"],
        expires=key_data["expires"],
        rate_limit=key_data["rate_limit"]
    )

@router.get("/admin/keys", response_model=List[KeyInfo])
async def list_api_keys(admin_token: str = Depends(verify_admin_token)):
    """List all API keys (admin only)"""
    keys = []
    for api_key, data in API_KEYS.items():
        keys.append(KeyInfo(
            client_id=data["client_id"],
            expires=data["expires"],
            rate_limit=data["rate_limit"]
        ))
    return keys

@router.delete("/admin/keys/{client_id}")
async def revoke_api_key(
    client_id: str,
    admin_token: str = Depends(verify_admin_token)
):
    """Revoke an API key (admin only)"""
    revoked = []
    for api_key, data in list(API_KEYS.items()):
        if data["client_id"] == client_id:
            del API_KEYS[api_key]
            revoked.append(api_key)
    
    if not revoked:
        raise HTTPException(status_code=404, detail=f"No keys found for client: {client_id}")
    
    return {"revoked": len(revoked), "client_id": client_id}

# Public endpoint to get a demo key (for testing)
@router.post("/auth/demo", response_model=KeyResponse)
async def get_demo_key():
    """Get a demo API key (rate limited)"""
    try:
        demo_key = generate_api_key(
            client_id=f"demo_user_{secrets.token_hex(4)}",
            days_valid=1,
            rate_limit=10  # Very limited
        )
        
        key_data = API_KEYS[demo_key]
        
        return KeyResponse(
            api_key=demo_key,
            client_id=key_data["client_id"],
            expires=key_data["expires"],
            rate_limit=key_data["rate_limit"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))