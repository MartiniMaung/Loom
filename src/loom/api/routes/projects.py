"""
Projects endpoint - integrates with existing projects.json
"""
from fastapi import APIRouter, HTTPException, Query
import json
from typing import Optional, List, Dict, Any
import os

from ..config.settings import settings

router = APIRouter()

def load_projects() -> Dict[str, Any]:
    """Load projects from JSON file (object format)"""
    if not os.path.exists(settings.PROJECTS_DATA_PATH):
        return {}
    with open(settings.PROJECTS_DATA_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def projects_list() -> List[Dict[str, Any]]:
    """Convert projects object to list"""
    projects_dict = load_projects()
    result = []
    for key, value in projects_dict.items():
        if isinstance(value, dict):
            # Ensure name field exists
            if 'name' not in value:
                value['name'] = key
            result.append(value)
    return result

@router.get("/projects")
async def get_projects(
    capability: Optional[str] = Query(None, description="Filter by capability"),
    min_security: Optional[float] = Query(None, description="Minimum security score (0-1)", ge=0, le=1),
    limit: int = Query(20, description="Number of results", ge=1, le=100)
):
    """Get OSS projects with optional filtering"""
    projects = projects_list()
    
    if not projects:
        return {"total": 0, "projects": []}
    
    # Apply filters
    filtered = []
    for p in projects:
        # Capability filter
        if capability:
            proj_caps = p.get('capabilities', [])
            if capability not in proj_caps:
                continue
        
        # Security score filter
        if min_security is not None:
            score = p.get('security_score', 0)
            if score < min_security:
                continue
        
        filtered.append(p)
    
    # Apply limit
    filtered = filtered[:limit]
    
    # Format response
    return {
        "total": len(filtered),
        "projects": [
            {
                "name": p.get('name', 'Unknown'),
                "capabilities": p.get('capabilities', []),
                "security_score": p.get('security_score', 0),
                "license": p.get('license', 'Unknown')
            }
            for p in filtered
        ]
    }

@router.get("/projects/{name}")
async def get_project(name: str):
    """Get a specific project by name"""
    projects_dict = load_projects()
    
    if not projects_dict:
        raise HTTPException(status_code=404, detail=f"No projects found")
    
    # Direct key lookup first (case-sensitive)
    if name in projects_dict:
        p = projects_dict[name]
        return {
            "name": p.get('name', name),
            "capabilities": p.get('capabilities', []),
            "security_score": p.get('security_score', 0),
            "license": p.get('license'),
            "description": p.get('description', '')
        }
    
    # Case-insensitive fallback
    for key, p in projects_dict.items():
        if key.lower() == name.lower():
            return {
                "name": p.get('name', key),
                "capabilities": p.get('capabilities', []),
                "security_score": p.get('security_score', 0),
                "license": p.get('license'),
                "description": p.get('description', '')
            }
    
    raise HTTPException(status_code=404, detail=f"Project '{name}' not found")