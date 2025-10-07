"""Journey and phase models"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class JourneyType(Enum):
    """Type of journey progression"""
    TIME_BASED = "time_based"  # e.g., 10 weeks, daily sessions
    SESSION_BASED = "session_based"  # e.g., each capture session
    MILESTONE_BASED = "milestone_based"  # e.g., achievement-triggered


class CompletionStatus(Enum):
    """Status of a journey phase"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class JourneyPhase:
    """A single phase in a user journey"""

    id: str
    name: str
    order: int

    # Phase configuration
    objectives: List[str]
    emotional_objectives: List[str] = field(default_factory=list)
    data_to_collect: List[str] = field(default_factory=list)

    # Completion criteria
    completion_threshold: float = 0.7
    duration_estimate: Optional[str] = None  # e.g., "1 week", "3 sessions"

    # Phase-specific content
    narrative_prompts: List[str] = field(default_factory=list)
    verification_questions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert phase to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "objectives": self.objectives,
            "emotional_objectives": self.emotional_objectives,
            "data_to_collect": self.data_to_collect,
            "completion_threshold": self.completion_threshold
        }


@dataclass
class JourneyStep:
    """A step within a journey phase (e.g., a single session or week)"""

    id: str
    phase_id: str
    step_number: int
    timestamp: datetime

    # Step data
    actions: List[str]
    emotional_state: str
    completion_status: CompletionStatus

    # Collected data
    data_captured: Dict[str, Any] = field(default_factory=dict)
    narrative_responses: Dict[str, str] = field(default_factory=dict)

    # Engagement metrics
    time_invested: Optional[int] = None  # minutes
    engagement_score: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary"""
        return {
            "id": self.id,
            "phase_id": self.phase_id,
            "step_number": self.step_number,
            "timestamp": self.timestamp.isoformat(),
            "actions": self.actions,
            "emotional_state": self.emotional_state,
            "completion_status": self.completion_status.value,
            "data_captured": self.data_captured,
            "narrative_responses": self.narrative_responses,
            "time_invested": self.time_invested,
            "engagement_score": self.engagement_score
        }


@dataclass
class Journey:
    """Complete user journey through all phases"""

    id: str
    user_id: str
    persona_type: str
    journey_type: JourneyType

    # Journey data
    phases: List[JourneyPhase]
    steps: List[JourneyStep] = field(default_factory=list)

    # Progression tracking
    current_phase: int = 0
    overall_completion: float = 0.0

    # Metadata
    started_at: datetime = field(default_factory=datetime.now)
    last_activity: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def add_step(self, step: JourneyStep) -> None:
        """Add a step to the journey"""
        self.steps.append(step)
        self.last_activity = step.timestamp
        self._update_completion()

    def _update_completion(self) -> None:
        """Calculate overall completion percentage"""
        if not self.steps:
            self.overall_completion = 0.0
            return

        completed_steps = sum(
            1 for step in self.steps
            if step.completion_status == CompletionStatus.COMPLETED
        )
        total_possible = len(self.phases) * 10  # Assume ~10 steps per phase
        self.overall_completion = min(completed_steps / total_possible, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert journey to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "persona_type": self.persona_type,
            "journey_type": self.journey_type.value,
            "phases": [p.to_dict() for p in self.phases],
            "steps": [s.to_dict() for s in self.steps],
            "current_phase": self.current_phase,
            "overall_completion": self.overall_completion,
            "started_at": self.started_at.isoformat(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
