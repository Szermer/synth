"""Load project configurations from YAML files"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..models.persona import PersonaConfig
from ..models.journey import JourneyType


class ConfigLoader:
    """Load and parse project configuration files"""

    def __init__(self, project_path: Path):
        """
        Initialize config loader for a project

        Args:
            project_path: Path to project directory
        """
        self.project_path = Path(project_path)

        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")

    def load_config(self) -> Dict[str, Any]:
        """Load main project configuration"""
        config_file = self.project_path / "config.yaml"
        return self._load_yaml(config_file)

    def load_personas(self) -> Dict[str, PersonaConfig]:
        """Load persona configurations"""
        personas_file = self.project_path / "personas.yaml"
        data = self._load_yaml(personas_file)

        personas = {}
        for persona_id, persona_data in data["personas"].items():
            config = self._parse_persona_config(persona_id, persona_data)
            personas[persona_id] = config

        return personas

    def load_journey_phases(self) -> List[Dict[str, Any]]:
        """Load journey phase configurations"""
        phases_file = self.project_path / "journey_phases.yaml"
        data = self._load_yaml(phases_file)
        return data.get("phases", [])

    def load_emotional_states(self) -> Dict[str, List[str]]:
        """Load emotional state progressions"""
        emotions_file = self.project_path / "emotional_states.yaml"
        data = self._load_yaml(emotions_file)
        return data.get("emotional_progressions", {})

    def load_narrative_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load narrative patterns"""
        patterns_file = self.project_path / "narrative_patterns.yaml"
        data = self._load_yaml(patterns_file)
        return data.get("patterns", {})

    def load_data_schema(self) -> Dict[str, Any]:
        """Load data schema configuration"""
        schema_file = self.project_path / "data_schema.yaml"
        return self._load_yaml(schema_file)

    def get_journey_type(self) -> JourneyType:
        """Get journey type from config"""
        config = self.load_config()
        journey_type_str = config.get("journey", {}).get("type", "session_based")

        if journey_type_str == "time_based":
            return JourneyType.TIME_BASED
        elif journey_type_str == "milestone_based":
            return JourneyType.MILESTONE_BASED
        else:
            return JourneyType.SESSION_BASED

    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a YAML file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, 'r') as f:
            return yaml.safe_load(f)

    def _parse_persona_config(
        self,
        persona_id: str,
        data: Dict[str, Any]
    ) -> PersonaConfig:
        """Parse persona data into PersonaConfig"""

        demographics = data.get("demographics", {})
        behavioral = data.get("behavioral", {})
        attributes = data.get("attributes", {})
        completion = data.get("completion_thresholds", {})

        return PersonaConfig(
            name=data["name"],
            description=data["description"],
            distribution=data["distribution"],
            age_range=tuple(demographics.get("age_range", [25, 65])),
            gender_distribution=demographics.get("gender_distribution", {"female": 0.5, "male": 0.5}),
            education_distribution=demographics.get("education_distribution", {"bachelors": 1.0}),
            engagement_pattern=behavioral.get("engagement_pattern", "balanced"),
            action_tendency=tuple(behavioral.get("action_tendency", [0.5, 0.7])),
            anxiety_level=tuple(behavioral.get("anxiety_level")) if behavioral.get("anxiety_level") else None,
            attributes=attributes,
            completion_thresholds=completion,
            emotional_progression=[],  # Will be loaded separately
            narrative_style={}  # Will be loaded separately
        )
