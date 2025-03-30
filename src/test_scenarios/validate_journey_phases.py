import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class JourneyPhaseValidator:
    def __init__(self):
        self.load_test_data()
        self.set_validation_thresholds()

    def load_test_data(self) -> None:
        """Load test data from JSON file."""
        with open("output/synthetic_customers.json", "r") as f:
            self.scenarios = json.load(f)

    def set_validation_thresholds(self) -> None:
        """Set validation thresholds for each persona type."""
        self.thresholds = {
            "health_aware_avoider": {
                "awareness": {
                    "anxiety": (0.4, 0.6),
                    "curiosity": (0.4, 0.6),
                    "completion": (0.3, 0.7)
                },
                "engagement": {
                    "engagement": (0.4, 0.7),
                    "reflection": (0.3, 0.6),
                    "completion": (0.4, 0.7)
                },
                "action": {
                    "motivation": (0.2, 0.5),
                    "determination": (0.2, 0.5),
                    "completion": (0.2, 0.5)
                },
                "continuity": {
                    "stability": (0.1, 0.3),
                    "reflection": (0.2, 0.4),
                    "completion": (0.1, 0.3)
                }
            },
            "structured_system_seeker": {
                "awareness": {
                    "anxiety": (0.0, 0.3),
                    "curiosity": (0.6, 0.9),
                    "completion": (0.6, 0.9)
                },
                "engagement": {
                    "engagement": (0.6, 0.9),
                    "reflection": (0.5, 0.8),
                    "completion": (0.7, 0.95)
                },
                "action": {
                    "motivation": (0.5, 0.8),
                    "determination": (0.5, 0.8),
                    "completion": (0.4, 0.7)
                },
                "continuity": {
                    "stability": (0.4, 0.7),
                    "reflection": (0.4, 0.7),
                    "completion": (0.3, 0.6)
                }
            },
            "balanced_life_integrator": {
                "awareness": {
                    "anxiety": (0.0, 0.3),
                    "curiosity": (0.4, 0.7),
                    "completion": (0.5, 0.8)
                },
                "engagement": {
                    "engagement": (0.5, 0.8),
                    "reflection": (0.4, 0.7),
                    "completion": (0.5, 0.8)
                },
                "action": {
                    "motivation": (0.4, 0.7),
                    "determination": (0.4, 0.7),
                    "completion": (0.4, 0.7)
                },
                "continuity": {
                    "stability": (0.2, 0.5),
                    "reflection": (0.3, 0.6),
                    "completion": (0.2, 0.5)
                }
            },
            "healthcare_professional": {
                "awareness": {
                    "anxiety": (0.0, 0.2),
                    "curiosity": (0.7, 0.95),
                    "completion": (0.7, 0.95)
                },
                "engagement": {
                    "engagement": (0.7, 0.95),
                    "reflection": (0.6, 0.9),
                    "completion": (0.8, 0.95)
                },
                "action": {
                    "motivation": (0.6, 0.9),
                    "determination": (0.7, 0.95),
                    "completion": (0.7, 0.9)
                },
                "continuity": {
                    "stability": (0.4, 0.7),
                    "reflection": (0.4, 0.7),
                    "completion": (0.4, 0.7)
                }
            },
            "overlooked_risk_group": {
                "awareness": {
                    "anxiety": (0.6, 0.9),
                    "curiosity": (0.1, 0.3),
                    "completion": (0.3, 0.6)
                },
                "engagement": {
                    "engagement": (0.3, 0.6),
                    "reflection": (0.2, 0.5),
                    "completion": (0.3, 0.6)
                },
                "action": {
                    "motivation": (0.2, 0.5),
                    "determination": (0.2, 0.4),
                    "completion": (0.2, 0.4)
                },
                "continuity": {
                    "stability": (0.2, 0.4),
                    "reflection": (0.2, 0.4),
                    "completion": (0.1, 0.3)
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

    def get_phase_steps(self, journey: List[Dict[str, Any]], phase_steps: List[str]) -> List[Dict[str, Any]]:
        """Get steps for a specific phase."""
        return [step for step in journey if step["step"] in phase_steps]

    def validate_awareness_phase(self, persona_type: str, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate awareness phase for a persona."""
        awareness_steps = ["initial_registration", "risk_assessment", "health_history", "initial_preferences"]
        steps = self.get_phase_steps(journey, awareness_steps)
        
        completion_rate = self.calculate_completion_rate(steps)
        emotional_rates = self.calculate_emotional_rates(steps)
        thresholds = self.thresholds[persona_type]["awareness"]
        
        emotional_progression = []
        for i in range(len(steps)-1):
            if i+1 < len(steps):
                emotional_progression.append([steps[i]["emotional_state"], steps[i+1]["emotional_state"]])
        
        return {
            "emotional_progression": emotional_progression,
            "anxiety_rate": emotional_rates["anxiety"],
            "curiosity_rate": emotional_rates["curiosity"],
            "completion_rate": completion_rate,
            "meets_thresholds": (
                thresholds["anxiety"][0] <= emotional_rates["anxiety"] <= thresholds["anxiety"][1] and
                thresholds["curiosity"][0] <= emotional_rates["curiosity"] <= thresholds["curiosity"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        }

    def validate_engagement_phase(self, persona_type: str, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate engagement phase for a persona."""
        engagement_steps = ["narrative_capture", "life_events_timeline", "support_network", "resource_exploration"]
        steps = self.get_phase_steps(journey, engagement_steps)
        
        completion_rate = self.calculate_completion_rate(steps)
        emotional_rates = self.calculate_emotional_rates(steps)
        thresholds = self.thresholds[persona_type]["engagement"]
        
        return {
            "completion_rate": completion_rate,
            "engagement_rate": emotional_rates["engagement"],
            "reflection_rate": emotional_rates["reflection"],
            "meets_thresholds": (
                thresholds["engagement"][0] <= emotional_rates["engagement"] <= thresholds["engagement"][1] and
                thresholds["reflection"][0] <= emotional_rates["reflection"] <= thresholds["reflection"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        }

    def validate_action_phase(self, persona_type: str, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate action phase for a persona."""
        action_steps = ["prevention_plan", "support_plan", "action_planning", "resource_commitment"]
        steps = self.get_phase_steps(journey, action_steps)
        
        completion_rate = self.calculate_completion_rate(steps)
        emotional_rates = self.calculate_emotional_rates(steps)
        thresholds = self.thresholds[persona_type]["action"]
        
        return {
            "completion_rate": completion_rate,
            "motivation_rate": emotional_rates["engagement"],
            "determination_rate": sum(1 for step in steps if step["emotional_state"] == "determined") / len(steps) if steps else 0,
            "meets_thresholds": (
                thresholds["motivation"][0] <= emotional_rates["engagement"] <= thresholds["motivation"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        }

    def validate_continuity_phase(self, persona_type: str, journey: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate continuity phase for a persona."""
        continuity_steps = ["follow_up", "risk_awareness", "barrier_identification", "long_term_planning"]
        steps = self.get_phase_steps(journey, continuity_steps)
        
        completion_rate = self.calculate_completion_rate(steps)
        emotional_rates = self.calculate_emotional_rates(steps)
        thresholds = self.thresholds[persona_type]["continuity"]
        
        return {
            "completion_rate": completion_rate,
            "stability_rate": sum(1 for step in steps if step["emotional_state"] == "stable") / len(steps) if steps else 0,
            "reflection_rate": emotional_rates["reflection"],
            "meets_thresholds": (
                thresholds["stability"][0] <= emotional_rates["reflection"] <= thresholds["stability"][1] and
                thresholds["completion"][0] <= completion_rate <= thresholds["completion"][1]
            )
        }

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
            "transitions": phase_transitions
        }

    def get_step_phase(self, step: str) -> str:
        """Get the phase for a step."""
        phase_steps = {
            "awareness": ["initial_registration", "risk_assessment", "health_history", "initial_preferences"],
            "engagement": ["narrative_capture", "life_events_timeline", "support_network", "resource_exploration"],
            "action": ["prevention_plan", "support_plan", "action_planning", "resource_commitment"],
            "continuity": ["follow_up", "risk_awareness", "barrier_identification", "long_term_planning"]
        }
        
        for phase, steps in phase_steps.items():
            if step in steps:
                return phase
        return "unknown"

    def generate_report(self) -> None:
        """Generate validation report."""
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
                result = self.validate_awareness_phase(persona_type, scenario["journey"])
                results.append(result)
            
            avg_anxiety = sum(r["anxiety_rate"] for r in results) / len(results)
            avg_curiosity = sum(r["curiosity_rate"] for r in results) / len(results)
            meets_thresholds = all(r["meets_thresholds"] for r in results)
            
            if meets_thresholds:
                passed_tests += 1
            else:
                awareness_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Average Anxiety Rate: {avg_anxiety:.1%}")
            report.append(f"- Average Curiosity Rate: {avg_curiosity:.1%}")
            report.append(f"- Meets Thresholds: {'✅' if meets_thresholds else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if awareness_passed else '❌ Failed'}")
        
        # Engagement Phase
        report.append("\n\n## Engagement Phase Validation")
        engagement_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_engagement_phase(persona_type, scenario["journey"])
                results.append(result)
            
            avg_completion = sum(r["completion_rate"] for r in results) / len(results)
            meets_thresholds = all(r["meets_thresholds"] for r in results)
            
            if meets_thresholds:
                passed_tests += 1
            else:
                engagement_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Average Completion Rate: {avg_completion:.1%}")
            report.append(f"- Meets Thresholds: {'✅' if meets_thresholds else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if engagement_passed else '❌ Failed'}")
        
        # Action Phase
        report.append("\n\n## Action Phase Validation")
        action_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_action_phase(persona_type, scenario["journey"])
                results.append(result)
            
            avg_completion = sum(r["completion_rate"] for r in results) / len(results)
            meets_thresholds = all(r["meets_thresholds"] for r in results)
            
            if meets_thresholds:
                passed_tests += 1
            else:
                action_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Average Completion Rate: {avg_completion:.1%}")
            report.append(f"- Meets Thresholds: {'✅' if meets_thresholds else '❌'}")
        
        report.append(f"\nPhase Status: {'✅ Passed' if action_passed else '❌ Failed'}")
        
        # Continuity Phase
        report.append("\n\n## Continuity Phase Validation")
        continuity_passed = True
        for persona_type, scenarios in persona_scenarios.items():
            total_tests += 1
            results = []
            for scenario in scenarios:
                result = self.validate_continuity_phase(persona_type, scenario["journey"])
                results.append(result)
            
            avg_completion = sum(r["completion_rate"] for r in results) / len(results)
            meets_thresholds = all(r["meets_thresholds"] for r in results)
            
            if meets_thresholds:
                passed_tests += 1
            else:
                continuity_passed = False
            
            report.append(f"\n### {persona_type.replace('_', ' ').title()}")
            report.append(f"- Average Completion Rate: {avg_completion:.1%}")
            report.append(f"- Meets Thresholds: {'✅' if meets_thresholds else '❌'}")
        
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
            meets_threshold = 0 < avg_transitions <= 3  # Expecting 1-3 transitions
            
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