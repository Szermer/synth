"""Generate user journeys through phases"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from ..models.persona import Persona
from ..models.journey import (
    Journey,
    JourneyPhase,
    JourneyStep,
    JourneyType,
    CompletionStatus
)

try:
    from .ssr_response_generator import SSRResponseGenerator
    SSR_AVAILABLE = True
except ImportError:
    SSR_AVAILABLE = False


class JourneyGenerator:
    """Generate user journeys based on persona and phase configurations"""

    def __init__(
        self,
        journey_type: JourneyType,
        phases_config: List[Dict[str, Any]],
        emotional_states: Dict[str, List[str]],
        ssr_config_path: Optional[str] = None,
        enable_ssr: bool = False
    ):
        """
        Initialize journey generator

        Args:
            journey_type: Type of journey progression
            phases_config: List of phase configurations
            emotional_states: Emotional progression by persona type
            ssr_config_path: Path to SSR response scales YAML (optional)
            enable_ssr: Whether to generate SSR-based responses (requires ssr_config_path)
        """
        self.journey_type = journey_type
        self.phases_config = phases_config
        self.emotional_states = emotional_states

        # Build phases
        self.phases = self._build_phases()

        # Initialize SSR generator if requested
        self.ssr_generator = None
        self.ssr_enabled = enable_ssr and SSR_AVAILABLE

        if enable_ssr:
            if not SSR_AVAILABLE:
                raise ImportError(
                    "SSR support requires semantic-similarity-rating package. "
                    "Install with: pip install git+https://github.com/pymc-labs/semantic-similarity-rating.git"
                )
            if not ssr_config_path:
                raise ValueError("ssr_config_path required when enable_ssr=True")

            self.ssr_generator = SSRResponseGenerator(
                reference_config_path=ssr_config_path
            )

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
        """Generate steps for session-based journeys with engagement and behavior patterns"""
        steps = []
        current_time = journey.started_at

        # Get engagement tier and capture behavior from attributes
        engagement_tier = persona.attributes.get('engagement_tier', 'standard')
        capture_behavior = persona.attributes.get('capture_behavior', 'opportunistic')

        # Adjust session count based on engagement tier
        # High: 15-25 sessions, Standard: 10-20, Low: 5-12
        if engagement_tier == 'high':
            total_sessions = random.randint(15, 25)
            completion_boost = 0.2
        elif engagement_tier == 'low':
            total_sessions = random.randint(5, 12)
            completion_boost = -0.2
        else:  # standard
            total_sessions = random.randint(10, 20)
            completion_boost = 0.0

        for session_num in range(total_sessions):
            # Pick a phase (could be random or sequential)
            phase_idx = min(session_num // 3, len(journey.phases) - 1)
            phase = journey.phases[phase_idx]

            # Determine completion based on engagement level + tier
            completion_prob = min(0.95, max(0.1, persona.engagement_level + completion_boost))
            is_completed = random.random() < completion_prob

            # Create session step
            step = self._create_step(
                phase=phase,
                step_number=session_num + 1,
                timestamp=current_time,
                persona=persona,
                is_completed=is_completed
            )
            steps.append(step)

            # Interval between sessions depends on capture behavior
            if capture_behavior == 'systematic':
                # Regular scheduled intervals (2-7 days)
                interval_days = random.randint(2, 7)
            elif capture_behavior == 'opportunistic':
                # Variable intervals (1-14 days)
                interval_days = random.randint(1, 14)
            elif capture_behavior == 'crisis_driven':
                # Bursty patterns - clusters with gaps
                if session_num % 5 < 3:
                    # Intense burst (1-3 days)
                    interval_days = random.randint(1, 3)
                else:
                    # Long gap (10-30 days)
                    interval_days = random.randint(10, 30)
            else:  # experimental
                # Very irregular - wide range
                interval_days = random.randint(1, 21)

            current_time += timedelta(days=interval_days)

            # Engagement-tier-based dropout risk
            if engagement_tier == 'low' and session_num > 3:
                # Higher dropout for low engagement users
                if not is_completed and random.random() < 0.15:
                    break

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

        # Generate SSR-based responses if enabled
        ssr_responses = {}
        if self.ssr_enabled and self.ssr_generator:
            ssr_responses = self._generate_ssr_responses(
                persona=persona,
                phase=phase,
                emotional_state=emotional_state,
                engagement_score=engagement_score
            )

        step = JourneyStep(
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

        # Add SSR responses to step if available
        if ssr_responses:
            step.ssr_responses = ssr_responses

        return step

    def _generate_ssr_responses(
        self,
        persona: Persona,
        phase: JourneyPhase,
        emotional_state: str,
        engagement_score: float
    ) -> Dict[str, Any]:
        """
        Generate SSR-based responses for a journey step.

        This creates simulated LLM responses and converts them to realistic
        probability distributions using Semantic Similarity Rating.

        Args:
            persona: User persona
            phase: Current journey phase
            emotional_state: Current emotional state
            engagement_score: Engagement level (0-1)

        Returns:
            Dictionary with SSR response data for multiple scales
        """
        if not self.ssr_generator:
            return {}

        # Create contextual stimulus
        stimulus = f"Phase: {phase.name}, Objectives: {', '.join(phase.objectives[:2])}"

        # Generate simulated LLM responses based on engagement and emotional state
        # In production, these would come from actual LLM calls
        responses = self._simulate_llm_responses(
            persona=persona,
            emotional_state=emotional_state,
            engagement_score=engagement_score
        )

        ssr_data = {}

        # Generate SSR ratings for available scales
        available_scales = ['engagement', 'satisfaction', 'progress', 'relevance']

        for scale_id in available_scales:
            if scale_id not in self.ssr_generator.available_scales:
                continue

            response_text = responses.get(scale_id, responses.get('default', ''))

            try:
                ssr_response = self.ssr_generator.generate_persona_response(
                    persona_config=persona.attributes,
                    stimulus=stimulus,
                    scale_id=scale_id,
                    llm_response=response_text
                )
                ssr_data[scale_id] = ssr_response
            except Exception as e:
                # Silently skip scales that fail
                continue

        return ssr_data

    def _simulate_llm_responses(
        self,
        persona: Persona,
        emotional_state: str,
        engagement_score: float
    ) -> Dict[str, str]:
        """
        Simulate LLM responses based on persona and state.

        In production, replace this with actual LLM API calls.

        Args:
            persona: User persona
            emotional_state: Current emotional state
            engagement_score: Engagement level (0-1)

        Returns:
            Dictionary of simulated responses for different scales
        """
        # Response templates based on engagement level
        if engagement_score > 0.7:
            templates = {
                'engagement': "This is really interesting and relevant to my goals. I'm excited to continue.",
                'satisfaction': "I'm very satisfied with this experience. It's meeting my expectations well.",
                'progress': "I can feel myself making good progress. Things are clicking.",
                'relevance': "This is highly relevant to what I need to learn right now."
            }
        elif engagement_score > 0.4:
            templates = {
                'engagement': "This seems useful. I'll keep going for now.",
                'satisfaction': "It's okay, nothing exceptional but reasonably helpful.",
                'progress': "I'm making some progress, though it's slower than I hoped.",
                'relevance': "Some of this is relevant, though not all of it applies to me."
            }
        else:
            templates = {
                'engagement': "I'm not really feeling engaged with this. It's not what I expected.",
                'satisfaction': "I'm somewhat disappointed. This isn't quite working for me.",
                'progress': "I don't feel like I'm making much progress. It's frustrating.",
                'relevance': "This doesn't seem very relevant to my actual needs."
            }

        # Modify based on emotional state
        if emotional_state in ['frustrated', 'overwhelmed']:
            for key in templates:
                templates[key] = templates[key].replace("I'm", "I'm feeling a bit overwhelmed but I'm")
        elif emotional_state in ['confident', 'motivated']:
            for key in templates:
                templates[key] = templates[key].replace(".", " and I feel confident about it.")

        templates['default'] = templates.get('engagement', '')

        return templates
