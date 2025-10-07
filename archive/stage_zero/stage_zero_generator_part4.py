"""
Stage Zero Generator - Part 4: Journey simulation and personalized plans
"""

from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional
from stage_zero_response_generator import ResponseGenerator


def generate_weekly_journey(
    self,
    demographics: Demographics,
    persona_type: str,
    family_history: FamilyHistory,
    reproductive_history: ReproductiveHistory,
    healthcare_access: HealthcareAccess,
    lifestyle_factors: LifestyleFactors,
    current_health: CurrentHealth,
    support_system: SupportSystem,
    values_preferences: ValuesPreferences
) -> List[WeeklyResponse]:
    """Generate the full 10-week journey with progressive completion"""
    
    weekly_responses = []
    response_generator = ResponseGenerator()
    
    # Context for response generation
    user_context = {
        "age": demographics.age,
        "occupation": lifestyle_factors.occupation_type,
        "has_children": reproductive_history.pregnancies > 0,
        "high_anxiety": persona_type == "health_aware_avoider",
        "location_type": demographics.location_type,
        "insurance_type": demographics.insurance_type
    }
    
    # Starting timestamp
    start_date = datetime.now() - timedelta(days=random.randint(70, 100))
    current_date = start_date
    
    # Trust progression
    trust_level = 5 if persona_type != "healthcare_professional" else 7
    
    # Emotional state progression
    emotional_journey = self.get_emotional_journey(persona_type)
    
    # Determine dropout week based on persona and random factors
    dropout_week = self.determine_dropout_week(persona_type)
    
    for week_num in range(1, 11):
        # Check if user drops out
        if week_num > dropout_week:
            break
        
        # Create weekly response
        week_response = WeeklyResponse(
            week_number=week_num,
            completion_status="completed" if week_num < dropout_week else "partial",
            completion_timestamp=current_date.isoformat(),
            time_spent_minutes=self.get_time_spent(week_num, persona_type),
            emotional_state=emotional_journey[week_num - 1],
            trust_level=min(10, trust_level),
            responses={},
            open_ended_responses={}
        )
        
        # Generate structured responses based on week
        week_response.responses = self.generate_structured_responses(
            week_num, demographics, family_history, reproductive_history,
            healthcare_access, lifestyle_factors, current_health,
            support_system, values_preferences
        )
        
        # Generate open-ended responses
        week_response.open_ended_responses = response_generator.generate_week_responses(
            week_num, persona_type, user_context
        )
        
        weekly_responses.append(week_response)
        
        # Update for next week
        current_date += timedelta(days=random.randint(6, 9))
        trust_level += 0.3 if week_num <= 5 else 0.2
    
    return weekly_responses


def get_emotional_journey(self, persona_type: str) -> List[str]:
    """Get emotional state progression for persona"""
    journeys = {
        "health_aware_avoider": [
            "anxious", "anxious", "overwhelmed", "anxious", "uncertain",
            "overwhelmed", "concerned", "anxious", "hopeful", "relieved"
        ],
        "structured_system_seeker": [
            "curious", "engaged", "motivated", "engaged", "determined",
            "engaged", "confident", "motivated", "satisfied", "accomplished"
        ],
        "balanced_life_integrator": [
            "curious", "thoughtful", "engaged", "thoughtful", "balanced",
            "engaged", "confident", "thoughtful", "satisfied", "grateful"
        ],
        "healthcare_professional": [
            "analytical", "engaged", "curious", "analytical", "engaged",
            "interested", "confident", "analytical", "satisfied", "validated"
        ],
        "overlooked_risk_group": [
            "uncertain", "confused", "uncertain", "overwhelmed", "confused",
            "uncertain", "concerned", "hopeful", "surprised", "empowered"
        ]
    }
    return journeys.get(persona_type, ["neutral"] * 10)


def determine_dropout_week(self, persona_type: str) -> int:
    """Determine which week user drops out (11 means completed)"""
    # Base completion probabilities by persona
    completion_probs = {
        "health_aware_avoider": 0.25,
        "structured_system_seeker": 0.65,
        "balanced_life_integrator": 0.45,
        "healthcare_professional": 0.55,
        "overlooked_risk_group": 0.20
    }
    
    base_prob = completion_probs[persona_type]
    
    # If user completes
    if random.random() < base_prob:
        return 11
    
    # Otherwise, determine dropout week
    # Higher probability of dropping out in middle weeks
    dropout_weights = {
        2: 0.10,
        3: 0.15,
        4: 0.15,
        5: 0.20,
        6: 0.15,
        7: 0.10,
        8: 0.10,
        9: 0.05
    }
    
    weeks = list(dropout_weights.keys())
    weights = list(dropout_weights.values())
    
    return random.choices(weeks, weights=weights)[0]


