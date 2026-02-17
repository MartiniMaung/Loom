"""
Core data models for Loom Pattern Weaver.
"""
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class CapabilityType(str, Enum):
    """Types of capabilities that OSS projects provide."""
    DATABASE = "database"
    WEB_FRAMEWORK = "web_framework"
    AI_MODEL = "ai_model"
    MESSAGE_QUEUE = "message_queue"
    CACHE = "cache"
    AUTHENTICATION = "authentication"
    STORAGE = "storage"
    MONITORING = "monitoring"
    SEARCH = "search"
    OBJECT_STORAGE = "object_storage"
    LOAD_BALANCER = "load_balancer"
    PAYMENT = "payment"
    CDN = "cdn"
    EMAIL = "email"
    OTHER = "other"
    HIGH_SECURITY = "high_security"

class OSSProject(BaseModel):
    """Represents an Open Source Software project."""
    name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Brief description")
    github_url: Optional[str] = Field(None, description="GitHub repository URL")
    capabilities: List[CapabilityType] = Field(default_factory=list, description="What this project can do")
    license: Optional[str] = Field(None, description="License type (MIT, Apache, GPL, etc.)")
    popularity_score: float = Field(0.0, description="Popularity metric (0-1)")
    security_score: float = Field(0.5, description="Security rating (0-1), default 0.5")
    compatibility_tags: List[str] = Field(default_factory=list, description="Tags for compatibility")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RelationshipType(str, Enum):
    """Types of relationships between OSS projects."""
    USES = "uses"
    COMPATIBLE_WITH = "compatible_with"
    SIMILAR_TO = "similar_to"
    DEPENDS_ON = "depends_on"
    ALTERNATIVE_TO = "alternative_to"
    EXTENDS = "extends"


class Relationship(BaseModel):
    """Relationship between two OSS projects."""
    source: str = Field(..., description="Source project name")
    target: str = Field(..., description="Target project name")
    relationship_type: RelationshipType = Field(..., description="Type of relationship")
    strength: float = Field(1.0, description="Strength of relationship (0-1)")
    evidence: Optional[str] = Field(None, description="Evidence for this relationship")


class Intent(BaseModel):
    """User's intention/requirement for a system."""
    description: str = Field(..., description="Natural language description")
    required_capabilities: List[CapabilityType] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    priority: str = Field("medium", description="Priority level")
