"""
Tests for core data models
"""
import pytest
from src.loom.core import CapabilityType, Intent, OSSProject

class TestCapabilityType:
    """Test capability enum"""
    
    def test_valid_capabilities(self):
        """Test that all expected capabilities exist"""
        assert CapabilityType.WEB_FRAMEWORK.value == "web_framework"
        assert CapabilityType.DATABASE.value == "database"
        assert CapabilityType.MESSAGE_QUEUE.value == "message_queue"
        assert CapabilityType.CACHE.value == "cache"
        assert CapabilityType.AUTHENTICATION.value == "authentication"
        assert CapabilityType.MONITORING.value == "monitoring"
        assert CapabilityType.HIGH_SECURITY.value == "high_security"
    
    def test_from_string(self):
        """Test creating capability from string"""
        assert CapabilityType("web_framework") == CapabilityType.WEB_FRAMEWORK
        assert CapabilityType("DATABASE") == CapabilityType.DATABASE
        
        with pytest.raises(ValueError):
            CapabilityType("invalid_capability")

class TestIntent:
    """Test intent creation and validation"""
    
    def test_create_intent(self):
        """Test basic intent creation"""
        intent = Intent(
            description="Build a web app",
            required_capabilities=[CapabilityType.WEB_FRAMEWORK]
        )
        assert intent.description == "Build a web app"
        assert CapabilityType.WEB_FRAMEWORK in intent.required_capabilities
        assert intent.priority == "medium"  # default
    
    def test_intent_with_priority(self):
        """Test intent with custom priority"""
        intent = Intent(
            description="High priority app",
            required_capabilities=[CapabilityType.DATABASE],
            priority="high"
        )
        assert intent.priority == "high"
    
    def test_intent_with_constraints(self):
        """Test intent with constraints"""
        intent = Intent(
            description="Cost-sensitive app",
            required_capabilities=[CapabilityType.WEB_FRAMEWORK],
            constraints={"max_cost": 0.3}
        )
        assert intent.constraints["max_cost"] == 0.3

class TestOSSProject:
    """Test OSSProject model"""
    
    def test_create_project(self):
        """Test basic project creation"""
        project = OSSProject(
            name="TestProject",
            description="A test project",
            capabilities=[CapabilityType.WEB_FRAMEWORK]
        )
        assert project.name == "TestProject"
        assert project.description == "A test project"
        assert CapabilityType.WEB_FRAMEWORK in project.capabilities
    
    def test_project_defaults(self):
        """Test default values"""
        project = OSSProject(name="DefaultProject")
        assert project.description == ""
        assert project.capabilities == []
        assert project.security_score == 0.5
        assert project.cost_score == 0.5
        assert project.complexity_score == 0.5
        assert project.maturity_score == 0.5
        assert project.license_risk_score == 0.5
    
    def test_project_with_scores(self):
        """Test project with custom scores"""
        project = OSSProject(
            name="ScoredProject",
            security_score=0.9,
            cost_score=0.2,
            complexity_score=0.3,
            maturity_score=0.8,
            license_risk_score=0.1
        )
        assert project.security_score == 0.9
        assert project.cost_score == 0.2
        assert project.complexity_score == 0.3
        assert project.maturity_score == 0.8
        assert project.license_risk_score == 0.1
    
    def test_string_capabilities_conversion(self):
        """Test that string capabilities convert to enum"""
        project = OSSProject(
            name="Converter",
            capabilities=["web_framework", "database"]
        )
        assert all(isinstance(c, CapabilityType) for c in project.capabilities)
        assert CapabilityType.WEB_FRAMEWORK in project.capabilities
        assert CapabilityType.DATABASE in project.capabilities
    
    def test_mixed_capabilities(self):
        """Test mix of enum and string capabilities"""
        project = OSSProject(
            name="Mixed",
            capabilities=[
                CapabilityType.WEB_FRAMEWORK,
                "database",
                CapabilityType.CACHE
            ]
        )
        assert len(project.capabilities) == 3
        assert all(isinstance(c, CapabilityType) for c in project.capabilities)