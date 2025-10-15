#!/usr/bin/env python3
"""
Estimate Anthropic API costs for SSR journey generation.
"""

import json
from pathlib import Path


def main():
    """Estimate costs for full journey generation with real LLM."""

    print("=" * 80)
    print("💰 LLM API Cost Estimation")
    print("=" * 80)
    print()

    # Load sample user to get typical journey length
    users_file = Path("output/private_language_synthetic_users.json")
    with open(users_file) as f:
        users_data = json.load(f)

    # Analyze journey lengths
    journey_lengths = []
    for user in users_data:
        if "journey" in user and "steps" in user["journey"]:
            journey_lengths.append(len(user["journey"]["steps"]))

    avg_steps = sum(journey_lengths) / len(journey_lengths) if journey_lengths else 15
    min_steps = min(journey_lengths) if journey_lengths else 12
    max_steps = max(journey_lengths) if journey_lengths else 19

    print("📊 Journey Analysis (from existing data)")
    print(f"   Average steps per journey: {avg_steps:.1f}")
    print(f"   Range: {min_steps} - {max_steps} steps")
    print()

    # API call structure
    scales_per_step = 4  # engagement, satisfaction, progress, relevance

    print("🔢 API Call Structure")
    print(f"   Scales per step: {scales_per_step}")
    print(f"   Total API calls per journey: {avg_steps:.0f} steps × {scales_per_step} scales = {avg_steps * scales_per_step:.0f} calls")
    print()

    # Token estimation (based on our test)
    # System prompt: ~150 tokens (persona context + instructions)
    # User prompt: ~50 tokens (stimulus + question)
    # Output: ~80-120 tokens (natural response)
    system_tokens = 150
    user_tokens = 50
    output_tokens = 100
    total_tokens_per_call = system_tokens + user_tokens + output_tokens

    print("🎯 Token Estimation (per API call)")
    print(f"   System prompt: ~{system_tokens} tokens")
    print(f"   User prompt: ~{user_tokens} tokens")
    print(f"   Response output: ~{output_tokens} tokens")
    print(f"   Total per call: ~{total_tokens_per_call} tokens")
    print()

    # Claude Sonnet 4.5 pricing (as of January 2025)
    input_cost_per_mtok = 3.00   # $3 per million input tokens
    output_cost_per_mtok = 15.00  # $15 per million output tokens

    print("💵 Claude Sonnet 4.5 Pricing")
    print(f"   Input tokens:  ${input_cost_per_mtok:.2f} per million")
    print(f"   Output tokens: ${output_cost_per_mtok:.2f} per million")
    print()

    # Calculate costs
    calls_per_journey = avg_steps * scales_per_step

    input_tokens_per_journey = calls_per_journey * (system_tokens + user_tokens)
    output_tokens_per_journey = calls_per_journey * output_tokens

    input_cost = (input_tokens_per_journey / 1_000_000) * input_cost_per_mtok
    output_cost = (output_tokens_per_journey / 1_000_000) * output_cost_per_mtok
    total_cost_per_journey = input_cost + output_cost

    print("=" * 80)
    print("💰 COST BREAKDOWN (per journey)")
    print("=" * 80)
    print()
    print(f"API calls: {calls_per_journey:.0f}")
    print()
    print(f"Input tokens:  {input_tokens_per_journey:>8,.0f} tokens × ${input_cost_per_mtok}/M = ${input_cost:>6.4f}")
    print(f"Output tokens: {output_tokens_per_journey:>8,.0f} tokens × ${output_cost_per_mtok}/M = ${output_cost:>6.4f}")
    print(f"{'-' * 80}")
    print(f"Total per journey: ${total_cost_per_journey:>6.4f} (~{total_cost_per_journey * 100:.1f}¢)")
    print()

    # Batch estimates
    print("=" * 80)
    print("📦 BATCH GENERATION COSTS")
    print("=" * 80)
    print()

    batch_sizes = [1, 10, 50, 100, 500]
    for size in batch_sizes:
        batch_cost = total_cost_per_journey * size
        print(f"   {size:>4} journeys: ${batch_cost:>8.2f} ({size * calls_per_journey:.0f} API calls)")

    print()

    # Time estimation
    seconds_per_call = 1.5  # Conservative estimate
    total_time_seconds = calls_per_journey * seconds_per_call
    total_time_minutes = total_time_seconds / 60

    print("=" * 80)
    print("⏱️  TIME ESTIMATION")
    print("=" * 80)
    print()
    print(f"Estimated time per API call: {seconds_per_call}s")
    print(f"Total time per journey: {total_time_seconds:.0f}s (~{total_time_minutes:.1f} minutes)")
    print()
    print("Note: Sequential calls. Could be parallelized for faster generation.")
    print()

    # Recommendations
    print("=" * 80)
    print("💡 RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("✅ ECONOMICAL:")
    print("   • Use simulated responses for bulk generation (free, instant)")
    print("   • Reserve real LLM for validation samples (5-10 users)")
    print("   • Enable real LLM only when needed for realism")
    print()
    print("⚠️  MODERATE:")
    print("   • Generate 10-50 journeys with real LLM (~$1-5)")
    print("   • Good for E2E testing with realistic data")
    print("   • Mix: Real LLM for critical personas, simulated for others")
    print()
    print("💸 EXPENSIVE:")
    print("   • Generate 500+ journeys with real LLM (~$50+)")
    print("   • Only if you need maximum realism across entire cohort")
    print("   • Consider caching/reusing responses where possible")
    print()

    # Cost comparison
    print("=" * 80)
    print("📊 COST COMPARISON")
    print("=" * 80)
    print()
    print(f"Simulated responses: $0.00 (instant)")
    print(f"Real LLM (Sonnet 4.5): ${total_cost_per_journey:.4f} per journey (~{total_time_minutes:.1f} min)")
    print()
    print("💡 Hybrid approach:")
    print(f"   • 5 real LLM journeys (validation): ${total_cost_per_journey * 5:.2f}")
    print(f"   • 495 simulated journeys (bulk): $0.00")
    print(f"   • Total: ${total_cost_per_journey * 5:.2f} for 500-user cohort")
    print()


if __name__ == "__main__":
    main()
