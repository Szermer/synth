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
        self.load_persona_config()
        self.set_completion_thresholds()
        self.set_emotional_states()
        self.current_time = datetime.now() - timedelta(days=random.randint(1, 30))

    def load_persona_config(self):
        """Load persona configurations."""
        self.persona_config = {
            "health_aware_avoider": {
                "age_range": (25, 45),
                "gender_distribution": {"female": 0.6, "male": 0.4},
                "education_distribution": {
                    "high_school": 0.3,
                    "bachelors": 0.5,
                    "masters": 0.2
                },
                "prevention_completion": (0.3, 0.7),
                "anxiety_level": (0.4, 0.6),
                "risk_factors": ["family_history", "lifestyle"],
                "health_awareness": "medium",
                "action_tendency": "low",
                "engagement_pattern": "cautious"
            },
            "structured_system_seeker": {
                "age_range": (35, 55),
                "gender_distribution": {"female": 0.5, "male": 0.5},
                "education_distribution": {
                    "bachelors": 0.4,
                    "masters": 0.4,
                    "phd": 0.2
                },
                "prevention_completion": (0.7, 0.9),
                "anxiety_level": (0.2, 0.4),
                "risk_factors": ["age", "lifestyle"],
                "health_awareness": "high",
                "action_tendency": "high",
                "engagement_pattern": "methodical"
            },
            "balanced_life_integrator": {
                "age_range": (30, 50),
                "gender_distribution": {"female": 0.55, "male": 0.45},
                "education_distribution": {
                    "high_school": 0.2,
                    "bachelors": 0.6,
                    "masters": 0.2
                },
                "prevention_completion": (0.5, 0.8),
                "anxiety_level": (0.3, 0.5),
                "risk_factors": ["lifestyle", "environment"],
                "health_awareness": "medium",
                "action_tendency": "medium",
                "engagement_pattern": "balanced"
            },
            "healthcare_professional": {
                "age_range": (30, 60),
                "gender_distribution": {"female": 0.7, "male": 0.3},
                "education_distribution": {
                    "bachelors": 0.3,
                    "masters": 0.5,
                    "phd": 0.2
                },
                "prevention_completion": (0.8, 0.95),
                "anxiety_level": (0.1, 0.3),
                "risk_factors": ["occupational", "lifestyle"],
                "health_awareness": "very_high",
                "action_tendency": "very_high",
                "engagement_pattern": "proactive"
            },
            "overlooked_risk_group": {
                "age_range": (40, 65),
                "gender_distribution": {"female": 0.8, "male": 0.2},
                "education_distribution": {
                    "high_school": 0.5,
                    "bachelors": 0.4,
                    "masters": 0.1
                },
                "prevention_completion": (0.2, 0.5),
                "anxiety_level": (0.6, 0.8),
                "risk_factors": ["age", "family_history", "socioeconomic"],
                "health_awareness": "low",
                "action_tendency": "very_low",
                "engagement_pattern": "resistant"
            }
        }

    def set_completion_thresholds(self) -> None:
        """Set completion thresholds for each persona type."""
        self.completion_thresholds = {
            "health_aware_avoider": {
                "awareness": (0.4, 0.7),
                "engagement": (0.3, 0.6),
                "action": (0.2, 0.5),
                "continuity": (0.1, 0.4)
            },
            "structured_system_seeker": {
                "awareness": (0.7, 0.9),
                "engagement": (0.6, 0.8),
                "action": (0.5, 0.7),
                "continuity": (0.4, 0.6)
            },
            "balanced_life_integrator": {
                "awareness": (0.5, 0.8),
                "engagement": (0.4, 0.7),
                "action": (0.3, 0.6),
                "continuity": (0.2, 0.5)
            },
            "healthcare_professional": {
                "awareness": (0.8, 0.95),
                "engagement": (0.7, 0.9),
                "action": (0.6, 0.8),
                "continuity": (0.5, 0.7)
            },
            "overlooked_risk_group": {
                "awareness": (0.3, 0.6),
                "engagement": (0.2, 0.5),
                "action": (0.1, 0.4),
                "continuity": (0.1, 0.3)
            }
        }

    def set_emotional_states(self):
        """Define emotional state progressions for each persona type."""
        self.emotional_states = {
            "health_aware_avoider": {
                "awareness": {
                    "essential": ["anxious", "concerned", "curious"],
                    "extended": ["concerned", "curious", "attentive"],
                    "comprehensive": ["curious", "attentive", "engaged"]
                },
                "engagement": {
                    "essential": ["concerned", "engaged", "reflective"],
                    "extended": ["engaged", "reflective", "motivated"],
                    "comprehensive": ["reflective", "motivated", "stable"]
                },
                "action": {
                    "essential": ["concerned", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "continuity": {
                    "essential": ["motivated", "stable", "reflective"],
                    "extended": ["stable", "reflective", "engaged"],
                    "comprehensive": ["reflective", "engaged", "stable"]
                }
            },
            "structured_system_seeker": {
                "awareness": {
                    "essential": ["curious", "attentive", "engaged"],
                    "extended": ["attentive", "engaged", "motivated"],
                    "comprehensive": ["engaged", "motivated", "determined"]
                },
                "engagement": {
                    "essential": ["engaged", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "action": {
                    "essential": ["motivated", "determined", "stable"],
                    "extended": ["determined", "stable", "reflective"],
                    "comprehensive": ["stable", "reflective", "engaged"]
                },
                "continuity": {
                    "essential": ["determined", "stable", "reflective"],
                    "extended": ["stable", "reflective", "engaged"],
                    "comprehensive": ["reflective", "engaged", "motivated"]
                }
            }
        }
        # Add similar patterns for other personas...

    def get_completion_probability(self, persona_type: str, phase: str, engagement_level: str, progress: float) -> float:
        """Calculate completion probability based on persona type and phase."""
        # Base probabilities for each tier with value-first architecture
        tier_base = {
            "essential": 0.9,    # Higher completion for essential tier (value-first)
            "extended": 0.65,    # Medium completion for extended tier
            "comprehensive": 0.45  # Lower completion for comprehensive tier
        }
        
        # Persona-specific adjustments
        persona_adjustments = {
            "health_aware_avoider": {
                "essential": -0.05,    # Slightly lower for essential
                "extended": -0.1,       # Lower for extended
                "comprehensive": -0.15   # Lower for comprehensive
            },
            "structured_system_seeker": {
                "essential": 0.05,      # Higher for essential
                "extended": 0.1,        # Higher for extended
                "comprehensive": 0.15    # Higher for comprehensive
            },
            "balanced_life_integrator": {
                "essential": 0.0,       # No adjustment needed
                "extended": 0.0,        # No adjustment needed
                "comprehensive": -0.05   # Slightly lower for comprehensive
            },
            "healthcare_professional": {
                "essential": 0.1,       # Much higher for essential
                "extended": 0.15,       # Much higher for extended
                "comprehensive": 0.2     # Much higher for comprehensive
            },
            "overlooked_risk_group": {
                "essential": -0.1,      # Lower for essential
                "extended": -0.15,      # Lower for extended
                "comprehensive": -0.2    # Lower for comprehensive
            }
        }
        
        # Phase-specific adjustments
        phase_adjustments = {
            "awareness": 0.0,     # No adjustment needed
            "engagement": -0.05,  # Slightly lower for engagement
            "action": -0.1,       # Lower for action
            "continuity": -0.15   # Much lower for continuity
        }
        
        # Calculate base probability
        base = tier_base[engagement_level]
        
        # Apply persona adjustment
        persona_adj = persona_adjustments[persona_type][engagement_level]
        
        # Apply phase adjustment
        phase_adj = phase_adjustments[phase]
        
        # Apply progress factor (up to 10% boost)
        progress_factor = 0.1 * progress
        
        # Add some randomness
        random_factor = random.uniform(-0.05, 0.05)
        
        # Calculate final probability
        final_prob = base + persona_adj + phase_adj + progress_factor + random_factor
        
        # Ensure probability stays within bounds
        return min(0.98, max(0.02, final_prob))

    def get_emotional_state(self, persona_type: str, phase: str, engagement_level: str, progress: float) -> str:
        """Get emotional state based on persona type, phase, engagement level and progress."""
        # Define emotional state progressions for each persona
        emotional_progressions = {
            "health_aware_avoider": {
                "awareness": {
                    "essential": ["anxious", "concerned", "curious"],
                    "extended": ["concerned", "curious", "attentive"],
                    "comprehensive": ["curious", "attentive", "engaged"]
                },
                "engagement": {
                    "essential": ["concerned", "engaged", "reflective"],
                    "extended": ["engaged", "reflective", "motivated"],
                    "comprehensive": ["reflective", "motivated", "stable"]
                },
                "action": {
                    "essential": ["concerned", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "continuity": {
                    "essential": ["motivated", "stable", "reflective"],
                    "extended": ["stable", "reflective", "engaged"],
                    "comprehensive": ["reflective", "engaged", "stable"]
                }
            },
            "structured_system_seeker": {
                "awareness": {
                    "essential": ["curious", "attentive", "engaged"],
                    "extended": ["attentive", "engaged", "motivated"],
                    "comprehensive": ["engaged", "motivated", "determined"]
                },
                "engagement": {
                    "essential": ["engaged", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "action": {
                    "essential": ["motivated", "determined", "stable"],
                    "extended": ["determined", "stable", "reflective"],
                    "comprehensive": ["stable", "reflective", "engaged"]
                },
                "continuity": {
                    "essential": ["determined", "stable", "reflective"],
                    "extended": ["stable", "reflective", "engaged"],
                    "comprehensive": ["reflective", "engaged", "motivated"]
                }
            },
            "balanced_life_integrator": {
                "awareness": {
                    "essential": ["neutral", "curious", "attentive"],
                    "extended": ["curious", "attentive", "engaged"],
                    "comprehensive": ["attentive", "engaged", "motivated"]
                },
                "engagement": {
                    "essential": ["attentive", "engaged", "motivated"],
                    "extended": ["engaged", "motivated", "determined"],
                    "comprehensive": ["motivated", "determined", "stable"]
                },
                "action": {
                    "essential": ["engaged", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "continuity": {
                    "essential": ["motivated", "determined", "stable"],
                    "extended": ["determined", "stable", "reflective"],
                    "comprehensive": ["stable", "reflective", "engaged"]
                }
            },
            "healthcare_professional": {
                "awareness": {
                    "essential": ["curious", "attentive", "engaged"],
                    "extended": ["attentive", "engaged", "motivated"],
                    "comprehensive": ["engaged", "motivated", "determined"]
                },
                "engagement": {
                    "essential": ["engaged", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "action": {
                    "essential": ["motivated", "determined", "stable"],
                    "extended": ["determined", "stable", "reflective"],
                    "comprehensive": ["stable", "reflective", "engaged"]
                },
                "continuity": {
                    "essential": ["determined", "stable", "reflective"],
                    "extended": ["stable", "reflective", "engaged"],
                    "comprehensive": ["reflective", "engaged", "motivated"]
                }
            },
            "overlooked_risk_group": {
                "awareness": {
                    "essential": ["anxious", "concerned", "curious"],
                    "extended": ["concerned", "curious", "attentive"],
                    "comprehensive": ["curious", "attentive", "engaged"]
                },
                "engagement": {
                    "essential": ["concerned", "engaged", "reflective"],
                    "extended": ["engaged", "reflective", "motivated"],
                    "comprehensive": ["reflective", "motivated", "stable"]
                },
                "action": {
                    "essential": ["concerned", "motivated", "determined"],
                    "extended": ["motivated", "determined", "stable"],
                    "comprehensive": ["determined", "stable", "reflective"]
                },
                "continuity": {
                    "essential": ["motivated", "stable", "reflective"],
                    "extended": ["stable", "reflective", "engaged"],
                    "comprehensive": ["reflective", "engaged", "stable"]
                }
            }
        }
        
        # Get the emotional progression for this persona, phase, and engagement level
        progression = emotional_progressions[persona_type][phase][engagement_level]
        
        # Calculate which state to use based on progress with weighted randomization
        if progress < 0.3:
            # Early progress - bias towards first state
            return random.choices([progression[0], progression[1]], weights=[0.7, 0.3])[0]
        elif progress < 0.7:
            # Mid progress - bias towards middle state
            return random.choices([progression[1], progression[2]], weights=[0.6, 0.4])[0]
        else:
            # Late progress - bias towards final state
            return random.choices([progression[1], progression[2]], weights=[0.3, 0.7])[0]

    def generate_step(self, persona_type: str, phase: str, engagement_level: str, step_name: str, progress: float) -> dict:
        """Generate a single step with appropriate emotional state and completion status."""
        # Get emotional state with weighted randomization
        state = self.get_emotional_state(persona_type, phase, engagement_level, progress)
        
        # Calculate completion probability
        completion_prob = self.get_completion_probability(persona_type, phase, engagement_level, progress)
        
        # Add dwell time based on engagement level
        dwell_time = {
            "essential": random.randint(2, 5),
            "extended": random.randint(5, 10),
            "comprehensive": random.randint(10, 20)
        }[engagement_level]
        
        return {
            "step": step_name,
            "timestamp": self.generate_timestamp(),
            "emotional_state": state,
            "completion_status": "completed" if random.random() < completion_prob else "incomplete",
            "progress": progress,
            "dwell_time_minutes": dwell_time
        }

    def generate_phase(self, persona_type: str, phase: str, steps: dict) -> List[dict]:
        """Generate steps for a phase with progressive disclosure."""
        phase_steps = []
        progress = 0.0
        
        # Generate essential steps
        essential_completed = True
        for step in steps["essential"]:
            progress += 0.2
            step_data = self.generate_step(persona_type, phase, "essential", step, progress)
            phase_steps.append(step_data)
            if step_data["completion_status"] == "incomplete":
                essential_completed = False
        
        # Generate extended steps if essential complete
        if essential_completed:
            extended_completed = True
            for step in steps["extended"]:
                progress += 0.15
                step_data = self.generate_step(persona_type, phase, "extended", step, progress)
                phase_steps.append(step_data)
                if step_data["completion_status"] == "incomplete":
                    extended_completed = False
            
            # Generate comprehensive steps if extended complete
            if extended_completed:
                for step in steps["comprehensive"]:
                    progress += 0.1
                    step_data = self.generate_step(persona_type, phase, "comprehensive", step, progress)
                    phase_steps.append(step_data)
        
        return phase_steps

    def generate_journey(self, persona_type: str) -> List[dict]:
        """Generate a complete journey for a persona."""
        journey = []
        
        # Define steps for each phase
        journey_steps = {
            "awareness": {
                "essential": ["risk_insight", "simple_action", "basic_profile"],
                "extended": ["narrative_elements", "choice_architecture", "support_network"],
                "comprehensive": ["contextual_analysis", "long_term_strategy", "genetic_factors"]
            },
            "engagement": {
                "essential": ["value_preview", "quick_win", "basic_goals"],
                "extended": ["progressive_disclosure", "contextual_support", "prevention_options"],
                "comprehensive": ["engagement_momentum", "advanced_planning", "community_connection"]
            },
            "action": {
                "essential": ["micro_action", "prevention_path", "basic_plan"],
                "extended": ["support_network", "resource_allocation", "plan_adjustment"],
                "comprehensive": ["advanced_strategies", "community_engagement", "long_term_planning"]
            },
            "continuity": {
                "essential": ["value_reminder", "barrier_resolution", "progress_tracking"],
                "extended": ["multi_channel_followup", "solution_pairing", "plan_adjustment"],
                "comprehensive": ["milestone_celebration", "achievement_recognition", "re_engagement"]
            }
        }
        
        # Generate steps for each phase
        for phase, steps in journey_steps.items():
            journey.extend(self.generate_phase(persona_type, phase, steps))
        
        return journey

    def generate_dataset(self, num_scenarios: int = 100) -> List[dict]:
        """Generate a dataset of scenarios."""
        scenarios = []
        
        # Distribution of persona types
        persona_distribution = {
            "health_aware_avoider": 0.25,
            "structured_system_seeker": 0.2,
            "balanced_life_integrator": 0.3,
            "healthcare_professional": 0.15,
            "overlooked_risk_group": 0.1
        }
        
        for _ in range(num_scenarios):
            persona_type = random.choices(
                list(persona_distribution.keys()),
                weights=list(persona_distribution.values())
            )[0]
            
            scenario = {
                "user": {
                    "persona_type": persona_type,
                    "id": str(uuid.uuid4())
                },
                "journey": self.generate_journey(persona_type)
            }
            scenarios.append(scenario)
        
        return scenarios

    def save_dataset(self, scenarios: List[dict], filename: str = "synthetic_customers.json"):
        """Save the generated dataset to a JSON file."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / filename, "w") as f:
            json.dump(scenarios, f, indent=2)
        
        print(f"Generated {len(scenarios)} scenarios and saved to output/{filename}")

    def generate_timestamp(self) -> str:
        """Generate a timestamp for a journey step."""
        # Add random time between steps (5 min to 2 hours)
        self.current_time += timedelta(minutes=random.randint(5, 120))
        return self.current_time.isoformat()

if __name__ == "__main__":
    generator = DataGenerator()
    scenarios = generator.generate_dataset()
    generator.save_dataset(scenarios) 