def get_time_spent(self, week_number: int, persona_type: str) -> int:
    """Get time spent on week based on persona and week number"""
    # Base time by week
    base_times = {
        1: 15, 2: 20, 3: 25, 4: 20, 5: 15,
        6: 30, 7: 20, 8: 20, 9: 15, 10: 25
    }
    
    base_time = base_times.get(week_number, 20)
    
    # Adjust by persona
    time_multipliers = {
        "health_aware_avoider": 0.7,  # Rushes through due to anxiety
        "structured_system_seeker": 1.3,  # Takes time to be thorough
        "balanced_life_integrator": 1.0,  # Average pace
        "healthcare_professional": 0.9,  # Efficient but thorough
        "overlooked_risk_group": 0.8   # May skip some parts
    }
    
    multiplier = time_multipliers.get(persona_type, 1.0)
    
    # Add some randomness
    final_time = int(base_time * multiplier * random.uniform(0.8, 1.2))
    
    return final_time


def generate_structured_responses(
    self,
    week_number: int,
    demographics: Demographics,
    family_history: FamilyHistory,
    reproductive_history: ReproductiveHistory,
    healthcare_access: HealthcareAccess,
    lifestyle_factors: LifestyleFactors,
    current_health: CurrentHealth,
    support_system: SupportSystem,
    values_preferences: ValuesPreferences
) -> Dict[str, Any]:
    """Generate structured responses for a specific week"""
    
    responses = {}
    
    if week_number == 1:
        # Week 1: Foundation
        responses["biological_sex"] = demographics.biological_sex
        responses["race_ethnicity"] = demographics.race_ethnicity
        responses["health_relationship"] = random.choice([
            "very_proactive", "somewhat_proactive", "reactive", "avoidant", "complicated"
        ])
        responses["current_health_status"] = current_health.overall_health
        responses["health_insurance"] = demographics.insurance_type != "uninsured"
        responses["healthcare_providers"] = {
            "primary_care": healthcare_access.has_primary_care,
            "obgyn": healthcare_access.has_obgyn,
            "specialists": random.random() < 0.3
        }
        responses["provider_comfort"] = healthcare_access.healthcare_comfort
        
    elif week_number == 2:
        # Week 2: Family history
        responses["mother_cancer"] = family_history.mother_cancer is not None
        if family_history.mother_cancer:
            responses["mother_cancer_details"] = family_history.mother_cancer
        responses["father_cancer"] = family_history.father_cancer is not None
        if family_history.father_cancer:
            responses["father_cancer_details"] = family_history.father_cancer
        responses["siblings_cancer"] = len(family_history.siblings_cancer) > 0
        if family_history.siblings_cancer:
            responses["siblings_cancer_details"] = family_history.siblings_cancer
        responses["family_communication"] = family_history.family_communication
        
    elif week_number == 3:
        # Week 3: Reproductive history
        responses["age_at_menarche"] = reproductive_history.age_at_menarche
        responses["pregnancies"] = reproductive_history.pregnancies
        if reproductive_history.pregnancies > 0:
            responses["age_at_first_birth"] = reproductive_history.age_at_first_birth
            responses["breastfeeding_months"] = reproductive_history.breastfeeding_months
        responses["menopause_status"] = reproductive_history.menopause_age is not None
        if reproductive_history.menopause_age:
            responses["menopause_age"] = reproductive_history.menopause_age
        responses["hormone_use"] = reproductive_history.hormone_use
        
    elif week_number == 4:
        # Week 4: Healthcare access
        responses["healthcare_access_quality"] = random.choice([
            "excellent", "good", "fair", "poor", "very_poor"
        ])
        responses["provider_relationships"] = healthcare_access.provider_relationship_quality
        responses["mammogram_history"] = healthcare_access.last_mammogram_age is not None
        if healthcare_access.last_mammogram_age:
            responses["last_mammogram_age"] = healthcare_access.last_mammogram_age
            responses["mammogram_experience"] = healthcare_access.mammogram_experience
        responses["screening_barriers"] = healthcare_access.screening_barriers
        responses["healthcare_decision_process"] = random.choice([
            "independent", "provider_guided", "family_involved", "research_based"
        ])
        
    elif week_number == 5:
        # Week 5: Lifestyle
        responses["work_routine"] = lifestyle_factors.occupation_type
        responses["schedule_control"] = random.choice(["high", "moderate", "low", "none"])
        responses["physical_activity"] = lifestyle_factors.physical_activity_level
        responses["alcohol_use"] = lifestyle_factors.alcohol_frequency
        responses["smoking_status"] = lifestyle_factors.smoking_status
        responses["stress_level"] = lifestyle_factors.stress_level
        responses["stress_sources"] = random.sample([
            "work", "family", "health", "financial", "relationships"
        ], k=random.randint(1, 3))
        responses["sleep_quality"] = lifestyle_factors.sleep_quality
        
    elif week_number == 6:
        # Week 6: Extended family
        responses["grandparents_cancer"] = len(family_history.grandparents_cancer)
        if family_history.grandparents_cancer:
            responses["grandparents_cancer_details"] = family_history.grandparents_cancer
        responses["aunts_uncles_cancer"] = len(family_history.aunts_uncles_cancer)
        if family_history.aunts_uncles_cancer:
            responses["aunts_uncles_cancer_details"] = family_history.aunts_uncles_cancer
        responses["family_patterns"] = family_history.family_patterns_recognized
        responses["ethnic_heritage"] = demographics.race_ethnicity
        responses["genetic_testing_interest"] = random.choice([
            "very_interested", "somewhat_interested", "unsure", "not_interested"
        ])
        
    elif week_number == 7:
        # Week 7: Current health
        responses["overall_health"] = current_health.overall_health
        responses["health_changes"] = random.random() < 0.3
        responses["breast_health_awareness"] = current_health.breast_health_awareness
        responses["current_symptoms"] = current_health.current_symptoms
        responses["self_exam_practice"] = random.choice([
            "regularly", "occasionally", "rarely", "never"
        ])
        responses["medical_exam_comfort"] = healthcare_access.healthcare_comfort
        responses["self_advocacy_confidence"] = healthcare_access.healthcare_navigation_confidence
        responses["health_priorities"] = random.sample([
            "prevention", "family", "career", "wellness", "longevity"
        ], k=random.randint(2, 3))
        
    elif week_number == 8:
        # Week 8: Support systems
        responses["family_support"] = support_system.family_support_level
        responses["partner_support"] = support_system.partner_support
        responses["community_connections"] = support_system.community_connections
        responses["financial_situation"] = support_system.financial_stability
        responses["transportation"] = support_system.transportation_access
        responses["childcare_needs"] = support_system.childcare_needs
        responses["work_flexibility"] = support_system.work_flexibility
        responses["healthcare_navigation_confidence"] = healthcare_access.healthcare_navigation_confidence
        
    elif week_number == 9:
        # Week 9: Values and preferences
        responses["health_philosophy"] = values_preferences.health_philosophy
        responses["prevention_approach"] = values_preferences.prevention_approach
        responses["information_preference"] = values_preferences.information_preference
        responses["control_preference"] = values_preferences.control_preference
        responses["screening_comfort"] = values_preferences.screening_comfort_levels
        responses["provider_preferences"] = {
            "gender": values_preferences.provider_gender_preference,
            "communication_style": random.choice(["direct", "gentle", "detailed", "efficient"]),
            "cultural_match": random.random() < 0.3
        }
        responses["decision_priorities"] = values_preferences.decision_priorities
        
    elif week_number == 10:
        # Week 10: Plan review
        responses["plan_alignment"] = random.choice(["excellent", "good", "fair"])
        responses["implementation_confidence"] = random.randint(6, 10)
        responses["main_concerns"] = random.sample([
            "cost", "time", "discomfort", "anxiety", "access"
        ], k=random.randint(0, 2))
        responses["commitment_areas"] = random.sample([
            "regular_screening", "lifestyle_changes", "provider_communication",
            "self_exams", "risk_reduction"
        ], k=random.randint(2, 4))
    
    return responses