import json
from pathlib import Path
from typing import Dict, List

import faker

from config.persona_config import PERSONA_DISTRIBUTION, PERSONA_TEMPLATES

# Initialize Faker with a seed for reproducibility
fake = faker.Faker()
fake.seed_instance(42)

# Persona names from Personas.md
PERSONA_NAMES = {
    "health_aware_avoider": ["Laura Martinez"],
    "structured_system_seeker": ["Rebecca Chen"],
    "balanced_life_integrator": ["Betsy Langford"],
    "healthcare_professional": ["Jessica Rivera"],
    "overlooked_risk_group": ["Michael Reynolds"]
}

def generate_names_for_persona(persona_type: str, count: int) -> List[str]:
    """Generate names that match the demographic characteristics of each persona type."""
    names = []
    
    # Get gender distribution from persona template
    gender_dist = PERSONA_TEMPLATES[persona_type]["gender_distribution"]
    
    for _ in range(count):
        # Determine gender based on distribution
        gender = "female" if fake.random.random() < gender_dist["female"] else "male"
        
        # Generate name based on persona type and gender
        if persona_type == "health_aware_avoider":
            # Hispanic and diverse names
            if gender == "female":
                names.append(fake.first_name_female() + " " + fake.last_name())
            else:
                names.append(fake.first_name_male() + " " + fake.last_name())
        elif persona_type == "structured_system_seeker":
            # Asian and diverse names
            if gender == "female":
                names.append(fake.first_name_female() + " " + fake.last_name())
            else:
                names.append(fake.first_name_male() + " " + fake.last_name())
        elif persona_type == "balanced_life_integrator":
            # Anglo and diverse names
            if gender == "female":
                names.append(fake.first_name_female() + " " + fake.last_name())
            else:
                names.append(fake.first_name_male() + " " + fake.last_name())
        elif persona_type == "healthcare_professional":
            # Diverse professional names
            if gender == "female":
                names.append(fake.first_name_female() + " " + fake.last_name())
            else:
                names.append(fake.first_name_male() + " " + fake.last_name())
        elif persona_type == "overlooked_risk_group":
            # Diverse names with focus on underrepresented groups
            if gender == "female":
                names.append(fake.first_name_female() + " " + fake.last_name())
            else:
                names.append(fake.first_name_male() + " " + fake.last_name())
    
    return names

def main():
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate names for each persona type
    persona_names: Dict[str, List[str]] = {}
    
    for persona_type, count in PERSONA_DISTRIBUTION.items():
        # Calculate number of profiles needed
        num_profiles = int(count * 500)
        
        # Generate names
        names = generate_names_for_persona(persona_type, num_profiles)
        
        # Add the canonical name from Personas.md as the first name
        if persona_type in PERSONA_NAMES:
            names.insert(0, PERSONA_NAMES[persona_type][0])
        
        persona_names[persona_type] = names
    
    # Save to JSON file
    output_file = output_dir / "persona_names.json"
    with open(output_file, "w") as f:
        json.dump(persona_names, f, indent=2)
    
    print(f"Generated persona names saved to {output_file}")
    
    # Print summary
    print("\nPersona Name Distribution:")
    print("-" * 50)
    for persona_type, names in persona_names.items():
        print(f"\n{persona_type.replace('_', ' ').title()}:")
        print(f"  Canonical Name: {names[0]}")
        print(f"  Total Names: {len(names)}")
        print(f"  Sample Names: {', '.join(names[1:6])}")

if __name__ == "__main__":
    main() 