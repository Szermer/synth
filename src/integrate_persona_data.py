import json
from pathlib import Path
from typing import Dict, List, Any
import random
from datetime import datetime, timedelta

from config.persona_config import PERSONA_TEMPLATES, PERSONA_DISTRIBUTION

def load_persona_names() -> Dict[str, List[str]]:
    """Load the generated persona names from JSON file."""
    with open("output/persona_names.json", "r") as f:
        return json.load(f)

def generate_age(persona_type: str) -> int:
    """Generate age based on persona type's age range."""
    age_range = PERSONA_TEMPLATES[persona_type]["age_range"]
    return random.randint(age_range[0], age_range[1])

def generate_education(persona_type: str) -> str:
    """Generate education level based on persona type's distribution."""
    edu_dist = PERSONA_TEMPLATES[persona_type]["education_distribution"]
    return random.choices(list(edu_dist.keys()), weights=list(edu_dist.values()))[0]

def generate_risk_level(persona_type: str) -> str:
    """Generate risk level based on persona type's characteristics."""
    if persona_type == "health_aware_avoider":
        return random.choices(["low", "moderate"], weights=[0.7, 0.3])[0]
    elif persona_type == "structured_system_seeker":
        return random.choices(["low", "moderate"], weights=[0.8, 0.2])[0]
    elif persona_type == "balanced_life_integrator":
        return random.choices(["low", "moderate"], weights=[0.75, 0.25])[0]
    elif persona_type == "healthcare_professional":
        return random.choices(["low", "moderate"], weights=[0.85, 0.15])[0]
    else:  # overlooked_risk_group
        return random.choices(["low", "moderate"], weights=[0.6, 0.4])[0]

def generate_screening_history(persona_type: str) -> Dict[str, Any]:
    """Generate screening history based on persona type."""
    if persona_type == "healthcare_professional":
        return {
            "has_history": True,
            "frequency": "annual",
            "last_screening": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            "completion_rate": random.uniform(0.8, 1.0)
        }
    elif persona_type == "structured_system_seeker":
        return {
            "has_history": True,
            "frequency": random.choice(["annual", "biennial"]),
            "last_screening": (datetime.now() - timedelta(days=random.randint(0, 730))).isoformat(),
            "completion_rate": random.uniform(0.7, 0.9)
        }
    elif persona_type == "balanced_life_integrator":
        has_history = random.random() < 0.7
        if has_history:
            return {
                "has_history": True,
                "frequency": random.choice(["annual", "biennial", "irregular"]),
                "last_screening": (datetime.now() - timedelta(days=random.randint(0, 1095))).isoformat(),
                "completion_rate": random.uniform(0.5, 0.8)
            }
        else:
            return {
                "has_history": False,
                "frequency": "never",
                "last_screening": None,
                "completion_rate": 0.0
            }
    elif persona_type == "health_aware_avoider":
        has_history = random.random() < 0.3
        if has_history:
            return {
                "has_history": True,
                "frequency": "irregular",
                "last_screening": (datetime.now() - timedelta(days=random.randint(365, 2190))).isoformat(),
                "completion_rate": random.uniform(0.1, 0.4)
            }
        else:
            return {
                "has_history": False,
                "frequency": "never",
                "last_screening": None,
                "completion_rate": 0.0
            }
    else:  # overlooked_risk_group
        has_history = random.random() < 0.2
        if has_history:
            return {
                "has_history": True,
                "frequency": "irregular",
                "last_screening": (datetime.now() - timedelta(days=random.randint(730, 3650))).isoformat(),
                "completion_rate": random.uniform(0.1, 0.3)
            }
        else:
            return {
                "has_history": False,
                "frequency": "never",
                "last_screening": None,
                "completion_rate": 0.0
            }

def generate_life_events(persona_type: str, age: int) -> List[Dict[str, Any]]:
    """Generate life events based on persona type and age."""
    events = []
    event_types = PERSONA_TEMPLATES[persona_type]["life_transitions"]["types"]
    
    # Generate 1-3 events based on persona type
    num_events = random.randint(1, 3)
    
    for _ in range(num_events):
        event_type = random.choice(event_types)
        event_date = (datetime.now() - timedelta(days=random.randint(0, 3650))).isoformat()
        
        events.append({
            "type": event_type,
            "date": event_date,
            "impact": random.choice(["high", "moderate", "low"]),
            "status": random.choice(["completed", "in_progress", "planned"])
        })
    
    return events

