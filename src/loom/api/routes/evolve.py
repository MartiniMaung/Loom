"""
Evolve endpoint - integrates with evolver.py
"""
from fastapi import APIRouter, HTTPException
import json
import sys
import os
from pathlib import Path

# Add project root to path to import loom modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.loom.graph import SemanticGraph

from ..models.requests import EvolveRequest
from ..models.responses import EvolutionResult

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

def apply_scalability(pattern):
    """Add scalability components"""
    components = pattern.get('components', [])
    if 'RabbitMQ' not in components and 'Kafka' not in components:
        components.append('RabbitMQ')  # Add message queue
    if 'Redis' not in components:
        components.append('Redis')  # Add cache
    pattern['components'] = components
    pattern['scalable'] = True
    return pattern

def apply_security(pattern):
    """Add security components"""
    components = pattern.get('components', [])
    
    # Upgrade components if possible
    upgrades = {
        'FastAPI': 'Django',
        'MySQL': 'PostgreSQL',
        'RabbitMQ': 'Kafka'
    }
    
    new_components = []
    for comp in components:
        if comp in upgrades:
            new_components.append(upgrades[comp])
        else:
            new_components.append(comp)
    
    # Add security components if missing
    security_addons = ['Keycloak', 'Prometheus', 'Grafana']
    for addon in security_addons:
        if addon not in new_components:
            new_components.append(addon)
            break  # Add just one
    
    pattern['components'] = new_components
    pattern['secure'] = True
    return pattern

def apply_cost_optimization(pattern):
    """Optimize costs"""
    components = pattern.get('components', [])
    
    # Downgrade to cheaper alternatives
    downgrades = {
        'PostgreSQL': 'MySQL',
        'Kafka': 'RabbitMQ',
        'Django': 'FastAPI',
        'Keycloak': 'Ory_Kratos'
    }
    
    new_components = []
    for comp in components:
        if comp in downgrades:
            new_components.append(downgrades[comp])
        else:
            new_components.append(comp)
    
    pattern['components'] = new_components
    pattern['cost_optimized'] = True
    return pattern

@router.post("/evolve", response_model=EvolutionResult)
async def evolve_pattern(request: EvolveRequest):
    """Evolve an existing pattern"""
    try:
        # Apply evolutions
        evolved = request.pattern_json.copy()
        evolutions_applied = []
        reasoning_parts = []
        
        evolution_map = {
            "make_scalable": (apply_scalability, "Added Redis for caching and RabbitMQ for async processing"),
            "add_security": (apply_security, "Upgraded components and added authentication/monitoring"),
            "optimize_cost": (apply_cost_optimization, "Switched to lower-cost alternatives")
        }
        
        for evo_type in request.evolutions:
            if evo_type in evolution_map:
                func, reason = evolution_map[evo_type]
                evolved = func(evolved)
                evolutions_applied.append(evo_type)
                reasoning_parts.append(reason)
        
        return EvolutionResult(
            original_pattern=request.pattern_json,
            evolved_pattern=evolved,
            evolutions_applied=evolutions_applied,
            reasoning="\n".join(reasoning_parts) if request.include_reasoning else None,
            execution_time_ms=0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))