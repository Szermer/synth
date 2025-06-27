#!/usr/bin/env python3
"""
Generate 500 synthetic Stage Zero Health users with full 10-week assessment data
This is a simplified version that demonstrates the structure.
"""

import json
import random
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import argparse

# For this demonstration, we'll create a simplified version
# In production, this would include all the methods from the generator parts

@dataclass
class StageZeroUser:
    """Simplified Stage Zero user for demonstration"""
    user_id: str
    persona_type: str
    demographics: Dict[str, Any]
    family_history: Dict[str, Any]
    reproductive_history: Dict[str, Any]
    healthcare_access: Dict[str, Any]
    lifestyle_factors: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    weekly_journey: List[Dict[str, Any]]
    personalized_plan: Optional[Dict[str, Any]]
    open_ended_responses: Dict[str, Any]


class StageZeroGenerator:
    """Simplified generator for demonstration"""
    
    PERSONAS = {
        "health_aware_avoider": 0.30,
        "structured_system_seeker": 0.25,
        "balanced_life_integrator": 0.20,
        "healthcare_professional": 0.15,
        "overlooked_risk_group": 0.10
    }
    
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
    
    def generate_users(self, count=500):
        """Generate synthetic users"""
        users = []
        
        # Calculate persona distribution
        for persona, ratio in self.PERSONAS.items():
            persona_count = int(count * ratio)
            for _ in range(persona_count):
                user = self.generate_user(persona)
                users.append(user)
        
        # Ensure we have exactly the requested count
        while len(users) < count:
            persona = random.choice(list(self.PERSONAS.keys()))
            users.append(self.generate_user(persona))
        
        return users[:count]
    
    def generate_user(self, persona_type):
        """Generate a single user with full journey"""
        user_id = str(uuid.uuid4())
        
        # Demographics
        age = random.randint(25, 60)
        demographics = {
            "user_id": user_id,
            "persona_type": persona_type,
            "preferred_name": self.generate_name(),
            "age": age,
            "biological_sex": "female" if random.random() < 0.95 else "male",
            "race_ethnicity": random.choice([
                "Non-Hispanic White", "Hispanic", "Non-Hispanic Black", 
                "Non-Hispanic Asian/Pacific Islander", "Other"
            ]),
            "education": random.choice(["high_school", "some_college", "bachelors", "masters"]),
            "location_type": random.choice(["urban", "suburban", "rural"]),
            "insurance_type": random.choice(["employer", "marketplace", "medicaid", "uninsured"])
        }
        
        # Family history
        family_history = {
            "mother_cancer": random.random() < 0.20,
            "father_cancer": random.random() < 0.15,
            "siblings_cancer": random.random() < 0.10,
            "family_communication": random.choice(["very_open", "somewhat_open", "private"]),
            "genetic_counseling_indicated": random.random() < 0.15
        }
        
        # Reproductive history (if female)
        reproductive_history = {}
        if demographics["biological_sex"] == "female":
            reproductive_history = {
                "age_at_menarche": random.randint(10, 16),
                "pregnancies": random.choices([0, 1, 2, 3], weights=[0.3, 0.3, 0.3, 0.1])[0],
                "age_at_first_birth": random.randint(20, 35) if random.random() < 0.7 else None,
                "breastfeeding_months": random.randint(0, 24) if random.random() < 0.6 else 0,
                "hormone_use": random.random() < 0.5
            }
        
        # Healthcare access
        healthcare_access = {
            "has_primary_care": random.random() < 0.80,
            "provider_relationship": random.choice(["excellent", "good", "fair", "poor"]),
            "healthcare_comfort": random.randint(3, 9),
            "screening_barriers": self.get_screening_barriers(persona_type),
            "last_mammogram": age - random.randint(1, 5) if age >= 40 and random.random() < 0.7 else None
        }
        
        # Lifestyle factors
        lifestyle_factors = {
            "physical_activity": random.choice(["high", "moderate", "low"]),
            "alcohol_use": random.choice(["never", "rare", "occasional", "moderate", "frequent"]),
            "smoking": random.choice(["never", "former", "current"]),
            "stress_level": random.randint(3, 9),
            "sleep_quality": random.choice(["excellent", "good", "fair", "poor"])
        }
        
        # Risk assessment
        risk_assessment = self.calculate_risk(demographics, family_history, reproductive_history, lifestyle_factors)
        
        # Generate 10-week journey
        weekly_journey = self.generate_weekly_journey(persona_type, demographics, family_history)
        
        # Generate open-ended responses
        open_ended_responses = self.generate_open_ended_responses(
            persona_type, demographics, family_history, weekly_journey
        )
        
        # Generate personalized plan if completed
        personalized_plan = None
        if len(weekly_journey) == 10 and weekly_journey[-1]["completed"]:
            personalized_plan = self.generate_personalized_plan(
                demographics, risk_assessment, healthcare_access
            )
        
        return StageZeroUser(
            user_id=user_id,
            persona_type=persona_type,
            demographics=demographics,
            family_history=family_history,
            reproductive_history=reproductive_history,
            healthcare_access=healthcare_access,
            lifestyle_factors=lifestyle_factors,
            risk_assessment=risk_assessment,
            weekly_journey=weekly_journey,
            personalized_plan=personalized_plan,
            open_ended_responses=open_ended_responses
        )
    
    def generate_name(self):
        """Generate a realistic name"""
        first_names = ["Sarah", "Emma", "Jessica", "Maria", "Lisa", "Jennifer", "Amanda", 
                      "Michelle", "Patricia", "Linda", "Barbara", "Elizabeth", "Susan"]
        return random.choice(first_names)
    
    def get_screening_barriers(self, persona_type):
        """Get screening barriers based on persona"""
        barrier_options = ["cost", "time", "fear", "access", "childcare", "work_schedule"]
        
        if persona_type == "health_aware_avoider":
            return random.sample(["fear", "anxiety", "avoidance"], k=2)
        elif persona_type == "overlooked_risk_group":
            return random.sample(["cost", "access", "time", "work_schedule"], k=2)
        else:
            return random.sample(barrier_options, k=random.randint(0, 2))
    
    def calculate_risk(self, demographics, family_history, reproductive_history, lifestyle_factors):
        """Calculate simplified risk scores"""
        # Simplified risk calculation
        risk_factors = 0
        
        if demographics["age"] >= 50:
            risk_factors += 1
        if family_history["mother_cancer"]:
            risk_factors += 2
        if lifestyle_factors["alcohol_use"] in ["moderate", "frequent"]:
            risk_factors += 1
        
        gail_score = 1.0 + (risk_factors * 0.3)
        
        return {
            "gail_score": round(gail_score, 2),
            "gail_category": "elevated" if gail_score >= 1.67 else "average" if gail_score >= 1.3 else "low",
            "risk_factors": risk_factors,
            "genetic_counseling_indicated": family_history["genetic_counseling_indicated"]
        }
    
    def generate_weekly_journey(self, persona_type, demographics, family_history):
        """Generate 10-week journey with progressive completion"""
        journey = []
        
        # Determine completion based on persona
        completion_probs = {
            "health_aware_avoider": 0.25,
            "structured_system_seeker": 0.65,
            "balanced_life_integrator": 0.45,
            "healthcare_professional": 0.55,
            "overlooked_risk_group": 0.20
        }
        
        completes_journey = random.random() < completion_probs[persona_type]
        dropout_week = 10 if completes_journey else random.randint(3, 8)
        
        # Progressive trust levels
        trust_level = 5
        
        for week in range(1, 11):
            if week > dropout_week:
                break
                
            journey.append({
                "week": week,
                "completed": True,
                "trust_level": min(10, trust_level),
                "time_spent_minutes": random.randint(10, 30),
                "emotional_state": self.get_emotional_state(persona_type, week)
            })
            
            trust_level += 0.5
        
        return journey
    
    def get_emotional_state(self, persona_type, week):
        """Get emotional state for week"""
        states = {
            "health_aware_avoider": ["anxious", "overwhelmed", "uncertain", "hopeful"],
            "structured_system_seeker": ["curious", "engaged", "motivated", "satisfied"],
            "balanced_life_integrator": ["thoughtful", "balanced", "confident", "grateful"],
            "healthcare_professional": ["analytical", "interested", "confident", "validated"],
            "overlooked_risk_group": ["confused", "uncertain", "hopeful", "empowered"]
        }
        
        persona_states = states[persona_type]
        if week <= 3:
            return persona_states[0]
        elif week <= 6:
            return persona_states[1]
        elif week <= 8:
            return persona_states[2]
        else:
            return persona_states[3]
    
    def generate_open_ended_responses(self, persona_type, demographics, family_history, journey):
        """Generate credible open-ended responses"""
        responses = {}
        
        # Week 1: What brought you here?
        motivations = {
            "health_aware_avoider": [
                f"My sister was diagnosed with breast cancer last year. I've been avoiding thinking about my own risk but I can't anymore.",
                f"I turned {demographics['age']} and my doctor keeps mentioning screening. I'm terrified but I know I need to face this.",
                f"I've been having anxiety about cancer for months. Maybe knowing my actual risk will help."
            ],
            "structured_system_seeker": [
                f"I'm {demographics['age']} now and want to understand my health risks comprehensively.",
                f"I track everything about my health. Time to add cancer risk assessment to my health data.",
                f"I like to plan ahead. Understanding my risk helps me make informed decisions."
            ],
            "balanced_life_integrator": [
                f"I've been focusing on overall wellness and this seems like an important piece.",
                f"A friend recommended this. I like the holistic approach to health assessment.",
                f"I want to be proactive about my health without letting fear control my life."
            ],
            "healthcare_professional": [
                f"I counsel patients about screening daily but realized I don't know my own risk profile.",
                f"As a healthcare provider, I should practice what I preach about prevention.",
                f"I want to understand the patient experience with risk assessment tools."
            ],
            "overlooked_risk_group": [
                f"My cousin said I should check this out. I don't usually do these health things.",
                f"My doctor mentioned it but I don't really understand why I need this.",
                f"I saw information about this and figured I should try it."
            ]
        }
        
        responses["week_1_motivation"] = random.choice(motivations[persona_type])
        
        # Week 2: Family impact
        if family_history["mother_cancer"]:
            impacts = {
                "health_aware_avoider": "Watching my mom go through treatment was traumatic. I've been terrified ever since.",
                "structured_system_seeker": "It made me very proactive about tracking family health history and screening schedules.",
                "balanced_life_integrator": "It taught me that health is important but you can't let fear control your life.",
                "healthcare_professional": "It influenced my career choice. I wanted to help families like mine.",
                "overlooked_risk_group": "It was scary and confusing. We didn't really understand what was happening."
            }
            responses["week_2_family_impact"] = impacts[persona_type]
        
        # Week 10: Journey value (if completed)
        if len(journey) == 10:
            values = {
                "health_aware_avoider": "I finally faced something I've been avoiding for years. The gradual approach made it manageable.",
                "structured_system_seeker": "The comprehensive assessment was exactly what I needed. Data-driven and thorough.",
                "balanced_life_integrator": "I loved how it considered my whole life, not just medical factors. Very holistic.",
                "healthcare_professional": "This gave me insights I'll use with my own patients. The personalization was impressive.",
                "overlooked_risk_group": "Someone finally explained everything in ways I could understand. I feel less lost now."
            }
            responses["week_10_value"] = values[persona_type]
        
        return responses
    
    def generate_personalized_plan(self, demographics, risk_assessment, healthcare_access):
        """Generate personalized detection plan"""
        plan = {
            "risk_summary": f"Based on your assessment, your breast cancer risk is {risk_assessment['gail_category']}. "
                          f"Your personalized GAIL score is {risk_assessment['gail_score']}.",
            "immediate_actions": [],
            "screening_schedule": {},
            "satisfaction_score": random.randint(7, 10),
            "implementation_commitment": random.randint(6, 9)
        }
        
        # Add immediate actions
        if not healthcare_access["has_primary_care"]:
            plan["immediate_actions"].append({
                "action": "Find primary care provider",
                "timeline": "Within 30 days",
                "priority": "high"
            })
        
        if demographics["age"] >= 40 and not healthcare_access["last_mammogram"]:
            plan["immediate_actions"].append({
                "action": "Schedule baseline mammogram",
                "timeline": "Within 60 days",
                "priority": "high"
            })
        
        # Screening schedule
        if risk_assessment["gail_category"] == "elevated":
            plan["screening_schedule"]["mammogram"] = "Annual"
        elif demographics["age"] >= 50:
            plan["screening_schedule"]["mammogram"] = "Every 2 years"
        else:
            plan["screening_schedule"]["mammogram"] = "Discuss with provider"
        
        return plan


