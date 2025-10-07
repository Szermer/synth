#!/usr/bin/env python3
"""
Generate Beta Test Simulation Cohort

Selects 3-5 Studio Practitioners from the 500-user cohort that match
the beta testing plan screening criteria:

Criteria (from BETA_TESTING_PLAN.md):
- Active studio practice (ceramics, woodworking, or similar hands-on)
- Teaching experience (workshops, classes, apprentices, or informal)
- 3+ years of practice (craft_experience_years)
- Tech comfort: moderate (0.4-0.7) - can navigate web apps
- Engagement tier: standard or high (willing to commit 2-4 hours/week)

Priority 1: Ceramics (best fit for initial validation)
Priority 2: Woodworking
"""

import json
import random
from collections import defaultdict

# Load 500-user cohort
with open('output/private_language_synthetic_users.json', 'r') as f:
    users = json.load(f)

print("=" * 80)
print("BETA TEST COHORT GENERATION")
print("=" * 80)
print(f"\nTotal Users in Cohort: {len(users)}\n")

# Filter for Studio Practitioners
studio_practitioners = [u for u in users if u['persona_type'] == 'studio_practitioner']
print(f"Studio Practitioners: {len(studio_practitioners)}")

# Apply beta tester criteria
beta_candidates = []

for user in studio_practitioners:
    attrs = user['attributes']

    # Criteria checks
    medium = attrs.get('medium', '')
    tech_comfort = attrs.get('tech_comfort', 0.5)
    engagement_tier = attrs.get('engagement_tier', 'standard')
    craft_experience = attrs.get('craft_experience_years', 0)
    teaching_hours = attrs.get('teaching_hours_per_month', 0)

    # Priority mediums
    is_ceramics = medium == 'ceramics_pottery'
    is_woodworking = medium == 'woodworking'
    is_priority_medium = is_ceramics or is_woodworking

    # Tech comfort range
    has_moderate_tech = 0.4 <= tech_comfort <= 0.7

    # Engagement (exclude low)
    is_engaged = engagement_tier in ['standard', 'high']

    # Experience (3+ years)
    has_experience = craft_experience >= 3

    # Teaching experience (any teaching)
    has_teaching = teaching_hours > 0

    # All criteria
    meets_criteria = (
        is_priority_medium and
        has_moderate_tech and
        is_engaged and
        has_experience and
        has_teaching
    )

    if meets_criteria:
        beta_candidates.append({
            'user': user,
            'medium': medium,
            'tech_comfort': tech_comfort,
            'engagement_tier': engagement_tier,
            'craft_experience_years': craft_experience,
            'teaching_hours_per_month': teaching_hours,
            'priority': 1 if is_ceramics else 2
        })

print(f"\nCandidates Meeting Beta Criteria: {len(beta_candidates)}")

# Sort by priority (ceramics first) and engagement tier
beta_candidates.sort(key=lambda x: (x['priority'], -['low', 'standard', 'high'].index(x['engagement_tier'])))

# Select 3-5 testers
num_testers = min(5, len(beta_candidates))
selected_testers = beta_candidates[:num_testers]

print(f"\n{'=' * 80}")
print(f"SELECTED BETA TESTERS ({num_testers})")
print('=' * 80)

beta_test_cohort = []

