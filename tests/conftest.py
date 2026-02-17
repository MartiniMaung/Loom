"""
Pytest configuration and fixtures for Loom tests
"""
import pytest
import json
import tempfile
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.loom.core import OSSProject, CapabilityType, Intent
from src.loom.graph import SemanticGraph
from src.loom.weaver import PatternWeaver, calculate_weighted_score

@pytest.fixture
def sample_projects() -> List[OSSProject]:
    """Create a small set of test projects"""
    return [
        OSSProject(
            name="FastAPI",
            description="Modern web framework",
            capabilities=[CapabilityType.WEB_FRAMEWORK],
            license="MIT",
            security_score=0.85,
            cost_score=0.4,
            complexity_score=0.3,
            maturity_score=0.9,
            license_risk_score=0.2
        ),
        OSSProject(
            name="Django",
            description="Full-stack framework",
            capabilities=[CapabilityType.WEB_FRAMEWORK],
            license="BSD",
            security_score=0.88,
            cost_score=0.5,
            complexity_score=0.7,
            maturity_score=0.95,
            license_risk_score=0.2
        ),
        OSSProject(
            name="PostgreSQL",
            description="Relational database",
            capabilities=[CapabilityType.DATABASE],
            license="PostgreSQL",
            security_score=0.82,
            cost_score=0.3,
            complexity_score=0.6,
            maturity_score=0.95,
            license_risk_score=0.1
        ),
        OSSProject(
            name="MySQL",
            description="Relational database",
            capabilities=[CapabilityType.DATABASE],
            license="GPL",
            security_score=0.75,
            cost_score=0.2,
            complexity_score=0.5,
            maturity_score=0.9,
            license_risk_score=0.4
        ),
        OSSProject(
            name="Redis",
            description="In-memory cache",
            capabilities=[CapabilityType.CACHE],
            license="BSD",
            security_score=0.80,
            cost_score=0.3,
            complexity_score=0.3,
            maturity_score=0.9,
            license_risk_score=0.2
        )
    ]


@pytest.fixture
def test_graph(sample_projects) -> SemanticGraph:
    """Create a test graph with sample projects"""
    graph = SemanticGraph(data_dir="tests/data")
    # Use the actual add_project method
    for project in sample_projects:
        graph.add_project(project)
    return graph

@pytest.fixture
def sample_intent() -> Intent:
    """Create a sample intent for testing"""
    return Intent(
        description="Test web app with database",
        required_capabilities=[
            CapabilityType.WEB_FRAMEWORK,
            CapabilityType.DATABASE
        ]
    )

@pytest.fixture
def sample_weights() -> Dict[str, float]:
    """Sample weights for multi-objective scoring"""
    return {
        'security': 0.4,
        'cost': 0.3,
        'complexity': 0.1,
        'maturity': 0.1,
        'license_risk': 0.1
    }

@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file for testing file operations"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        yield Path(f.name)
    # Cleanup after test
    Path(f.name).unlink(missing_ok=True)