def main():
    parser = argparse.ArgumentParser(description='Generate Stage Zero Health synthetic users')
    parser.add_argument('--count', type=int, default=500)
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--output', type=str, default='output/stage_zero_users.json')
    parser.add_argument('--summary', action='store_true')
    
    args = parser.parse_args()
    
    print(f"Generating {args.count} synthetic Stage Zero Health users...")
    
    # Create generator
    generator = StageZeroGenerator(seed=args.seed)
    
    # Generate users
    users = generator.generate_users(count=args.count)
    
    # Convert to dict for JSON serialization
    users_data = []
    for user in users:
        user_dict = {
            "user_id": user.user_id,
            "persona_type": user.persona_type,
            "demographics": user.demographics,
            "family_history": user.family_history,
            "reproductive_history": user.reproductive_history,
            "healthcare_access": user.healthcare_access,
            "lifestyle_factors": user.lifestyle_factors,
            "risk_assessment": user.risk_assessment,
            "weekly_journey": user.weekly_journey,
            "personalized_plan": user.personalized_plan,
            "open_ended_responses": user.open_ended_responses
        }
        users_data.append(user_dict)
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(users_data, f, indent=2, default=str)
    
    print(f"✓ Generated {len(users)} users")
    print(f"✓ Saved to {output_path}")
    
    if args.summary:
        print("\n=== Summary Statistics ===")
        
        # Completion stats
        completed = sum(1 for u in users if len(u.weekly_journey) == 10)
        print(f"\nCompletion rate: {completed}/{len(users)} ({completed/len(users)*100:.1f}%)")
        
        # Risk distribution
        risk_dist = {"low": 0, "average": 0, "elevated": 0}
        for user in users:
            risk_dist[user.risk_assessment["gail_category"]] += 1
        
        print("\nRisk Distribution:")
        for cat, count in risk_dist.items():
            print(f"  {cat}: {count} ({count/len(users)*100:.1f}%)")
        
        # Sample responses
        print("\n=== Sample Open-Ended Responses ===")
        sample_user = random.choice([u for u in users if u.open_ended_responses])
        print(f"\nUser: {sample_user.demographics['preferred_name']} ({sample_user.persona_type})")
        print(f"\nWeek 1 - Motivation:")
        print(f'"{sample_user.open_ended_responses.get("week_1_motivation", "N/A")}"')


if __name__ == "__main__":
    main()