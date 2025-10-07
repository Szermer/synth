#!/usr/bin/env python3
"""
Example: Generate synthetic users programmatically

This demonstrates how to use Synth's core generators directly in Python code,
without using the CLI.
"""

from pathlib import Path
import json

from core.utils.config_loader import ConfigLoader
from core.generators.persona_generator import PersonaGenerator
from core.generators.journey_generator import JourneyGenerator
from core.models.user_profile import UserProfile


def main():
    # Configuration
    project_name = "private_language"
    user_count = 100
    output_file = "example_output.json"

    print(f"🚀 Generating {user_count} synthetic users for {project_name}\n")

    # Load project configuration
    project_path = Path("projects") / project_name
    loader = ConfigLoader(project_path)

    # Load all configurations
    print("📋 Loading configurations...")
    config = loader.load_config()
    personas = loader.load_personas()
    journey_phases = loader.load_journey_phases()
    emotional_states = loader.load_emotional_states()
    journey_type = loader.get_journey_type()

    print(f"   ✓ Loaded {len(personas)} personas")
    print(f"   ✓ Loaded {len(journey_phases)} journey phases")
    print(f"   ✓ Journey type: {journey_type.value}\n")

    # Initialize generators
    print("🔧 Initializing generators...")
    persona_generator = PersonaGenerator(personas)
    journey_generator = JourneyGenerator(
        journey_type,
        journey_phases,
        emotional_states
    )

    # Generate personas
    print(f"👥 Generating {user_count} personas...")
    generated_personas = persona_generator.generate(user_count)

    # Generate users with journeys
    print("🗺️  Generating user journeys...\n")
    users = []

    for i, persona in enumerate(generated_personas, 1):
        # Create user profile
        user = UserProfile(
            persona_type=persona.persona_type,
            name=f"User_{i}",
            age=persona.age,
            gender=persona.gender,
            education=persona.education,
            engagement_level=persona.engagement_level,
            action_tendency=persona.action_tendency,
            anxiety_level=persona.anxiety_level,
            attributes=persona.attributes
        )

        # Generate journey for this user
        journey = journey_generator.generate(persona, user.id)
        user.journey_id = journey.id

        # Combine data
        user_data = user.to_dict()
        user_data["journey"] = journey.to_dict()
        users.append(user_data)

        # Progress indicator
        if i % 25 == 0:
            print(f"   Progress: {i}/{user_count} users generated")

    # Save results
    print(f"\n💾 Saving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(users, f, indent=2)

    # Print summary
    print("\n✅ Generation complete!\n")
    print("📊 Summary:")
    print(f"   Total Users: {len(users)}")

    # Persona distribution
    print("\n   Persona Distribution:")
    persona_counts = {}
    for user in users:
        p_type = user["persona_type"]
        persona_counts[p_type] = persona_counts.get(p_type, 0) + 1

    for persona_type, count in sorted(persona_counts.items()):
        percentage = (count / len(users)) * 100
        print(f"      • {persona_type}: {count} ({percentage:.1f}%)")

    # Journey completion
    print("\n   Average Journey Completion:")
    avg_completion = sum(u["journey"]["overall_completion"] for u in users) / len(users)
    print(f"      {avg_completion:.1%}")

    print(f"\n📁 Output saved to: {Path(output_file).absolute()}")


if __name__ == "__main__":
    main()
