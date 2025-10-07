"""Generate user journeys through phases"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from ..models.persona import Persona
from ..models.journey import (
    Journey,
    JourneyPhase,
    JourneyStep,
    JourneyType,
    CompletionStatus
)


class JourneyGenerator:
    """Generate user journeys based on persona and phase configurations"""

    def __init__(
        self,
        journey_type: JourneyType,
        phases_config: List[Dict[str, Any]],
        emotional_states: Dict[str, List[str]]
    ):
        """
        Initialize journey generator

        Args:
            journey_type: Type of journey progression
            phases_config: List of phase configurations
            emotional_states: Emotional progression by persona type
        """
        self.journey_type = journey_type
        self.phases_config = phases_config
        self.emotional_states = emotional_states

        # Build phases
        self.phases = self._build_phases()

    def _build_phases(self) -> List[JourneyPhase]:
        """Build JourneyPhase objects from configuration"""
        phases = []

        for i, config in enumerate(self.phases_config):
            phase = JourneyPhase(
                id=f"phase_{i+1}",
                name=config["name"],
                order=i,
                objectives=config.get("objectives", []),
                emotional_objectives=config.get("emotional_objectives", []),
                data_to_collect=config.get("data_to_collect", []),
                completion_threshold=config.get("completion_threshold", 0.7),
                duration_estimate=config.get("duration_estimate"),
                narrative_prompts=config.get("narrative_prompts", []),
                verification_questions=config.get("verification_questions", [])
            )
            phases.append(phase)

        return phases

    def generate(self, persona: Persona, user_id: str) -> Journey:
        """
        Generate a complete journey for a user

        Args:
            persona: The user's persona
            user_id: User identifier

        Returns:
            Journey instance
        """
        journey = Journey(
            id=str(uuid.uuid4()),
            user_id=user_id,
            persona_type=persona.persona_type,
            journey_type=self.journey_type,
            phases=self.phases,
            started_at=datetime.now() - timedelta(days=random.randint(1, 90))
        )

        # Generate steps based on journey type
        if self.journey_type == JourneyType.TIME_BASED:
            steps = self._generate_time_based_steps(persona, journey)
        elif self.journey_type == JourneyType.SESSION_BASED:
            steps = self._generate_session_based_steps(persona, journey)
        else:  # MILESTONE_BASED
            steps = self._generate_milestone_based_steps(persona, journey)

        for step in steps:
            journey.add_step(step)

        # Set completion if journey is done
        if journey.overall_completion >= 0.9:
            journey.completed_at = journey.last_activity

        return journey

    def _generate_time_based_steps(
        self,
        persona: Persona,
        journey: Journey
    ) -> List[JourneyStep]:
        """Generate steps for time-based journeys (e.g., weekly)"""
        steps = []
        current_time = journey.started_at

        for phase in journey.phases:
            # Get completion threshold for this persona and phase
            threshold = persona.config.completion_thresholds.get(
                phase.name,
                (phase.completion_threshold, phase.completion_threshold)
            )
            completion_prob = random.uniform(threshold[0], threshold[1])

            # Generate steps for this phase
            num_steps = random.randint(3, 10)  # 3-10 steps per phase

            for i in range(num_steps):
                # Determine if step is completed based on persona tendency
                is_completed = random.random() < completion_prob

                step = self._create_step(
                    phase=phase,
                    step_number=i + 1,
                    timestamp=current_time,
                    persona=persona,
                    is_completed=is_completed
                )
                steps.append(step)

                # Advance time (e.g., 7 days for weekly)
                current_time += timedelta(days=7)

                # Potential dropout
                if not is_completed and random.random() < 0.1:
                    break

        return steps

    def _generate_session_based_steps(
        self,
        persona: Persona,
        journey: Journey
    ) -> List[JourneyStep]:
        """Generate steps for session-based journeys"""
        steps = []
        current_time = journey.started_at

        total_sessions = random.randint(5, 20)  # Variable session count

        for session_num in range(total_sessions):
            # Pick a phase (could be random or sequential)
            phase_idx = min(session_num // 3, len(journey.phases) - 1)
            phase = journey.phases[phase_idx]

            # Create session step
            step = self._create_step(
                phase=phase,
                step_number=session_num + 1,
                timestamp=current_time,
                persona=persona,
                is_completed=random.random() < persona.engagement_level
            )
            steps.append(step)

            # Sessions happen at irregular intervals
            current_time += timedelta(days=random.randint(1, 14))

        return steps

    def _generate_milestone_based_steps(
        self,
        persona: Persona,
        journey: Journey
    ) -> List[JourneyStep]:
        """Generate steps for milestone-based journeys"""
        steps = []
        current_time = journey.started_at

        for phase in journey.phases:
            # Generate steps until milestone is reached
            milestone_reached = False
            step_count = 0

            while not milestone_reached and step_count < 10:
                step = self._create_step(
                    phase=phase,
                    step_number=step_count + 1,
                    timestamp=current_time,
                    persona=persona,
                    is_completed=random.random() < persona.engagement_level
                )
                steps.append(step)

                # Check if milestone reached
                milestone_reached = (
                    step.completion_status == CompletionStatus.COMPLETED
                    and random.random() < 0.3
                )

                step_count += 1
                current_time += timedelta(days=random.randint(1, 7))

        return steps

    def _create_step(
        self,
        phase: JourneyPhase,
        step_number: int,
        timestamp: datetime,
        persona: Persona,
        is_completed: bool
    ) -> JourneyStep:
        """Create a single journey step"""

        # Determine emotional state
        # Get emotional states for this persona and phase
        persona_emotions = self.emotional_states.get(
            persona.persona_type,
            {}
        )
        phase_emotions = persona_emotions.get(
            phase.name,
            ["neutral", "engaged", "motivated"]
        )
        emotional_state = random.choice(phase_emotions)

        # Generate actions
        actions = random.sample(
            phase.objectives,
            min(len(phase.objectives), random.randint(1, 3))
        )

        # Completion status
        if is_completed:
            status = CompletionStatus.COMPLETED
        elif random.random() < 0.1:
            status = CompletionStatus.ABANDONED
        else:
            status = CompletionStatus.IN_PROGRESS

        # Time investment (minutes)
        base_time = 15
        time_invested = int(random.gauss(base_time, base_time / 3))
        time_invested = max(5, min(time_invested, 60))

        # Engagement score
        engagement_score = persona.engagement_level * random.uniform(0.7, 1.0)

        # Collect data
        data_captured = {}
        for field in random.sample(
            phase.data_to_collect,
            min(len(phase.data_to_collect), random.randint(1, len(phase.data_to_collect)))
        ):
            data_captured[field] = f"generated_{field}_value"

        return JourneyStep(
            id=str(uuid.uuid4()),
            phase_id=phase.id,
            step_number=step_number,
            timestamp=timestamp,
            actions=actions,
            emotional_state=emotional_state,
            completion_status=status,
            data_captured=data_captured,
            time_invested=time_invested,
            engagement_score=engagement_score
        )
