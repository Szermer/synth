"""Generate persona instances from configurations"""

import random
import uuid
from typing import Dict, List, Any
from faker import Faker

from ..models.persona import Persona, PersonaConfig


class PersonaGenerator:
    """Generate persona instances based on configurations"""

    def __init__(self, persona_configs: Dict[str, PersonaConfig]):
        """
        Initialize generator with persona configurations

        Args:
            persona_configs: Dictionary mapping persona type to configuration
        """
        self.configs = persona_configs
        self.fake = Faker()

        # Validate configurations
        total_distribution = sum(config.distribution for config in persona_configs.values())
        assert abs(total_distribution - 1.0) < 0.01, \
            f"Persona distributions must sum to 1.0, got {total_distribution}"

    def generate(self, count: int) -> List[Persona]:
        """
        Generate a list of persona instances

        Args:
            count: Number of personas to generate

        Returns:
            List of Persona instances
        """
        personas = []

        # Calculate distribution
        persona_counts = self._calculate_distribution(count)

        # Generate personas for each type
        for persona_type, target_count in persona_counts.items():
            config = self.configs[persona_type]

            for _ in range(target_count):
                persona = self._generate_single(persona_type, config)
                personas.append(persona)

        # Shuffle to avoid clustering by type
        random.shuffle(personas)

        return personas

    def _calculate_distribution(self, count: int) -> Dict[str, int]:
        """Calculate how many of each persona type to generate"""
        persona_counts = {}
        remaining = count

        # Sort by distribution to handle rounding consistently
        sorted_types = sorted(
            self.configs.items(),
            key=lambda x: x[1].distribution,
            reverse=True
        )

        for i, (persona_type, config) in enumerate(sorted_types):
            if i == len(sorted_types) - 1:
                # Last persona gets remaining count
                persona_counts[persona_type] = remaining
            else:
                target = round(count * config.distribution)
                persona_counts[persona_type] = target
                remaining -= target

        return persona_counts

    def _generate_single(self, persona_type: str, config: PersonaConfig) -> Persona:
        """Generate a single persona instance"""

        # Generate demographics
        age = random.randint(config.age_range[0], config.age_range[1])
        gender = self._weighted_choice(config.gender_distribution)
        education = self._weighted_choice(config.education_distribution)

        # Generate behavioral traits
        engagement_level = random.uniform(
            config.action_tendency[0],
            config.action_tendency[1]
        )
        action_tendency = random.uniform(
            config.action_tendency[0],
            config.action_tendency[1]
        )

        anxiety_level = None
        if config.anxiety_level:
            anxiety_level = random.uniform(
                config.anxiety_level[0],
                config.anxiety_level[1]
            )

        # Create persona instance
        persona = Persona(
            id=str(uuid.uuid4()),
            persona_type=persona_type,
            config=config,
            age=age,
            gender=gender,
            education=education,
            engagement_level=engagement_level,
            action_tendency=action_tendency,
            anxiety_level=anxiety_level,
            attributes=self._generate_attributes(config)
        )

        return persona

    def _generate_attributes(self, config: PersonaConfig) -> Dict[str, Any]:
        """Generate domain-specific attributes from config"""
        attributes = {}

        # Copy over any default attributes from config
        if config.attributes:
            for key, value in config.attributes.items():
                if isinstance(value, tuple) and len(value) == 2:
                    # Range value - pick random value in range
                    attributes[key] = random.uniform(value[0], value[1])
                elif isinstance(value, list):
                    # List of options - pick one
                    attributes[key] = random.choice(value)
                else:
                    # Fixed value
                    attributes[key] = value

        return attributes

    def _weighted_choice(self, distribution: Dict[str, float]) -> str:
        """Make a weighted random choice from distribution"""
        choices = list(distribution.keys())
        weights = list(distribution.values())
        return random.choices(choices, weights=weights)[0]
