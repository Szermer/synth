import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

def load_profiles() -> List[Dict[str, Any]]:
    """Load the complete profiles dataset."""
    with open("output/complete_profiles.json", "r") as f:
        return json.load(f)

def create_first_time_user_scenario(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Create a first-time user journey scenario."""
    return {
        "scenario_type": "first_time_user",
        "user": {
            "name": profile["name"],
            "age": profile["age"],
            "persona_type": profile["persona_type"],
            "risk_level": profile["risk_level"],
            "screening_history": profile["screening_history"]
        },
        "journey": [
            {
                "step": "initial_registration",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                "actions": ["create_account", "complete_basic_profile"],
                "emotional_state": "neutral",
                "completion_status": "completed"
            },
            {
                "step": "risk_assessment",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                "actions": ["view_risk_factors", "complete_risk_questionnaire"],
                "emotional_state": "anxious" if profile["persona_type"] == "health_aware_avoider" else "engaged",
                "completion_status": "completed"
            },
            {
                "step": "prevention_plan",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 3))).isoformat(),
                "actions": ["view_recommendations", "review_prevention_options"],
                "emotional_state": "engaged",
                "completion_status": "in_progress"
            }
        ],
        "expected_outcomes": {
            "risk_assessment_completion": True,
            "prevention_plan_creation": True,
            "screening_scheduling": profile["persona_type"] in ["structured_system_seeker", "healthcare_professional"]
        }
    }

def create_life_transition_scenario(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Create a life transition scenario."""
    # Find a recent life event
    recent_events = [
        event for event in profile["life_events"]
        if event["impact"] in ["high", "moderate"]
        and datetime.fromisoformat(event["date"]) > datetime.now() - timedelta(days=365)
    ]
    
    if not recent_events:
        return None
    
    event = random.choice(recent_events)
    
    return {
        "scenario_type": "life_transition",
        "user": {
            "name": profile["name"],
            "age": profile["age"],
            "persona_type": profile["persona_type"],
            "risk_level": profile["risk_level"],
            "screening_history": profile["screening_history"]
        },
        "trigger_event": event,
        "journey": [
            {
                "step": "event_trigger",
                "timestamp": event["date"],
                "actions": ["receive_transition_notification", "view_impact_assessment"],
                "emotional_state": "concerned" if event["impact"] == "high" else "attentive",
                "completion_status": "completed"
            },
            {
                "step": "support_plan",
                "timestamp": (datetime.fromisoformat(event["date"]) + timedelta(days=random.randint(1, 14))).isoformat(),
                "actions": ["review_support_options", "select_support_services"],
                "emotional_state": "engaged",
                "completion_status": "completed"
            },
            {
                "step": "follow_up",
                "timestamp": (datetime.fromisoformat(event["date"]) + timedelta(days=random.randint(30, 90))).isoformat(),
                "actions": ["complete_follow_up_assessment", "update_prevention_plan"],
                "emotional_state": "stable",
                "completion_status": "planned"
            }
        ],
        "expected_outcomes": {
            "support_plan_creation": True,
            "prevention_plan_update": True,
            "follow_up_completion": profile["persona_type"] in ["structured_system_seeker", "healthcare_professional"]
        }
    }

def create_prevention_conversion_scenario(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Create a prevention conversion scenario for non-screeners."""
    if profile["screening_history"]["has_history"]:
        return None
    
    return {
        "scenario_type": "prevention_conversion",
        "user": {
            "name": profile["name"],
            "age": profile["age"],
            "persona_type": profile["persona_type"],
            "risk_level": profile["risk_level"],
            "screening_history": profile["screening_history"]
        },
        "journey": [
            {
                "step": "risk_awareness",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat(),
                "actions": ["view_risk_education", "complete_awareness_quiz"],
                "emotional_state": "engaged",
                "completion_status": "completed"
            },
            {
                "step": "barrier_identification",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                "actions": ["identify_barriers", "review_support_options"],
                "emotional_state": "reflective",
                "completion_status": "completed"
            },
            {
                "step": "action_planning",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                "actions": ["create_action_plan", "set_reminders"],
                "emotional_state": "motivated",
                "completion_status": "in_progress"
            }
        ],
        "expected_outcomes": {
            "risk_awareness_completion": True,
            "barrier_identification": True,
            "screening_scheduling": profile["persona_type"] == "structured_system_seeker"
        }
    }

def generate_test_scenarios() -> Dict[str, List[Dict[str, Any]]]:
    """Generate test scenarios for each persona type."""
    profiles = load_profiles()
    
    scenarios = {
        "first_time_user": [],
        "life_transition": [],
        "prevention_conversion": []
    }
    
    # Generate scenarios for each profile
    for profile in profiles:
        # First-time user scenarios
        scenarios["first_time_user"].append(create_first_time_user_scenario(profile))
        
        # Life transition scenarios
        transition_scenario = create_life_transition_scenario(profile)
        if transition_scenario:
            scenarios["life_transition"].append(transition_scenario)
        
        # Prevention conversion scenarios
        conversion_scenario = create_prevention_conversion_scenario(profile)
        if conversion_scenario:
            scenarios["prevention_conversion"].append(conversion_scenario)
    
    return scenarios

def save_scenarios(scenarios: Dict[str, List[Dict[str, Any]]]) -> None:
    """Save the generated scenarios to JSON files."""
    output_dir = Path("output") / "test_scenarios"
    output_dir.mkdir(exist_ok=True)
    
    for scenario_type, scenario_list in scenarios.items():
        output_file = output_dir / f"{scenario_type}_scenarios.json"
        with open(output_file, "w") as f:
            json.dump(scenario_list, f, indent=2)

def print_scenario_summary(scenarios: Dict[str, List[Dict[str, Any]]]) -> None:
    """Print a summary of the generated scenarios."""
    print("\nTest Scenario Generation Summary")
    print("=" * 50)
    
    for scenario_type, scenario_list in scenarios.items():
        print(f"\n{scenario_type.replace('_', ' ').title()} Scenarios:")
        print(f"  Total Scenarios: {len(scenario_list)}")
        
        # Group by persona type
        persona_counts = {}
        for scenario in scenario_list:
            persona_type = scenario["user"]["persona_type"]
            persona_counts[persona_type] = persona_counts.get(persona_type, 0) + 1
        
        print("\n  Distribution by Persona Type:")
        for persona_type, count in persona_counts.items():
            print(f"    {persona_type.replace('_', ' ').title()}: {count}")

def main():
    """Generate and save test scenarios."""
    scenarios = generate_test_scenarios()
    save_scenarios(scenarios)
    print_scenario_summary(scenarios)

if __name__ == "__main__":
    main() 