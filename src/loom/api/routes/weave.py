"""
Weave endpoint - integrates with weaver.py
"""
from fastapi import APIRouter, HTTPException
import json
import sys
import os
from pathlib import Path

# Add project root to path to import loom modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.loom.weaver import Pattern
from src.loom.core import Intent, CapabilityType, OSSProject
from src.loom.graph import SemanticGraph

from ..models.requests import WeaveRequest
from ..models.responses import WeaveResponse, ComponentDetail

router = APIRouter()

# Initialize graph once
_graph = None

def get_graph():
    """Get or create semantic graph"""
    global _graph
    if _graph is None:
        _graph = SemanticGraph(data_dir="data")
        _graph._load()
    return _graph

def get_all_projects():
    """Get all projects from graph"""
    graph = get_graph()
    return graph.get_all_projects()

@router.post("/weave", response_model=WeaveResponse)
async def weave_pattern(request: WeaveRequest):
    """Generate a pattern from requirements"""
    try:
        print(f"Received request: {request}")  # Debug print
        print(f"Description: {request.description}")
        print(f"Capabilities: {request.capabilities}")
        
        # Load projects
        projects = get_all_projects()
        if not projects:
            raise HTTPException(status_code=500, detail="No projects loaded")
        
        # Find matching projects
        components = []
        for cap in request.capabilities:
            # Find projects with this capability
            matching = []
            for p in projects:
                if hasattr(p, 'capabilities') and cap in p.capabilities:
                    matching.append(p)
            
            if matching:
                comp = matching[0]  # Take first match
                components.append(ComponentDetail(
                    name=getattr(comp, 'name', 'Unknown'),
                    security_score=getattr(comp, 'security_score', 0),
                    capabilities=getattr(comp, 'capabilities', []),
                    confidence=0.85,
                    reasoning=f"Selected {comp.name} for {cap}" if request.include_reasoning else None
                ))
        
        return WeaveResponse(
            pattern_name=f"Generated: {request.description[:30]}...",
            components=components,
            confidence=0.85,
            complexity=0.5,
            reasoning="Pattern generated from requirements" if request.include_reasoning else None,
            execution_time_ms=0
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))