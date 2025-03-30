import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict

from config.persona_config import PERSONA_TEMPLATES, PERSONA_DISTRIBUTION

def load_dataset() -> List[Dict[str, Any]]:
    """Load the complete profiles dataset."""
    with open("output/complete_profiles.json", "r") as f:
        return json.load(f)

def validate_structure(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate the structural integrity of the dataset."""
    required_fields = {
        "name", "persona_type", "age", "education", "risk_level",
        "screening_history", "life_events", "narrative_elements",
        "pain_points", "primary_motivations", "prevention_approach"
    }
    
    required_screening_fields = {
        "has_history", "frequency", "last_screening", "completion_rate"
    }
    
    required_narrative_fields = {
        "self_description", "health_goals"
    }
    
    required_event_fields = {
        "type", "date", "impact", "status"
    }
    
    validation_results = {
        "missing_fields": [],
        "invalid_types": [],
        "nested_structure_issues": []
    }
    
    for i, profile in enumerate(dataset):
        # Check required top-level fields
        missing = required_fields - set(profile.keys())
        if missing:
            validation_results["missing_fields"].append({
                "profile_index": i,
                "name": profile.get("name", "unknown"),
                "missing_fields": list(missing)
            })
        
        # Check screening history structure
        if "screening_history" in profile:
            missing = required_screening_fields - set(profile["screening_history"].keys())
            if missing:
                validation_results["nested_structure_issues"].append({
                    "profile_index": i,
                    "name": profile["name"],
                    "section": "screening_history",
                    "missing_fields": list(missing)
                })
        
        # Check narrative elements structure
        if "narrative_elements" in profile:
            missing = required_narrative_fields - set(profile["narrative_elements"].keys())
            if missing:
                validation_results["nested_structure_issues"].append({
                    "profile_index": i,
                    "name": profile["name"],
                    "section": "narrative_elements",
                    "missing_fields": list(missing)
                })
        
        # Check life events structure
        if "life_events" in profile:
            for j, event in enumerate(profile["life_events"]):
                missing = required_event_fields - set(event.keys())
                if missing:
                    validation_results["nested_structure_issues"].append({
                        "profile_index": i,
                        "name": profile["name"],
                        "section": f"life_events[{j}]",
                        "missing_fields": list(missing)
                    })
    
    return validation_results

def validate_demographics(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate demographic consistency with persona models."""
    validation_results = {
        "age_distribution": {},
        "education_distribution": {},
        "risk_level_distribution": {}
    }
    
    # Group profiles by persona type
    profiles_by_persona = defaultdict(list)
    for profile in dataset:
        profiles_by_persona[profile["persona_type"]].append(profile)
    
    for persona_type, profiles in profiles_by_persona.items():
        # Validate age ranges
        age_range = PERSONA_TEMPLATES[persona_type]["age_range"]
        ages = [p["age"] for p in profiles]
        out_of_range = [p for p in profiles if not age_range[0] <= p["age"] <= age_range[1]]
        
        validation_results["age_distribution"][persona_type] = {
            "count": len(profiles),
            "min_age": min(ages),
            "max_age": max(ages),
            "avg_age": sum(ages) / len(ages),
            "out_of_range": len(out_of_range)
        }
        
        # Validate education distribution
        edu_dist = PERSONA_TEMPLATES[persona_type]["education_distribution"]
        actual_edu_dist = defaultdict(int)
        for profile in profiles:
            actual_edu_dist[profile["education"]] += 1
        
        validation_results["education_distribution"][persona_type] = {
            "expected": edu_dist,
            "actual": dict(actual_edu_dist)
        }
        
        # Validate risk level distribution
        risk_levels = defaultdict(int)
        for profile in profiles:
            risk_levels[profile["risk_level"]] += 1
        
        validation_results["risk_level_distribution"][persona_type] = dict(risk_levels)
    
    return validation_results

def validate_behaviors(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate behavioral patterns in the dataset."""
    validation_results = {
        "screening_patterns": {},
        "life_event_patterns": {},
        "prevention_approaches": {}
    }
    
    # Group profiles by persona type
    profiles_by_persona = defaultdict(list)
    for profile in dataset:
        profiles_by_persona[profile["persona_type"]].append(profile)
    
    for persona_type, profiles in profiles_by_persona.items():
        # Validate screening patterns
        screening_stats = {
            "total": len(profiles),
            "has_history": sum(1 for p in profiles if p["screening_history"]["has_history"]),
            "frequencies": defaultdict(int),
            "completion_rates": []
        }
        
        for profile in profiles:
            screening_stats["frequencies"][profile["screening_history"]["frequency"]] += 1
            screening_stats["completion_rates"].append(
                profile["screening_history"]["completion_rate"]
            )
        
        validation_results["screening_patterns"][persona_type] = {
            "has_history_rate": screening_stats["has_history"] / screening_stats["total"],
            "frequency_distribution": dict(screening_stats["frequencies"]),
            "avg_completion_rate": sum(screening_stats["completion_rates"]) / len(screening_stats["completion_rates"])
        }
        
        # Validate life event patterns
        event_types = defaultdict(int)
        event_impacts = defaultdict(int)
        event_statuses = defaultdict(int)
        
        for profile in profiles:
            for event in profile["life_events"]:
                event_types[event["type"]] += 1
                event_impacts[event["impact"]] += 1
                event_statuses[event["status"]] += 1
        
        validation_results["life_event_patterns"][persona_type] = {
            "event_types": dict(event_types),
            "impacts": dict(event_impacts),
            "statuses": dict(event_statuses)
        }
        
        # Validate prevention approaches
        prevention_approaches = defaultdict(int)
        for profile in profiles:
            prevention_approaches[profile["prevention_approach"]] += 1
        
        validation_results["prevention_approaches"][persona_type] = dict(prevention_approaches)
    
    return validation_results

def validate_narratives(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate narrative authenticity in the dataset."""
    validation_results = {
        "narrative_consistency": {},
        "pain_point_alignment": {},
        "motivation_alignment": {}
    }
    
    # Group profiles by persona type
    profiles_by_persona = defaultdict(list)
    for profile in dataset:
        profiles_by_persona[profile["persona_type"]].append(profile)
    
    for persona_type, profiles in profiles_by_persona.items():
        # Check narrative consistency
        narrative_keywords = {
            "health_aware_avoider": ["anxiety", "avoid", "aware", "nervous"],
            "structured_system_seeker": ["system", "organized", "track", "plan"],
            "balanced_life_integrator": ["balance", "lifestyle", "wellness", "holistic"],
            "healthcare_professional": ["professional", "expertise", "evidence", "research"],
            "overlooked_risk_group": ["specific", "guidance", "unique", "tailored"]
        }
        
        keyword_counts = defaultdict(int)
        for profile in profiles:
            narrative = profile["narrative_elements"]
            for keyword in narrative_keywords[persona_type]:
                if keyword in narrative["self_description"].lower():
                    keyword_counts[keyword] += 1
                if keyword in narrative["health_goals"].lower():
                    keyword_counts[keyword] += 1
        
        validation_results["narrative_consistency"][persona_type] = dict(keyword_counts)
        
        # Check pain point alignment
        expected_pain_points = set(PERSONA_TEMPLATES[persona_type]["pain_points"])
        actual_pain_points = defaultdict(int)
        
        for profile in profiles:
            for point in profile["pain_points"]:
                actual_pain_points[point] += 1
        
        validation_results["pain_point_alignment"][persona_type] = {
            "expected": list(expected_pain_points),
            "actual": dict(actual_pain_points)
        }
        
        # Check motivation alignment
        expected_motivations = set(PERSONA_TEMPLATES[persona_type]["primary_motivations"])
        actual_motivations = defaultdict(int)
        
        for profile in profiles:
            for motivation in profile["primary_motivations"]:
                actual_motivations[motivation] += 1
        
        validation_results["motivation_alignment"][persona_type] = {
            "expected": list(expected_motivations),
            "actual": dict(actual_motivations)
        }
    
    return validation_results

def identify_edge_cases(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Identify potential edge cases and anomalies in the dataset."""
    edge_cases = {
        "unusual_age_combinations": [],
        "inconsistent_screening": [],
        "unusual_event_patterns": [],
        "narrative_anomalies": []
    }
    
    for profile in dataset:
        # Check unusual age combinations
        if profile["age"] < 25 and profile["screening_history"]["has_history"]:
            edge_cases["unusual_age_combinations"].append({
                "name": profile["name"],
                "age": profile["age"],
                "screening_history": profile["screening_history"]
            })
        
        # Check inconsistent screening patterns
        if (profile["screening_history"]["has_history"] and 
            profile["screening_history"]["frequency"] == "never"):
            edge_cases["inconsistent_screening"].append({
                "name": profile["name"],
                "screening_history": profile["screening_history"]
            })
        
        # Check unusual event patterns
        if len(profile["life_events"]) > 5:
            edge_cases["unusual_event_patterns"].append({
                "name": profile["name"],
                "event_count": len(profile["life_events"])
            })
        
        # Check narrative anomalies
        narrative = profile["narrative_elements"]
        if len(narrative["self_description"]) < 10 or len(narrative["health_goals"]) < 10:
            edge_cases["narrative_anomalies"].append({
                "name": profile["name"],
                "narrative_length": {
                    "self_description": len(narrative["self_description"]),
                    "health_goals": len(narrative["health_goals"])
                }
            })
    
    return edge_cases

def validate_synthetic_dataset() -> Dict[str, Any]:
    """Run comprehensive validation of the synthetic dataset."""
    dataset = load_dataset()
    
    validation_report = {
        "structural_integrity": validate_structure(dataset),
        "demographic_consistency": validate_demographics(dataset),
        "behavioral_patterns": validate_behaviors(dataset),
        "narrative_authenticity": validate_narratives(dataset),
        "edge_cases": identify_edge_cases(dataset)
    }
    
    # Save validation report
    output_file = Path("output") / "validation_report.json"
    with open(output_file, "w") as f:
        json.dump(validation_report, f, indent=2)
    
    return validation_report

def print_validation_summary(report: Dict[str, Any]) -> None:
    """Print a summary of the validation results."""
    print("\nValidation Report Summary")
    print("=" * 50)
    
    # Structural Integrity
    print("\nStructural Integrity:")
    print("-" * 20)
    if report["structural_integrity"]["missing_fields"]:
        print(f"Found {len(report['structural_integrity']['missing_fields'])} profiles with missing fields")
    if report["structural_integrity"]["nested_structure_issues"]:
        print(f"Found {len(report['structural_integrity']['nested_structure_issues'])} nested structure issues")
    
    # Demographic Consistency
    print("\nDemographic Consistency:")
    print("-" * 20)
    for persona_type, age_stats in report["demographic_consistency"]["age_distribution"].items():
        print(f"\n{persona_type.replace('_', ' ').title()}:")
        print(f"  Age Range: {age_stats['min_age']}-{age_stats['max_age']}")
        print(f"  Average Age: {age_stats['avg_age']:.1f}")
        if age_stats["out_of_range"] > 0:
            print(f"  ⚠️ {age_stats['out_of_range']} profiles out of age range")
    
    # Behavioral Patterns
    print("\nBehavioral Patterns:")
    print("-" * 20)
    for persona_type, patterns in report["behavioral_patterns"]["screening_patterns"].items():
        print(f"\n{persona_type.replace('_', ' ').title()}:")
        print(f"  Screening Rate: {patterns['has_history_rate']*100:.1f}%")
        print(f"  Average Completion Rate: {patterns['avg_completion_rate']*100:.1f}%")
    
    # Edge Cases
    print("\nEdge Cases:")
    print("-" * 20)
    for category, cases in report["edge_cases"].items():
        print(f"\n{category.replace('_', ' ').title()}:")
        print(f"  Found {len(cases)} cases")

def main():
    """Run the validation process and print results."""
    report = validate_synthetic_dataset()
    print_validation_summary(report)

if __name__ == "__main__":
    main() 