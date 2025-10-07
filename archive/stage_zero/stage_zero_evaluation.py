#!/usr/bin/env python3
"""
Evaluation framework for Stage Zero synthetic user responses and recommendations
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter
import statistics
import re


class StageZeroEvaluator:
    """Evaluate Stage Zero synthetic user data quality and patterns"""
    
    def __init__(self, data_path):
        with open(data_path, 'r') as f:
            self.users = json.load(f)
        print(f"Loaded {len(self.users)} users for evaluation")
    
    def evaluate_all(self):
        """Run all evaluation metrics"""
        print("\n" + "="*60)
        print("STAGE ZERO HEALTH - SYNTHETIC USER EVALUATION REPORT")
        print("="*60)
        
        self.evaluate_demographics()
        self.evaluate_completion_patterns()
        self.evaluate_risk_distribution()
        self.evaluate_open_ended_responses()
        self.evaluate_personalized_plans()
        self.evaluate_journey_quality()
        self.evaluate_learning_objectives()
    
    def evaluate_demographics(self):
        """Evaluate demographic distribution"""
        print("\n### DEMOGRAPHIC ANALYSIS ###")
        
        # Persona distribution
        personas = Counter(u["persona_type"] for u in self.users)
        print("\nPersona Distribution:")
        for persona, count in personas.most_common():
            print(f"  {persona}: {count} ({count/len(self.users)*100:.1f}%)")
        
        # Age distribution
        ages = [u["demographics"]["age"] for u in self.users]
        print(f"\nAge Statistics:")
        print(f"  Mean: {statistics.mean(ages):.1f}")
        print(f"  Median: {statistics.median(ages)}")
        print(f"  Range: {min(ages)}-{max(ages)}")
        
        # Age groups
        age_groups = defaultdict(int)
        for age in ages:
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
        
        print("\nAge Groups:")
        for group in ["18-29", "30-39", "40-49", "50-59", "60+"]:
            count = age_groups[group]
            print(f"  {group}: {count} ({count/len(self.users)*100:.1f}%)")
        
        # Gender distribution
        genders = Counter(u["demographics"]["biological_sex"] for u in self.users)
        print("\nGender Distribution:")
        for gender, count in genders.items():
            print(f"  {gender}: {count} ({count/len(self.users)*100:.1f}%)")
        
        # Insurance status
        insurance = Counter(u["demographics"]["insurance_type"] for u in self.users)
        print("\nInsurance Types:")
        for ins_type, count in insurance.most_common():
            print(f"  {ins_type}: {count} ({count/len(self.users)*100:.1f}%)")
    
    def evaluate_completion_patterns(self):
        """Evaluate journey completion patterns"""
        print("\n### COMPLETION PATTERN ANALYSIS ###")
        
        # Overall completion
        completion_by_week = defaultdict(int)
        for user in self.users:
            weeks_completed = len(user["weekly_journey"])
            completion_by_week[weeks_completed] += 1
        
        print("\nWeeks Completed Distribution:")
        for weeks in range(1, 11):
            count = completion_by_week.get(weeks, 0)
            cumulative = sum(completion_by_week.get(w, 0) for w in range(weeks, 11))
            print(f"  Week {weeks}: {cumulative} users ({cumulative/len(self.users)*100:.1f}% still active)")
        
        # Completion by persona
        print("\nCompletion Rates by Persona:")
        for persona in ["health_aware_avoider", "structured_system_seeker", 
                       "balanced_life_integrator", "healthcare_professional", 
                       "overlooked_risk_group"]:
            persona_users = [u for u in self.users if u["persona_type"] == persona]
            completed = sum(1 for u in persona_users if len(u["weekly_journey"]) == 10)
            print(f"  {persona}: {completed}/{len(persona_users)} ({completed/len(persona_users)*100:.1f}%)")
        
        # Dropout analysis
        dropout_weeks = []
        for user in self.users:
            if len(user["weekly_journey"]) < 10:
                dropout_weeks.append(len(user["weekly_journey"]))
        
        if dropout_weeks:
            print(f"\nDropout Statistics:")
            print(f"  Total dropouts: {len(dropout_weeks)} ({len(dropout_weeks)/len(self.users)*100:.1f}%)")
            print(f"  Average dropout week: {statistics.mean(dropout_weeks):.1f}")
            print(f"  Most common dropout week: {statistics.mode(dropout_weeks)}")
    
    def evaluate_risk_distribution(self):
        """Evaluate risk assessment distribution"""
        print("\n### RISK ASSESSMENT ANALYSIS ###")
        
        # GAIL risk categories
        gail_categories = Counter(u["risk_assessment"]["gail_category"] for u in self.users)
        print("\nGAIL Risk Categories:")
        for category in ["low", "average", "elevated"]:
            count = gail_categories.get(category, 0)
            print(f"  {category}: {count} ({count/len(self.users)*100:.1f}%)")
        
        # Genetic counseling indication
        genetic_counseling = sum(1 for u in self.users 
                               if u["risk_assessment"]["genetic_counseling_indicated"])
        print(f"\nGenetic Counseling Indicated: {genetic_counseling} ({genetic_counseling/len(self.users)*100:.1f}%)")
        
        # Risk factors by persona
        print("\nAverage Risk Factors by Persona:")
        for persona in ["health_aware_avoider", "structured_system_seeker", 
                       "balanced_life_integrator", "healthcare_professional", 
                       "overlooked_risk_group"]:
            persona_users = [u for u in self.users if u["persona_type"] == persona]
            avg_factors = statistics.mean(u["risk_assessment"]["risk_factors"] for u in persona_users)
            print(f"  {persona}: {avg_factors:.2f}")
    
    def evaluate_open_ended_responses(self):
        """Evaluate quality of open-ended responses"""
        print("\n### OPEN-ENDED RESPONSE ANALYSIS ###")
        
        # Response availability
        users_with_responses = sum(1 for u in self.users if u.get("open_ended_responses"))
        print(f"\nUsers with open-ended responses: {users_with_responses} ({users_with_responses/len(self.users)*100:.1f}%)")
        
        # Response types
        response_types = defaultdict(int)
        total_responses = 0
        
        for user in self.users:
            if user.get("open_ended_responses"):
                for key in user["open_ended_responses"]:
                    response_types[key] += 1
                    total_responses += 1
        
        print("\nResponse Types Collected:")
        for resp_type, count in sorted(response_types.items()):
            print(f"  {resp_type}: {count}")
        
        # Response quality metrics
        response_lengths = []
        for user in self.users:
            if user.get("open_ended_responses"):
                for response in user["open_ended_responses"].values():
                    response_lengths.append(len(response))
        
        if response_lengths:
            print(f"\nResponse Length Statistics:")
            print(f"  Average length: {statistics.mean(response_lengths):.0f} characters")
            print(f"  Median length: {statistics.median(response_lengths):.0f} characters")
            print(f"  Range: {min(response_lengths)}-{max(response_lengths)} characters")
        
        # Sample responses by persona
        print("\n### SAMPLE RESPONSES BY PERSONA ###")
        for persona in ["health_aware_avoider", "structured_system_seeker"]:
            print(f"\n{persona.upper()}:")
            persona_users = [u for u in self.users 
                           if u["persona_type"] == persona and u.get("open_ended_responses")]
            if persona_users:
                sample_user = persona_users[0]
                for key, response in list(sample_user["open_ended_responses"].items())[:2]:
                    print(f"\n{key}:")
                    print(f'"{response}"')
    
    def evaluate_personalized_plans(self):
        """Evaluate personalized plan quality"""
        print("\n### PERSONALIZED PLAN ANALYSIS ###")
        
        users_with_plans = [u for u in self.users if u.get("personalized_plan")]
        print(f"\nUsers with personalized plans: {len(users_with_plans)} ({len(users_with_plans)/len(self.users)*100:.1f}%)")
        
        if users_with_plans:
            # Satisfaction scores
            satisfaction_scores = [u["personalized_plan"]["satisfaction_score"] 
                                 for u in users_with_plans]
            print(f"\nPlan Satisfaction Scores:")
            print(f"  Average: {statistics.mean(satisfaction_scores):.1f}/10")
            print(f"  Median: {statistics.median(satisfaction_scores)}/10")
            
            # Implementation commitment
            commitment_scores = [u["personalized_plan"]["implementation_commitment"] 
                               for u in users_with_plans]
            print(f"\nImplementation Commitment:")
            print(f"  Average: {statistics.mean(commitment_scores):.1f}/10")
            print(f"  Median: {statistics.median(commitment_scores)}/10")
            
            # Immediate actions analysis
            action_counts = defaultdict(int)
            for user in users_with_plans:
                for action in user["personalized_plan"]["immediate_actions"]:
                    action_counts[action["action"]] += 1
            
            print("\nMost Common Immediate Actions:")
            for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {action}: {count} ({count/len(users_with_plans)*100:.1f}%)")
    
    def evaluate_journey_quality(self):
        """Evaluate journey quality metrics"""
        print("\n### JOURNEY QUALITY ANALYSIS ###")
        
        # Trust progression
        print("\nTrust Level Progression:")
        for week in range(1, 11):
            week_trust = []
            for user in self.users:
                week_data = next((w for w in user["weekly_journey"] if w["week"] == week), None)
                if week_data:
                    week_trust.append(week_data["trust_level"])
            
            if week_trust:
                print(f"  Week {week}: avg {statistics.mean(week_trust):.1f}, "
                      f"users: {len(week_trust)}")
        
        # Time spent analysis
        total_times = []
        for user in self.users:
            total_time = sum(w["time_spent_minutes"] for w in user["weekly_journey"])
            total_times.append(total_time)
        
        print(f"\nTotal Time Spent (minutes):")
        print(f"  Average: {statistics.mean(total_times):.0f}")
        print(f"  Median: {statistics.median(total_times):.0f}")
        print(f"  Range: {min(total_times)}-{max(total_times)}")
        
        # Emotional state patterns
        print("\nEmotional States by Week:")
        for week in [1, 5, 10]:
            week_emotions = []
            for user in self.users:
                week_data = next((w for w in user["weekly_journey"] if w["week"] == week), None)
                if week_data:
                    week_emotions.append(week_data["emotional_state"])
            
            if week_emotions:
                emotion_counts = Counter(week_emotions)
                print(f"\n  Week {week} (n={len(week_emotions)}):")
                for emotion, count in emotion_counts.most_common(3):
                    print(f"    {emotion}: {count} ({count/len(week_emotions)*100:.0f}%)")
    
    def evaluate_learning_objectives(self):
        """Evaluate against Stage Zero learning objectives"""
        print("\n### LEARNING OBJECTIVES EVALUATION ###")
        
        # Learning Objective 1: User Experience Validation
        print("\nLO1: User Experience Validation")
        week_1_completion = sum(1 for u in self.users if len(u["weekly_journey"]) >= 1)
        week_5_completion = sum(1 for u in self.users if len(u["weekly_journey"]) >= 5)
        week_10_completion = sum(1 for u in self.users if len(u["weekly_journey"]) >= 10)
        
        print(f"  Week 1 completion: {week_1_completion/len(self.users)*100:.1f}% (target: >85%)")
        print(f"  Week 5 completion: {week_5_completion/len(self.users)*100:.1f}% (target: >55%)")
        print(f"  Week 10 completion: {week_10_completion/len(self.users)*100:.1f}% (target: >35%)")
        
        # Trust progression
        users_with_full_journey = [u for u in self.users if len(u["weekly_journey"]) >= 5]
        if users_with_full_journey:
            early_trust = statistics.mean(u["weekly_journey"][0]["trust_level"] 
                                        for u in users_with_full_journey)
            late_trust = statistics.mean(u["weekly_journey"][-1]["trust_level"] 
                                       for u in users_with_full_journey)
            print(f"  Trust progression: {early_trust:.1f} → {late_trust:.1f}")
        
        # Learning Objective 2: Clinical Model Validation
        print("\nLO2: Clinical Model Validation")
        users_with_plans = [u for u in self.users if u.get("personalized_plan")]
        if users_with_plans:
            high_satisfaction = sum(1 for u in users_with_plans 
                                  if u["personalized_plan"]["satisfaction_score"] >= 8)
            print(f"  High plan satisfaction (≥8/10): {high_satisfaction/len(users_with_plans)*100:.1f}%")
        
        # Learning Objective 3: Business Model Validation
        print("\nLO3: Business Model Validation")
        if users_with_plans:
            high_commitment = sum(1 for u in users_with_plans 
                                if u["personalized_plan"]["implementation_commitment"] >= 7)
            print(f"  High implementation commitment (≥7/10): {high_commitment/len(users_with_plans)*100:.1f}%")
        
        # Net Promoter Score proxy (based on satisfaction)
        if users_with_plans:
            promoters = sum(1 for u in users_with_plans 
                          if u["personalized_plan"]["satisfaction_score"] >= 9)
            detractors = sum(1 for u in users_with_plans 
                           if u["personalized_plan"]["satisfaction_score"] <= 6)
            nps = (promoters - detractors) / len(users_with_plans) * 100
            print(f"  NPS proxy: {nps:.0f} (based on satisfaction scores)")


def main():
    parser = argparse.ArgumentParser(description='Evaluate Stage Zero synthetic user data')
    parser.add_argument(
        'data_file',
        help='Path to the synthetic user JSON file'
    )
    parser.add_argument(
        '--output',
        help='Save evaluation report to file'
    )
    
    args = parser.parse_args()
    
    # Create evaluator and run evaluation
    evaluator = StageZeroEvaluator(args.data_file)
    
    if args.output:
        # Redirect output to file
        import sys
        orig_stdout = sys.stdout
        with open(args.output, 'w') as f:
            sys.stdout = f
            evaluator.evaluate_all()
        sys.stdout = orig_stdout
        print(f"Evaluation report saved to {args.output}")
    else:
        evaluator.evaluate_all()


if __name__ == "__main__":
    main()