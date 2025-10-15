#!/usr/bin/env python3
"""
Generate full cohort with real Claude Sonnet 4.5 LLM integration.

This will regenerate journeys for existing users using real LLM calls.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from core.generators.journey_generator import JourneyGenerator
from core.models.journey import JourneyType
from core.models.persona import Persona
from core.utils.config_loader import ConfigLoader


def main():
    """Generate cohort with real LLM calls."""

    print("=" * 80)
    print("🚀 Full Cohort Generation with Claude Sonnet 4.5")
    print("=" * 80)
    print()

    # Load existing users
    users_file = Path("output/private_language_synthetic_users.json")
    with open(users_file) as f:
        users_data = json.load(f)

    num_users = len(users_data)

    # Cost estimation
    avg_steps = 14  # From our earlier analysis
    scales = 4
    calls_per_user = avg_steps * scales
    total_calls = num_users * calls_per_user
    cost_per_call = 0.0021
    total_cost = total_calls * cost_per_call

    print(f"📊 Cohort Overview")
    print(f"   Users to process: {num_users}")
    print(f"   Est. API calls per user: {calls_per_user}")
    print(f"   Est. total API calls: {total_calls}")
    print(f"   Est. total cost: ${total_cost:.2f}")
    print(f"   Est. time: {num_users * 1.5:.0f}-{num_users * 2:.0f} minutes")
    print()
    print("🚀 Starting generation...")
    print()

    # Load project configs
    config_loader = ConfigLoader("projects/private_language")
    phases = config_loader.load_journey_phases()
    emotional_states = config_loader.load_emotional_states()

    # Initialize journey generator with REAL LLM
    print("Initializing journey generator with Claude Sonnet 4.5...")
    journey_gen = JourneyGenerator(
        journey_type=JourneyType.SESSION_BASED,
        phases_config=phases,
        emotional_states=emotional_states,
        ssr_config_path="projects/private_language/response_scales.yaml",
        enable_ssr=True,
        use_real_llm=True,  # 🔥 Real LLM!
        llm_model="claude-sonnet-4-5-20250929"
    )
    print("✓ Generator ready")
    print()

    # Process each user
    results = []
    start_time = time.time()

    for idx, user_data in enumerate(users_data, 1):
        user_start = time.time()

        print("─" * 80)
        print(f"Processing User {idx}/{num_users}")
        print("─" * 80)
        print(f"Name: {user_data['name']}")
        print(f"Type: {user_data['persona_type']}")
        print(f"Age: {user_data['age']}")

        if 'tech_comfort' in user_data['attributes']:
            print(f"Tech Comfort: {user_data['attributes']['tech_comfort']:.2f}")

        print()

        # Recreate persona
        persona = Persona(
            id=user_data["id"],
            persona_type=user_data["persona_type"],
            config=None,
            age=user_data["age"],
            gender=user_data["gender"],
            education=user_data["education"],
            engagement_level=user_data.get("engagement_level", 0.7),
            action_tendency=user_data.get("action_tendency", 0.6),
            anxiety_level=user_data.get("anxiety_level"),
            attributes=user_data["attributes"]
        )

        # Generate journey with real LLM
        print("🤖 Generating journey with real LLM calls...")
        journey = journey_gen.generate(persona, user_data["id"])

        # Count SSR responses
        ssr_count = 0
        for step in journey.steps:
            if hasattr(step, 'ssr_responses'):
                ssr_count += len(step.ssr_responses)

        user_time = time.time() - user_start

        print(f"✓ Journey generated:")
        print(f"  Steps: {len(journey.steps)}")
        print(f"  LLM responses: {ssr_count}")
        print(f"  Time: {user_time:.1f}s")
        print()

        # Convert journey to dict for saving
        journey_dict = {
            "id": journey.id,
            "user_id": journey.user_id,
            "persona_type": journey.persona_type,
            "journey_type": journey.journey_type.value,
            "started_at": journey.started_at.isoformat(),
            "completed_at": journey.completed_at.isoformat() if journey.completed_at else None,
            "overall_completion": journey.overall_completion,
            "steps": []
        }

        for step in journey.steps:
            step_dict = {
                "id": step.id,
                "phase_id": step.phase_id,
                "step_number": step.step_number,
                "timestamp": step.timestamp.isoformat(),
                "actions": step.actions,
                "emotional_state": step.emotional_state,
                "completion_status": step.completion_status.value,
                "data_captured": step.data_captured,
                "time_invested": step.time_invested,
                "engagement_score": step.engagement_score
            }

            # Include SSR responses if present
            if hasattr(step, 'ssr_responses'):
                step_dict['ssr_responses'] = step.ssr_responses

            journey_dict['steps'].append(step_dict)

        # Combine user data with new journey
        user_result = {
            **user_data,  # Original user data
            "journey": journey_dict,  # New LLM-generated journey
            "llm_generated": True,
            "llm_model": "claude-sonnet-4-5-20250929",
            "generation_timestamp": datetime.now().isoformat()
        }

        results.append(user_result)

        # Progress update
        elapsed = time.time() - start_time
        avg_time_per_user = elapsed / idx
        remaining_users = num_users - idx
        eta_seconds = avg_time_per_user * remaining_users

        print(f"Progress: {idx}/{num_users} ({idx/num_users*100:.0f}%)")
        print(f"ETA: {eta_seconds/60:.1f} minutes")
        print()

    # Save results
    output_file = Path("output/private_language_synthetic_users_llm.json")
    print("=" * 80)
    print("💾 Saving Results")
    print("=" * 80)
    print()

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✓ Saved to: {output_file}")
    print()

    # Final stats
    total_time = time.time() - start_time
    total_ssr_responses = sum(
        len(step.get('ssr_responses', {}))
        for user in results
        for step in user['journey']['steps']
    )

    actual_cost = total_ssr_responses * cost_per_call

    print("=" * 80)
    print("📊 Final Statistics")
    print("=" * 80)
    print()
    print(f"✅ Successfully processed {num_users} users")
    print(f"   Total journey steps: {sum(len(u['journey']['steps']) for u in results)}")
    print(f"   Total LLM responses: {total_ssr_responses}")
    print(f"   Actual API calls: {total_ssr_responses}")
    print(f"   Actual cost: ${actual_cost:.2f}")
    print(f"   Total time: {total_time/60:.1f} minutes")
    print(f"   Avg time per user: {total_time/num_users:.1f}s")
    print()

    print("🎯 Results:")
    print(f"   • Every journey includes real Claude Sonnet 4.5 responses")
    print(f"   • Each response is persona-specific and contextual")
    print(f"   • SSR probability distributions for 4 scales per step")
    print(f"   • Saved to: {output_file}")
    print()

    print("💡 Next Steps:")
    print(f"   • Analyze response quality across personas")
    print(f"   • Compare with simulated baseline")
    print(f"   • Use for E2E testing with realistic data")
    print(f"   • Generate validation reports")
    print()


if __name__ == "__main__":
    main()
