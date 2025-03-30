import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pytest
from datetime import datetime, timedelta

class TestExecutionFramework:
    def __init__(self):
        self.test_results = []
        self.test_cases = []
        self.load_test_data()

    def load_test_data(self) -> None:
        """Load test data from JSON files."""
        with open("output/test_scenarios/journey_analysis.json", "r") as f:
            self.analysis_data = json.load(f)
        
        with open("output/test_scenarios/first_time_user_scenarios.json", "r") as f:
            self.first_time_scenarios = json.load(f)
        
        with open("output/test_scenarios/life_transition_scenarios.json", "r") as f:
            self.life_transition_scenarios = json.load(f)
        
        with open("output/test_scenarios/prevention_conversion_scenarios.json", "r") as f:
            self.prevention_scenarios = json.load(f)

    def validate_persona_distribution(self) -> Dict[str, Any]:
        """Validate the distribution of personas across scenarios."""
        expected_distribution = {
            "health_aware_avoider": 0.30,
            "structured_system_seeker": 0.25,
            "balanced_life_integrator": 0.20,
            "healthcare_professional": 0.15,
            "overlooked_risk_group": 0.10
        }
        
        actual_distribution = {}
        total_scenarios = len(self.first_time_scenarios)
        
        for scenario in self.first_time_scenarios:
            persona_type = scenario["user"]["persona_type"]
            actual_distribution[persona_type] = actual_distribution.get(persona_type, 0) + 1
        
        for persona_type in actual_distribution:
            actual_distribution[persona_type] /= total_scenarios
        
        return {
            "test_name": "Persona Distribution Validation",
            "expected": expected_distribution,
            "actual": actual_distribution,
            "passed": all(abs(actual_distribution.get(k, 0) - v) < 0.05 
                         for k, v in expected_distribution.items())
        }

    def validate_emotional_states(self) -> Dict[str, Any]:
        """Validate emotional state patterns for each persona."""
        results = []
        
        for persona_type, states in self.analysis_data["emotional_states"].items():
            total_states = sum(states.values())
            if total_states == 0:
                continue
                
            # Check if emotional states sum to 100%
            state_percentages = {k: (v / total_states) * 100 for k, v in states.items()}
            total_percentage = sum(state_percentages.values())
            
            results.append({
                "persona_type": persona_type,
                "total_percentage": total_percentage,
                "state_distribution": state_percentages,
                "passed": abs(total_percentage - 100) < 0.01
            })
        
        return {
            "test_name": "Emotional States Validation",
            "results": results,
            "passed": all(r["passed"] for r in results)
        }

    def validate_journey_completion(self) -> Dict[str, Any]:
        """Validate journey completion patterns."""
        results = []
        
        for persona_type, steps in self.analysis_data["completion_rates"].items():
            step_results = []
            for step, stats in steps.items():
                completion_rate = (stats["completed"] / stats["total"]) * 100
                step_results.append({
                    "step": step,
                    "completion_rate": completion_rate,
                    "passed": 0 <= completion_rate <= 100
                })
            
            results.append({
                "persona_type": persona_type,
                "step_results": step_results,
                "passed": all(r["passed"] for r in step_results)
            })
        
        return {
            "test_name": "Journey Completion Validation",
            "results": results,
            "passed": all(r["passed"] for r in results)
        }

    def validate_risk_levels(self) -> Dict[str, Any]:
        """Validate risk level distribution."""
        results = []
        
        for persona_type, risks in self.analysis_data["risk_levels"].items():
            total_risks = sum(risks.values())
            if total_risks == 0:
                continue
                
            risk_percentages = {k: (v / total_risks) * 100 for k, v in risks.items()}
            total_percentage = sum(risk_percentages.values())
            
            results.append({
                "persona_type": persona_type,
                "total_percentage": total_percentage,
                "risk_distribution": risk_percentages,
                "passed": abs(total_percentage - 100) < 0.01
            })
        
        return {
            "test_name": "Risk Levels Validation",
            "results": results,
            "passed": all(r["passed"] for r in results)
        }

    def validate_scenario_consistency(self) -> Dict[str, Any]:
        """Validate consistency across different scenario types."""
        results = []
        
        # Check persona types are consistent across scenario types
        persona_types = set()
        for scenario in self.first_time_scenarios:
            persona_types.add(scenario["user"]["persona_type"])
        
        for scenario in self.life_transition_scenarios:
            if scenario["user"]["persona_type"] not in persona_types:
                results.append({
                    "test": "Persona Type Consistency",
                    "scenario_type": "life_transition",
                    "persona_type": scenario["user"]["persona_type"],
                    "passed": False
                })
        
        for scenario in self.prevention_scenarios:
            if scenario["user"]["persona_type"] not in persona_types:
                results.append({
                    "test": "Persona Type Consistency",
                    "scenario_type": "prevention",
                    "persona_type": scenario["user"]["persona_type"],
                    "passed": False
                })
        
        return {
            "test_name": "Scenario Consistency Validation",
            "results": results,
            "passed": not results
        }

    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all validation tests."""
        tests = [
            self.validate_persona_distribution(),
            self.validate_emotional_states(),
            self.validate_journey_completion(),
            self.validate_risk_levels(),
            self.validate_scenario_consistency()
        ]
        
        self.test_results = tests
        return tests

    def generate_test_report(self) -> None:
        """Generate a test execution report."""
        if not self.test_results:
            self.run_all_tests()
        
        report = [
            "# Test Execution Report",
            f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Test Results Summary",
            f"Total Tests: {len(self.test_results)}",
            f"Passed Tests: {sum(1 for t in self.test_results if t['passed'])}",
            f"Failed Tests: {sum(1 for t in self.test_results if not t['passed'])}",
            "\n## Detailed Test Results"
        ]
        
        for test in self.test_results:
            report.append(f"\n### {test['test_name']}")
            report.append(f"Status: {'✅ Passed' if test['passed'] else '❌ Failed'}")
            
            if "results" in test:
                for result in test["results"]:
                    report.append("\n#### " + result.get("persona_type", "General"))
                    for key, value in result.items():
                        if key not in ["persona_type", "passed"]:
                            report.append(f"- {key}: {value}")
            
            if "expected" in test:
                report.append("\n#### Expected vs Actual")
                for key in test["expected"]:
                    expected = test["expected"][key]
                    actual = test["actual"].get(key, 0)
                    report.append(f"- {key}: Expected {expected:.2%}, Actual {actual:.2%}")
        
        # Save report
        output_dir = Path("output/test_scenarios")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "test_execution_report.md", "w") as f:
            f.write("\n".join(report))
        
        print("Test execution report has been generated and saved to output/test_scenarios/test_execution_report.md")

if __name__ == "__main__":
    framework = TestExecutionFramework()
    framework.generate_test_report() 