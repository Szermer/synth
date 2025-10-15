#!/usr/bin/env python3
"""
Generate 2 users with real Claude Sonnet 4.5 - Quick test.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from core.generators.journey_generator import JourneyGenerator
from core.models.journey import JourneyType
from core.models.persona import Persona
from core.utils.config_loader import ConfigLoader


def main():
    """Generate 2 users with real LLM."""

    print("=" * 80, flush=True)
    print("🚀 2-User Test with Claude Sonnet 4.5", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)

    # Load existing users
    users_file = Path("output/private_language_synthetic_users.json")
    with open(users_file) as f:
        users_data = json.load(f)

    # Just 2 users
    users_to_process = users_data[:2]

    print(f"Processing {len(users_to_process)} users...", flush=True)
    print(f"Est. cost: ~${len(users_to_process) * 0.12:.2f}", flush=True)
    print(flush=True)

    # Load configs
    config_loader = ConfigLoader("projects/private_language")
    phases = config_loader.load_journey_phases()
    emotional_states = config_loader.load_emotional_states()

    print("Initializing journey generator...", flush=True)
    journey_gen = JourneyGenerator(
        journey_type=JourneyType.SESSION_BASED,
        phases_config=phases,
        emotional_states=emotional_states,
        ssr_config_path="projects/private_language/response_scales.yaml",
        enable_ssr=True,
        use_real_llm=True,
        llm_model="claude-sonnet-4-5-20250929"
    )
    print("✓ Ready", flush=True)
    print(flush=True)

    results = []
    start_time = time.time()

    for idx, user_data in enumerate(users_to_process, 1):
        print("─" * 80, flush=True)
        print(f"User {idx}/{len(users_to_process)}: {user_data['name']} ({user_data['persona_type']})", flush=True)
        print("─" * 80, flush=True)

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

        print("Generating journey...", flush=True)
        user_start = time.time()

        journey = journey_gen.generate(persona, user_data["id"])

        user_time = time.time() - user_start

        # Count responses
        ssr_count = sum(len(step.ssr_responses) for step in journey.steps if hasattr(step, 'ssr_responses'))

        print(f"✓ Complete: {len(journey.steps)} steps, {ssr_count} LLM responses, {user_time:.1f}s", flush=True)
        print(flush=True)

        # Save journey
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

            if hasattr(step, 'ssr_responses'):
                step_dict['ssr_responses'] = step.ssr_responses

            journey_dict['steps'].append(step_dict)

        user_result = {
            **user_data,
            "journey": journey_dict,
            "llm_generated": True,
            "llm_model": "claude-sonnet-4-5-20250929",
            "generation_timestamp": datetime.now().isoformat()
        }

        results.append(user_result)

    # Save
    output_file = Path("output/private_language_2users_llm.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    total_time = time.time() - start_time
    total_responses = sum(
        len(step.get('ssr_responses', {}))
        for user in results
        for step in user['journey']['steps']
    )

    print("=" * 80, flush=True)
    print("✅ Complete!", flush=True)
    print("=" * 80, flush=True)
    print(f"Users: {len(results)}", flush=True)
    print(f"LLM responses: {total_responses}", flush=True)
    print(f"Cost: ${total_responses * 0.0021:.2f}", flush=True)
    print(f"Time: {total_time:.1f}s", flush=True)
    print(f"Saved: {output_file}", flush=True)
    print(flush=True)


if __name__ == "__main__":
    main()
