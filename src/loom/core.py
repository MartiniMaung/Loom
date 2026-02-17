"""
Core data models for Loom Pattern Weaver.
"""
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

"""
Core data models for Loom
"""
from dataclasses import dataclass, field  # Add this line
from enum import Enum
from typing import List, Optional, Dict, Any


class CapabilityType(str, Enum):
    """Types of capabilities an OSS project can provide"""

    # ... existing capabilities ...
    PAYMENT = "payment"  # Add this
    BILLING = "billing"  # Add this too
    SUBSCRIPTION = "subscription"
    INVOICING = "invoicing"

    # ... existing capabilities ...
    EMAIL = "email"  # Add this
    NOTIFICATION = "notification"  # Add this too
    SMS = "sms"
    PUSH = "push"


    # ... existing capabilities ...
    LOAD_BALANCER = "load_balancer"  # Add this
    REVERSE_PROXY = "reverse_proxy"  # Add this too
    CDN = "cdn"

    # Web & API
    WEB_FRAMEWORK = "web_framework"
    API_GATEWAY = "api_gateway"
    GRAPHQL = "graphql"
    
    # Data Storage
    DATABASE = "database"
    CACHE = "cache"
    STORAGE = "storage"
    OBJECT_STORAGE = "object_storage"
    SEARCH = "search"  # Add this
    DATA_WAREHOUSE = "data_warehouse"
    
    # Messaging & Streaming
    MESSAGE_QUEUE = "message_queue"
    STREAMING = "streaming"
    EVENT_BUS = "event_bus"
    
    # Security & Identity
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    SECRETS = "secrets"
    HIGH_SECURITY = "high_security"
    
    # Observability
    MONITORING = "monitoring"
    LOGGING = "logging"
    TRACING = "tracing"
    METRICS = "metrics"
    
    # AI/ML
    AI_MODEL = "ai_model"
    ML_FRAMEWORK = "ml_framework"
    ML_PLATFORM = "ml_platform"
    VECTOR_DB = "vector_db"
    
    # Infrastructure
    CONTAINER = "container"
    ORCHESTRATION = "orchestration"
    SERVICE_MESH = "service_mesh"
    INFRASTRUCTURE = "infrastructure"
    CI_CD = "ci_cd"
    
    # Frontend
    FRONTEND = "frontend"
    UI_FRAMEWORK = "ui_framework"
    MOBILE = "mobile"
    
    # Integration
    MESSAGE_BROKER = "message_broker"
    ESB = "esb"
    WORKFLOW = "workflow"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive lookup"""
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member
        return None

     
@dataclass
class OSSProject:
    """Open Source Software Project"""
    name: str
    description: str = ""
    capabilities: List[CapabilityType] = field(default_factory=list)
    github_url: Optional[str] = None
    license: Optional[str] = None
    security_score: float = 0.5
    popularity_score: float = 0.5
    compatibility_tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Add this line
    # New fields for multi-objective scoring
    cost_score: float = 0.5
    complexity_score: float = 0.5
    maturity_score: float = 0.5
    license_risk_score: float = 0.5
    
    def __post_init__(self):
        # Convert string capabilities to enum
        if self.capabilities and isinstance(self.capabilities[0], str):
            self.capabilities = [CapabilityType(c) for c in self.capabilities]

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