def generate_narrative_elements(persona_type: str) -> Dict[str, str]:
    """Generate narrative elements based on persona type."""
    if persona_type == "health_aware_avoider":
        return {
            "self_description": random.choice([
                "I'm aware of health risks but prefer to avoid medical appointments.",
                "I know I should be more proactive about my health.",
                "I get anxious thinking about medical procedures."
            ]),
            "health_goals": random.choice([
                "To reduce my anxiety about healthcare.",
                "To find a more comfortable way to manage my health.",
                "To understand my risks without feeling overwhelmed."
            ])
        }
    elif persona_type == "structured_system_seeker":
        return {
            "self_description": random.choice([
                "I maintain a systematic approach to my health.",
                "I track and plan my health activities carefully.",
                "I value organization in my healthcare routine."
            ]),
            "health_goals": random.choice([
                "To maintain my organized health routine.",
                "To optimize my prevention schedule.",
                "To track my health metrics systematically."
            ])
        }
    elif persona_type == "balanced_life_integrator":
        return {
            "self_description": random.choice([
                "I take a balanced approach to health and wellness.",
                "I focus on overall well-being rather than specific metrics.",
                "I integrate health into my lifestyle naturally."
            ]),
            "health_goals": random.choice([
                "To maintain a healthy work-life balance.",
                "To enjoy life while staying healthy.",
                "To integrate prevention into my daily routine."
            ])
        }
    elif persona_type == "healthcare_professional":
        return {
            "self_description": random.choice([
                "I approach health with professional expertise.",
                "I balance clinical knowledge with personal health.",
                "I stay informed about the latest health research."
            ]),
            "health_goals": random.choice([
                "To apply evidence-based practices to my health.",
                "To maintain professional health standards.",
                "To stay current with health recommendations."
            ])
        }
    else:  # overlooked_risk_group
        return {
            "self_description": random.choice([
                "I'm learning about my specific health risks.",
                "I need guidance tailored to my situation.",
                "I want to understand my unique health needs."
            ]),
            "health_goals": random.choice([
                "To find appropriate health guidance.",
                "To understand my specific risk factors.",
                "To get personalized health recommendations."
            ])
        }

def create_profile(name: str, persona_type: str) -> Dict[str, Any]:
    """Create a complete profile for a persona."""
    age = generate_age(persona_type)
    
    return {
        "name": name,
        "persona_type": persona_type,
        "age": age,
        "education": generate_education(persona_type),
        "risk_level": generate_risk_level(persona_type),
        "screening_history": generate_screening_history(persona_type),
        "life_events": generate_life_events(persona_type, age),
        "narrative_elements": generate_narrative_elements(persona_type),
        "pain_points": PERSONA_TEMPLATES[persona_type]["pain_points"],
        "primary_motivations": PERSONA_TEMPLATES[persona_type]["primary_motivations"],
        "prevention_approach": PERSONA_TEMPLATES[persona_type]["prevention_approach"]
    }

def main():
    # Load persona names
    persona_names = load_persona_names()
    
    # Generate complete profiles
    complete_profiles = []
    
    for persona_type, names in persona_names.items():
        for name in names:
            profile = create_profile(name, persona_type)
            complete_profiles.append(profile)
    
    # Save complete profiles
    output_file = Path("output") / "complete_profiles.json"
    with open(output_file, "w") as f:
        json.dump(complete_profiles, f, indent=2)
    
    print(f"Generated {len(complete_profiles)} complete profiles")
    print(f"Saved to {output_file}")
    
    # Print summary statistics
    print("\nProfile Distribution Summary:")
    print("-" * 50)
    for persona_type in PERSONA_DISTRIBUTION.keys():
        count = sum(1 for p in complete_profiles if p["persona_type"] == persona_type)
        print(f"\n{persona_type.replace('_', ' ').title()}:")
        print(f"  Count: {count}")
        print(f"  Percentage: {(count/len(complete_profiles))*100:.1f}%")
        print(f"  Average Age: {sum(p['age'] for p in complete_profiles if p['persona_type'] == persona_type)/count:.1f}")
        print(f"  Screening Rate: {(sum(1 for p in complete_profiles if p['persona_type'] == persona_type and p['screening_history']['has_history'])/count)*100:.1f}%")

if __name__ == "__main__":
    main() 