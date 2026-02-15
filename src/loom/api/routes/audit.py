"""
Audit endpoint - integrates with auditor.py
"""
from fastapi import APIRouter, HTTPException
import json
import sys
import os
from pathlib import Path

# Add project root to path to import loom modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.loom.graph import SemanticGraph

from ..models.requests import AuditRequest
from ..models.responses import AuditResponse, AuditFinding

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

def audit_pattern_logic(pattern):
    """Simple pattern audit logic"""
    findings = []
    components = pattern.get('components', [])
    
    # Check for security issues
    security_scores = {
        'FastAPI': 0.75,
        'Django': 0.85,
        'MySQL': 0.78,
        'PostgreSQL': 0.80,
        'RabbitMQ': 0.77,
        'Kafka': 0.84,
        'Redis': 0.82,
        'Keycloak': 0.90,
        'Ory_Kratos': 0.88
    }
    
    # Security audit
    low_security = []
    for comp in components:
        score = security_scores.get(comp, 0.5)
        if score < 0.8:
            low_security.append(comp)
    
    if low_security:
        findings.append({
            'category': 'Security',
            'severity': 'Warning',
            'message': f'Low security components: {", ".join(low_security)}',
            'component': low_security[0],
            'recommendation': 'Consider upgrading to more secure alternatives'
        })
    
    # Check for database
    if not any(db in components for db in ['MySQL', 'PostgreSQL', 'MongoDB']):
        findings.append({
            'category': 'Compatibility',
            'severity': 'Error',
            'message': 'No database component found',
            'component': None,
            'recommendation': 'Add a database like PostgreSQL or MySQL'
        })
    
    # Check for license compatibility
    open_source = all(comp not in ['Oracle', 'MS SQL'] for comp in components)
    if not open_source:
        findings.append({
            'category': 'License',
            'severity': 'Warning',
            'message': 'Proprietary components detected',
            'component': None,
            'recommendation': 'Review license compatibility'
        })
    
    # Check for redundancy
    if 'RabbitMQ' in components and 'Kafka' in components:
        findings.append({
            'category': 'Redundancy',
            'severity': 'Info',
            'message': 'Multiple message queues detected',
            'component': None,
            'recommendation': 'Consider using a single message queue solution'
        })
    
    return findings

@router.post("/audit", response_model=AuditResponse)
async def audit_pattern(request: AuditRequest):
    """Audit a pattern for issues"""
    try:
        # Audit the pattern
        findings = audit_pattern_logic(request.pattern_json)
        
        # Format findings
        audit_findings = []
        severity_counts = {"Info": 0, "Warning": 0, "Error": 0, "Critical": 0}
        
        for finding in findings:
            severity = finding.get('severity', 'Info')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            audit_findings.append(AuditFinding(
                category=finding.get('category', 'Unknown'),
                severity=severity,
                message=finding.get('message', ''),
                component=finding.get('component'),
                recommendation=finding.get('recommendation', '')
            ))
        
        # Determine if pattern passed (no errors or critical issues)
        passed = severity_counts.get('Error', 0) == 0 and severity_counts.get('Critical', 0) == 0
        
        # Get pattern name
        pattern_name = request.pattern_json.get('name', 'Unnamed Pattern')
        
        return AuditResponse(
            pattern_name=pattern_name,
            findings=audit_findings,
            summary=severity_counts,
            passed=passed,
            execution_time_ms=0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))