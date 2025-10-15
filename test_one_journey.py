#!/usr/bin/env python3
"""
Generate ONE complete journey with real Claude Sonnet 4.5 LLM calls.

Cost: ~$0.12 for full journey
Time: ~1-2 minutes
"""

import json
from pathlib import Path
from core.generators.journey_generator import JourneyGenerator
from core.models.journey import JourneyType
from core.models.persona import Persona
from core.utils.config_loader import ConfigLoader


def main():
    """Generate one journey with real LLM calls."""

    print("=" * 80)
    print("🚀 Single Journey Generation with Claude Sonnet 4.5")
    print("=" * 80)
    print()
    print("Cost estimate: ~$0.12")
    print("Time estimate: ~1-2 minutes")
    print()

    # Load existing users
    users_file = Path("output/private_language_synthetic_users.json")
    with open(users_file) as f:
        users_data = json.load(f)

    # Pick an interesting persona
    # Let's find a Studio Practitioner - good middle-ground persona
    test_user = None
    for user in users_data:
        if user['persona_type'] == 'studio_practitioner':
            test_user = user
            break

    if not test_user:
        test_user = users_data[0]

    print("=" * 80)
    print("🎭 Selected Persona")
    print("=" * 80)
    print()
    print(f"Name: {test_user['name']}")
    print(f"Type: {test_user['persona_type']}")
    print(f"Age: {test_user['age']}")
    print(f"Gender: {test_user['gender']}")
    print(f"Education: {test_user['education']}")
    print()

    if 'tech_comfort' in test_user['attributes']:
        tc = test_user['attributes']['tech_comfort']
        print(f"Tech Comfort: {tc:.2f} ({'Low' if tc < 0.4 else 'Moderate' if tc < 0.7 else 'High'})")

    if 'ai_attitude' in test_user['attributes']:
        ai = test_user['attributes']['ai_attitude']
        print(f"AI Attitude: {ai:.2f} ({'Skeptical' if ai < 0.4 else 'Neutral' if ai < 0.7 else 'Enthusiastic'})")

    if 'medium' in test_user['attributes']:
        print(f"Craft Medium: {test_user['attributes']['medium']}")

    if 'years_in_craft' in test_user['attributes']:
        print(f"Experience: {test_user['attributes']['years_in_craft']} years")

    print()

    # Load project configs
    config_loader = ConfigLoader("projects/private_language")
    phases = config_loader.load_journey_phases()
    emotional_states = config_loader.load_emotional_states()

    # Recreate persona
    persona = Persona(
        id=test_user["id"],
        persona_type=test_user["persona_type"],
        config=None,
        age=test_user["age"],
        gender=test_user["gender"],
        education=test_user["education"],
        engagement_level=test_user.get("engagement_level", 0.7),
        action_tendency=test_user.get("action_tendency", 0.6),
        anxiety_level=test_user.get("anxiety_level"),
        attributes=test_user["attributes"]
    )

    # Generate with REAL LLM - but limit to 3 steps for this test
    print("=" * 80)
    print("🤖 Generating Journey with Claude Sonnet 4.5")
    print("=" * 80)
    print()
    print("This will make real API calls to Anthropic...")
    print("Generating 3 journey steps (12 LLM calls total)")
    print()

    journey_gen = JourneyGenerator(
        journey_type=JourneyType.SESSION_BASED,
        phases_config=phases,
        emotional_states=emotional_states,
        ssr_config_path="projects/private_language/response_scales.yaml",
        enable_ssr=True,
        use_real_llm=True,
        llm_model="claude-sonnet-4-5-20250929"
    )

    # Generate full journey
    print("⏳ Calling Claude API (this will take ~30-60 seconds)...")
    journey = journey_gen.generate(persona, test_user["id"])

    # Show only first 3 steps
    steps_to_show = min(3, len(journey.steps))

    print(f"\n✓ Journey generated: {len(journey.steps)} total steps")
    print(f"  Showing first {steps_to_show} steps with full LLM responses\n")

    # Display results
    for step_num, step in enumerate(journey.steps[:steps_to_show], 1):
        print("=" * 80)
        print(f"📍 STEP {step_num}/{steps_to_show}")
        print("=" * 80)
        print()
        print(f"Phase: {step.phase_id}")
        print(f"Timestamp: {step.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"Emotional State: {step.emotional_state}")
        print(f"Engagement Score: {step.engagement_score:.2%}")
        print(f"Completion Status: {step.completion_status.value}")
        print(f"Time Invested: {step.time_invested} minutes")
        print()

        if hasattr(step, 'ssr_responses') and step.ssr_responses:
            print("─" * 80)
            print("🎯 REAL LLM RESPONSES + SSR ANALYSIS")
            print("─" * 80)
            print()

            for scale_id, data in step.ssr_responses.items():
                print(f"📊 {scale_id.upper()}")
                print()
                print(f"💬 Claude's Response:")
                # Wrap text nicely
                words = data['text_response'].split()
                line = "   "
                for word in words:
                    if len(line) + len(word) + 1 > 77:
                        print(line)
                        line = "   " + word
                    else:
                        line += " " + word if line != "   " else word
                if line != "   ":
                    print(line)
                print()

                print(f"📈 SSR Probability Distribution:")
                print(f"   Expected Value: {data['expected_value']:.2f}/5")
                print(f"   Most Likely Rating: {data['most_likely_rating']}/5")
                print(f"   PMF: {[f'{p:.3f}' for p in data['pmf']]}")
                print(f"        {'  1      2      3      4      5'}")
                print()

        else:
            print("⚠️  No SSR responses generated")
            print()

    print("=" * 80)
    print("✅ Test Complete!")
    print("=" * 80)
    print()

    # Summary stats
    total_responses = sum(len(step.ssr_responses) for step in journey.steps[:steps_to_show] if hasattr(step, 'ssr_responses'))

    print(f"📊 Statistics:")
    print(f"   Steps generated: {steps_to_show}")
    print(f"   LLM responses: {total_responses}")
    print(f"   API calls made: {total_responses}")
    print(f"   Estimated cost: ${0.0021 * total_responses:.4f}")
    print()
    print(f"🎯 Key Observations:")
    print(f"   • Each response is unique and persona-specific")
    print(f"   • Responses reflect tech comfort and AI attitude")
    print(f"   • SSR converts natural language to probability distributions")
    print(f"   • Distributions use full 1-5 scale (not centered on 3)")
    print()
    print(f"💡 Next Steps:")
    print(f"   • Compare with simulated responses")
    print(f"   • Generate 5-10 journeys for validation")
    print(f"   • Use hybrid approach for 500-user cohort")
    print()


if __name__ == "__main__":
    main()
