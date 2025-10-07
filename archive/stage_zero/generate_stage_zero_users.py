#!/usr/bin/env python3
"""
Generate 500 synthetic Stage Zero Health users with full 10-week assessment data
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
import argparse

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

# Import generator components (need to combine them into single file)
from stage_zero_generator import StageZeroGenerator


def convert_to_json_serializable(obj):
    """Convert dataclass objects to JSON-serializable format"""
    if hasattr(obj, '__dict__'):
        return {k: convert_to_json_serializable(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_json_serializable(v) for k, v in obj.items()}
    else:
        return obj


def main():
    parser = argparse.ArgumentParser(description='Generate Stage Zero Health synthetic users')
    parser.add_argument(
        '--count',
        type=int,
        default=500,
        help='Number of synthetic users to generate (default: 500)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducible generation'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output/stage_zero_users.json',
        help='Output file path (default: output/stage_zero_users.json)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Generate summary statistics'
    )
    
    args = parser.parse_args()
    
    print(f"Generating {args.count} synthetic Stage Zero Health users...")
    print(f"This includes full 10-week assessment journeys with open-ended responses.")
    
    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize generator
    generator = StageZeroGenerator(seed=args.seed)
    
    # Generate users
    start_time = datetime.now()
    users = generator.generate_users(count=args.count)
    
    # Convert to JSON-serializable format
    users_data = []
    for user in users:
        user_dict = asdict(user)
        users_data.append(user_dict)
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(users_data, f, indent=2, default=str)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n✓ Generated {len(users)} users in {duration:.1f} seconds")
    print(f"✓ Saved to {output_path}")
    
    # Generate summary statistics if requested
    if args.summary:
        print("\n=== Summary Statistics ===")
        
        # Persona distribution
        persona_counts = {}
        for user in users:
            persona = user.demographics.persona_type
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
        
        print("\nPersona Distribution:")
        for persona, count in sorted(persona_counts.items()):
            percentage = (count / len(users)) * 100
            print(f"  {persona}: {count} ({percentage:.1f}%)")
        
        # Completion statistics
        completion_stats = {
            "completed": 0,
            "partial": 0,
            "by_week": {i: 0 for i in range(1, 11)}
        }
        
        for user in users:
            weeks_completed = len(user.weekly_responses)
            if weeks_completed == 10:
                completion_stats["completed"] += 1
            else:
                completion_stats["partial"] += 1
            
            for i in range(1, weeks_completed + 1):
                completion_stats["by_week"][i] += 1
        
        print(f"\nCompletion Statistics:")
        print(f"  Completed full journey: {completion_stats['completed']} ({completion_stats['completed']/len(users)*100:.1f}%)")
        print(f"  Partial completion: {completion_stats['partial']} ({completion_stats['partial']/len(users)*100:.1f}%)")
        
        print(f"\nWeekly Completion Rates:")
        for week, count in completion_stats["by_week"].items():
            percentage = (count / len(users)) * 100
            print(f"  Week {week}: {count} ({percentage:.1f}%)")
        
        # Risk assessment distribution
        risk_categories = {
            "low": 0,
            "average": 0,
            "elevated": 0
        }
        
        genetic_counseling_count = 0
        
        for user in users:
            risk_categories[user.risk_assessment.gail_risk_category] += 1
            if user.risk_assessment.genetic_counseling_indicated:
                genetic_counseling_count += 1
        
        print(f"\nRisk Assessment Distribution:")
        for category, count in risk_categories.items():
            percentage = (count / len(users)) * 100
            print(f"  {category}: {count} ({percentage:.1f}%)")
        
        print(f"\nGenetic Counseling Indicated: {genetic_counseling_count} ({genetic_counseling_count/len(users)*100:.1f}%)")
        
        # Age distribution
        age_groups = {
            "18-29": 0,
            "30-39": 0,
            "40-49": 0,
            "50-59": 0,
            "60+": 0
        }
        
        for user in users:
            age = user.demographics.age
            if age < 30:
                age_groups["18-29"] += 1
            elif age < 40:
                age_groups["30-39"] += 1
            elif age < 50:
                age_groups["40-49"] += 1
            elif age < 60:
                age_groups["50-59"] += 1
            else:
                age_groups["60+"] += 1
        
        print(f"\nAge Distribution:")
        for group, count in age_groups.items():
            percentage = (count / len(users)) * 100
            print(f"  {group}: {count} ({percentage:.1f}%)")
        
        # Sample open-ended responses
        print(f"\n=== Sample Open-Ended Responses ===")
        
        # Find users with good responses
        completed_users = [u for u in users if len(u.weekly_responses) == 10]
        if completed_users:
            sample_user = completed_users[0]
            print(f"\nUser: {sample_user.demographics.preferred_name} ({sample_user.demographics.persona_type})")
            
            # Week 1 motivation
            week1_responses = sample_user.weekly_responses[0].open_ended_responses
            if "What brought you here today?" in week1_responses:
                print(f"\nWeek 1 - What brought you here today?")
                print(f'"{week1_responses["What brought you here today?"]}"')
            
            # Week 10 journey value
            if len(sample_user.weekly_responses) >= 10:
                week10_responses = sample_user.weekly_responses[9].open_ended_responses
                if "What was most valuable about this journey?" in week10_responses:
                    print(f"\nWeek 10 - What was most valuable about this journey?")
                    print(f'"{week10_responses["What was most valuable about this journey?"]}"')
        
        print(f"\n=== Personalized Plan Sample ===")
        
        # Find user with personalized plan
        users_with_plans = [u for u in users if u.personalized_plan is not None]
        if users_with_plans:
            sample_plan_user = users_with_plans[0]
            plan = sample_plan_user.personalized_plan
            
            print(f"\nUser: {sample_plan_user.demographics.preferred_name}")
            print(f"Risk Category: {sample_plan_user.risk_assessment.gail_risk_category}")
            print(f"\nRisk Summary:")
            print(f'"{plan.risk_summary}"')
            
            print(f"\nImmediate Actions:")
            for i, action in enumerate(plan.immediate_actions[:2], 1):
                print(f"{i}. {action['action']} - {action['timeline']}")
            
            print(f"\nPlan Satisfaction: {plan.plan_satisfaction_score}/10")
            print(f"Implementation Commitment: {plan.implementation_commitment}/10")


if __name__ == "__main__":
    main()