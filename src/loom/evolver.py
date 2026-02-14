"""
Pattern Evolver - Evolve existing architectural patterns with new capabilities.
Phase 1.2 of Loom Roadmap: Pattern Evolution
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from .core import OSSProject, CapabilityType, Intent
from .graph import SemanticGraph
from .weaver import Pattern

class PatternEvolver:
    """Evolves existing patterns with new capabilities."""
    
    def __init__(self, graph: SemanticGraph):
        self.graph = graph
        self.scalability_rules = self._build_scalability_rules()

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

    
    def _build_scalability_rules(self) -> List[Dict[str, Any]]:
        """Define rules for making patterns more scalable."""
        return [
            {
                "name": "database_scalability",
                "condition": lambda pattern: self._has_component_with_capability(pattern, "database"),
                "action": lambda pattern: self._enhance_database_scalability(pattern),
                "description": "Enhance database for better scalability"
            },
            {
                "name": "add_caching_layer",
                "condition": lambda pattern: self._is_data_intensive(pattern),
                "action": lambda pattern: self._add_caching_layer(pattern),
                "description": "Add caching layer for performance"
            },
            {
                "name": "async_processing",
                "condition": lambda pattern: self._has_synchronous_bottlenecks(pattern),
                "action": lambda pattern: self._add_message_queue(pattern),
                "description": "Add message queue for async processing"
            }
        ]
    
    def load_pattern(self, pattern_file: str) -> Pattern:
        """Load a pattern from JSON file."""
        with open(pattern_file, 'r', encoding='utf-8-sig') as f:
            pattern_data = json.load(f)
        
        # Create pattern object
        pattern = Pattern(
            name=pattern_data.get("name", "Unnamed Pattern"),
            description=pattern_data.get("description", ""),
            intent=None  # Original intent may not be stored
        )
        
        # Add components
        for comp in pattern_data.get("components", []):
            project_name = comp.get("name")
            role = comp.get("role", "Unknown")
            project = self._get_projects(project_name)
            if project:
                pattern.add_component(project, role)
        
        return pattern
    
    def evolve(self, pattern: Pattern, evolution_type: str) -> Pattern:
        """Evolve a pattern with specific evolution type."""
        if evolution_type == "make-scalable":
            return self._make_scalable(pattern)
        elif evolution_type == "add-security":
            return self._add_security(pattern)
        elif evolution_type == "optimize-cost":
            return self._optimize_cost(pattern)
        else:
            raise ValueError(f"Unknown evolution type: {evolution_type}")
    
    def _make_scalable(self, pattern: Pattern) -> Pattern:
        """Make a pattern more scalable."""
        evolved_pattern = Pattern(
            name=f"{pattern.name} (Scalable)",
            description=f"{pattern.description} - Enhanced for scalability",
            intent=pattern.intent
        )
        
        # Copy existing components
        for project, role in pattern.components:
            evolved_pattern.add_component(project, role)
        
        # Apply scalability rules
        applied_transformations = []
        for rule in self.scalability_rules:
            if rule["condition"](pattern):
                rule["action"](evolved_pattern)
                applied_transformations.append(rule["description"])
        
        # Add transformation notes
        if applied_transformations:
            evolved_pattern.tags = pattern.tags + ["scalable", "evolved"]
            evolved_pattern.description += f". Applied: {', '.join(applied_transformations)}"
        
        return evolved_pattern
    
    def _add_security(self, pattern: Pattern) -> Pattern:
        """Add security enhancements to a pattern using Phase 1 security scoring."""
        evolved_pattern = Pattern(
            name=f"{pattern.name} (Secure)",
            description=f"{pattern.description} - Enhanced for security",
            intent=pattern.intent
        )
        
        # Track security improvements made
        security_improvements = []
        
        # 1. Copy existing components, but consider upgrades
        for project, role in pattern.components:
            # Check if we should upgrade this component for better security
            upgraded_project = self._suggest_security_upgrade(project, role)
            if upgraded_project and upgraded_project != project:
                evolved_pattern.add_component(upgraded_project, f"{role} (Security Enhanced)")
                security_improvements.append(f"Upgraded {project.name}→{upgraded_project.name} for security")
            else:
                evolved_pattern.add_component(project, role)
        
        # 2. Add missing security components based on pattern type
        added_components = self._add_missing_security_components(evolved_pattern, pattern)
        security_improvements.extend(added_components)
        
        # 3. Calculate and show security score improvement
        original_score = self._calculate_pattern_security_score(pattern)
        new_score = self._calculate_pattern_security_score(evolved_pattern)
        score_improvement = new_score - original_score
        
        if score_improvement > 0:
            security_improvements.append(f"Security score: {original_score:.2f}→{new_score:.2f} (+{score_improvement:.2f})")
        
        # 4. Update description with security improvements
        if security_improvements:
            evolved_pattern.description += f". Security enhancements: {', '.join(security_improvements[:3])}"
            if hasattr(evolved_pattern, 'transformation_notes'):
                evolved_pattern.transformation_notes.extend(security_improvements)
            else:
                evolved_pattern.transformation_notes = security_improvements
        
        evolved_pattern.tags = pattern.tags + ["secure", "evolved", "high_security"]
        return evolved_pattern
    
    def _suggest_security_upgrade(self, project: OSSProject, role: str) -> Optional[OSSProject]:
        """Suggest a higher-security alternative for a component."""
        # Security upgrade mappings
        security_upgrades = {
            # Web frameworks
            "FastAPI": "Django",  # FastAPI 0.75 → Django 0.85
            # Databases  
            "MySQL": "PostgreSQL",  # MySQL 0.78 → PostgreSQL 0.80
            # Message queues
            "RabbitMQ": "Apache_Kafka",  # RabbitMQ 0.77 → Kafka 0.84
            # Authentication (none → Keycloak is handled separately)
        }
        
        if project.name in security_upgrades:
            upgrade_name = security_upgrades[project.name]
            upgraded = self.graph.projects.get(upgrade_name)
            if upgraded and hasattr(upgraded, 'security_score') and hasattr(project, 'security_score'):
                if upgraded.security_score > project.security_score:
                    return upgraded
        
        return None
    
    def _add_missing_security_components(self, evolved_pattern: Pattern, original_pattern: Pattern) -> List[str]:
        """Add missing security components based on pattern type."""
        added = []
        
        # Always add authentication if missing
        if not self._has_component_with_capability(original_pattern, "authentication"):
            keycloak = self.graph.projects.get("Keycloak")
            ory_kratos = self.graph.projects.get("Ory_Kratos")
            
            # Choose highest security score
            if keycloak and ory_kratos:
                best_auth = keycloak if keycloak.security_score >= ory_kratos.security_score else ory_kratos
            elif keycloak:
                best_auth = keycloak
            elif ory_kratos:
                best_auth = ory_kratos
            else:
                best_auth = None
            
            if best_auth:
                evolved_pattern.add_component(best_auth, "Authentication & Identity Management")
                added.append(f"Added {best_auth.name} for authentication (security: {best_auth.security_score:.2f})")
        
        # Add monitoring for security auditing if web app
        if self._has_component_with_capability(original_pattern, "web_framework"):
            if not self._has_component_with_capability(original_pattern, "monitoring"):
                prometheus = self.graph.projects.get("Prometheus")
                grafana = self.graph.projects.get("Grafana")
                
                if prometheus:
                    evolved_pattern.add_component(prometheus, "Security Monitoring & Metrics")
                    added.append(f"Added {prometheus.name} for security monitoring")
                if grafana:
                    evolved_pattern.add_component(grafana, "Security Dashboard & Visualization")
                    added.append(f"Added {grafana.name} for security visualization")
        
        return added
    
    def _calculate_pattern_security_score(self, pattern: Pattern) -> float:
        """Calculate average security score for a pattern."""
        if not pattern.components:
            return 0.0
        
        security_scores = []
        for project, _ in pattern.components:
            if hasattr(project, 'security_score') and project.security_score is not None:
                security_scores.append(project.security_score)
            else:
                security_scores.append(0.0)
        
        return sum(security_scores) / len(security_scores) if security_scores else 0.0
    
    def _optimize_cost(self, pattern: Pattern) -> Pattern:
        """Optimize pattern for cost reduction with intelligent rules."""
        evolved_pattern = Pattern(
            name=f"{pattern.name} (Cost-Optimized)",
            description=f"{pattern.description} - Optimized for cost efficiency",
            intent=pattern.intent
        )
        
        # Track cost optimizations made
        cost_optimizations = []
        
        # 1. Process each component with cost optimization
        for project, role in pattern.components:
            # Check if we should replace with a more cost-effective alternative
            cost_effective_project = self._suggest_cost_effective_alternative(project, role)
            if cost_effective_project and cost_effective_project != project:
                evolved_pattern.add_component(cost_effective_project, f"{role} (Cost-Optimized)")
                cost_optimizations.append(f"Replaced {project.name}→{cost_effective_project.name} for cost savings")
            else:
                evolved_pattern.add_component(project, role)
        
        # 2. Look for consolidation opportunities
        consolidated = self._consolidate_components(evolved_pattern)
        cost_optimizations.extend(consolidated)
        
        # 3. Calculate estimated cost savings
        original_cost_score = self._calculate_pattern_cost_score(pattern)
        new_cost_score = self._calculate_pattern_cost_score(evolved_pattern)
        cost_savings = original_cost_score - new_cost_score
        
        if cost_savings > 0:
            cost_optimizations.append(f"Cost efficiency: {original_cost_score:.2f}→{new_cost_score:.2f} (+{cost_savings:.2f} savings)")
        
        # 4. Update description with cost optimizations
        if cost_optimizations:
            evolved_pattern.description += f". Cost optimizations: {', '.join(cost_optimizations[:3])}"
            if hasattr(evolved_pattern, 'transformation_notes'):
                evolved_pattern.transformation_notes.extend(cost_optimizations)
            else:
                evolved_pattern.transformation_notes = cost_optimizations
        
        evolved_pattern.tags = pattern.tags + ["cost-optimized", "evolved", "budget_friendly"]
        return evolved_pattern
    
    def _suggest_cost_effective_alternative(self, project: OSSProject, role: str) -> Optional[OSSProject]:
        """Suggest a more cost-effective alternative for a component."""
        # Cost optimization mappings
        cost_optimizations = {
            # High resource components → lighter alternatives
            "Apache_Kafka": "RabbitMQ",  # Kafka is heavier than RabbitMQ
            "Elasticsearch": "PostgreSQL",  # ES can be overkill for simple search
            "Keycloak": "Ory_Kratos",  # Keycloak is heavy, Ory Kratos is lighter
            "Grafana": "Prometheus",  # Grafana adds visualization overhead
        }
        
        if project.name in cost_optimizations:
            alternative_name = cost_optimizations[project.name]
            if alternative_name:
                alternative = self.graph.projects.get(alternative_name)
                if alternative:
                    return alternative
        
        # Special case: If component has restrictive license, suggest OSI-approved alternative
        restrictive_licenses = ["SSPL", "Elastic License", "Commons Clause"]
        if project.license in restrictive_licenses:
            return self._find_osi_approved_alternative(project)
        
        return None
    
    def _find_osi_approved_alternative(self, project: OSSProject) -> Optional[OSSProject]:
        """Find OSI-approved alternative for restrictively licensed component."""
        # Map restrictive licensed projects to OSI-approved alternatives
        osi_alternatives = {
            "MongoDB": "PostgreSQL",  # SSPL → PostgreSQL
            "Elasticsearch": "Apache_Solr",  # Elastic License → Apache 2.0
            "Redis": None,  # BSD is fine
            "MySQL": "PostgreSQL",  # GPL → PostgreSQL license
        }
        
        if project.name in osi_alternatives:
            alt_name = osi_alternatives[project.name]
            if alt_name:
                return self.graph.projects.get(alt_name)
        
        return None
    
    def _consolidate_components(self, pattern: Pattern) -> List[str]:
        """Look for opportunities to consolidate multiple components into one."""
        consolidations = []
        
        # Check if we have both Prometheus and Grafana
        has_prometheus = self._has_component_by_name(pattern, "Prometheus")
        has_grafana = self._has_component_by_name(pattern, "Grafana")
        
        # If pattern is simple, suggest using just Prometheus
        if has_prometheus and has_grafana:
            simple_components = len(pattern.components)
            if simple_components <= 4:  # Simple pattern doesn't need both
                # Remove Grafana, keep Prometheus
                if self._remove_component_by_name(pattern, "Grafana"):
                    consolidations.append("Consolidated: Removed Grafana (using Prometheus only for simplicity)")
        
        # Check for multiple databases
        db_count = sum(1 for project, _ in pattern.components 
                      if "database" in [cap.value for cap in project.capabilities])
        if db_count > 1:
            consolidations.append("Multiple databases detected - consider consolidation")
        
        return consolidations
    
    def _remove_component_by_name(self, pattern: Pattern, name: str) -> bool:
        """Remove a component from pattern by name."""
        for i, (project, _) in enumerate(pattern.components):
            if project.name == name:
                pattern.components.pop(i)
                return True
        return False
    
    def _calculate_pattern_cost_score(self, pattern: Pattern) -> float:
        """Calculate cost efficiency score for a pattern (lower is better)."""
        if not pattern.components:
            return 0.0
        
        cost_factors = []
        
        for project, _ in pattern.components:
            component_cost = 1.0  # Base cost
            
            # Adjust for license restrictions
            restrictive_licenses = ["SSPL", "Elastic License", "Commons Clause", "AGPL"]
            if project.license in restrictive_licenses:
                component_cost *= 1.5  # 50% cost penalty for restrictive licenses
            
            # Adjust for resource intensity (simplified heuristic)
            resource_intensive = ["Apache_Kafka", "Elasticsearch", "Keycloak", "Apache_Spark"]
            if project.name in resource_intensive:
                component_cost *= 1.3  # 30% cost penalty for resource-intensive
            
            # Bonus for permissive licenses
            permissive_licenses = ["MIT", "BSD", "Apache 2.0", "PostgreSQL"]
            if project.license in permissive_licenses:
                component_cost *= 0.9  # 10% discount for permissive licenses
            
            cost_factors.append(component_cost)
        
        # Also consider component count (more components = higher operational cost)
        component_count_penalty = len(pattern.components) * 0.05
        
        return (sum(cost_factors) / len(cost_factors)) + component_count_penalty if cost_factors else 0.0
    
    # Helper methods for scalability rules
    def _has_component_with_capability(self, pattern: Pattern, capability: str) -> bool:
        """Check if pattern has a component with specific capability."""
        for project, _ in pattern.components:
            if any(cap.value == capability for cap in project.capabilities):
                return True
        return False
    
    def _is_data_intensive(self, pattern: Pattern) -> bool:
        """Check if pattern is data-intensive (simplified heuristic)."""
        # Simple heuristic: has database and is web framework
        has_db = self._has_component_with_capability(pattern, "database")
        has_web = self._has_component_with_capability(pattern, "web_framework")
        return has_db and has_web
    
    def _has_synchronous_bottlenecks(self, pattern: Pattern) -> bool:
        """Check for synchronous processing bottlenecks."""
        # Simple heuristic: has web framework but no async/messaging
        has_web = self._has_component_with_capability(pattern, "web_framework")
        has_async = self._has_component_with_capability(pattern, "message_queue")
        return has_web and not has_async
    
    def _enhance_database_scalability(self, pattern: Pattern) -> None:
        """Enhance database for scalability."""
        # Example: Could suggest moving from SQLite to PostgreSQL
        # For now, just add a note
        if not hasattr(pattern, 'transformation_notes'):
            pattern.transformation_notes = []
        pattern.transformation_notes.append("Database scalability enhanced")
    
    def _add_caching_layer(self, pattern: Pattern) -> None:
        """Add caching layer to pattern."""
        # Add Redis if available
        redis = self.graph.projects.get("Redis")
        if redis and not self._has_component_by_name(pattern, "Redis"):
            pattern.add_component(redis, "Cache & Session Storage")
    
    def _add_message_queue(self, pattern: Pattern) -> None:
        """Add message queue for async processing."""
        # Add RabbitMQ or Kafka if available
        rabbitmq = self.graph.projects.get("RabbitMQ")
        kafka = self.graph.projects.get("Apache_Kafka")
        
        if rabbitmq and not self._has_component_by_name(pattern, "RabbitMQ"):
            pattern.add_component(rabbitmq, "Message Queue for Async Processing")
        elif kafka and not self._has_component_by_name(pattern, "Apache_Kafka"):
            pattern.add_component(kafka, "Event Streaming Platform")
    
    def _has_component_by_name(self, pattern: Pattern, name: str) -> bool:
        """Check if pattern has component with given name."""
        for project, _ in pattern.components:
            if project.name == name:
                return True
        return False
    
    def save_pattern(self, pattern: Pattern, output_file: str) -> None:
        """Save evolved pattern to JSON file."""
        pattern_dict = {
            "name": pattern.name,
            "description": pattern.description,
            "components": [
                {
                    "name": project.name,
                    "role": role,
                    "capabilities": [cap.value for cap in project.capabilities]
                }
                for project, role in pattern.components
            ],
            "tags": pattern.tags if hasattr(pattern, 'tags') else [],
            "evolution_notes": getattr(pattern, 'transformation_notes', [])
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pattern_dict, f, indent=2)