"""
API Response Models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ComponentDetail(BaseModel):
    """Detailed component information"""
    name: str
    security_score: float
    capabilities: List[str]
    confidence: float
    reasoning: Optional[str] = None

class WeaveResponse(BaseModel):
    """Response from /weave endpoint"""
    pattern_name: str
    components: List[ComponentDetail]
    confidence: float
    complexity: float
    reasoning: Optional[str] = None
    execution_time_ms: float

class ProjectInfo(BaseModel):
    """Project information"""
    name: str
    capabilities: List[str]
    security_score: float
    license: Optional[str] = None

class ProjectsResponse(BaseModel):
    """Response from /projects endpoint"""
    total: int
    projects: List[ProjectInfo]

class EvolutionResult(BaseModel):
    """Result of pattern evolution"""
    original_pattern: Dict[str, Any]
    evolved_pattern: Dict[str, Any]
    evolutions_applied: List[str]
    reasoning: Optional[str] = None
    execution_time_ms: float

class AuditFinding(BaseModel):
    """Single audit finding"""
    category: str
    severity: str
    message: str
    component: Optional[str] = None
    recommendation: str

class AuditResponse(BaseModel):
    """Response from /audit endpoint"""
    pattern_name: str
    findings: List[AuditFinding]
    summary: Dict[str, int]
    passed: bool
    execution_time_ms: float