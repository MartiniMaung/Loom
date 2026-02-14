"""
Semantic Graph - The 'Yarn Barn' of Loom.
Stores knowledge about OSS projects and their relationships.
"""
import networkx as nx
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from .core import OSSProject, Relationship, RelationshipType, CapabilityType


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
        """Save graph and projects to disk."""
        # Save graph using pickle
        with open(self.graph_file, 'wb') as f:
            pickle.dump(self.graph, f)
        
        # Save projects as JSON
        projects_data = {
            name: project.dict() for name, project in self.projects.items()
        }
        with open(self.projects_file, 'w') as f:
            json.dump(projects_data, f, indent=2)
    
    def _load(self) -> None:
        """Load graph and projects from disk."""
        try:
            if self.graph_file.exists():
                with open(self.graph_file, 'rb') as f:
                    self.graph = pickle.load(f)
                print(f"📂 Loaded graph from {self.graph_file}")
        except Exception as e:
            print(f"⚠️  Could not load graph: {e}")
            self.graph = nx.DiGraph()
  
        try:
            if self.projects_file.exists():
                with open(self.projects_file, 'r', encoding='utf-8-sig') as f:  # <-- CHANGE HERE
                    projects_data = json.load(f)

                for name, data in projects_data.items():
                    self.projects[name] = OSSProject(**data)
                print(f"📂 Loaded {len(self.projects)} projects from {self.projects_file}")
        except Exception as e:
              print(f"⚠️  Could not load projects: {e}")         
    
    def add_project(self, project: OSSProject) -> None:
        """Add an OSS project to the graph."""
        self.projects[project.name] = project
        self.graph.add_node(
            project.name,
            type="project",
            capabilities=[c.value for c in project.capabilities],
            license=project.license,
            popularity=project.popularity_score,
            metadata=project.metadata
        )
        self._save()
        print(f"✅ Added project: {project.name}")
        
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
        # Get all unique capabilities
        all_capabilities = set()
        for project in self.projects.values():
            all_capabilities.update([c.value for c in project.capabilities])
        
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "projects": len(self.projects),
            "capability_coverage": len(all_capabilities)
        }
        
    def search(self, query: str) -> List[str]:
        """Simple search for projects matching a query."""
        query = query.lower()
        results = []
        for name, project in self.projects.items():
            if (query in name.lower() or 
                query in project.description.lower() or
                any(query in tag.lower() for tag in project.compatibility_tags)):
                results.append(name)
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

