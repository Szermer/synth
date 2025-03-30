import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any
import json
from pathlib import Path

import faker
from faker.providers import person, address, job, company, date_time

from config.persona_config import (
    PERSONA_DISTRIBUTION,
    PERSONA_TEMPLATES,
    HEALTH_CONDITIONS,
    LIFE_EVENTS,
    LOCATION_TYPES,
    ENGAGEMENT_METRICS,
    BREAST_CANCER_RISKS,
    RACE_ETHNICITY_RISKS,
    PERSONA_CONFIG
)

fake = faker.Faker()
fake.add_provider(person)
fake.add_provider(address)
fake.add_provider(job)
fake.add_provider(company)
fake.add_provider(date_time)


class DataGenerator:
    def __init__(self):
        self.persona_config = PERSONA_CONFIG
        self.set_completion_thresholds()
        self.set_emotional_states()

    def set_completion_thresholds(self) -> None:
        """Set completion thresholds for each persona type."""
        self.completion_thresholds = {
            "health_aware_avoider": {
                "awareness": (0.3, 0.7),
                "engagement": (0.4, 0.7),
                "action": (0.2, 0.5),
                "continuity": (0.1, 0.3)
            },
            "structured_system_seeker": {
                "awareness": (0.6, 0.9),
                "engagement": (0.6, 0.9),
                "action": (0.4, 0.7),
                "continuity": (0.3, 0.6)
            },
            "balanced_life_integrator": {
                "awareness": (0.5, 0.8),
                "engagement": (0.5, 0.8),
                "action": (0.3, 0.6),
                "continuity": (0.2, 0.5)
            },
            "healthcare_professional": {
                "awareness": (0.7, 0.95),
                "engagement": (0.7, 0.95),
                "action": (0.5, 0.8),
                "continuity": (0.4, 0.7)
            },
            "overlooked_risk_group": {
                "awareness": (0.3, 0.6),
                "engagement": (0.3, 0.6),
                "action": (0.2, 0.4),
                "continuity": (0.1, 0.3)
            }
        }

    def set_emotional_states(self) -> None:
        """Set emotional state progressions for each persona type."""
        self.emotional_states = {
            "health_aware_avoider": {
                "awareness": [
                    ["anxious", "concerned", "neutral", "curious"],
                    ["concerned", "neutral", "curious", "attentive"],
                    ["neutral", "curious", "attentive", "engaged"]
                ],
                "engagement": [
                    ["neutral", "curious", "engaged", "motivated"],
                    ["curious", "engaged", "motivated", "reflective"]
                ],
                "action": [
                    ["engaged", "motivated", "determined", "stable"],
                    ["motivated", "determined", "stable", "reflective"]
                ],
                "continuity": [
                    ["motivated", "stable", "reflective", "stable"],
                    ["stable", "reflective", "stable", "reflective"]
                ]
            },
            "structured_system_seeker": {
                "awareness": [
                    ["neutral", "curious", "attentive", "engaged"],
                    ["curious", "attentive", "engaged", "motivated"]
                ],
                "engagement": [
                    ["attentive", "engaged", "motivated", "determined"],
                    ["engaged", "motivated", "determined", "reflective"]
                ],
                "action": [
                    ["motivated", "determined", "stable", "reflective"],
                    ["determined", "stable", "reflective", "stable"]
                ],
                "continuity": [
                    ["stable", "reflective", "stable", "reflective"],
                    ["reflective", "stable", "reflective", "stable"]
                ]
            },
            "balanced_life_integrator": {
                "awareness": [
                    ["neutral", "curious", "attentive", "engaged"],
                    ["curious", "attentive", "engaged", "reflective"]
                ],
                "engagement": [
                    ["attentive", "engaged", "motivated", "reflective"],
                    ["engaged", "motivated", "reflective", "stable"]
                ],
                "action": [
                    ["motivated", "reflective", "stable", "determined"],
                    ["reflective", "stable", "determined", "stable"]
                ],
                "continuity": [
                    ["stable", "reflective", "stable", "reflective"],
                    ["reflective", "stable", "reflective", "stable"]
                ]
            },
            "healthcare_professional": {
                "awareness": [
                    ["neutral", "curious", "attentive", "engaged"],
                    ["curious", "attentive", "engaged", "determined"]
                ],
                "engagement": [
                    ["attentive", "engaged", "determined", "motivated"],
                    ["engaged", "determined", "motivated", "reflective"]
                ],
                "action": [
                    ["determined", "motivated", "stable", "reflective"],
                    ["motivated", "stable", "reflective", "stable"]
                ],
                "continuity": [
                    ["stable", "reflective", "stable", "reflective"],
                    ["reflective", "stable", "reflective", "stable"]
                ]
            },
            "overlooked_risk_group": {
                "awareness": [
                    ["anxious", "concerned", "neutral", "curious"],
                    ["concerned", "neutral", "curious", "neutral"]
                ],
                "engagement": [
                    ["neutral", "curious", "engaged", "neutral"],
                    ["curious", "engaged", "neutral", "engaged"]
                ],
                "action": [
                    ["engaged", "motivated", "neutral", "motivated"],
                    ["motivated", "neutral", "motivated", "stable"]
                ],
                "continuity": [
                    ["motivated", "stable", "neutral", "stable"],
                    ["stable", "neutral", "stable", "neutral"]
                ]
            }
        }

    def get_emotional_state(self, persona_type: str, phase: str, progress: float) -> str:
        """Get emotional state based on persona type, phase and progress."""
        states = self.emotional_states[persona_type][phase]
        progression = random.choice(states)
        
        # Adjust progress based on persona type and phase
        if persona_type == "health_aware_avoider":
            if phase == "awareness":
                # Maintain 50/50 balance
                return random.choice(["anxious", "curious"])
            elif phase == "engagement":
                # Gradual shift from anxiety to engagement
                if progress < 0.3:
                    return random.choice(["concerned", "neutral"])
                else:
                    return random.choice(["engaged", "motivated"])
        elif persona_type == "structured_system_seeker":
            if phase == "awareness":
                # High curiosity and engagement from start
                if random.random() < 0.7:  # 70% chance of curiosity/engagement
                    return random.choice(["curious", "attentive", "engaged"])
                else:
                    return "neutral"
            elif phase == "action":
                # Strong motivation and determination
                return random.choice(["motivated", "determined"])
        elif persona_type == "balanced_life_integrator":
            if phase == "awareness":
                # Low anxiety, moderate curiosity
                if random.random() < 0.2:  # 20% chance of anxiety
                    return "concerned"
                else:
                    return random.choice(["curious", "attentive"])
        elif persona_type == "healthcare_professional":
            if phase == "awareness":
                # Very low anxiety, high curiosity
                if random.random() < 0.1:  # 10% chance of anxiety
                    return "concerned"
                else:
                    return random.choice(["curious", "attentive", "engaged"])
        elif persona_type == "overlooked_risk_group":
            if phase == "awareness":
                # High anxiety, low curiosity
                if random.random() < 0.75:  # 75% chance of anxiety
                    return random.choice(["anxious", "concerned"])
                else:
                    return random.choice(["neutral", "curious"])
        
        # Default progression
        index = min(int(progress * len(progression)), len(progression) - 1)
        return progression[index]

    def calculate_completion_probability(self, persona_type: str, phase: str, step_index: int, total_steps: int) -> float:
        """Calculate completion probability based on persona type and phase."""
        base_threshold = self.completion_thresholds[persona_type][phase]
        progress = step_index / total_steps
        
        # Adjust probability based on persona type and phase
        if persona_type == "health_aware_avoider":
            if phase == "awareness":
                return random.uniform(base_threshold[0] + 0.1, base_threshold[1])
            elif phase == "action":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.1)
            elif phase == "continuity":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.05)
        elif persona_type == "structured_system_seeker":
            if phase == "awareness":
                return random.uniform(base_threshold[0] + 0.1, base_threshold[1])
            elif phase == "engagement":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.1)
            elif phase == "action":
                return random.uniform(base_threshold[0] + 0.1, base_threshold[1])
        elif persona_type == "healthcare_professional":
            if phase == "awareness":
                return random.uniform(base_threshold[0] + 0.1, base_threshold[1])
            elif phase == "engagement":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.15)
            elif phase == "action":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.1)
        elif persona_type == "overlooked_risk_group":
            if phase == "awareness":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.1)
            elif phase == "continuity":
                return random.uniform(base_threshold[0], base_threshold[1] - 0.05)
        
        # Default probability with slight progress-based adjustment
        base_prob = random.uniform(base_threshold[0], base_threshold[1])
        progress_factor = 1.0 - (progress * 0.2)  # Slightly decrease probability as steps progress
        return base_prob * progress_factor

    def generate_awareness_phase(self, persona_type: str, start_time: datetime) -> List[Dict[str, Any]]:
        """Generate awareness phase steps."""
        steps = []
        current_time = start_time
        awareness_steps = [
            "initial_registration",
            "risk_assessment",
            "health_history",
            "initial_preferences"
        ]
        
        for i, step in enumerate(awareness_steps):
            progress = i / len(awareness_steps)
            completion_prob = self.calculate_completion_probability(
                persona_type, "awareness", i, len(awareness_steps)
            )
            completed = random.random() <= completion_prob
            
            steps.append({
                "step": step,
                "timestamp": current_time.isoformat(),
                "emotional_state": self.get_emotional_state(persona_type, "awareness", progress),
                "completion_status": "completed" if completed else "incomplete"
            })
            current_time += timedelta(minutes=random.randint(5, 15))
        
        return steps

    def generate_engagement_phase(self, persona_type: str, start_time: datetime) -> List[Dict[str, Any]]:
        """Generate engagement phase steps."""
        steps = []
        current_time = start_time
        engagement_steps = [
            "narrative_capture",
            "life_events_timeline",
            "support_network",
            "resource_exploration"
        ]
        
        for i, step in enumerate(engagement_steps):
            progress = i / len(engagement_steps)
            completion_prob = self.calculate_completion_probability(
                persona_type, "engagement", i, len(engagement_steps)
            )
            completed = random.random() <= completion_prob
            
            steps.append({
                "step": step,
                "timestamp": current_time.isoformat(),
                "emotional_state": self.get_emotional_state(persona_type, "engagement", progress),
                "completion_status": "completed" if completed else "incomplete"
            })
            current_time += timedelta(minutes=random.randint(10, 30))
        
        return steps

    def generate_action_phase(self, persona_type: str, start_time: datetime) -> List[Dict[str, Any]]:
        """Generate action phase steps."""
        steps = []
        current_time = start_time
        action_steps = [
            "prevention_plan",
            "support_plan",
            "action_planning",
            "resource_commitment"
        ]
        
        for i, step in enumerate(action_steps):
            progress = i / len(action_steps)
            completion_prob = self.calculate_completion_probability(
                persona_type, "action", i, len(action_steps)
            )
            completed = random.random() <= completion_prob
            
            steps.append({
                "step": step,
                "timestamp": current_time.isoformat(),
                "emotional_state": self.get_emotional_state(persona_type, "action", progress),
                "completion_status": "completed" if completed else "incomplete"
            })
            current_time += timedelta(minutes=random.randint(15, 45))
        
        return steps

    def generate_continuity_phase(self, persona_type: str, start_time: datetime) -> List[Dict[str, Any]]:
        """Generate continuity phase steps."""
        steps = []
        current_time = start_time
        continuity_steps = [
            "follow_up",
            "risk_awareness",
            "barrier_identification",
            "long_term_planning"
        ]
        
        for i, step in enumerate(continuity_steps):
            progress = i / len(continuity_steps)
            completion_prob = self.calculate_completion_probability(
                persona_type, "continuity", i, len(continuity_steps)
            )
            completed = random.random() <= completion_prob
            
            steps.append({
                "step": step,
                "timestamp": current_time.isoformat(),
                "emotional_state": self.get_emotional_state(persona_type, "continuity", progress),
                "completion_status": "completed" if completed else "incomplete"
            })
            current_time += timedelta(minutes=random.randint(20, 60))
        
        return steps

    def generate_user(self, persona_type: str) -> Dict[str, Any]:
        """Generate user data based on persona type."""
        config = self.persona_config[persona_type]
        
        return {
            "name": f"user_{random.randint(1000, 9999)}",
            "persona_type": persona_type,
            "age": random.randint(config["age_range"][0], config["age_range"][1]),
            "gender": random.choices(
                list(config["gender_distribution"].keys()),
                list(config["gender_distribution"].values())
            )[0],
            "education": random.choices(
                list(config["education_distribution"].keys()),
                list(config["education_distribution"].values())
            )[0]
        }

    def generate_scenario(self, persona_type: str) -> Dict[str, Any]:
        """Generate a complete scenario for a persona type."""
        start_time = datetime.now() - timedelta(days=random.randint(1, 30))
        
        # Generate journey steps for each phase
        journey = []
        journey.extend(self.generate_awareness_phase(persona_type, start_time))
        journey.extend(self.generate_engagement_phase(
            persona_type,
            datetime.fromisoformat(journey[-1]["timestamp"]) + timedelta(hours=random.randint(1, 24))
        ))
        journey.extend(self.generate_action_phase(
            persona_type,
            datetime.fromisoformat(journey[-1]["timestamp"]) + timedelta(hours=random.randint(24, 72))
        ))
        journey.extend(self.generate_continuity_phase(
            persona_type,
            datetime.fromisoformat(journey[-1]["timestamp"]) + timedelta(days=random.randint(7, 14))
        ))
        
        return {
            "user": self.generate_user(persona_type),
            "journey": journey
        }

    def generate_dataset(self, num_scenarios: int = 100) -> List[Dict[str, Any]]:
        """Generate a dataset of scenarios based on persona distribution."""
        scenarios = []
        
        # Calculate number of scenarios per persona type
        persona_distribution = {
            "health_aware_avoider": 0.25,
            "structured_system_seeker": 0.20,
            "balanced_life_integrator": 0.30,
            "healthcare_professional": 0.15,
            "overlooked_risk_group": 0.10
        }
        
        for persona_type, ratio in persona_distribution.items():
            num_persona_scenarios = int(num_scenarios * ratio)
            for _ in range(num_persona_scenarios):
                scenarios.append(self.generate_scenario(persona_type))
        
        # Add remaining scenarios randomly
        remaining = num_scenarios - len(scenarios)
        for _ in range(remaining):
            persona_type = random.choice(list(persona_distribution.keys()))
            scenarios.append(self.generate_scenario(persona_type))
        
        return scenarios

    def save_dataset(self, scenarios: List[Dict[str, Any]], filename: str = "synthetic_customers.json") -> None:
        """Save generated scenarios to a JSON file."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / filename, "w") as f:
            json.dump(scenarios, f, indent=2)
        
        print(f"Generated {len(scenarios)} scenarios and saved to {output_dir / filename}")

if __name__ == "__main__":
    generator = DataGenerator()
    scenarios = generator.generate_dataset(100)
    generator.save_dataset(scenarios) 