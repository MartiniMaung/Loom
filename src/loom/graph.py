"""
Semantic Graph - The 'Yarn Barn' of Loom.
Stores knowledge about OSS projects and their relationships.
"""
import networkx as nx
import json
import logging
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from .core import OSSProject, Relationship, RelationshipType, CapabilityType

# Add this line
logger = logging.getLogger(__name__)

class SemanticGraph:
    """Knowledge graph of OSS projects and their capabilities."""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.graph_file = self.data_dir / "semantic_graph.pkl"
        self.projects_file = self.data_dir / "projects.json"
        
        self.graph = nx.DiGraph()
        self.projects: Dict[str, OSSProject] = {}
        
        # Try to load existing data
        self._load()
        
    def _save(self) -> None:
        """Save graph to JSON file"""
        data = {}
        for name, project in self.projects.items():
            # Convert project to dict using __dict__
            if hasattr(project, '__dict__'):
                project_dict = project.__dict__.copy()
                # Convert capabilities to strings
                if 'capabilities' in project_dict:
                    project_dict['capabilities'] = [
                        c.value if hasattr(c, 'value') else c 
                        for c in project_dict['capabilities']
                    ]
                data[name] = project_dict
            else:
                data[name] = project
        
        # Ensure directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = self.data_dir / "projects.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"💾 Saved {len(self.projects)} projects to {file_path}")       

    def _load(self) -> None:
        """Load projects from JSON file"""
        projects_file = self.data_dir / "projects.json"
        if not projects_file.exists():
            logger.warning(f"Projects file not found: {projects_file}")
            return

        try:
            with open(projects_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            # Handle both dictionary (old) and list (new) formats
            if isinstance(data, dict):
                # Old format: {"ProjectName": {...}}
                for name, proj_data in data.items():
                    try:
                        # Ensure name is in the data
                        if 'name' not in proj_data:
                            proj_data['name'] = name
                        project = OSSProject(**proj_data)
                        self.add_project(project)
                    except Exception as e:
                        logger.error(f"Error loading project {name}: {e}")
            elif isinstance(data, list):
                # New format: [{...}, {...}]
                for proj_data in data:
                    try:
                        if isinstance(proj_data, dict):
                            project = OSSProject(**proj_data)
                            self.add_project(project)
                        else:
                            logger.warning(f"Skipping non-dict project data: {type(proj_data)}")
                    except Exception as e:
                        logger.error(f"Error loading project: {e}")
            else:
                logger.error(f"Unexpected data format: {type(data)}")
                
            logger.info(f"📂 Loaded {len(self.projects)} projects from {projects_file}")
            
        except Exception as e:
            logger.error(f"Failed to load projects: {e}")
    
    def add_project(self, project: OSSProject) -> None:
        """Add a project to the graph."""
        self.projects[project.name] = project
        self._save()
        logger.info(f"✅ Added project: {project.name}")

    def get_project(self, name: str) -> Optional[OSSProject]:
        """Get a project by name (case-insensitive)"""
        # Direct match first
        if name in self.projects:
            return self.projects[name]
        
        # Case-insensitive match
        name_lower = name.lower()
        for proj_name, project in self.projects.items():
            if proj_name.lower() == name_lower:
                return project
        
        return None     
       
    def add_relationship(self, relationship: Relationship) -> None:
        """Add a relationship between two projects."""
        if relationship.source not in self.projects:
            print(f"⚠️  Warning: Source project {relationship.source} not found")
            return
        if relationship.target not in self.projects:
            print(f"⚠️  Warning: Target project {relationship.target} not found")
            return
            
        self.graph.add_edge(
            relationship.source,
            relationship.target,
            relationship_type=relationship.relationship_type.value,
            strength=relationship.strength,
            evidence=relationship.evidence
        )
        self._save()
        print(f"🔗 Added relationship: {relationship.source} -> {relationship.target}")
        
    def find_by_capability(self, capability: CapabilityType) -> List[str]:
        """Find projects that provide a specific capability."""
        matching_projects = []
        for name, project in self.projects.items():
            if capability in project.capabilities:
                matching_projects.append(name)
        return matching_projects
        
    def get_compatible_projects(self, project_name: str) -> List[str]:
        """Get projects that are compatible with a given project."""
        if project_name not in self.graph:
            return []
            
        compatible = []
        for _, target, data in self.graph.edges(project_name, data=True):
            if data.get("relationship_type") == RelationshipType.COMPATIBLE_WITH.value:
                compatible.append(target)
        return compatible
        
    def find_alternatives(self, project_name: str) -> List[str]:
        """Find alternative projects to a given project."""
        if project_name not in self.graph:
            return []
            
        alternatives = []
        for _, target, data in self.graph.edges(project_name, data=True):
            if data.get("relationship_type") == RelationshipType.ALTERNATIVE_TO.value:
                alternatives.append(target)
        return alternatives
 
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the graph."""
        stats = {
            'projects': len(self.projects),
            'capability_coverage': 0,
            'nodes': len(self.projects),
            'edges': 0  # We don't track edges in current implementation
        }
        
        # Count unique capabilities
        all_caps = set()
        for project in self.projects.values():
            for cap in project.capabilities:
                all_caps.add(cap.value)
        stats['capability_coverage'] = len(all_caps)
        
        return stats   
      
    def search(self, query: str) -> List[tuple[OSSProject, float]]:
        """
        Search for projects by name, description, or tags.
        
        Returns:
            List of tuples (project, score) where score is match relevance
        """
        results = []
        query = query.lower()
        
        for project in self.projects.values():
            score = 0.0
            
            # Name match (highest weight)
            if query in project.name.lower():
                score += 0.5
            
            # Description match
            if project.description and query in project.description.lower():
                score += 0.3
            
            # Capabilities match
            for cap in project.capabilities:
                if query in cap.value.lower():
                    score += 0.2
                    break
            
            if score > 0:
                results.append((project, score))
        
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results 
        
    def clear(self) -> None:
        """Clear all data from the graph."""
        self.graph = nx.DiGraph()
        self.projects = {}
        if self.graph_file.exists():
            self.graph_file.unlink()
        if self.projects_file.exists():
            self.projects_file.unlink()
        print("🧹 Graph cleared!")

    def get_all_projects(self) -> List[OSSProject]:
        """Get all projects in the graph."""
        return list(self.projects.values())

