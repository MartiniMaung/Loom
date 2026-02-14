"""
Pattern Auditor - Analyze architectural patterns for issues and improvements.
Phase 1.3 of Loom Roadmap: Audit Mode
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

from .core import OSSProject, CapabilityType, RelationshipType
from .graph import SemanticGraph
from .weaver import Pattern

class AuditSeverity(Enum):
    """Severity levels for audit findings."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AuditCategory(Enum):
    """Categories for audit findings."""
    COMPATIBILITY = "compatibility"
    LICENSE = "license"
    SECURITY = "security"
    REDUNDANCY = "redundancy"
    BEST_PRACTICE = "best_practice"
    PERFORMANCE = "performance"

@dataclass
class AuditFinding:
    """An individual audit finding."""
    category: AuditCategory
    severity: AuditSeverity
    component: Optional[str]
    message: str
    recommendation: Optional[str]
    evidence: Optional[str] = None

class PatternAuditor:
    """Audits architectural patterns for issues and improvements."""
    
    def __init__(self, graph: SemanticGraph):
        self.graph = graph
        self.findings: List[AuditFinding] = []

    def _get_project(self, name: str) -> Optional[OSSProject]:
        """Get project by name, handling space/underscore variations."""
        # Try exact match first
        if name in self.graph.projects:
            return self.graph.projects[name]
        
        # Try common variations
        variations = [
            name,  # Original
            name.replace(" ", "_"),  # Spaces to underscores
            name.replace("_", " "),  # Underscores to spaces
            name.lower(),  # Lowercase
            name.replace(" ", "_").lower(),  # Lowercase with underscores
        ]
        
        for variation in variations:
            if variation in self.graph.projects:
                return self.graph.projects[variation]
        
        # Try case-insensitive partial match
        name_lower = name.lower()
        for key, project in self.graph.projects.items():
            if key.lower() == name_lower:
                return project
        
        return None

    
    def audit_pattern(self, pattern: Pattern) -> List[AuditFinding]:
        """Run comprehensive audit on a pattern."""
        self.findings = []
        
        # Run all audit checks
        self._check_compatibility(pattern)
        self._check_licenses(pattern)
        self._check_security(pattern)
        self._check_redundancy(pattern)
        self._check_best_practices(pattern)
        
        return self.findings
    
    def audit_pattern_file(self, pattern_file: str) -> List[AuditFinding]:
        """Load and audit a pattern from JSON file."""
        pattern = self._load_pattern(pattern_file)
        return self.audit_pattern(pattern)
    
    def _load_pattern(self, pattern_file: str) -> Pattern:
        """Load a pattern from JSON file."""
        with open(pattern_file, 'r', encoding='utf-8-sig') as f:
            pattern_data = json.load(f)
        
        pattern = Pattern(
            name=pattern_data.get("name", "Unnamed Pattern"),
            description=pattern_data.get("description", ""),
            intent=None
        )
        
        for comp in pattern_data.get("components", []):
            project_name = comp.get("name")
            role = comp.get("role", "Unknown")
            project = self._get_project(project_name)
            if project:
                pattern.add_component(project, role)
        
        return pattern
    
    def _check_compatibility(self, pattern: Pattern) -> None:
        """Check compatibility between components."""
        component_names = [comp[0].name for comp in pattern.components]
        
        for i, (source, _) in enumerate(pattern.components):
            for j, (target, _) in enumerate(pattern.components):
                if i != j:
                    # Check if there's a known compatibility relationship
                    if self.graph.graph.has_edge(source.name, target.name):
                        edge_data = self.graph.graph[source.name][target.name]
                        rel_type = edge_data.get('relationship_type')
                        strength = edge_data.get('strength', 0.5)
                        
                        if rel_type == RelationshipType.COMPATIBLE_WITH.value:
                            if strength < 0.7:
                                self.findings.append(AuditFinding(
                                    category=AuditCategory.COMPATIBILITY,
                                    severity=AuditSeverity.WARNING,
                                    component=f"{source.name} ↔ {target.name}",
                                    message=f"Low compatibility confidence ({strength:.2f}) between {source.name} and {target.name}",
                                    recommendation="Consider alternative pairings or verify integration",
                                    evidence=edge_data.get('evidence', '')
                                ))
                        elif rel_type == RelationshipType.INCOMPATIBLE_WITH.value:
                            self.findings.append(AuditFinding(
                                category=AuditCategory.COMPATIBILITY,
                                severity=AuditSeverity.ERROR,
                                component=f"{source.name} ↔ {target.name}",
                                message=f"Incompatible components: {source.name} and {target.name}",
                                recommendation="Replace one of the components",
                                evidence=edge_data.get('evidence', '')
                            ))
    
    def _check_licenses(self, pattern: Pattern) -> None:
        """Check for license conflicts and issues."""
        licenses = {}
        
        for project, role in pattern.components:
            if project.license:
                if project.license not in licenses:
                    licenses[project.license] = []
                licenses[project.license].append(project.name)
        
        # Check for restrictive licenses
        restrictive_licenses = ["SSPL", "Elastic License", "Commons Clause", "AGPL"]
        for license_type, projects in licenses.items():
            if license_type in restrictive_licenses:
                self.findings.append(AuditFinding(
                    category=AuditCategory.LICENSE,
                    severity=AuditSeverity.WARNING,
                    component=", ".join(projects),
                    message=f"Restrictive license detected: {license_type}",
                    recommendation="Consider open source alternatives with permissive licenses",
                    evidence=f"Affects: {', '.join(projects)}"
                ))
        
        # Check for GPL contamination risk
        has_gpl = any("GPL" in lic for lic in licenses.keys())
        has_proprietary_compatible = any(lic in ["MIT", "BSD", "Apache 2.0"] for lic in licenses.keys())
        
        if has_gpl and has_proprietary_compatible and len(licenses) > 1:
            self.findings.append(AuditFinding(
                category=AuditCategory.LICENSE,
                severity=AuditSeverity.WARNING,
                component="Multiple components",
                message="Potential GPL license contamination risk",
                recommendation="Review license compatibility or isolate GPL components",
                evidence=f"Mixed licenses: {', '.join(licenses.keys())}"
            ))
    
    def _check_security(self, pattern: Pattern) -> None:
        """Check security aspects of the pattern."""
        security_scores = []
        low_security_components = []
        
        for project, role in pattern.components:
            if hasattr(project, 'security_score') and project.security_score is not None:
                security_scores.append(project.security_score)
                if project.security_score < 0.7:
                    low_security_components.append(f"{project.name} ({project.security_score:.2f})")
        
        if security_scores:
            avg_security = sum(security_scores) / len(security_scores)
            
            if avg_security < 0.75:
                self.findings.append(AuditFinding(
                    category=AuditCategory.SECURITY,
                    severity=AuditSeverity.WARNING,
                    component="Pattern average",
                    message=f"Low average security score: {avg_security:.2f}",
                    recommendation="Consider higher-security alternatives or add security components",
                    evidence=f"Components: {', '.join(low_security_components) if low_security_components else 'All components'}"
                ))
            
            # Check for missing authentication
            has_auth = any("authentication" in [cap.value for cap in project.capabilities] 
                          for project, _ in pattern.components)
            
            if not has_auth and any("web_framework" in [cap.value for cap in project.capabilities] 
                                   for project, _ in pattern.components):
                self.findings.append(AuditFinding(
                    category=AuditCategory.SECURITY,
                    severity=AuditSeverity.ERROR,
                    component="Authentication",
                    message="Missing authentication component in web application",
                    recommendation="Add authentication service (Keycloak, Ory Kratos, etc.)",
                    evidence="Web framework present without authentication"
                ))
    
    def _check_redundancy(self, pattern: Pattern) -> None:
        """Check for redundant or duplicate components."""
        # Check for duplicate capabilities
        capability_counts = {}
        
        for project, _ in pattern.components:
            for capability in project.capabilities:
                cap_name = capability.value
                if cap_name not in capability_counts:
                    capability_counts[cap_name] = []
                capability_counts[cap_name].append(project.name)
        
        for capability, projects in capability_counts.items():
            if len(projects) > 1 and capability not in ["database", "cache"]:  # Multiple DBs/caches might be intentional
                self.findings.append(AuditFinding(
                    category=AuditCategory.REDUNDANCY,
                    severity=AuditSeverity.WARNING,
                    component=", ".join(projects),
                    message=f"Multiple components providing same capability: {capability}",
                    recommendation=f"Consider consolidating {capability} functionality",
                    evidence=f"Provided by: {', '.join(projects)}"
                ))
        
        # Check for multiple databases
        if "database" in capability_counts and len(capability_counts["database"]) > 1:
            self.findings.append(AuditFinding(
                category=AuditCategory.REDUNDANCY,
                severity=AuditSeverity.INFO,
                component=", ".join(capability_counts["database"]),
                message=f"Multiple databases detected: {len(capability_counts['database'])}",
                recommendation="Ensure multiple databases are intentional (e.g., polyglot persistence)",
                evidence=f"Databases: {', '.join(capability_counts['database'])}"
            ))
    
    def _check_best_practices(self, pattern: Pattern) -> None:
        """Check against architectural best practices."""
        components = [project.name for project, _ in pattern.components]
        
        # Check for caching with database
        has_db = any("database" in [cap.value for cap in project.capabilities] 
                    for project, _ in pattern.components)
        has_cache = any("cache" in [cap.value for cap in project.capabilities] 
                       for project, _ in pattern.components)
        
        if has_db and not has_cache and len(components) >= 3:
            self.findings.append(AuditFinding(
                category=AuditCategory.BEST_PRACTICE,
                severity=AuditSeverity.INFO,
                component="Database layer",
                message="Database present without caching layer",
                recommendation="Consider adding Redis for caching to improve performance",
                evidence=f"Database components: {[p.name for p, _ in pattern.components if 'database' in [c.value for c in p.capabilities]]}"
            ))
        
        # Check for monitoring
        has_monitoring = any("monitoring" in [cap.value for cap in project.capabilities] 
                           for project, _ in pattern.components)
        
        if not has_monitoring and len(components) >= 3:
            self.findings.append(AuditFinding(
                category=AuditCategory.BEST_PRACTICE,
                severity=AuditSeverity.INFO,
                component="Operations",
                message="No monitoring/observability components",
                recommendation="Add monitoring (Prometheus) and visualization (Grafana)",
                evidence=f"Current components: {', '.join(components)}"
            ))
    
    def generate_report(self, findings: List[AuditFinding], output_format: str = "text") -> str:
        """Generate audit report in specified format."""
        if output_format == "text":
            return self._generate_text_report(findings)
        elif output_format == "json":
            return self._generate_json_report(findings)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_text_report(self, findings: List[AuditFinding]) -> str:
        """Generate human-readable text report."""
        if not findings:
            return "✅ No issues found. Pattern looks good!"
        
        report_lines = ["🔍 ARCHITECTURE AUDIT REPORT", "=" * 50, ""]
        
        # Group by severity
        by_severity = {}
        for finding in findings:
            if finding.severity not in by_severity:
                by_severity[finding.severity] = []
            by_severity[finding.severity].append(finding)
        
        # Severity order
        severity_order = [AuditSeverity.CRITICAL, AuditSeverity.ERROR, 
                         AuditSeverity.WARNING, AuditSeverity.INFO]
        
        for severity in severity_order:
            if severity in by_severity:
                severity_findings = by_severity[severity]
                report_lines.append(f"\n{severity.value.upper()} ({len(severity_findings)})")
                report_lines.append("-" * 30)
                
                for finding in severity_findings:
                    report_lines.append(f"• [{finding.category.value}] {finding.message}")
                    if finding.component:
                        report_lines.append(f"  Component: {finding.component}")
                    if finding.recommendation:
                        report_lines.append(f"  Recommendation: {finding.recommendation}")
                    if finding.evidence:
                        report_lines.append(f"  Evidence: {finding.evidence}")
                    report_lines.append("")
        
        # Summary
        report_lines.append("=" * 50)
        report_lines.append("📊 SUMMARY")
        total = len(findings)
        counts = {sev: len(by_severity.get(sev, [])) for sev in severity_order}
        report_lines.append(f"Total findings: {total}")
        for sev in severity_order:
            if counts[sev] > 0:
                report_lines.append(f"  {sev.value}: {counts[sev]}")
        
        return "\n".join(report_lines)
    
    def _generate_json_report(self, findings: List[AuditFinding]) -> str:
        """Generate JSON report."""
        report = {
            "summary": {
                "total_findings": len(findings),
                "by_severity": {},
                "by_category": {}
            },
            "findings": []
        }
        
        for finding in findings:
            report["findings"].append({
                "category": finding.category.value,
                "severity": finding.severity.value,
                "component": finding.component,
                "message": finding.message,
                "recommendation": finding.recommendation,
                "evidence": finding.evidence
            })
            
            # Update counts
            sev = finding.severity.value
            cat = finding.category.value
            
            report["summary"]["by_severity"][sev] = report["summary"]["by_severity"].get(sev, 0) + 1
            report["summary"]["by_category"][cat] = report["summary"]["by_category"].get(cat, 0) + 1
        
        return json.dumps(report, indent=2)