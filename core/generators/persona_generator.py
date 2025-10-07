"""Generate persona instances from configurations"""

import random
import uuid
from typing import Dict, List, Any, Tuple
from faker import Faker

from ..models.persona import Persona, PersonaConfig


class PersonaGenerator:
    """Generate persona instances based on configurations with correlation matrices"""

    # Correlation coefficients from Synthetic User Generation Framework
    CORRELATIONS = {
        'age': {
            'years_experience': 0.85,  # Strong positive
            'tech_comfort': -0.3,      # Moderate negative
            'retirement_urgency': 0.6   # Moderate positive
        },
        'tech_comfort': {
            'ai_attitude': 0.7,        # Strong positive
            'feature_adoption': 0.8,    # Strong positive
            'documentation_volume': 0.4 # Moderate positive
        },
        'department_size': {
            'budget_authority': 0.5,    # Moderate positive
            'knowledge_complexity': 0.3,
            'collaboration_needs': 0.7
        }
    }

    # Engagement stratification: 20% high, 60% standard, 20% low
    ENGAGEMENT_LEVELS = {
        'high': 0.20,
        'standard': 0.60,
        'low': 0.20
    }

    # Knowledge capture behaviors
    CAPTURE_BEHAVIORS = {
        'systematic': 0.25,
        'opportunistic': 0.35,
        'crisis_driven': 0.25,
        'experimental': 0.15
    }

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
        """Generate a single persona instance with correlations"""

        # Generate demographics
        age = random.randint(config.age_range[0], config.age_range[1])
        gender = self._weighted_choice(config.gender_distribution)
        education = self._weighted_choice(config.education_distribution)

        # Generate tech_comfort (needed for correlations)
        tech_comfort_range = config.tech_comfort if hasattr(config, 'tech_comfort') and config.tech_comfort else [0.5, 0.8]
        tech_comfort = random.uniform(tech_comfort_range[0], tech_comfort_range[1])

        # Apply age -> tech_comfort correlation (negative)
        age_normalized = (age - config.age_range[0]) / (config.age_range[1] - config.age_range[0])
        tech_comfort = self._apply_correlation(tech_comfort, age_normalized, -0.3)

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

        # Generate attributes with correlations
        attributes = self._generate_attributes(config, age, tech_comfort)

        # Add engagement stratification
        attributes['engagement_tier'] = self._weighted_choice(self.ENGAGEMENT_LEVELS)

        # Add knowledge capture behavior
        attributes['capture_behavior'] = self._weighted_choice(self.CAPTURE_BEHAVIORS)

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
            attributes=attributes
        )

        return persona

    def _generate_attributes(self, config: PersonaConfig, age: int, tech_comfort: float) -> Dict[str, Any]:
        """Generate domain-specific attributes from config with correlations"""
        attributes = {}

        # Copy over any default attributes from config
        if config.attributes:
            for key, value in config.attributes.items():
                # Handle distribution-based attributes (e.g., career_stage_distribution)
                if key.endswith('_distribution') and isinstance(value, dict):
                    # Get the base attribute name (remove _distribution suffix)
                    base_key = key.replace('_distribution', '')
                    # Use weighted choice for the distribution
                    attributes[base_key] = self._weighted_choice(value)
                    continue

                # Handle range values
                if isinstance(value, tuple) and len(value) == 2:
                    # Apply correlations if relevant
                    if key == 'years_experience' or key.endswith('_experience_years'):
                        # Correlate with age (0.85)
                        age_range = config.age_range
                        age_normalized = (age - age_range[0]) / (age_range[1] - age_range[0])
                        base_value = random.uniform(value[0], value[1])
                        attributes[key] = int(self._apply_correlation(base_value, age_normalized, 0.85))
                    elif key == 'retirement_timeline' or key == 'years_until_retirement':
                        # Correlate with age (negative - older = less time)
                        age_range = config.age_range
                        age_normalized = (age - age_range[0]) / (age_range[1] - age_range[0])
                        base_value = random.uniform(value[0], value[1])
                        attributes[key] = int(self._apply_correlation(base_value, 1 - age_normalized, 0.6))
                    else:
                        # No correlation - random in range
                        if isinstance(value[0], int):
                            attributes[key] = random.randint(value[0], value[1])
                        else:
                            attributes[key] = random.uniform(value[0], value[1])

                elif isinstance(value, list):
                    # List of options - pick one (unless it has a distribution)
                    if f"{key}_distribution" not in config.attributes:
                        attributes[key] = random.choice(value)

                else:
                    # Fixed value
                    attributes[key] = value

        # Add tech_comfort to attributes
        attributes['tech_comfort'] = tech_comfort

        # Generate AI attitude based on tech_comfort correlation (0.7)
        if 'ai_attitude' in config.attributes and isinstance(config.attributes['ai_attitude'], list):
            # Higher tech comfort = more positive AI attitude
            ai_attitudes = config.attributes['ai_attitude']
            if tech_comfort > 0.7:
                # Bias toward enthusiastic/pragmatic
                weights = [3 if att in ['enthusiastic', 'pragmatic'] else 1 for att in ai_attitudes]
            elif tech_comfort < 0.4:
                # Bias toward skeptical/cautious
                weights = [3 if att in ['skeptical', 'cautious', 'fearful'] else 1 for att in ai_attitudes]
            else:
                # Neutral
                weights = [1] * len(ai_attitudes)

            attributes['ai_attitude'] = random.choices(ai_attitudes, weights=weights)[0]

        return attributes

    def _apply_correlation(self, base_value: float, driver_normalized: float, correlation: float) -> float:
        """
        Apply correlation between two variables

        Args:
            base_value: The base random value
            driver_normalized: The driving variable (0-1 normalized)
            correlation: Correlation coefficient (-1 to 1)

        Returns:
            Adjusted value incorporating correlation
        """
        # Blend the base random value with the correlated value
        # correlation of 0 = pure random, correlation of 1 = fully driven
        correlation_strength = abs(correlation)

        if correlation > 0:
            # Positive correlation
            correlated_value = base_value * (1 - correlation_strength) + driver_normalized * correlation_strength
        else:
            # Negative correlation
            correlated_value = base_value * (1 - correlation_strength) + (1 - driver_normalized) * correlation_strength

        # Clamp to 0-1 range
        return max(0.0, min(1.0, correlated_value))

    def _weighted_choice(self, distribution: Dict[str, float]) -> str:
        """Make a weighted random choice from distribution"""
        choices = list(distribution.keys())
        weights = list(distribution.values())
        return random.choices(choices, weights=weights)[0]
