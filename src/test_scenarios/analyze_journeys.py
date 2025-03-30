import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime

def load_scenarios() -> Dict[str, List[Dict[str, Any]]]:
    """Load all test scenarios."""
    scenarios = {}
    scenario_dir = Path("output") / "test_scenarios"
    
    for scenario_file in scenario_dir.glob("*_scenarios.json"):
        scenario_type = scenario_file.stem.replace("_scenarios", "")
        with open(scenario_file, "r") as f:
            scenarios[scenario_type] = json.load(f)
    
    return scenarios

def analyze_emotional_states(scenarios: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze emotional states across different persona types."""
    emotional_analysis = defaultdict(lambda: defaultdict(int))
    
    for scenario_type, scenario_list in scenarios.items():
        for scenario in scenario_list:
            persona_type = scenario["user"]["persona_type"]
            for step in scenario["journey"]:
                emotional_analysis[persona_type][step["emotional_state"]] += 1
    
    return dict(emotional_analysis)

def analyze_completion_rates(scenarios: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze completion rates for different steps across persona types."""
    completion_analysis = defaultdict(lambda: defaultdict(lambda: {"completed": 0, "total": 0}))
    
    for scenario_type, scenario_list in scenarios.items():
        for scenario in scenario_list:
            persona_type = scenario["user"]["persona_type"]
            for step in scenario["journey"]:
                completion_analysis[persona_type][step["step"]]["total"] += 1
                if step["completion_status"] == "completed":
                    completion_analysis[persona_type][step["step"]]["completed"] += 1
    
    return dict(completion_analysis)

def analyze_journey_durations(scenarios: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze journey durations across persona types."""
    duration_analysis = defaultdict(list)
    
    for scenario_type, scenario_list in scenarios.items():
        for scenario in scenario_list:
            persona_type = scenario["user"]["persona_type"]
            if len(scenario["journey"]) >= 2:
                start_time = datetime.fromisoformat(scenario["journey"][0]["timestamp"])
                end_time = datetime.fromisoformat(scenario["journey"][-1]["timestamp"])
                duration = (end_time - start_time).days
                duration_analysis[persona_type].append(duration)
    
    return {
        persona_type: {
            "min_days": min(durations),
            "max_days": max(durations),
            "avg_days": sum(durations) / len(durations),
            "total_journeys": len(durations)
        }
        for persona_type, durations in duration_analysis.items()
    }

def analyze_expected_outcomes(scenarios: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze expected outcomes across persona types."""
    outcome_analysis = defaultdict(lambda: defaultdict(int))
    
    for scenario_type, scenario_list in scenarios.items():
        for scenario in scenario_list:
            persona_type = scenario["user"]["persona_type"]
            for outcome, expected in scenario["expected_outcomes"].items():
                if expected:
                    outcome_analysis[persona_type][outcome] += 1
    
    return dict(outcome_analysis)

def analyze_risk_levels(scenarios: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze risk level distribution across persona types."""
    risk_analysis = defaultdict(lambda: defaultdict(int))
    
    for scenario_type, scenario_list in scenarios.items():
        for scenario in scenario_list:
            persona_type = scenario["user"]["persona_type"]
            risk_level = scenario["user"]["risk_level"]
            risk_analysis[persona_type][risk_level] += 1
    
    return dict(risk_analysis)

def print_journey_analysis(analysis_results: Dict[str, Any]) -> None:
    """Print detailed analysis of persona journeys."""
    print("\nPersona Journey Analysis")
    print("=" * 50)
    
    for persona_type in analysis_results["emotional_states"].keys():
        print(f"\n{persona_type.replace('_', ' ').title()} Analysis")
        print("-" * 30)
        
        # Emotional States
        print("\nEmotional States:")
        emotional_states = analysis_results["emotional_states"][persona_type]
        total_states = sum(emotional_states.values())
        for state, count in emotional_states.items():
            percentage = (count / total_states) * 100
            print(f"  {state}: {count} ({percentage:.1f}%)")
        
        # Completion Rates
        print("\nStep Completion Rates:")
        completion_rates = analysis_results["completion_rates"][persona_type]
        for step, stats in completion_rates.items():
            rate = (stats["completed"] / stats["total"]) * 100
            print(f"  {step}: {rate:.1f}% ({stats['completed']}/{stats['total']})")
        
        # Journey Durations
        print("\nJourney Durations:")
        durations = analysis_results["journey_durations"][persona_type]
        print(f"  Average: {durations['avg_days']:.1f} days")
        print(f"  Range: {durations['min_days']} - {durations['max_days']} days")
        print(f"  Total Journeys: {durations['total_journeys']}")
        
        # Expected Outcomes
        print("\nExpected Outcomes:")
        outcomes = analysis_results["expected_outcomes"][persona_type]
        for outcome, count in outcomes.items():
            print(f"  {outcome}: {count}")
        
        # Risk Levels
        print("\nRisk Level Distribution:")
        risk_levels = analysis_results["risk_levels"][persona_type]
        total_risks = sum(risk_levels.values())
        for risk_level, count in risk_levels.items():
            percentage = (count / total_risks) * 100
            print(f"  {risk_level}: {count} ({percentage:.1f}%)")

def save_analysis_results(analysis_results: Dict[str, Any]) -> None:
    """Save analysis results to JSON file."""
    output_file = Path("output") / "test_scenarios" / "journey_analysis.json"
    with open(output_file, "w") as f:
        json.dump(analysis_results, f, indent=2)

def main():
    """Run the journey analysis."""
    scenarios = load_scenarios()
    
    analysis_results = {
        "emotional_states": analyze_emotional_states(scenarios),
        "completion_rates": analyze_completion_rates(scenarios),
        "journey_durations": analyze_journey_durations(scenarios),
        "expected_outcomes": analyze_expected_outcomes(scenarios),
        "risk_levels": analyze_risk_levels(scenarios)
    }
    
    print_journey_analysis(analysis_results)
    save_analysis_results(analysis_results)

if __name__ == "__main__":
    main() 