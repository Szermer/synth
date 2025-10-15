"""User profile model"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class UserProfile:
    """Complete user profile combining persona and journey data"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    persona_type: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    # Core demographics
    name: str = ""
    age: int = 0
    gender: str = ""
    education: str = ""
    location: Optional[str] = None

    # Behavioral attributes
    engagement_level: float = 0.5
    action_tendency: float = 0.5
    anxiety_level: Optional[float] = None

    # Domain-specific attributes
    attributes: Dict[str, Any] = field(default_factory=dict)

    # Journey reference
    journey_id: Optional[str] = None

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert user profile to dictionary"""
        return {
            "id": self.id,
            "persona_type": self.persona_type,
            "created_at": self.created_at.isoformat(),
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "education": self.education,
            "location": self.location,
            "engagement_level": self.engagement_level,
            "action_tendency": self.action_tendency,
            "anxiety_level": self.anxiety_level,
            "attributes": self.attributes,
            "journey_id": self.journey_id,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfile":
        """Create user profile from dictionary"""
        profile = cls()
        for key, value in data.items():
            if key == "created_at" and isinstance(value, str):
                value = datetime.fromisoformat(value)
            if hasattr(profile, key):
                setattr(profile, key, value)
        return profile
