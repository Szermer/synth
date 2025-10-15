"""
LLM-based response generation for SSR integration.

This module provides real LLM integration for generating free-text responses
that can be converted to SSR probability distributions.
"""

import os
from typing import Dict, Optional
from anthropic import Anthropic
from dotenv import load_dotenv


class LLMResponseGenerator:
    """
    Generate persona-appropriate free-text responses using LLMs.

    Supports:
    - Anthropic Claude models
    - Persona context injection
    - Scale-specific prompting
    """

    def __init__(self, model: str = "claude-sonnet-4-5-20250929", api_key: Optional[str] = None):
        """
        Initialize LLM response generator.

        Args:
            model: Anthropic model name (default: claude-sonnet-4-5-20250929 - Claude Sonnet 4.5)
            api_key: Anthropic API key (if None, loads from ANTHROPIC_API_KEY env var)
        """
        # Load environment variables
        load_dotenv()

        # Get API key
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No Anthropic API key provided. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )

        self.model = model
        self.client = Anthropic(api_key=self.api_key)

    def generate_response(
        self,
        persona: Dict,
        stimulus: str,
        scale_id: str,
        phase: str,
        emotional_state: str,
        engagement_score: float
    ) -> str:
        """
        Generate a persona-appropriate free-text response to a stimulus.

        Args:
            persona: Persona attributes (age, tech_comfort, etc.)
            stimulus: The prompt/stimulus to respond to
            scale_id: Scale being measured (engagement, satisfaction, etc.)
            phase: Current journey phase name
            emotional_state: Current emotional state
            engagement_score: Engagement level (0-1)

        Returns:
            Free-text response string
        """
        # Build persona context
        persona_context = self._build_persona_context(persona, emotional_state, engagement_score)

        # Build scale-specific prompt
        scale_prompts = {
            "engagement": "How engaging do you find this? Would you want to continue?",
            "satisfaction": "How satisfied are you with this experience so far?",
            "progress": "Do you feel like you're making progress? How is it going?",
            "relevance": "How relevant is this to your goals and needs?",
            "difficulty": "How difficult is this for your current level?",
            "completion": "How likely are you to complete this?",
            "confidence": "How confident do you feel about using what you've learned?",
            "interest": "How interested are you in continuing with similar content?"
        }

        scale_prompt = scale_prompts.get(scale_id, "What are your thoughts on this?")

        # Create system prompt
        system_prompt = f"""You are roleplaying as a realistic user with the following characteristics:

{persona_context}

Current situation:
- Journey Phase: {phase}
- Emotional State: {emotional_state}
- Current Engagement: {engagement_score:.0%}

Generate a natural, authentic response in 1-3 sentences that reflects this persona's perspective.
Be specific and genuine. Avoid generic corporate-speak. Use first person ("I").
"""

        # Create user prompt
        user_prompt = f"""Stimulus: {stimulus}

Question: {scale_prompt}

Respond naturally as the persona described, reflecting your current emotional state and engagement level."""

        # Call Anthropic API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            temperature=0.8,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        # Extract response text
        response_text = message.content[0].text

        return response_text.strip()

    def _build_persona_context(
        self,
        persona: Dict,
        emotional_state: str,
        engagement_score: float
    ) -> str:
        """Build a natural language description of the persona."""

        lines = []

        # Age and demographics
        if "age" in persona:
            lines.append(f"Age: {persona['age']}")

        # Tech comfort
        tech_comfort = persona.get("tech_comfort", 0.5)
        if tech_comfort < 0.3:
            lines.append("Tech comfort: Low (prefers simple interfaces, may feel overwhelmed)")
        elif tech_comfort < 0.7:
            lines.append("Tech comfort: Moderate (comfortable with standard tech)")
        else:
            lines.append("Tech comfort: High (early adopter, embraces new technology)")

        # AI attitude
        ai_attitude = persona.get("ai_attitude", 0.5)
        if ai_attitude < 0.3:
            lines.append("AI attitude: Skeptical (concerns about privacy, prefers human touch)")
        elif ai_attitude < 0.7:
            lines.append("AI attitude: Neutral (pragmatic, will use if helpful)")
        else:
            lines.append("AI attitude: Enthusiastic (excited about AI capabilities)")

        # Domain-specific attributes
        if "medium" in persona:
            lines.append(f"Craft medium: {persona['medium']}")

        if "years_in_craft" in persona:
            years = persona["years_in_craft"]
            if years < 3:
                lines.append(f"Experience: Beginner ({years} years)")
            elif years < 10:
                lines.append(f"Experience: Intermediate ({years} years)")
            else:
                lines.append(f"Experience: Expert ({years} years)")

        # Engagement tendency
        if engagement_score > 0.7:
            lines.append("Current mood: Engaged and motivated")
        elif engagement_score > 0.4:
            lines.append("Current mood: Moderately interested")
        else:
            lines.append("Current mood: Less engaged, somewhat distracted")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"LLMResponseGenerator(model={self.model})"
