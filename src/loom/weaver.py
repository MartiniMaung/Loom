"""
Pattern Weaver - The intelligent engine that finds architectural patterns.
"""
from typing import List, Dict, Any, Optional, Tuple
from .core import Intent, CapabilityType, OSSProject, RelationshipType
from .graph import SemanticGraph

class Pattern:
    """A discovered architectural pattern."""
    
    def __init__(self, name: str, description: str, intent: Intent = None):        
        self.name = name
        self.description = description
        self.intent = intent  # ⬅️⬅️⬅️ CRITICAL: ADD THIS LINE
        self.components: List[Tuple[OSSProject, str]] = []  # (project, role)
        self.connections: List[Dict[str, Any]] = []
        self.complexity: float = 0.0  # 0-1 scale
        self.confidence: float = 0.0  # 0-1 scale
        self.tags: List[str] = []
        
    def add_component(self, project: OSSProject, role: str):
        """Add a component to the pattern."""
        self.components.append((project, role))
        
    def calculate_metrics(self, graph: SemanticGraph):
        """Calculate pattern metrics."""
        # Complexity based on number of components and relationships
        num_components = len(self.components)
        
        # Count internal connections between components
        internal_connections = 0
        component_names = [comp[0].name for comp in self.components]
        for source in component_names:
            for target in component_names:
                if source != target and graph.graph.has_edge(source, target):
                    internal_connections += 1
        
        self.complexity = min(1.0, (num_components * 0.1) + (internal_connections * 0.05))
        
        # Confidence based on popularity and compatibility
        if self.components:
            # Average popularity
            pop_sum = sum(comp[0].popularity_score for comp in self.components)
            pop_avg = pop_sum / len(self.components)
            
            # Compatibility score
            compat_score = 0.0
            compat_pairs = 0
            for i, (source_comp, _) in enumerate(self.components):
                for j, (target_comp, _) in enumerate(self.components):
                    if i != j:
                        if graph.graph.has_edge(source_comp.name, target_comp.name):
                            edge_data = graph.graph[source_comp.name][target_comp.name]
                            if edge_data.get('relationship_type') == RelationshipType.COMPATIBLE_WITH.value:
                                compat_score += edge_data.get('strength', 0.5)
                                compat_pairs += 1
            
            avg_compat = compat_score / max(1, compat_pairs)
            self.confidence = (pop_avg * 0.7) + (avg_compat * 0.3)
            # ===== SECURITY WEIGHTING =====
            if self.intent and CapabilityType.HIGH_SECURITY in self.intent.required_capabilities:
               # Calculate average security score for components
                security_scores = []
                for comp, _ in self.components:
                    if hasattr(comp, 'security_score') and comp.security_score is not None:
                        security_scores.append(comp.security_score)
                    else:
                        # Default to 0 if security_score not available
                        security_scores.append(0.0)
                
                if security_scores:
                    avg_security = sum(security_scores) / len(security_scores)
                    # Apply security boost: up to 20% increase for high-security patterns
                    security_boost = avg_security * 0.2
                    self.confidence = min(1.0, self.confidence + security_boost)
            # ===== END SECURITY WEIGHTING =====
        else:
            self.confidence = 0.0
            
    def to_dict(self, graph: SemanticGraph) -> Dict[str, Any]:
        """Convert pattern to dictionary."""
        self.calculate_metrics(graph)
        return {
            "name": self.name,
            "description": self.description,
            "complexity": round(self.complexity, 3),
            "confidence": round(self.confidence, 3),
            "components": [
                {
                    "name": project.name,
                    "role": role,
                    "capabilities": [c.value for c in project.capabilities],
                    "license": project.license or "Unknown",
                    "popularity": project.popularity_score
                }
                for project, role in self.components
            ],
            "connections": self._get_connections(graph)
        }
        
    def _get_connections(self, graph: SemanticGraph) -> List[Dict[str, Any]]:
        """Get connections between components in this pattern."""
        connections = []
        component_names = [comp[0].name for comp in self.components]
        
        for source_name in component_names:
            for target_name in component_names:
                if source_name != target_name and graph.graph.has_edge(source_name, target_name):
                    edge_data = graph.graph[source_name][target_name]
                    connections.append({
                        "from": source_name,
                        "to": target_name,
                        "type": edge_data.get('relationship_type', 'unknown'),
                        "strength": edge_data.get('strength', 0.5),
                        "evidence": edge_data.get('evidence', '')
                    })
        
        return connections


