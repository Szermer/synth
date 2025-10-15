#!/usr/bin/env python3
"""
Quickest test: Generate 1 journey step-by-step showing progress.
"""

import json
import sys
from pathlib import Path
from core.generators.llm_response_generator import LLMResponseGenerator
from core.generators.ssr_response_generator import SSRResponseGenerator

def main():
    print("=" * 80)
    print("Quick LLM Test - 1 User, Step-by-Step")
    print("=" * 80)
    print()

    # Load user
    users_file = Path("output/private_language_synthetic_users.json")
    with open(users_file) as f:
        users_data = json.load(f)

    user = users_data[0]
    print(f"User: {user['name']} ({user['persona_type']})")
    print()

    # Check journey
    if 'journey' in user and 'steps' in user['journey']:
        steps = user['journey']['steps']
        print(f"✓ Found existing journey with {len(steps)} steps")
        print()

        # Show first step's info
        step1 = steps[0]
        print("Step 1 Info:")
        print(f"  Phase: {step1['phase_id']}")
        print(f"  Emotional: {step1['emotional_state']}")
        print(f"  Engagement: {step1['engagement_score']:.2f}")
        print()

        # Now generate real LLM responses for this step
        print("Generating real LLM responses for Step 1...")
        print()

        llm_gen = LLMResponseGenerator()
        ssr_gen = SSRResponseGenerator("projects/private_language/response_scales.yaml")

        stimulus = "Starting your knowledge capture journey"

        for scale in ['engagement', 'satisfaction']:
            print(f"  {scale}... ", end="", flush=True)

            response = llm_gen.generate_response(
                persona=user['attributes'],
                stimulus=stimulus,
                scale_id=scale,
                phase=step1['phase_id'],
                emotional_state=step1['emotional_state'],
                engagement_score=step1['engagement_score']
            )

            ssr = ssr_gen.generate_persona_response(
                persona_config=user['attributes'],
                stimulus=stimulus,
                scale_id=scale,
                llm_response=response
            )

            print("✓")
            print(f'    "{response}"')
            print(f"    → {ssr['expected_value']:.2f}/5")
            print()

        print("✅ Test successful!")
        print(f"Cost: ~${0.0021 * 2:.4f} (2 API calls)")

    else:
        print("❌ No journey found")

if __name__ == "__main__":
    main()
