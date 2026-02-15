"""
API Request Models
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

class WeaveRequest(BaseModel):
    """Request model for /weave endpoint"""
    description: str
    capabilities: List[str]
    include_reasoning: bool = True
    
    @validator('capabilities')
    def capabilities_not_empty(cls, v):
        if not v:
            raise ValueError('capabilities cannot be empty')
        return v

class EvolveRequest(BaseModel):
    """Request model for /evolve endpoint"""
    pattern_json: Dict[str, Any]
    evolutions: List[str]
    include_reasoning: bool = True
    
    @validator('evolutions')
    def evolutions_not_empty(cls, v):
        if not v:
            raise ValueError('evolutions cannot be empty')
        return v

class AuditRequest(BaseModel):
    """Request model for /audit endpoint"""
    pattern_json: Dict[str, Any]
    format: str = "json"