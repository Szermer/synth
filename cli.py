#!/usr/bin/env python3
"""
Synth CLI - Multi-Domain Synthetic User Data Generator

Usage:
    python cli.py generate <project_name> [--count COUNT] [--output DIR]
    python cli.py list-projects
    python cli.py validate <project_name>
"""

import argparse
import json
from pathlib import Path
import sys

from core.utils.config_loader import ConfigLoader
from core.generators.persona_generator import PersonaGenerator
from core.generators.journey_generator import JourneyGenerator
from core.models.user_profile import UserProfile


def main():
    parser = argparse.ArgumentParser(description="Synth - Synthetic User Data Generator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate synthetic users")
    generate_parser.add_argument("project", help="Project name")
    generate_parser.add_argument("--count", type=int, default=100, help="Number of users to generate")
    generate_parser.add_argument("--output", default="output", help="Output directory")

    # List projects command
    subparsers.add_parser("list-projects", help="List available projects")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate project configuration")
    validate_parser.add_argument("project", help="Project name")

    args = parser.parse_args()

    if args.command == "generate":
        generate_users(args.project, args.count, args.output)
    elif args.command == "list-projects":
        list_projects()
    elif args.command == "validate":
        validate_project(args.project)
    else:
        parser.print_help()


def generate_users(project_name: str, count: int, output_dir: str):
    """Generate synthetic users for a project"""
    print(f"🚀 Generating {count} synthetic users for {project_name}...")

    # Load project configuration
    project_path = Path("projects") / project_name
    if not project_path.exists():
        print(f"❌ Project not found: {project_name}")
        print(f"   Looking in: {project_path.absolute()}")
        sys.exit(1)

    try:
        loader = ConfigLoader(project_path)

        # Load configurations
        print("📋 Loading configurations...")
        config = loader.load_config()
        personas = loader.load_personas()
        journey_phases = loader.load_journey_phases()
        emotional_states = loader.load_emotional_states()
        journey_type = loader.get_journey_type()

        print(f"   Found {len(personas)} persona types")
        print(f"   Found {len(journey_phases)} journey phases")
        print(f"   Journey type: {journey_type.value}")

        # Generate personas
        print(f"\n👥 Generating {count} persona instances...")
        persona_gen = PersonaGenerator(personas)
        generated_personas = persona_gen.generate(count)

        # Generate journeys
        print(f"🗺️  Generating user journeys...")
        journey_gen = JourneyGenerator(journey_type, journey_phases, emotional_states)

        # Create user profiles with journeys
        users = []
        for i, persona in enumerate(generated_personas):
            if (i + 1) % 50 == 0:
                print(f"   Progress: {i + 1}/{count}")

            # Create user profile
            user = UserProfile(
                persona_type=persona.persona_type,
                name=f"{persona.persona_type}_user_{i+1}",
                age=persona.age,
                gender=persona.gender,
                education=persona.education,
                engagement_level=persona.engagement_level,
                action_tendency=persona.action_tendency,
                anxiety_level=persona.anxiety_level,
                attributes=persona.attributes
            )

            # Generate journey
            journey = journey_gen.generate(persona, user.id)
            user.journey_id = journey.id

            # Combine user and journey data
            user_data = user.to_dict()
            user_data["journey"] = journey.to_dict()

            users.append(user_data)

        # Save to output
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_file = output_path / f"{project_name}_synthetic_users.json"
        with open(output_file, 'w') as f:
            json.dump(users, f, indent=2)

        print(f"\n✅ Generated {len(users)} users")
        print(f"📁 Saved to: {output_file.absolute()}")

        # Print summary
        print("\n📊 Persona Distribution:")
        persona_counts = {}
        for user in users:
            persona_type = user["persona_type"]
            persona_counts[persona_type] = persona_counts.get(persona_type, 0) + 1

        for persona_type, count in sorted(persona_counts.items()):
            percentage = (count / len(users)) * 100
            print(f"   {persona_type}: {count} ({percentage:.1f}%)")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def list_projects():
    """List available projects"""
    projects_dir = Path("projects")

    if not projects_dir.exists():
        print("❌ Projects directory not found")
        sys.exit(1)

    projects = [p for p in projects_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]

    if not projects:
        print("📭 No projects found in projects/")
        return

    print("📂 Available Projects:\n")
    for project in sorted(projects):
        config_file = project / "config.yaml"
        if config_file.exists():
            try:
                loader = ConfigLoader(project)
                config = loader.load_config()
                print(f"   • {project.name}")
                print(f"     {config.get('description', 'No description')}")
                print(f"     Domain: {config.get('domain', 'Unknown')}")
                print()
            except Exception as e:
                print(f"   • {project.name} (⚠️  config error: {e})")
        else:
            print(f"   • {project.name} (⚠️  missing config.yaml)")


def validate_project(project_name: str):
    """Validate project configuration"""
    print(f"🔍 Validating {project_name}...")

    project_path = Path("projects") / project_name
    if not project_path.exists():
        print(f"❌ Project not found: {project_name}")
        sys.exit(1)

    try:
        loader = ConfigLoader(project_path)

        # Validate each config file
        print("✅ config.yaml loaded")
        config = loader.load_config()

        print("✅ personas.yaml loaded")
        personas = loader.load_personas()

        # Validate persona distributions
        total_dist = sum(p.distribution for p in personas.values())
        if abs(total_dist - 1.0) > 0.01:
            print(f"⚠️  Warning: Persona distributions sum to {total_dist:.2f}, not 1.0")

        print("✅ journey_phases.yaml loaded")
        journey_phases = loader.load_journey_phases()

        print("✅ emotional_states.yaml loaded")
        emotional_states = loader.load_emotional_states()

        print("✅ narrative_patterns.yaml loaded")
        narrative_patterns = loader.load_narrative_patterns()

        print("\n✅ All validations passed!")
        print(f"\nProject: {config.get('name')}")
        print(f"Personas: {len(personas)}")
        print(f"Journey Phases: {len(journey_phases)}")
        print(f"Journey Type: {loader.get_journey_type().value}")

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
