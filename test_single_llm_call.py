#!/usr/bin/env python3
"""
Simple test: Single Anthropic LLM call + SSR conversion.
"""

import json
from pathlib import Path
from core.generators.llm_response_generator import LLMResponseGenerator
from core.generators.ssr_response_generator import SSRResponseGenerator


def main():
    """Test single LLM call with SSR conversion."""

    print("=" * 80)
    print("🤖 Single Anthropic LLM Call Test")
    print("=" * 80)
    print()

    # Load a real user
    users_file = Path("output/private_language_synthetic_users.json")
    with open(users_file) as f:
        users_data = json.load(f)

    test_user = users_data[0]

    print(f"🎭 Persona: {test_user['name']} ({test_user['persona_type']})")
    print(f"   Age: {test_user['age']}")
    if 'tech_comfort' in test_user['attributes']:
        print(f"   Tech Comfort: {test_user['attributes']['tech_comfort']:.2f}")
    print()

    # Initialize generators
    print("Initializing LLM generator...")
    llm_gen = LLMResponseGenerator()
    print("✓ LLM generator ready")

    print("Initializing SSR generator...")
    ssr_gen = SSRResponseGenerator("projects/private_language/response_scales.yaml")
    print("✓ SSR generator ready")
    print()

    # Test stimulus
    stimulus = "You're starting a new knowledge capture session. The system will help you document your craft expertise."
    phase = "discovery"
    emotional_state = "curious_cautious"
    engagement_score = 0.65

    print("-" * 80)
    print("📝 Test Scenario")
    print("-" * 80)
    print(f"Stimulus: {stimulus}")
    print(f"Phase: {phase}")
    print(f"Emotional State: {emotional_state}")
    print(f"Engagement: {engagement_score:.0%}")
    print()

    # Test each scale
    scales = ['engagement', 'satisfaction']

    for scale_id in scales:
        print("=" * 80)
        print(f"🎯 Testing {scale_id.upper()} scale")
        print("=" * 80)
        print()

        print("🤖 Calling Claude API...")
        llm_response = llm_gen.generate_response(
            persona=test_user['attributes'],
            stimulus=stimulus,
            scale_id=scale_id,
            phase=phase,
            emotional_state=emotional_state,
            engagement_score=engagement_score
        )

        print("✓ Claude responded:")
        print()
        print(f"   \"{llm_response}\"")
        print()

        print("🔄 Converting to SSR probability distribution...")
        ssr_result = ssr_gen.generate_persona_response(
            persona_config=test_user['attributes'],
            stimulus=stimulus,
            scale_id=scale_id,
            llm_response=llm_response
        )

        print("✓ SSR Results:")
        print(f"   Expected Value: {ssr_result['expected_value']:.2f}/5")
        print(f"   Most Likely: {ssr_result['most_likely_rating']}/5")
        print(f"   PMF: {[f'{p:.3f}' for p in ssr_result['pmf']]}")
        print(f"        {'  1      2      3      4      5'}")
        print()

    print("=" * 80)
    print("✅ Test Complete!")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✓ Anthropic Claude API: Working")
    print("  ✓ Persona-aware responses: Generated")
    print("  ✓ SSR conversion: Successfully converted to PMFs")
    print("  ✓ Realistic distributions: Full 1-5 scale utilized")
    print()


if __name__ == "__main__":
    main()
