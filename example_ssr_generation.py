#!/usr/bin/env python3
"""
Example usage of SSRResponseGenerator for synthetic user responses.

This script demonstrates how to use the Semantic Similarity Rating (SSR)
methodology to generate realistic persona responses to learning content.

Run with:
    PYTHONPATH=. python example_ssr_generation.py
"""

import json
from pathlib import Path
from core.generators.ssr_response_generator import SSRResponseGenerator


def main():
    """Demonstrate SSR response generation with example personas and stimuli."""

    print("=" * 80)
    print("Semantic Similarity Rating (SSR) Example")
    print("=" * 80)
    print()

    # Initialize the generator
    print("Initializing SSR generator...")
    generator = SSRResponseGenerator(
        reference_config_path="projects/private_language/response_scales.yaml",
        model_name="all-MiniLM-L6-v2"
    )
    print(f"✓ Loaded {len(generator.available_scales)} scales")
    print(f"  Available scales: {', '.join(generator.available_scales)}")
    print()

    # Example 1: Single response generation
    print("-" * 80)
    print("Example 1: Single Persona Response")
    print("-" * 80)
    print()

    persona_beginner = {
        "age": 25,
        "level": "beginner",
        "experience": "just started",
        "goal": "travel conversation"
    }

    stimulus = "Complete this 15-minute interactive lesson on common Spanish verbs"

    # Simulated LLM response (in practice, this would come from an actual LLM)
    llm_response_beginner = (
        "This looks really interesting! I've been wanting to learn basic verbs "
        "for my upcoming trip. 15 minutes is perfect for my schedule. I'm "
        "definitely going to try this right now."
    )

    print(f"Persona: {persona_beginner}")
    print(f"Stimulus: {stimulus}")
    print(f"LLM Response: {llm_response_beginner}")
    print()

    response = generator.generate_persona_response(
        persona_config=persona_beginner,
        stimulus=stimulus,
        scale_id="engagement",
        llm_response=llm_response_beginner
    )

    print("Results:")
    print(f"  Expected Value: {response['expected_value']:.2f}/5")
    print(f"  Most Likely Rating: {response['most_likely_rating']}/5")
    print(f"  PMF: {[f'{p:.3f}' for p in response['pmf']]}")
    print(f"       {'  1      2      3      4      5'}")
    print()

    # Example 2: Different persona, different response
    print("-" * 80)
    print("Example 2: Advanced Learner, Less Engaged")
    print("-" * 80)
    print()

    persona_advanced = {
        "age": 40,
        "level": "advanced",
        "experience": "5 years",
        "goal": "professional fluency"
    }

    llm_response_advanced = (
        "Hmm, basic verbs? I'm already quite comfortable with these. "
        "This might be too elementary for my current level. I'd prefer "
        "something more challenging with subjunctive mood and complex tenses."
    )

    print(f"Persona: {persona_advanced}")
    print(f"Stimulus: {stimulus}")
    print(f"LLM Response: {llm_response_advanced}")
    print()

    response_advanced = generator.generate_persona_response(
        persona_config=persona_advanced,
        stimulus=stimulus,
        scale_id="engagement",
        llm_response=llm_response_advanced
    )

    print("Results:")
    print(f"  Expected Value: {response_advanced['expected_value']:.2f}/5")
    print(f"  Most Likely Rating: {response_advanced['most_likely_rating']}/5")
    print(f"  PMF: {[f'{p:.3f}' for p in response_advanced['pmf']]}")
    print(f"       {'  1      2      3      4      5'}")
    print()

    # Example 3: Journey with multiple touchpoints
    print("-" * 80)
    print("Example 3: Learning Journey with Multiple Touchpoints")
    print("-" * 80)
    print()

    journey_stimuli = [
        "Lesson 1: Basic greetings and introductions",
        "Lesson 2: Numbers and telling time",
        "Lesson 3: Ordering food at a restaurant"
    ]

    # Simulated progression of LLM responses
    journey_responses = [
        "Perfect! This is exactly what I need to start. Very excited to begin!",
        "Good, practical content. I'm finding this useful for my trip planning.",
        "This is really relevant! I can already imagine using these phrases."
    ]

    print(f"Persona: {persona_beginner}")
    print(f"Journey: {len(journey_stimuli)} lessons")
    print()

    journey_results = generator.generate_journey_responses(
        persona_config=persona_beginner,
        journey_stimuli=journey_stimuli,
        llm_responses=journey_responses,
        scale_id="engagement"
    )

    print("Journey Results:")
    for i, result in enumerate(journey_results, 1):
        print(f"\n  Touchpoint {i}: {journey_stimuli[i-1]}")
        print(f"    Response: {journey_responses[i-1][:50]}...")
        print(f"    Expected Value: {result['expected_value']:.2f}/5")
        print(f"    Most Likely: {result['most_likely_rating']}/5")
    print()

    # Example 4: Aggregate survey statistics
    print("-" * 80)
    print("Example 4: Aggregate Survey Statistics")
    print("-" * 80)
    print()

    import numpy as np

    survey_aggregate = generator.get_survey_aggregate(
        response_pmfs=[np.array(r['pmf']) for r in journey_results]
    )

    print("Survey Aggregate (across journey):")
    print(f"  N responses: {survey_aggregate['n_responses']}")
    print(f"  Aggregate Expected Value: {survey_aggregate['aggregate_expected_value']:.2f}/5")
    print(f"  Aggregate PMF: {[f'{p:.3f}' for p in survey_aggregate['aggregate_pmf']]}")
    print(f"                 {'  1      2      3      4      5'}")
    print()

    # Example 5: Different scales
    print("-" * 80)
    print("Example 5: Using Different Scales")
    print("-" * 80)
    print()

    # Test different scales with the same response
    test_response = "This content is okay, but it could be better designed."

    scales_to_test = ["engagement", "satisfaction", "relevance"]

    print(f"Test Response: {test_response}")
    print()

    for scale_id in scales_to_test:
        scale_info = generator.get_scale_info(scale_id)
        result = generator.generate_persona_response(
            persona_config=persona_beginner,
            stimulus="General learning content",
            scale_id=scale_id,
            llm_response=test_response
        )

        print(f"{scale_id.upper()} Scale:")
        print(f"  Description: {scale_info['description']}")
        print(f"  Expected Value: {result['expected_value']:.2f}/5")
        print(f"  Most Likely: {result['most_likely_rating']}/5")
        print()

    # Example 6: Temperature effects
    print("-" * 80)
    print("Example 6: Temperature Effects on Distribution")
    print("-" * 80)
    print()

    test_response_ambiguous = "It's interesting, I guess. Maybe I'll try it."

    temperatures = [0.5, 1.0, 2.0]

    print(f"Ambiguous Response: {test_response_ambiguous}")
    print()

    for temp in temperatures:
        result = generator.generate_persona_response(
            persona_config=persona_beginner,
            stimulus="Learning content",
            scale_id="engagement",
            llm_response=test_response_ambiguous,
            temperature=temp
        )

        print(f"Temperature {temp}:")
        print(f"  Expected Value: {result['expected_value']:.2f}/5")
        print(f"  PMF: {[f'{p:.3f}' for p in result['pmf']]}")
        print(f"       {'  1      2      3      4      5'}")
        print(f"  (Lower temp = sharper distribution, Higher temp = flatter)")
        print()

    print("=" * 80)
    print("Examples Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("  • SSR converts free text to realistic probability distributions")
    print("  • Different personas produce different response patterns")
    print("  • Works across multiple scales (engagement, satisfaction, etc.)")
    print("  • Temperature controls distribution sharpness")
    print("  • Can aggregate across journeys for survey-level statistics")
    print()
    print("Next Steps:")
    print("  • Integrate with your LLM for automated text generation")
    print("  • Use with persona/journey generators for end-to-end simulation")
    print("  • Analyze distributions for realistic test scenario creation")
    print()


if __name__ == "__main__":
    main()
