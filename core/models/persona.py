"""Persona data models"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum


class EngagementPattern(Enum):
    """Common engagement patterns across domains"""
    CAUTIOUS = "cautious"
    METHODICAL = "methodical"
    BALANCED = "balanced"
    PROACTIVE = "proactive"
    RESISTANT = "resistant"
    EXPLORATORY = "exploratory"


@dataclass
class PersonaConfig:
    """Configuration for a persona archetype"""

    name: str
    description: str
    distribution: float  # Percentage of total users (0.0-1.0)

    # Demographics
    age_range: Tuple[int, int]
    gender_distribution: Dict[str, float]
    education_distribution: Dict[str, float]

    # Behavioral characteristics
    engagement_pattern: str
    action_tendency: Tuple[float, float]  # Min-max range
    anxiety_level: Optional[Tuple[float, float]] = None

    # Domain-specific attributes (flexible)
    attributes: Dict[str, Any] = field(default_factory=dict)

    # Journey completion thresholds
    completion_thresholds: Dict[str, Tuple[float, float]] = field(default_factory=dict)

    # Emotional states
    emotional_progression: List[str] = field(default_factory=list)

    # Narrative patterns
    narrative_style: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate persona configuration"""
        assert 0.0 <= self.distribution <= 1.0, "Distribution must be between 0 and 1"
        assert self.age_range[0] < self.age_range[1], "Invalid age range"
        assert abs(sum(self.gender_distribution.values()) - 1.0) < 0.01, "Gender distribution must sum to 1"
        assert abs(sum(self.education_distribution.values()) - 1.0) < 0.01, "Education distribution must sum to 1"
        return True


@dataclass
class Persona:
    """An instantiated persona with specific characteristics"""

    id: str
    persona_type: str
    config: PersonaConfig

    # Generated attributes
    age: int
    gender: str
    education: str

    # Behavioral traits
    engagement_level: float
    action_tendency: float
    anxiety_level: Optional[float] = None

    # Domain-specific data
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary"""
        return {
            "id": self.id,
            "persona_type": self.persona_type,
            "age": self.age,
            "gender": self.gender,
            "education": self.education,
            "engagement_level": self.engagement_level,
            "action_tendency": self.action_tendency,
            "anxiety_level": self.anxiety_level,
            "attributes": self.attributes
        }
