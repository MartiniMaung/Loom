"""
Tests for graph.py - Semantic Knowledge Graph
"""
import pytest
import json
from pathlib import Path
from src.loom.graph import SemanticGraph
from src.loom.core import OSSProject, CapabilityType

class TestSemanticGraph:
    """Test the SemanticGraph class"""
    
    def test_graph_initialization(self, test_graph):
        """Test graph initialization"""
        assert test_graph is not None
        assert len(test_graph.get_all_projects()) > 0
    

    def test_get_project(self, test_graph, sample_projects):
        """Test getting a project by name"""
        # Case-sensitive exact match
        project = test_graph.get_project("FastAPI")
        assert project is not None
        assert project.name == "FastAPI"
        
        # Case-insensitive match
        project = test_graph.get_project("fastapi")
        assert project is not None
        assert project.name == "FastAPI"
        
        # Non-existent project
        project = test_graph.get_project("NonExistent")
        assert project is None
    
    def test_add_project(self, test_graph):
        """Test adding a project to the graph"""
        # Get initial count
        initial_projects = test_graph.get_all_projects()
        initial_count = len(initial_projects)
        
        new_project = OSSProject(
            name="NewProject",
            description="A new test project",
            capabilities=[CapabilityType.MONITORING]
        )
        
        test_graph.add_project(new_project)
        
        # Get new count
        new_projects = test_graph.get_all_projects()
        new_count = len(new_projects)
        
        # Verify count increased by 1
        assert new_count == initial_count + 1
        
        # Verify new project was added
        project_names = [p.name for p in new_projects]
        assert "NewProject" in project_names        

    def test_find_by_capability(self, test_graph):
        """Test finding projects by capability"""
        # Find web frameworks
        web_projects = test_graph.find_by_capability(CapabilityType.WEB_FRAMEWORK)
        assert len(web_projects) >= 2
        assert "FastAPI" in web_projects
        assert "Django" in web_projects
        
        # Find databases
        db_projects = test_graph.find_by_capability(CapabilityType.DATABASE)
        assert len(db_projects) >= 2
        assert "PostgreSQL" in db_projects
        assert "MySQL" in db_projects
        
        # Find non-existent capability
        # Note: This might return empty list or raise exception based on implementation
        try:
            result = test_graph.find_by_capability("nonexistent")
            assert result == [] or result is None
        except (ValueError, AttributeError):
            pass  # Exception is acceptable if that's the design
    
    def test_search(self, test_graph):
        """Test searching projects by query"""
        # Search by name
        results = test_graph.search("Fast")
        assert len(results) > 0
        assert any("FastAPI" in r[0].name for r in results)
        
        # Search by description
        results = test_graph.search("database")
        assert len(results) > 0
        assert any("PostgreSQL" in r[0].name for r in results)
        
        # Search with no matches
        results = test_graph.search("xyzabc123")
        assert results == [] or len(results) == 0
    
    def test_save_and_load(self, test_graph, temp_json_file):
        """Test saving and loading the graph"""
        # Save graph to temp file
        test_graph._save()  # This should save to its default location
        
        # Create new graph and load from same data source
        new_graph = SemanticGraph(data_dir="tests/data")
        new_graph._load()
        
        # Should have same number of projects
        assert len(new_graph.get_all_projects()) == len(test_graph.get_all_projects())
    
   
    def test_get_stats(self, test_graph):
        """Test getting graph statistics"""
        stats = test_graph.get_stats()
    
        assert "projects" in stats  # Changed from 'total_projects'
        assert stats["projects"] >= len(test_graph.get_all_projects())
        assert "capability_coverage" in stats
    
  