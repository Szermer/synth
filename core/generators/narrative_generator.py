"""Generate narrative responses for user journeys"""

import random
from typing import Dict, List, Any, Optional
from faker import Faker

from ..models.persona import Persona
from ..models.journey import JourneyStep


class NarrativeGenerator:
    """Generate realistic narrative responses based on persona"""

    def __init__(self, narrative_patterns: Dict[str, Dict[str, Any]]):
        """
        Initialize narrative generator

        Args:
            narrative_patterns: Narrative patterns by persona type
        """
        self.patterns = narrative_patterns
        self.fake = Faker()

    def generate_response(
        self,
        persona: Persona,
        step: JourneyStep,
        prompt: str
    ) -> str:
        """
        Generate a narrative response for a journey step

        Args:
            persona: User's persona
            step: Current journey step
            prompt: The prompt/question being responded to

        Returns:
            Generated narrative response
        """
        pattern = self.patterns.get(persona.persona_type, {})

        # Get response style
        style = pattern.get("response_style", "neutral")
        detail_level = pattern.get("detail_level", "moderate")

        # Generate response based on style and detail level
        response = self._generate_styled_response(
            style=style,
            detail_level=detail_level,
            emotional_state=step.emotional_state,
            prompt=prompt
        )

        # Add persona-specific markers
        response = self._add_persona_markers(response, persona, pattern)

        return response

    def _generate_styled_response(
        self,
        style: str,
        detail_level: str,
        emotional_state: str,
        prompt: str
    ) -> str:
        """Generate response based on style and detail level"""

        # Base response templates
        templates = {
            "analytical_personal": [
                "Based on my experience, {detail}. I've noticed that {observation}.",
                "From a technical perspective, {detail}. Personally, {observation}.",
            ],
            "cautious_gradual": [
                "I think {detail}. I'm not entirely sure, but {observation}.",
                "Maybe {detail}. It's hard to say, but {observation}.",
            ],
            "organized_comprehensive": [
                "Let me break this down systematically: {detail}. In terms of timeline, {observation}.",
                "First, {detail}. Second, {observation}. This follows my usual approach.",
            ],
            "reflective_holistic": [
                "When I consider this holistically, {detail}. In the broader context, {observation}.",
                "This connects to {detail}. Looking at the bigger picture, {observation}.",
            ],
            "learning_engaged": [
                "I'm still learning about this, but {detail}. From what I understand, {observation}.",
                "This is new to me, and {detail}. I'd like to understand more about {observation}.",
            ]
        }

        template = random.choice(templates.get(style, templates["analytical_personal"]))

        # Generate detail and observation based on detail level
        if detail_level == "brief":
            detail = self.fake.sentence(nb_words=6)
            observation = self.fake.sentence(nb_words=6)
        elif detail_level == "moderate":
            detail = self.fake.sentence(nb_words=12)
            observation = self.fake.sentence(nb_words=12)
        else:  # comprehensive
            detail = " ".join([self.fake.sentence() for _ in range(2)])
            observation = " ".join([self.fake.sentence() for _ in range(2)])

        response = template.format(detail=detail, observation=observation)

        # Add emotional coloring
        if "anxious" in emotional_state.lower():
            response += " I'm a bit concerned about this."
        elif "confident" in emotional_state.lower():
            response += " I feel good about this direction."
        elif "frustrated" in emotional_state.lower():
            response += " This has been challenging."

        return response

    def _add_persona_markers(
        self,
        response: str,
        persona: Persona,
        pattern: Dict[str, Any]
    ) -> str:
        """Add persona-specific linguistic markers"""

        markers = pattern.get("linguistic_markers", [])

        # Add markers with low probability to keep it natural
        if markers and random.random() < 0.3:
            marker = random.choice(markers)
            # Insert marker at random position
            words = response.split()
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, marker)
            response = " ".join(words)

        return response

    def generate_multiple_responses(
        self,
        persona: Persona,
        step: JourneyStep,
        prompts: List[str]
    ) -> Dict[str, str]:
        """Generate multiple narrative responses for different prompts"""

        responses = {}
        for prompt in prompts:
            response = self.generate_response(persona, step, prompt)
            responses[prompt] = response

        return responses