class PatternWeaver:
    """The engine that weaves OSS capabilities into patterns."""
    
    def __init__(self, graph: SemanticGraph):
        self.graph = graph
        self.patterns: List[Pattern] = []
        
    def weave_for_intent(self, intent: Intent) -> List[Pattern]:
        """Weave patterns based on user intent."""
        self.patterns = []
        
        # Get all projects that match required capabilities
        matching_projects = self._get_matching_projects(intent)
        
        if not matching_projects:
            return self.patterns
            
        # Check for domain-specific patterns based on intent description
        intent_lower = intent.description.lower()
        
        # CMS Pattern Detection
        if any(keyword in intent_lower for keyword in ['cms', 'content management', 'content publishing', 'blog', 'article']):
            self._generate_cms_pattern(intent, matching_projects)
        
        # E-commerce Pattern Detection  
        elif any(keyword in intent_lower for keyword in ['e-commerce', 'ecommerce', 'shop', 'store', 'cart', 'checkout']):
            self._generate_ecommerce_pattern(intent, matching_projects)
        
        # Analytics Pattern Detection
        elif any(keyword in intent_lower for keyword in ['analytics', 'dashboard', 'metrics', 'reporting', 'visualization']):
            self._generate_analytics_pattern(intent, matching_projects)
        
        # Generic patterns if no domain detected or if we need more options
        self._generate_capability_patterns(intent, matching_projects)
        
        # Sort patterns by confidence (highest first)
        self.patterns.sort(key=lambda p: p.confidence, reverse=True)
        
        return self.patterns
        
    def _get_matching_projects(self, intent: Intent) -> Dict[CapabilityType, List[OSSProject]]:
        """Get projects matching each required capability."""
        matching = {}
        
        for capability in intent.required_capabilities:
            project_names = self.graph.find_by_capability(capability)
            projects = []
            for name in project_names:
                proj = self.graph.projects.get(name)
                if proj:
                    projects.append(proj)
            
            if projects:
                # Sort by popularity
                projects.sort(key=lambda p: p.popularity_score, reverse=True)
                matching[capability] = projects
                
        return matching
    
    def _generate_cms_pattern(self, intent: Intent, matching_projects: Dict[CapabilityType, List[OSSProject]]) -> None:
        """Generate CMS-specific patterns."""
        if (CapabilityType.WEB_FRAMEWORK in matching_projects and 
            CapabilityType.DATABASE in matching_projects):
            
            web_projs = matching_projects[CapabilityType.WEB_FRAMEWORK]
            db_projs = matching_projects[CapabilityType.DATABASE]
            
            # Try to find Django (best for CMS) or FastAPI
            django = next((p for p in web_projs if p.name == "Django"), None)
            fastapi = next((p for p in web_projs if p.name == "FastAPI"), None)
            web_framework = django or fastapi or (web_projs[0] if web_projs else None)
            
            # Find PostgreSQL (best for CMS)
            postgres = next((p for p in db_projs if p.name == "PostgreSQL"), None)
            database = postgres or (db_projs[0] if db_projs else None)
            
            if web_framework and database:
                # CMS Pattern 1: Full Featured CMS
                pattern = Pattern(
                    name="Modern Content Management System",
                description="Complete CMS with authentication, media storage, and search",
                intent=intent  # ADD THIS LINE
            )           
                
                pattern.add_component(web_framework, "CMS Framework")
                pattern.add_component(database, "Content Database")
                
                # Add authentication if available
                if CapabilityType.AUTHENTICATION in matching_projects:
                    auth_projs = matching_projects[CapabilityType.AUTHENTICATION]
                    if auth_projs:
                        pattern.add_component(auth_projs[0], "Authentication & User Management")
                
                # Add storage if available
                if CapabilityType.STORAGE in matching_projects:
                    storage_projs = matching_projects[CapabilityType.STORAGE]
                    if storage_projs:
                        pattern.add_component(storage_projs[0], "Media & File Storage")
                
                # Add search if available
                if CapabilityType.SEARCH in matching_projects:
                    search_projs = matching_projects[CapabilityType.SEARCH]
                    if search_projs:
                        pattern.add_component(search_projs[0], "Content Search Engine")
                
                # Add cache (important for CMS performance)
                if CapabilityType.CACHE in matching_projects:
                    cache_projs = matching_projects[CapabilityType.CACHE]
                    redis = next((p for p in cache_projs if p.name == "Redis"), None)
                    if redis:
                        pattern.add_component(redis, "Content Cache")
                
                pattern.tags = ["cms", "content", "publishing", "media"]
                self.patterns.append(pattern)
    
    def _generate_ecommerce_pattern(self, intent: Intent, matching_projects: Dict[CapabilityType, List[OSSProject]]) -> None:
        """Generate e-commerce specific patterns."""
        if (CapabilityType.WEB_FRAMEWORK in matching_projects and 
            CapabilityType.DATABASE in matching_projects):
            
            # E-commerce needs: web framework, database, cache, message queue, monitoring
            pattern = Pattern(
                name="E-commerce Platform",
                description="Scalable online store with inventory, cart, orders, and payments",
                intent=intent
            )
            
            # Add web framework
            web_projs = matching_projects[CapabilityType.WEB_FRAMEWORK]
            if web_projs:
                pattern.add_component(web_projs[0], "Store Frontend & API")
            
            # Add database
            db_projs = matching_projects[CapabilityType.DATABASE]
            if db_projs:
                pattern.add_component(db_projs[0], "Product & Order Database")
            
            # Add cache (for sessions and product catalog)
            if CapabilityType.CACHE in matching_projects:
                cache_projs = matching_projects[CapabilityType.CACHE]
                if cache_projs:
                    pattern.add_component(cache_projs[0], "Session & Catalog Cache")
            
            # Add message queue (for order processing)
            if CapabilityType.MESSAGE_QUEUE in matching_projects:
                mq_projs = matching_projects[CapabilityType.MESSAGE_QUEUE]
                if mq_projs:
                    pattern.add_component(mq_projs[0], "Order Processing Queue")
            
            # Add monitoring
            if CapabilityType.MONITORING in matching_projects:
                monitor_projs = matching_projects[CapabilityType.MONITORING]
                if monitor_projs:
                    pattern.add_component(monitor_projs[0], "Store Analytics")
            
            pattern.tags = ["ecommerce", "store", "retail", "payments"]
            self.patterns.append(pattern)
    
    def _generate_analytics_pattern(self, intent: Intent, matching_projects: Dict[CapabilityType, List[OSSProject]]) -> None:
        """Generate analytics/dashboard specific patterns."""
        # Analytics Pattern
        pattern = Pattern(
            name="Real-time Analytics Dashboard",
            description="Data processing pipeline with visualization and monitoring",
            intent=intent
        )
        
        # Add message queue for data ingestion
        if CapabilityType.MESSAGE_QUEUE in matching_projects:
            mq_projs = matching_projects[CapabilityType.MESSAGE_QUEUE]
            kafka = next((p for p in mq_projs if p.name == "Kafka"), None)
            if kafka:
                pattern.add_component(kafka, "Data Ingestion Pipeline")
        
        # Add database
        if CapabilityType.DATABASE in matching_projects:
            db_projs = matching_projects[CapabilityType.DATABASE]
            # Prefer MongoDB for analytics if available
            mongodb = next((p for p in db_projs if p.name == "MongoDB"), None)
            database = mongodb or (db_projs[0] if db_projs else None)
            if database:
                pattern.add_component(database, "Analytics Data Store")
        
        # Add monitoring/visualization
        if CapabilityType.MONITORING in matching_projects:
            monitor_projs = matching_projects[CapabilityType.MONITORING]
            grafana = next((p for p in monitor_projs if p.name == "Grafana"), None)
            if grafana:
                pattern.add_component(grafana, "Dashboard & Visualization")
        
        pattern.tags = ["analytics", "dashboard", "metrics", "visualization"]
        self.patterns.append(pattern)
    
    def _generate_capability_patterns(self, intent: Intent, 
                                    matching_projects: Dict[CapabilityType, List[OSSProject]]) -> None:
        """Generate patterns based on capability combinations."""
        
        # Pattern 1: Full Stack Web Application
        if (CapabilityType.WEB_FRAMEWORK in matching_projects and 
            CapabilityType.DATABASE in matching_projects):
            
            web_projs = matching_projects[CapabilityType.WEB_FRAMEWORK]
            db_projs = matching_projects[CapabilityType.DATABASE]
            
            # Try to find FastAPI + PostgreSQL combination
            fastapi = next((p for p in web_projs if p.name == "FastAPI"), None)
            postgres = next((p for p in db_projs if p.name == "PostgreSQL"), None)
            
            if fastapi and postgres:
                pattern = Pattern(
                    name="Full Stack Python API",
                    description="Production-ready web API with PostgreSQL database",
                    intent=intent
                )
                pattern.add_component(fastapi, "API Framework")
                pattern.add_component(postgres, "Primary Database")
                
                # Add cache if requested
                if CapabilityType.CACHE in matching_projects:
                    cache_projs = matching_projects[CapabilityType.CACHE]
                    redis = next((p for p in cache_projs if p.name == "Redis"), None)
                    if redis:
                        pattern.add_component(redis, "Cache & Session Store")
                
                # Add ORM layer if SQLAlchemy available
                sqlalchemy = next((p for p in db_projs if p.name == "SQLAlchemy"), None)
                if sqlalchemy:
                    pattern.add_component(sqlalchemy, "ORM & Data Layer")
                
                pattern.tags = ["production", "python", "api", "database"]
                self.patterns.append(pattern)
        
        # Pattern 2: Minimal Viable Pattern (one component per capability)
        pattern = Pattern(
            name="Minimal Viable Architecture",
            description="Minimal components to satisfy all requirements",
            intent=intent
        )
        
        role_map = {
            CapabilityType.WEB_FRAMEWORK: "Application Framework",
            CapabilityType.DATABASE: "Data Storage",
            CapabilityType.CACHE: "Cache Layer",
            CapabilityType.MESSAGE_QUEUE: "Message Queue",
            CapabilityType.AI_MODEL: "AI/ML Framework",
            CapabilityType.AUTHENTICATION: "Authentication",
            CapabilityType.STORAGE: "File Storage",
            CapabilityType.MONITORING: "Monitoring",
            CapabilityType.SEARCH: "Search Engine",
            CapabilityType.LOAD_BALANCER: "Load Balancer",
            CapabilityType.EMAIL: "Email Service",
            CapabilityType.OBJECT_STORAGE: "Object Storage",
            CapabilityType.PAYMENT: "Payment Processor",
            CapabilityType.CDN: "CDN",
        }
        
        for capability, projects in matching_projects.items():
            if projects:
                role = role_map.get(capability, capability.value.replace('_', ' ').title())
                pattern.add_component(projects[0], role)
        
        if pattern.components:  # Only add if we have components
            pattern.tags = ["minimal", "simple", "beginner"]
            self.patterns.append(pattern)
    
    def get_all_patterns(self) -> List[Dict[str, Any]]:
        """Get all discovered patterns as dictionaries."""
        return [p.to_dict(self.graph) for p in self.patterns]
