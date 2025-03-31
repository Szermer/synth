import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class JourneyPhaseValidator:
    def __init__(self):
        self.load_test_data()
        self.set_validation_thresholds()
        self.set_journey_steps()

    def load_test_data(self) -> None:
        """Load test data from JSON file."""
        with open("output/synthetic_customers.json", "r") as f:
            self.scenarios = json.load(f)

    def set_journey_steps(self) -> None:
        """Define journey steps for each phase and engagement level."""
        self.journey_steps = {
            "awareness": {
                "essential": ["risk_insight", "simple_action", "basic_profile"],  # Value-first approach
                "extended": ["narrative_elements", "choice_architecture", "support_network"],  # Progressive disclosure
                "comprehensive": ["contextual_analysis", "long_term_strategy", "genetic_factors"]  # Deep personalization
            },
            "engagement": {
                "essential": ["value_preview", "quick_win", "basic_goals"],  # Immediate value delivery
                "extended": ["progressive_disclosure", "contextual_support", "prevention_options"],  # Enhanced guidance
                "comprehensive": ["engagement_momentum", "advanced_planning", "community_connection"]  # Deep engagement
            },
            "action": {
                "essential": ["micro_action", "prevention_path", "basic_plan"],  # Small wins first
                "extended": ["support_network", "resource_allocation", "plan_adjustment"],  # Enhanced support
                "comprehensive": ["advanced_strategies", "community_engagement", "long_term_planning"]  # Comprehensive approach
            },
            "continuity": {
                "essential": ["value_reminder", "barrier_resolution", "progress_tracking"],  # Sustained value
                "extended": ["multi_channel_followup", "solution_pairing", "plan_adjustment"],  # Enhanced support
                "comprehensive": ["milestone_celebration", "achievement_recognition", "re_engagement"]  # Deep engagement
            }
        }

    def set_validation_thresholds(self) -> None:
        """Set validation thresholds for each persona type and engagement level."""
        self.thresholds = {
            "health_aware_avoider": {
                "awareness": {
                    "essential": {
                        "anxiety": (0.7, 0.8),  # High anxiety
                        "curiosity": (0.2, 0.25),  # Very low curiosity
                        "completion": (0.85, 0.95)  # High completion
                    },
                    "extended": {
                        "anxiety": (0.5, 0.7),  # High anxiety
                        "curiosity": (0.3, 0.5),  # Low curiosity
                        "completion": (0.5, 0.65)  # Moderate completion
                    },
                    "comprehensive": {
                        "anxiety": (0.3, 0.5),  # Moderate anxiety
                        "curiosity": (0.4, 0.6),  # Moderate curiosity
                        "completion": (0.05, 0.1)  # Very low completion
                    }
                },
                "engagement": {
                    "essential": {
                        "engagement": (0.8, 0.9),  # High engagement
                        "reflection": (0.4, 0.6),  # Moderate reflection
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "extended": {
                        "engagement": (0.4, 0.6),  # Moderate engagement
                        "reflection": (0.3, 0.5),  # Moderate reflection
                        "completion": (0.2, 0.3)  # Low completion
                    },
                    "comprehensive": {
                        "engagement": (0.2, 0.4),  # Low engagement
                        "reflection": (0.2, 0.4),  # Low reflection
                        "completion": (0.0, 0.05)  # Very low completion
                    }
                },
                "action": {
                    "essential": {
                        "motivation": (0.8, 0.9),  # High motivation
                        "determination": (0.8, 0.9),  # High determination
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "extended": {
                        "motivation": (0.4, 0.6),  # Moderate motivation
                        "determination": (0.4, 0.6),  # Moderate determination
                        "completion": (0.7, 0.8)  # High completion
                    },
                    "comprehensive": {
                        "motivation": (0.2, 0.4),  # Low motivation
                        "determination": (0.2, 0.4),  # Low determination
                        "completion": (0.05, 0.1)  # Very low completion
                    }
                },
                "continuity": {
                    "essential": {
                        "stability": (0.8, 0.9),  # High stability
                        "reflection": (0.8, 0.9),  # High reflection
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "extended": {
                        "stability": (0.4, 0.6),  # Moderate stability
                        "reflection": (0.4, 0.6),  # Moderate reflection
                        "completion": (0.4, 0.5)  # Moderate completion
                    },
                    "comprehensive": {
                        "stability": (0.2, 0.4),  # Low stability
                        "reflection": (0.2, 0.4),  # Low reflection
                        "completion": (0.05, 0.1)  # Very low completion
                    }
                }
            },
            "structured_system_seeker": {
                "awareness": {
                    "essential": {
                        "anxiety": (0.0, 0.1),  # Very low anxiety
                        "curiosity": (0.7, 0.8),  # High curiosity
                        "completion": (0.9, 1.0)  # Very high completion
                    },
                    "extended": {
                        "anxiety": (0.0, 0.2),  # Very low anxiety
                        "curiosity": (0.6, 0.8),  # Moderate-high curiosity
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "comprehensive": {
                        "anxiety": (0.0, 0.2),  # Very low anxiety
                        "curiosity": (0.5, 0.7),  # Moderate curiosity
                        "completion": (0.4, 0.5)  # Moderate completion
                    }
                },
                "engagement": {
                    "essential": {
                        "engagement": (0.9, 1.0),  # Very high engagement
                        "reflection": (0.7, 0.85),  # High reflection
                        "completion": (0.95, 1.0)  # Very high completion
                    },
                    "extended": {
                        "engagement": (0.7, 0.85),  # High engagement
                        "reflection": (0.6, 0.8),  # Moderate-high reflection
                        "completion": (0.75, 0.85)  # High completion
                    },
                    "comprehensive": {
                        "engagement": (0.4, 0.6),  # Moderate engagement
                        "reflection": (0.4, 0.6),  # Moderate reflection
                        "completion": (0.2, 0.3)  # Low completion
                    }
                },
                "action": {
                    "essential": {
                        "motivation": (0.85, 0.95),  # Very high motivation
                        "determination": (0.9, 1.0),  # Very high determination
                        "completion": (0.85, 0.95)  # Very high completion
                    },
                    "extended": {
                        "motivation": (0.7, 0.85),  # High motivation
                        "determination": (0.7, 0.85),  # High determination
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "comprehensive": {
                        "motivation": (0.4, 0.6),  # Moderate motivation
                        "determination": (0.4, 0.6),  # Moderate determination
                        "completion": (0.15, 0.25)  # Low completion
                    }
                },
                "continuity": {
                    "essential": {
                        "stability": (0.8, 0.9),  # High stability
                        "reflection": (0.8, 0.9),  # High reflection
                        "completion": (0.9, 1.0)  # Very high completion
                    },
                    "extended": {
                        "stability": (0.6, 0.8),  # Moderate-high stability
                        "reflection": (0.6, 0.8),  # Moderate-high reflection
                        "completion": (0.7, 0.8)  # High completion
                    },
                    "comprehensive": {
                        "stability": (0.4, 0.6),  # Moderate stability
                        "reflection": (0.4, 0.6),  # Moderate reflection
                        "completion": (0.3, 0.4)  # Moderate completion
                    }
                }
            },
            "balanced_life_integrator": {
                "awareness": {
                    "essential": {
                        "anxiety": (0.0, 0.2),  # Low anxiety
                        "curiosity": (0.7, 0.8),  # High curiosity
                        "completion": (0.9, 1.0)  # Very high completion
                    },
                    "extended": {
                        "anxiety": (0.0, 0.2),  # Low anxiety
                        "curiosity": (0.6, 0.8),  # Moderate-high curiosity
                        "completion": (0.55, 0.65)  # Moderate completion
                    },
                    "comprehensive": {
                        "anxiety": (0.0, 0.2),  # Low anxiety
                        "curiosity": (0.5, 0.7),  # Moderate curiosity
                        "completion": (0.1, 0.15)  # Low completion
                    }
                },
                "engagement": {
                    "essential": {
                        "engagement": (0.85, 0.95),  # Very high engagement
                        "reflection": (0.6, 0.8),  # Moderate-high reflection
                        "completion": (0.85, 0.95)  # High completion
                    },
                    "extended": {
                        "engagement": (0.6, 0.8),  # Moderate-high engagement
                        "reflection": (0.5, 0.7),  # Moderate reflection
                        "completion": (0.45, 0.5)  # Moderate completion
                    },
                    "comprehensive": {
                        "engagement": (0.4, 0.6),  # Moderate engagement
                        "reflection": (0.4, 0.6),  # Moderate reflection
                        "completion": (0.1, 0.15)  # Low completion
                    }
                },
                "action": {
                    "essential": {
                        "motivation": (0.85, 0.95),  # Very high motivation
                        "determination": (0.85, 0.95),  # Very high determination
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "extended": {
                        "motivation": (0.5, 0.7),  # Moderate motivation
                        "determination": (0.5, 0.7),  # Moderate determination
                        "completion": (0.5, 0.6)  # Moderate completion
                    },
                    "comprehensive": {
                        "motivation": (0.3, 0.5),  # Low-moderate motivation
                        "determination": (0.3, 0.5),  # Low-moderate determination
                        "completion": (0.05, 0.1)  # Very low completion
                    }
                },
                "continuity": {
                    "essential": {
                        "stability": (0.8, 0.9),  # High stability
                        "reflection": (0.8, 0.9),  # High reflection
                        "completion": (0.85, 0.95)  # High completion
                    },
                    "extended": {
                        "stability": (0.5, 0.7),  # Moderate stability
                        "reflection": (0.5, 0.7),  # Moderate reflection
                        "completion": (0.6, 0.7)  # Moderate completion
                    },
                    "comprehensive": {
                        "stability": (0.3, 0.5),  # Low-moderate stability
                        "reflection": (0.3, 0.5),  # Low-moderate reflection
                        "completion": (0.3, 0.4)  # Moderate completion
                    }
                }
            },
            "healthcare_professional": {
                "awareness": {
                    "essential": {
                        "anxiety": (0.0, 0.1),  # Very low anxiety
                        "curiosity": (0.7, 0.8),  # High curiosity
                        "completion": (0.95, 1.0)  # Very high completion
                    },
                    "extended": {
                        "anxiety": (0.0, 0.1),  # Very low anxiety
                        "curiosity": (0.8, 0.9),  # Very high curiosity
                        "completion": (0.9, 1.0)  # Very high completion
                    },
                    "comprehensive": {
                        "anxiety": (0.0, 0.1),  # Very low anxiety
                        "curiosity": (0.7, 0.85),  # High curiosity
                        "completion": (0.55, 0.65)  # Moderate-high completion
                    }
                },
                "engagement": {
                    "essential": {
                        "engagement": (0.9, 1.0),  # Very high engagement
                        "reflection": (0.8, 0.9),  # High reflection
                        "completion": (0.95, 1.0)  # Very high completion
                    },
                    "extended": {
                        "engagement": (0.8, 0.9),  # High engagement
                        "reflection": (0.7, 0.85),  # High reflection
                        "completion": (0.65, 0.75)  # Moderate-high completion
                    },
                    "comprehensive": {
                        "engagement": (0.7, 0.85),  # High engagement
                        "reflection": (0.6, 0.8),  # Moderate-high reflection
                        "completion": (0.4, 0.5)  # Moderate completion
                    }
                },
                "action": {
                    "essential": {
                        "motivation": (0.9, 1.0),  # Very high motivation
                        "determination": (0.9, 1.0),  # Very high determination
                        "completion": (0.9, 1.0)  # Very high completion
                    },
                    "extended": {
                        "motivation": (0.8, 0.9),  # High motivation
                        "determination": (0.8, 0.9),  # High determination
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "comprehensive": {
                        "motivation": (0.6, 0.8),  # High motivation
                        "determination": (0.6, 0.8),  # High motivation
                        "completion": (0.3, 0.4)  # Moderate completion
                    }
                },
                "continuity": {
                    "essential": {
                        "stability": (0.9, 1.0),  # Very high stability
                        "reflection": (0.9, 1.0),  # Very high reflection
                        "completion": (0.9, 1.0)  # Very high completion
                    },
                    "extended": {
                        "stability": (0.8, 0.9),  # High stability
                        "reflection": (0.8, 0.9),  # High reflection
                        "completion": (0.8, 0.9)  # High completion
                    },
                    "comprehensive": {
                        "stability": (0.7, 0.85),  # High stability
                        "reflection": (0.7, 0.85),  # High reflection
                        "completion": (0.6, 0.7)  # Moderate-high completion
                    }
                }
            },
            "overlooked_risk_group": {
                "awareness": {
                    "essential": {
                        "anxiety": (0.8, 0.9),  # Very high anxiety
                        "curiosity": (0.1, 0.15),  # Very low curiosity
                        "completion": (0.75, 0.85)  # Moderate-high completion
                    },
                    "extended": {
                        "anxiety": (0.6, 0.8),  # High anxiety
                        "curiosity": (0.1, 0.2),  # Very low curiosity
                        "completion": (0.25, 0.35)  # Low completion
                    },
                    "comprehensive": {
                        "anxiety": (0.5, 0.7),  # High anxiety
                        "curiosity": (0.1, 0.25),  # Very low curiosity
                        "completion": (0.0, 0.05)  # Very low completion
                    }
                },
                "engagement": {
                    "essential": {
                        "engagement": (0.7, 0.85),  # High engagement
                        "reflection": (0.4, 0.6),  # Moderate reflection
                        "completion": (0.75, 0.85)  # Moderate-high completion
                    },
                    "extended": {
                        "engagement": (0.3, 0.5),  # Moderate engagement
                        "reflection": (0.3, 0.5),  # Moderate reflection
                        "completion": (0.15, 0.25)  # Low completion
                    },
                    "comprehensive": {
                        "engagement": (0.2, 0.4),  # Low engagement
                        "reflection": (0.2, 0.4),  # Low reflection
                        "completion": (0.0, 0.05)  # Very low completion
                    }
                },
                "action": {
                    "essential": {
                        "motivation": (0.7, 0.85),  # High motivation
                        "determination": (0.7, 0.85),  # High determination
                        "completion": (0.65, 0.75)  # Moderate-high completion
                    },
                    "extended": {
                        "motivation": (0.3, 0.5),  # Moderate motivation
                        "determination": (0.3, 0.5),  # Moderate determination
                        "completion": (0.35, 0.45)  # Moderate completion
                    },
                    "comprehensive": {
                        "motivation": (0.2, 0.4),  # Low motivation
                        "determination": (0.2, 0.4),  # Low determination
                        "completion": (0.0, 0.05)  # Very low completion
                    }
                },
                "continuity": {
                    "essential": {
                        "stability": (0.7, 0.85),  # High stability
                        "reflection": (0.7, 0.85),  # High reflection
                        "completion": (0.7, 0.8)  # Moderate-high completion
                    },
                    "extended": {
                        "stability": (0.3, 0.5),  # Moderate stability
                        "reflection": (0.3, 0.5),  # Moderate reflection
                        "completion": (0.35, 0.45)  # Moderate completion
                    },
                    "comprehensive": {
                        "stability": (0.2, 0.4),  # Low stability
                        "reflection": (0.2, 0.4),  # Low reflection
                        "completion": (0.0, 0.05)  # Very low completion
                    }
                }
            }
        }

    def calculate_completion_rate(self, steps: List[Dict[str, Any]]) -> float:
        """Calculate completion rate for a set of steps."""
        if not steps:
            return 0.0
        completed = sum(1 for step in steps if step["completion_status"] == "completed")
        return completed / len(steps)

    def calculate_emotional_rates(self, steps: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate emotional state rates for a set of steps."""
        if not steps:
            return {"anxiety": 0.0, "curiosity": 0.0, "engagement": 0.0, "reflection": 0.0}

        total = len(steps)
        rates = {
            "anxiety": sum(1 for step in steps if step["emotional_state"] in ["anxious", "concerned"]) / total,
            "curiosity": sum(1 for step in steps if step["emotional_state"] in ["curious", "attentive"]) / total,
            "engagement": sum(1 for step in steps if step["emotional_state"] in ["engaged", "motivated"]) / total,
            "reflection": sum(1 for step in steps if step["emotional_state"] in ["reflective", "stable"]) / total
        }
        return rates

    def get_phase_steps(self, journey: List[Dict[str, Any]], phase: str, engagement_level: str) -> List[Dict[str, Any]]:
        """Get steps for a specific phase and engagement level."""
        steps = self.journey_steps[phase][engagement_level]
        return [step for step in journey if step["step"] in steps]

    def validate_phase_engagement_level(self, persona_type: str, phase: str, engagement_level: str, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate a specific phase and engagement level for a persona."""
        steps = self.get_phase_steps(journey, phase, engagement_level)
        completion_rate = self.calculate_completion_rate(steps)
        emotional_rates = self.calculate_emotional_rates(steps)
        thresholds = self.thresholds[persona_type][phase][engagement_level]
        
        emotional_progression = []
        for i in range(len(steps)-1):
            if i+1 < len(steps):
                emotional_progression.append([steps[i]["emotional_state"], steps[i+1]["emotional_state"]])
        
        # Phase-specific validation
        if phase == "awareness":
            meets_thresholds = (
                thresholds["anxiety"][0] <= emotional_rates["anxiety"] <= thresholds["anxiety"][1] and
                thresholds["curiosity"][0] <= emotional_rates["curiosity"] <= thresholds["curiosity"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        elif phase == "engagement":
            meets_thresholds = (
                thresholds["engagement"][0] <= emotional_rates["engagement"] <= thresholds["engagement"][1] and
                thresholds["reflection"][0] <= emotional_rates["reflection"] <= thresholds["reflection"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        elif phase == "action":
            meets_thresholds = (
                thresholds["motivation"][0] <= emotional_rates["engagement"] <= thresholds["motivation"][1] and
                thresholds["determination"][0] <= emotional_rates["reflection"] <= thresholds["determination"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        elif phase == "continuity":
            meets_thresholds = (
                thresholds["stability"][0] <= emotional_rates["reflection"] <= thresholds["stability"][1] and
                thresholds["reflection"][0] <= emotional_rates["reflection"] <= thresholds["reflection"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        else:
            meets_thresholds = False
        
        return {
            "emotional_progression": emotional_progression,
            "anxiety_rate": emotional_rates["anxiety"],
            "curiosity_rate": emotional_rates["curiosity"],
            "engagement_rate": emotional_rates["engagement"],
            "reflection_rate": emotional_rates["reflection"],
            "completion_rate": completion_rate,
            "meets_thresholds": meets_thresholds
        }

    def assess_progressive_disclosure(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the progressive disclosure pattern across engagement levels."""
        essential_completion = results["essential"]["completion_rate"]
        extended_completion = results["extended"]["completion_rate"]
        comprehensive_completion = results["comprehensive"]["completion_rate"]
        
        # Check if completion rates follow progressive disclosure pattern
        meets_pattern = (
            0.6 <= essential_completion <= 0.9 and  # Essential tier: 60-90% completion
            extended_completion <= essential_completion * 0.7 and  # Extended tier: 30% lower
            comprehensive_completion <= essential_completion * 0.3  # Comprehensive tier: 70% lower
        )
        
        return {
            "meets_pattern": meets_pattern,
            "essential_rate": essential_completion,
            "extended_rate": extended_completion,
            "comprehensive_rate": comprehensive_completion
        }

    def assess_persona_differentiation(self, results: Dict[str, Any], persona_type: str) -> Dict[str, Any]:
        """Assess persona-specific engagement patterns."""
        essential_completion = results["essential"]["completion_rate"]
        
        # Define expected completion ranges for each persona
        persona_ranges = {
            "healthcare_professional": (0.85, 0.95),  # Highest overall engagement
            "structured_system_seeker": (0.75, 0.85),  # Strong methodical progression
            "balanced_life_integrator": (0.65, 0.75),  # Moderate consistent engagement
            "health_aware_avoider": (0.55, 0.65),  # Strong essential but steep drop-off
            "overlooked_risk_group": (0.45, 0.55)  # Lowest overall engagement
        }
        
        expected_range = persona_ranges.get(persona_type, (0.6, 0.8))
        meets_pattern = expected_range[0] <= essential_completion <= expected_range[1]
        
        return {
            "meets_pattern": meets_pattern,
            "completion_rate": essential_completion,
            "expected_range": expected_range
        }

    def assess_emotional_alignment(self, results: Dict[str, Any], persona_type: str) -> Dict[str, Any]:
        """Assess emotional state alignment with persona characteristics."""
        anxiety_rate = results["essential"]["anxiety_rate"]
        
        # Define expected anxiety ranges for each persona
        persona_anxiety = {
            "health_aware_avoider": (0.5, 0.7),  # High anxiety
            "overlooked_risk_group": (0.7, 0.85),  # Very high anxiety
            "healthcare_professional": (0.0, 0.15),  # Very low anxiety
            "structured_system_seeker": (0.0, 0.15),  # Very low anxiety
            "balanced_life_integrator": (0.0, 0.15)  # Very low anxiety
        }
        
        expected_range = persona_anxiety.get(persona_type, (0.0, 0.2))
        meets_pattern = expected_range[0] <= anxiety_rate <= expected_range[1]
        
        return {
            "meets_pattern": meets_pattern,
            "anxiety_rate": anxiety_rate,
            "expected_range": expected_range
        }

    def assess_phase_progression(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess phase progression patterns."""
        essential_completion = results["essential"]["completion_rate"]
        
        # Check if completion maintains appropriate level
        meets_pattern = 0.6 <= essential_completion <= 0.9
        
        return {
            "meets_pattern": meets_pattern,
            "completion_rate": essential_completion
        }

    def calculate_pattern_validity_score(self, pattern_alignment: Dict[str, Dict[str, Any]]) -> float:
        """Calculate overall pattern validity score."""
        patterns = [
            pattern_alignment["progressive_disclosure"]["meets_pattern"],
            pattern_alignment["persona_differentiation"]["meets_pattern"],
            pattern_alignment["emotional_alignment"]["meets_pattern"],
            pattern_alignment["phase_progression"]["meets_pattern"]
        ]
        
        return sum(1 for p in patterns if p) / len(patterns)

    def calculate_engagement_patterns(self, results: Dict[str, Any], persona_type: str) -> Dict[str, Any]:
        """Calculate comprehensive engagement patterns across multiple dimensions."""
        essential_results = results["essential"]
        extended_results = results["extended"]
        comprehensive_results = results["comprehensive"]
        
        # Value delivery tracking
        value_realization = {
            "essential_completion": essential_results["completion_rate"],
            "essential_satisfaction": essential_results["engagement_rate"],
            "value_perception": essential_results["reflection_rate"]
        }
        
        # Progressive disclosure tracking
        disclosure_progression = {
            "essential_to_extended_ratio": extended_results["completion_rate"] / essential_results["completion_rate"] if essential_results["completion_rate"] > 0 else 0,
            "extended_to_comprehensive_ratio": comprehensive_results["completion_rate"] / extended_results["completion_rate"] if extended_results["completion_rate"] > 0 else 0,
            "progression_pattern_valid": (
                0.6 <= essential_results["completion_rate"] <= 0.9 and
                extended_results["completion_rate"] <= essential_results["completion_rate"] * 0.7 and
                comprehensive_results["completion_rate"] <= extended_results["completion_rate"] * 0.7
            )
        }
        
        # Emotional progression tracking
        emotional_patterns = {
            "anxiety_reduction": 1 - essential_results["anxiety_rate"],
            "curiosity_satisfaction": essential_results["curiosity_rate"],
            "motivation_development": essential_results["engagement_rate"],
            "emotional_alignment_valid": self.assess_emotional_alignment({"essential": essential_results}, persona_type)["meets_pattern"]
        }
        
        # Persona alignment tracking
        persona_alignment = {
            "expected_pattern_match": self.assess_persona_differentiation({"essential": essential_results}, persona_type)["meets_pattern"],
            "behavioral_confirmation": self.assess_phase_progression({"essential": essential_results})["meets_pattern"],
            "adaptation_effectiveness": (
                emotional_patterns["emotional_alignment_valid"] +
                disclosure_progression["progression_pattern_valid"]
            ) / 2.0
        }
        
        return {
            "value_realization": value_realization,
            "disclosure_progression": disclosure_progression,
            "emotional_patterns": emotional_patterns,
            "persona_alignment": persona_alignment
        }

    def validate_phase(self, persona_type: str, phase: str, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate all engagement levels for a specific phase using pattern-based approach."""
        results = {
            "essential": self.validate_phase_engagement_level(persona_type, phase, "essential", journey),
            "extended": self.validate_phase_engagement_level(persona_type, phase, "extended", journey),
            "comprehensive": self.validate_phase_engagement_level(persona_type, phase, "comprehensive", journey)
        }
        
        # Assess patterns
        pattern_alignment = {
            "progressive_disclosure": self.assess_progressive_disclosure(results),
            "persona_differentiation": self.assess_persona_differentiation(results, persona_type),
            "emotional_alignment": self.assess_emotional_alignment(results, persona_type),
            "phase_progression": self.assess_phase_progression(results)
        }
        
        # Calculate pattern validity score
        pattern_validity_score = self.calculate_pattern_validity_score(pattern_alignment)
        
        # Calculate comprehensive engagement patterns
        engagement_patterns = self.calculate_engagement_patterns(results, persona_type)
        
        # Phase is considered passed if pattern validity score is high enough
        results["phase_passed"] = pattern_validity_score >= 0.6  # Require at least 2 out of 4 patterns to be valid
        results["pattern_alignment"] = pattern_alignment
        results["pattern_validity_score"] = pattern_validity_score
        results["engagement_patterns"] = engagement_patterns
        
        return results

    def validate_phase_transitions(self, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate transitions between phases."""
        phase_transitions = []
        current_phase = self.get_step_phase(journey[0]["step"])
        
        for i in range(1, len(journey)):
            next_phase = self.get_step_phase(journey[i]["step"])
            if next_phase != current_phase:
                phase_transitions.append((current_phase, next_phase))
                current_phase = next_phase
        
        return {
            "num_transitions": len(phase_transitions),
            "transitions": phase_transitions,
            "meets_threshold": 0 < len(phase_transitions) <= 3
        }

    def get_step_phase(self, step: str) -> str:
        """Get the phase for a step."""
        for phase, levels in self.journey_steps.items():
            for level_steps in levels.values():
                if step in level_steps:
                    return phase
        return "unknown"

    def generate_report(self) -> None:
        """Generate validation report with pattern-based analysis."""
        report = []
        report.append("# Journey Phase Validation Report\n")
        report.append(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Group scenarios by persona type
        persona_scenarios = {}
        for scenario in self.scenarios:
            persona_type = scenario["user"]["persona_type"]
            if persona_type not in persona_scenarios:
                persona_scenarios[persona_type] = []
            persona_scenarios[persona_type].append(scenario)
        
        # Validate each phase for each persona type
        total_tests = 0
        passed_tests = 0
        
        # Awareness Phase
        report.append("\n## Awareness Phase Validation")
        awareness_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_phase(persona_type, "awareness", scenario["journey"])
                results.append(result)
            
            # Calculate averages and pattern validity
            avg_pattern_score = sum(r["pattern_validity_score"] for r in results) / len(results)
            meets_patterns = all(r["phase_passed"] for r in results)
            
            if meets_patterns:
                passed_tests += 1
            else:
                awareness_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Pattern Validity Score: {avg_pattern_score:.2f}")
            report.append(f"- Meets Patterns: {'✅' if meets_patterns else '❌'}")
            
            # Add engagement pattern analysis
            report.append("\n#### Engagement Pattern Analysis")
            engagement_patterns = results[0]["engagement_patterns"]
            
            report.append("\n##### Value Realization")
            vr = engagement_patterns["value_realization"]
            report.append(f"- Essential Completion: {vr['essential_completion']:.1%}")
            report.append(f"- Essential Satisfaction: {vr['essential_satisfaction']:.1%}")
            report.append(f"- Value Perception: {vr['value_perception']:.1%}")
            
            report.append("\n##### Progressive Disclosure")
            dp = engagement_patterns["disclosure_progression"]
            report.append(f"- Essential to Extended Ratio: {dp['essential_to_extended_ratio']:.2f}")
            report.append(f"- Extended to Comprehensive Ratio: {dp['extended_to_comprehensive_ratio']:.2f}")
            report.append(f"- Progression Pattern Valid: {'✅' if dp['progression_pattern_valid'] else '❌'}")
            
            report.append("\n##### Emotional Progression")
            ep = engagement_patterns["emotional_patterns"]
            report.append(f"- Anxiety Reduction: {ep['anxiety_reduction']:.1%}")
            report.append(f"- Curiosity Satisfaction: {ep['curiosity_satisfaction']:.1%}")
            report.append(f"- Motivation Development: {ep['motivation_development']:.1%}")
            report.append(f"- Emotional Alignment Valid: {'✅' if ep['emotional_alignment_valid'] else '❌'}")
            
            report.append("\n##### Persona Alignment")
            pa = engagement_patterns["persona_alignment"]
            report.append(f"- Expected Pattern Match: {'✅' if pa['expected_pattern_match'] else '❌'}")
            report.append(f"- Behavioral Confirmation: {'✅' if pa['behavioral_confirmation'] else '❌'}")
            report.append(f"- Adaptation Effectiveness: {pa['adaptation_effectiveness']:.2f}")
            
            # Add pattern details
            report.append("\n#### Pattern Analysis")
            pattern_alignment = results[0]["pattern_alignment"]
            
            report.append("##### Progressive Disclosure")
            pd = pattern_alignment["progressive_disclosure"]
            report.append(f"- Essential: {pd['essential_rate']:.1%}")
            report.append(f"- Extended: {pd['extended_rate']:.1%}")
            report.append(f"- Comprehensive: {pd['comprehensive_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Persona Differentiation")
            pd = pattern_alignment["persona_differentiation"]
            report.append(f"- Completion Rate: {pd['completion_rate']:.1%}")
            report.append(f"- Expected Range: {pd['expected_range'][0]:.1%} - {pd['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Emotional Alignment")
            ea = pattern_alignment["emotional_alignment"]
            report.append(f"- Anxiety Rate: {ea['anxiety_rate']:.1%}")
            report.append(f"- Expected Range: {ea['expected_range'][0]:.1%} - {ea['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if ea['meets_pattern'] else '❌'}")
            
            report.append("\n##### Phase Progression")
            pp = pattern_alignment["phase_progression"]
            report.append(f"- Completion Rate: {pp['completion_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pp['meets_pattern'] else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if awareness_passed else '❌ Failed'}")
        
        # Engagement Phase
        report.append("\n\n## Engagement Phase Validation")
        engagement_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_phase(persona_type, "engagement", scenario["journey"])
                results.append(result)
            
            # Calculate averages and pattern validity
            avg_pattern_score = sum(r["pattern_validity_score"] for r in results) / len(results)
            meets_patterns = all(r["phase_passed"] for r in results)
            
            if meets_patterns:
                passed_tests += 1
            else:
                engagement_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Pattern Validity Score: {avg_pattern_score:.2f}")
            report.append(f"- Meets Patterns: {'✅' if meets_patterns else '❌'}")
            
            # Add engagement pattern analysis
            report.append("\n#### Engagement Pattern Analysis")
            engagement_patterns = results[0]["engagement_patterns"]
            
            report.append("\n##### Value Realization")
            vr = engagement_patterns["value_realization"]
            report.append(f"- Essential Completion: {vr['essential_completion']:.1%}")
            report.append(f"- Essential Satisfaction: {vr['essential_satisfaction']:.1%}")
            report.append(f"- Value Perception: {vr['value_perception']:.1%}")
            
            report.append("\n##### Progressive Disclosure")
            dp = engagement_patterns["disclosure_progression"]
            report.append(f"- Essential to Extended Ratio: {dp['essential_to_extended_ratio']:.2f}")
            report.append(f"- Extended to Comprehensive Ratio: {dp['extended_to_comprehensive_ratio']:.2f}")
            report.append(f"- Progression Pattern Valid: {'✅' if dp['progression_pattern_valid'] else '❌'}")
            
            report.append("\n##### Emotional Progression")
            ep = engagement_patterns["emotional_patterns"]
            report.append(f"- Anxiety Reduction: {ep['anxiety_reduction']:.1%}")
            report.append(f"- Curiosity Satisfaction: {ep['curiosity_satisfaction']:.1%}")
            report.append(f"- Motivation Development: {ep['motivation_development']:.1%}")
            report.append(f"- Emotional Alignment Valid: {'✅' if ep['emotional_alignment_valid'] else '❌'}")
            
            report.append("\n##### Persona Alignment")
            pa = engagement_patterns["persona_alignment"]
            report.append(f"- Expected Pattern Match: {'✅' if pa['expected_pattern_match'] else '❌'}")
            report.append(f"- Behavioral Confirmation: {'✅' if pa['behavioral_confirmation'] else '❌'}")
            report.append(f"- Adaptation Effectiveness: {pa['adaptation_effectiveness']:.2f}")
            
            # Add pattern details
            report.append("\n#### Pattern Analysis")
            pattern_alignment = results[0]["pattern_alignment"]
            
            report.append("##### Progressive Disclosure")
            pd = pattern_alignment["progressive_disclosure"]
            report.append(f"- Essential: {pd['essential_rate']:.1%}")
            report.append(f"- Extended: {pd['extended_rate']:.1%}")
            report.append(f"- Comprehensive: {pd['comprehensive_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Persona Differentiation")
            pd = pattern_alignment["persona_differentiation"]
            report.append(f"- Completion Rate: {pd['completion_rate']:.1%}")
            report.append(f"- Expected Range: {pd['expected_range'][0]:.1%} - {pd['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Emotional Alignment")
            ea = pattern_alignment["emotional_alignment"]
            report.append(f"- Anxiety Rate: {ea['anxiety_rate']:.1%}")
            report.append(f"- Expected Range: {ea['expected_range'][0]:.1%} - {ea['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if ea['meets_pattern'] else '❌'}")
            
            report.append("\n##### Phase Progression")
            pp = pattern_alignment["phase_progression"]
            report.append(f"- Completion Rate: {pp['completion_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pp['meets_pattern'] else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if engagement_passed else '❌ Failed'}")
        
        # Action Phase
        report.append("\n\n## Action Phase Validation")
        action_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_phase(persona_type, "action", scenario["journey"])
                results.append(result)
            
            # Calculate averages and pattern validity
            avg_pattern_score = sum(r["pattern_validity_score"] for r in results) / len(results)
            meets_patterns = all(r["phase_passed"] for r in results)
            
            if meets_patterns:
                passed_tests += 1
            else:
                action_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Pattern Validity Score: {avg_pattern_score:.2f}")
            report.append(f"- Meets Patterns: {'✅' if meets_patterns else '❌'}")
            
            # Add engagement pattern analysis
            report.append("\n#### Engagement Pattern Analysis")
            engagement_patterns = results[0]["engagement_patterns"]
            
            report.append("\n##### Value Realization")
            vr = engagement_patterns["value_realization"]
            report.append(f"- Essential Completion: {vr['essential_completion']:.1%}")
            report.append(f"- Essential Satisfaction: {vr['essential_satisfaction']:.1%}")
            report.append(f"- Value Perception: {vr['value_perception']:.1%}")
            
            report.append("\n##### Progressive Disclosure")
            dp = engagement_patterns["disclosure_progression"]
            report.append(f"- Essential to Extended Ratio: {dp['essential_to_extended_ratio']:.2f}")
            report.append(f"- Extended to Comprehensive Ratio: {dp['extended_to_comprehensive_ratio']:.2f}")
            report.append(f"- Progression Pattern Valid: {'✅' if dp['progression_pattern_valid'] else '❌'}")
            
            report.append("\n##### Emotional Progression")
            ep = engagement_patterns["emotional_patterns"]
            report.append(f"- Anxiety Reduction: {ep['anxiety_reduction']:.1%}")
            report.append(f"- Curiosity Satisfaction: {ep['curiosity_satisfaction']:.1%}")
            report.append(f"- Motivation Development: {ep['motivation_development']:.1%}")
            report.append(f"- Emotional Alignment Valid: {'✅' if ep['emotional_alignment_valid'] else '❌'}")
            
            report.append("\n##### Persona Alignment")
            pa = engagement_patterns["persona_alignment"]
            report.append(f"- Expected Pattern Match: {'✅' if pa['expected_pattern_match'] else '❌'}")
            report.append(f"- Behavioral Confirmation: {'✅' if pa['behavioral_confirmation'] else '❌'}")
            report.append(f"- Adaptation Effectiveness: {pa['adaptation_effectiveness']:.2f}")
            
            # Add pattern details
            report.append("\n#### Pattern Analysis")
            pattern_alignment = results[0]["pattern_alignment"]
            
            report.append("##### Progressive Disclosure")
            pd = pattern_alignment["progressive_disclosure"]
            report.append(f"- Essential: {pd['essential_rate']:.1%}")
            report.append(f"- Extended: {pd['extended_rate']:.1%}")
            report.append(f"- Comprehensive: {pd['comprehensive_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Persona Differentiation")
            pd = pattern_alignment["persona_differentiation"]
            report.append(f"- Completion Rate: {pd['completion_rate']:.1%}")
            report.append(f"- Expected Range: {pd['expected_range'][0]:.1%} - {pd['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Emotional Alignment")
            ea = pattern_alignment["emotional_alignment"]
            report.append(f"- Anxiety Rate: {ea['anxiety_rate']:.1%}")
            report.append(f"- Expected Range: {ea['expected_range'][0]:.1%} - {ea['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if ea['meets_pattern'] else '❌'}")
            
            report.append("\n##### Phase Progression")
            pp = pattern_alignment["phase_progression"]
            report.append(f"- Completion Rate: {pp['completion_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pp['meets_pattern'] else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if action_passed else '❌ Failed'}")
        
        # Continuity Phase
        report.append("\n\n## Continuity Phase Validation")
        continuity_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_phase(persona_type, "continuity", scenario["journey"])
                results.append(result)
            
            # Calculate averages and pattern validity
            avg_pattern_score = sum(r["pattern_validity_score"] for r in results) / len(results)
            meets_patterns = all(r["phase_passed"] for r in results)
            
            if meets_patterns:
                passed_tests += 1
            else:
                continuity_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Pattern Validity Score: {avg_pattern_score:.2f}")
            report.append(f"- Meets Patterns: {'✅' if meets_patterns else '❌'}")
            
            # Add engagement pattern analysis
            report.append("\n#### Engagement Pattern Analysis")
            engagement_patterns = results[0]["engagement_patterns"]
            
            report.append("\n##### Value Realization")
            vr = engagement_patterns["value_realization"]
            report.append(f"- Essential Completion: {vr['essential_completion']:.1%}")
            report.append(f"- Essential Satisfaction: {vr['essential_satisfaction']:.1%}")
            report.append(f"- Value Perception: {vr['value_perception']:.1%}")
            
            report.append("\n##### Progressive Disclosure")
            dp = engagement_patterns["disclosure_progression"]
            report.append(f"- Essential to Extended Ratio: {dp['essential_to_extended_ratio']:.2f}")
            report.append(f"- Extended to Comprehensive Ratio: {dp['extended_to_comprehensive_ratio']:.2f}")
            report.append(f"- Progression Pattern Valid: {'✅' if dp['progression_pattern_valid'] else '❌'}")
            
            report.append("\n##### Emotional Progression")
            ep = engagement_patterns["emotional_patterns"]
            report.append(f"- Anxiety Reduction: {ep['anxiety_reduction']:.1%}")
            report.append(f"- Curiosity Satisfaction: {ep['curiosity_satisfaction']:.1%}")
            report.append(f"- Motivation Development: {ep['motivation_development']:.1%}")
            report.append(f"- Emotional Alignment Valid: {'✅' if ep['emotional_alignment_valid'] else '❌'}")
            
            report.append("\n##### Persona Alignment")
            pa = engagement_patterns["persona_alignment"]
            report.append(f"- Expected Pattern Match: {'✅' if pa['expected_pattern_match'] else '❌'}")
            report.append(f"- Behavioral Confirmation: {'✅' if pa['behavioral_confirmation'] else '❌'}")
            report.append(f"- Adaptation Effectiveness: {pa['adaptation_effectiveness']:.2f}")
            
            # Add pattern details
            report.append("\n#### Pattern Analysis")
            pattern_alignment = results[0]["pattern_alignment"]
            
            report.append("##### Progressive Disclosure")
            pd = pattern_alignment["progressive_disclosure"]
            report.append(f"- Essential: {pd['essential_rate']:.1%}")
            report.append(f"- Extended: {pd['extended_rate']:.1%}")
            report.append(f"- Comprehensive: {pd['comprehensive_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Persona Differentiation")
            pd = pattern_alignment["persona_differentiation"]
            report.append(f"- Completion Rate: {pd['completion_rate']:.1%}")
            report.append(f"- Expected Range: {pd['expected_range'][0]:.1%} - {pd['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pd['meets_pattern'] else '❌'}")
            
            report.append("\n##### Emotional Alignment")
            ea = pattern_alignment["emotional_alignment"]
            report.append(f"- Anxiety Rate: {ea['anxiety_rate']:.1%}")
            report.append(f"- Expected Range: {ea['expected_range'][0]:.1%} - {ea['expected_range'][1]:.1%}")
            report.append(f"- Pattern Valid: {'✅' if ea['meets_pattern'] else '❌'}")
            
            report.append("\n##### Phase Progression")
            pp = pattern_alignment["phase_progression"]
            report.append(f"- Completion Rate: {pp['completion_rate']:.1%}")
            report.append(f"- Pattern Valid: {'✅' if pp['meets_pattern'] else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if continuity_passed else '❌ Failed'}")
        
        # Phase Transitions
        report.append("\n\n## Phase Transitions Validation")
        transitions_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_phase_transitions(scenario["journey"])
                results.append(result)
            
            avg_transitions = sum(r["num_transitions"] for r in results) / len(results)
            meets_threshold = all(r["meets_threshold"] for r in results)
            
            if meets_threshold:
                passed_tests += 1
            else:
                transitions_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Average Phase Transitions: {avg_transitions:.1f}")
            report.append(f"- Meets Threshold: {'✅' if meets_threshold else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if transitions_passed else '❌ Failed'}")
        
        # Summary
        report.insert(2, f"\n## Test Results Summary")
        report.insert(3, f"Total Tests: {total_tests}")
        report.insert(4, f"Passed Tests: {passed_tests}")
        report.insert(5, f"Failed Tests: {total_tests - passed_tests}\n")
        
        # Save report
        output_dir = Path("output/test_scenarios")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / "journey_phase_validation.md", "w") as f:
            f.write("\n".join(report))
        
        print("Journey phase validation report has been generated and saved to output/test_scenarios/journey_phase_validation.md")

if __name__ == "__main__":
    validator = JourneyPhaseValidator()
    validator.generate_report() 