for i, tester in enumerate(selected_testers, 1):
    user = tester['user']
    attrs = user['attributes']

    print(f"\n--- BETA TESTER #{i} ---")
    print(f"Name: {user['name']}")
    print(f"Age: {user['age']}")
    print(f"Gender: {user['gender']}")
    print(f"Medium: {tester['medium']}")
    print(f"Craft Experience: {tester['craft_experience_years']:.0f} years")
    print(f"Tech Comfort: {tester['tech_comfort']:.2f} (moderate)")
    print(f"Engagement Tier: {tester['engagement_tier']}")
    print(f"Teaching Hours/Month: {tester['teaching_hours_per_month']:.0f}")
    print(f"Practice Type: {attrs.get('practice_type', 'unknown')}")
    print(f"Career Stage: {attrs.get('career_stage', 'unknown')}")
    print(f"Capture Behavior: {attrs.get('capture_behavior', 'unknown')}")

    # Journey stats
    if 'journey' in user and 'steps' in user['journey']:
        steps = user['journey']['steps']
        completed_steps = [s for s in steps if s.get('completion_status') == 'completed']
        print(f"Journey Sessions: {len(steps)}")
        print(f"Completed Sessions: {len(completed_steps)} ({len(completed_steps)/len(steps)*100:.0f}%)")

        # First session details (beta test focus)
        if steps:
            first_session = steps[0]
            print(f"\nFirst Session Simulation:")
            print(f"  Phase: {first_session.get('phase_name', 'discovery')}")
            print(f"  Emotional State: {first_session.get('emotional_state', 'unknown')}")
            print(f"  Time Invested: {first_session.get('time_invested_minutes', 15)} min")
            print(f"  Completed: {'Yes' if first_session.get('completion_status') == 'completed' else 'No'}")
            print(f"  Engagement Score: {first_session.get('engagement_score', 0.5):.2f}")

    # Add to cohort
    beta_test_cohort.append(user)

# Save beta test cohort
with open('output/beta_test_cohort.json', 'w') as f:
    json.dump(beta_test_cohort, f, indent=2, default=str)

print(f"\n{'=' * 80}")
print("BETA COHORT CHARACTERISTICS")
print('=' * 80)

# Analyze cohort
mediums = [t['medium'] for t in selected_testers]
engagements = [t['engagement_tier'] for t in selected_testers]
captures = [t['user']['attributes'].get('capture_behavior') for t in selected_testers]

print(f"\nMedium Distribution:")
for medium in set(mediums):
    count = mediums.count(medium)
    print(f"  {medium}: {count} ({count/len(mediums)*100:.0f}%)")

print(f"\nEngagement Tier Distribution:")
for tier in ['high', 'standard', 'low']:
    count = engagements.count(tier)
    if count > 0:
        print(f"  {tier}: {count} ({count/len(engagements)*100:.0f}%)")

print(f"\nCapture Behavior Distribution:")
for behavior in set(captures):
    count = captures.count(behavior)
    print(f"  {behavior}: {count} ({count/len(captures)*100:.0f}%)")

print(f"\nTech Comfort Range:")
tech_comforts = [t['tech_comfort'] for t in selected_testers]
print(f"  Min: {min(tech_comforts):.2f}")
print(f"  Max: {max(tech_comforts):.2f}")
print(f"  Avg: {sum(tech_comforts)/len(tech_comforts):.2f}")

print(f"\nCraft Experience Range:")
experiences = [t['craft_experience_years'] for t in selected_testers]
print(f"  Min: {min(experiences):.0f} years")
print(f"  Max: {max(experiences):.0f} years")
print(f"  Avg: {sum(experiences)/len(experiences):.1f} years")

print(f"\n{'=' * 80}")
print("BETA TEST SCENARIOS")
print('=' * 80)

print("""
These beta testers represent realistic users for Nov-Dec 2025 beta test:

Use Cases:
1. First capture session validation (Week 1-2)
2. Extraction quality across 6 dimensions (Week 1-4)
3. Natural language query satisfaction (Week 3-4)
4. Review interface usability (Week 5-6)
5. Long-term value assessment (Week 5-6)

Expected Patterns:
- High engagement: Daily uploads, comprehensive feedback
- Standard engagement: 2-3x weekly uploads, focused testing
- Systematic capture: Regular 2-7 day intervals
- Opportunistic: Variable intervals based on studio schedule
- Crisis-driven: Burst testing around deadlines

Validation Metrics:
- Extraction accuracy >85% (measured by tester approval)
- Query satisfaction >85% "helpful"
- Review efficiency: >60% of flagged items reviewed
- Retention: >75% complete all 6 weeks
- NPS: >0 (more promoters than detractors)
""")

print(f"\n✅ Beta test cohort saved to: output/beta_test_cohort.json")
print(f"✅ {num_testers} testers selected matching screening criteria")
print(f"✅ Ready for E2E test scenario generation\n")
