"""
Stage Zero Generator - Part 5: Personalized plan generation and journey metadata
"""

import uuid
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any, Optional


def generate_personalized_plan(
    self,
    demographics: Demographics,
    risk_assessment: RiskAssessment,
    healthcare_access: HealthcareAccess,
    values_preferences: ValuesPreferences
) -> PersonalizedPlan:
    """Generate a personalized detection plan based on user data"""
    
    plan = PersonalizedPlan(
        plan_id=str(uuid.uuid4()),
        created_date=datetime.now().isoformat()
    )
    
    # Generate risk summary
    plan.risk_summary = self.generate_risk_summary(demographics, risk_assessment)
    
    # Generate immediate actions
    plan.immediate_actions = self.generate_immediate_actions(
        demographics, risk_assessment, healthcare_access, values_preferences
    )
    
    # Generate ongoing schedule
    plan.ongoing_schedule = self.generate_ongoing_schedule(
        demographics, risk_assessment, values_preferences
    )
    
    # Generate provider recommendations
    plan.provider_recommendations = self.generate_provider_recommendations(
        demographics, healthcare_access, values_preferences
    )
    
    # Generate support resources
    plan.support_resources = self.generate_support_resources(
        demographics, healthcare_access
    )
    
    # User satisfaction with plan
    satisfaction_factors = {
        "excellent": 0.3 if values_preferences.prevention_approach in ["comprehensive", "guideline_based"] else 0.1,
        "good": 0.5,
        "fair": 0.15,
        "poor": 0.05
    }
    
    plan.plan_satisfaction_score = random.choices(
        [9, 8, 7, 6, 5],
        weights=[0.3, 0.4, 0.2, 0.08, 0.02]
    )[0]
    
    # Implementation commitment
    commitment_factors = {
        "high_risk": 0.2 if risk_assessment.gail_risk_category == "elevated" else 0.0,
        "good_access": 0.2 if healthcare_access.has_primary_care else -0.1,
        "high_comfort": 0.1 if healthcare_access.healthcare_comfort >= 7 else -0.1
    }
    
    base_commitment = 7
    for factor, adjustment in commitment_factors.items():
        base_commitment += adjustment
    
    plan.implementation_commitment = min(10, max(1, int(base_commitment + random.uniform(-1, 1))))
    
    return plan


def generate_risk_summary(self, demographics: Demographics, risk_assessment: RiskAssessment) -> str:
    """Generate personalized risk summary"""
    
    summaries = {
        "low": [
            f"At age {demographics.age}, your breast cancer risk is lower than average. Your GAIL score of {risk_assessment.gail_score:.2f} reflects protective factors in your profile.",
            f"Your comprehensive assessment shows below-average risk across all models. This is encouraging, but regular screening remains important.",
            f"Good news, {demographics.preferred_name}. Your risk factors place you in a lower risk category, though vigilance is still recommended."
        ],
        "average": [
            f"Your breast cancer risk is similar to most women your age. Your GAIL score of {risk_assessment.gail_score:.2f} indicates average risk.",
            f"Your assessment shows typical risk for a {demographics.age}-year-old woman. This means standard screening guidelines are appropriate for you.",
            f"{demographics.preferred_name}, your risk profile is in the average range. This is neither cause for alarm nor complacency."
        ],
        "elevated": [
            f"Your assessment indicates elevated breast cancer risk. With a GAIL score of {risk_assessment.gail_score:.2f}, enhanced screening may be beneficial.",
            f"Based on your family history and other factors, your risk is higher than average. This means we should discuss enhanced screening options.",
            f"{demographics.preferred_name}, your risk factors place you in an elevated category. This information helps us create a more protective screening plan."
        ]
    }
    
    base_summary = random.choice(summaries[risk_assessment.gail_risk_category])
    
    # Add genetic counseling note if indicated
    if risk_assessment.genetic_counseling_indicated:
        base_summary += " Your family history pattern suggests genetic counseling could provide valuable additional insights."
    
    # Add positive note about taking action
    base_summary += f" By completing this assessment, you've taken an important step in understanding and managing your health."
    
    return base_summary


def generate_immediate_actions(
    self,
    demographics: Demographics,
    risk_assessment: RiskAssessment,
    healthcare_access: HealthcareAccess,
    values_preferences: ValuesPreferences
) -> List[Dict[str, Any]]:
    """Generate immediate action items (next 3 months)"""
    
    actions = []
    
    # Primary care establishment if needed
    if not healthcare_access.has_primary_care:
        actions.append({
            "action": "Establish primary care",
            "priority": "high",
            "timeline": "Within 30 days",
            "description": "Find and schedule appointment with primary care provider",
            "resources": ["Insurance provider directory", "Community health center locator"]
        })
    
    # Mammogram scheduling based on age and risk
    if demographics.age >= 40 or (demographics.age >= 35 and risk_assessment.gail_risk_category == "elevated"):
        last_mammo_age = healthcare_access.last_mammogram_age
        if not last_mammo_age or (demographics.age - last_mammo_age) >= 2:
            actions.append({
                "action": "Schedule mammogram",
                "priority": "high",
                "timeline": "Within 60 days",
                "description": "Schedule baseline or follow-up mammogram based on your risk profile",
                "resources": ["Preferred imaging centers", "Insurance coverage information"]
            })
    
    # Genetic counseling if indicated
    if risk_assessment.genetic_counseling_indicated:
        actions.append({
            "action": "Genetic counseling consultation",
            "priority": "medium",
            "timeline": "Within 90 days",
            "description": "Meet with genetic counselor to discuss family history and testing options",
            "resources": ["Genetic counselor referral", "Insurance pre-authorization guide"]
        })
    
    # Lifestyle modifications
    if "sedentary_lifestyle" in risk_assessment.risk_factors_identified:
        actions.append({
            "action": "Increase physical activity",
            "priority": "medium",
            "timeline": "Start this week",
            "description": "Begin moderate exercise program, aiming for 150 minutes per week",
            "resources": ["Community fitness programs", "Walking group information"]
        })
    
    # Risk discussion with provider
    actions.append({
        "action": "Discuss risk assessment with provider",
        "priority": "medium",
        "timeline": "At next appointment",
        "description": "Share your comprehensive risk assessment with your healthcare provider",
        "resources": ["Risk assessment summary report", "Questions to ask your provider"]
    })
    
    return actions[:4]  # Limit to 4 most important actions


def generate_ongoing_schedule(
    self,
    demographics: Demographics,
    risk_assessment: RiskAssessment,
    values_preferences: ValuesPreferences
) -> Dict[str, Any]:
    """Generate ongoing screening schedule"""
    
    schedule = {
        "screening_frequency": {},
        "self_care": {},
        "follow_up": {}
    }
    
    # Mammogram frequency based on risk and preferences
    if risk_assessment.gail_risk_category == "elevated":
        mammo_freq = "Annual"
    elif demographics.age >= 50:
        mammo_freq = "Annual" if values_preferences.prevention_approach == "comprehensive" else "Every 2 years"
    else:
        mammo_freq = "Every 2 years" if demographics.age >= 40 else "Discuss with provider"
    
    schedule["screening_frequency"]["mammogram"] = mammo_freq
    
    # Clinical breast exam
    schedule["screening_frequency"]["clinical_breast_exam"] = "Annual with physical exam"
    
    # Self-exam recommendation
    if values_preferences.screening_comfort_levels.get("self_exam", 5) >= 5:
        schedule["self_care"]["breast_self_exam"] = "Monthly breast self-awareness"
    else:
        schedule["self_care"]["breast_self_exam"] = "General breast awareness (no pressure for monthly exams)"
    
    # MRI if high risk
    if risk_assessment.boadicea_category == "elevated" and risk_assessment.genetic_counseling_indicated:
        schedule["screening_frequency"]["breast_mri"] = "Annual, alternating with mammogram"
    
    # Follow-up timeline
    schedule["follow_up"]["risk_reassessment"] = "Every 2 years or with major life changes"
    schedule["follow_up"]["plan_review"] = "Annual with primary care provider"
    
    return schedule


def generate_provider_recommendations(
    self,
    demographics: Demographics,
    healthcare_access: HealthcareAccess,
    values_preferences: ValuesPreferences
) -> List[Dict[str, Any]]:
    """Generate provider recommendations based on location and preferences"""
    
    recommendations = []
    
    # Primary care if needed
    if not healthcare_access.has_primary_care:
        recommendations.append({
            "type": "Primary Care Provider",
            "criteria": {
                "location": f"Within 15 miles of {demographics.zip_code}",
                "insurance": f"Accepts {demographics.insurance_type}",
                "approach": values_preferences.health_philosophy
            },
            "search_resources": ["Insurance directory", "Healthgrades", "Community recommendations"]
        })
    
    # Breast specialist based on risk
    if risk_assessment.gail_risk_category == "elevated":
        recommendations.append({
            "type": "Breast Health Specialist",
            "criteria": {
                "specialization": "High-risk breast clinic",
                "gender_preference": values_preferences.provider_gender_preference,
                "communication_style": values_preferences.control_preference
            },
            "search_resources": ["Major medical centers", "Cancer center networks"]
        })
    
    # Imaging center
    recommendations.append({
        "type": "Imaging Center",
        "criteria": {
            "certification": "ACR accredited",
            "services": "3D mammography available",
            "environment": "Comfort-focused" if healthcare_access.healthcare_comfort < 7 else "Efficient"
        },
        "search_resources": ["ACR facility search", "Insurance preferred providers"]
    })
    
    return recommendations


def generate_support_resources(
    self,
    demographics: Demographics,
    healthcare_access: HealthcareAccess
) -> List[Dict[str, Any]]:
    """Generate relevant support resources"""
    
    resources = []
    
    # Financial assistance if needed
    if demographics.insurance_type in ["uninsured", "medicaid"]:
        resources.append({
            "type": "Financial Assistance",
            "name": "National Breast and Cervical Cancer Early Detection Program",
            "description": "Free or low-cost mammograms for eligible women",
            "contact": "CDC program locator"
        })
    
    # Transportation if needed
    if demographics.location_type == "rural":
        resources.append({
            "type": "Transportation",
            "name": "Local transportation services",
            "description": "Medical transportation assistance programs",
            "contact": "211 helpline or local health department"
        })
    
    # Support groups based on persona
    if demographics.persona_type == "health_aware_avoider":
        resources.append({
            "type": "Support Group",
            "name": "Anxiety and Cancer Risk Support",
            "description": "Online support for managing health anxiety",
            "contact": "Virtual meeting information"
        })
    
    # Educational resources
    resources.append({
        "type": "Education",
        "name": "Breast Cancer Risk Education",
        "description": "Evidence-based information about risk factors and prevention",
        "contact": "National Cancer Institute resources"
    })
    
    # Lifestyle support
    resources.append({
        "type": "Lifestyle Support",
        "name": "Healthy Living Programs",
        "description": "Community programs for exercise, nutrition, and stress management",
        "contact": "Local YMCA or community center"
    })
    
    return resources


def generate_journey_metadata(
    self,
    persona_type: str,
    weekly_responses: List[WeeklyResponse]
) -> Dict[str, Any]:
    """Generate metadata about the user's journey"""
    
    metadata = {
        "journey_start": weekly_responses[0].completion_timestamp if weekly_responses else None,
        "journey_end": weekly_responses[-1].completion_timestamp if weekly_responses else None,
        "weeks_completed": len(weekly_responses),
        "total_time_minutes": sum(w.time_spent_minutes for w in weekly_responses),
        "completion_rate": len(weekly_responses) / 10.0,
        "dropout_week": None if len(weekly_responses) == 10 else len(weekly_responses) + 1,
        "average_trust_level": sum(w.trust_level for w in weekly_responses) / len(weekly_responses) if weekly_responses else 0,
        "emotional_journey": [w.emotional_state for w in weekly_responses],
        "engagement_quality": self.calculate_engagement_quality(weekly_responses),
        "response_depth": self.calculate_response_depth(weekly_responses),
        "persona_consistency": self.calculate_persona_consistency(persona_type, weekly_responses)
    }
    
    return metadata


def calculate_engagement_quality(self, weekly_responses: List[WeeklyResponse]) -> str:
    """Calculate overall engagement quality"""
    if not weekly_responses:
        return "none"
    
    avg_time = sum(w.time_spent_minutes for w in weekly_responses) / len(weekly_responses)
    completion_rate = len(weekly_responses) / 10.0
    
    if completion_rate >= 0.8 and avg_time >= 15:
        return "excellent"
    elif completion_rate >= 0.5 and avg_time >= 10:
        return "good"
    elif completion_rate >= 0.3:
        return "fair"
    else:
        return "poor"


def calculate_response_depth(self, weekly_responses: List[WeeklyResponse]) -> str:
    """Calculate depth of responses"""
    if not weekly_responses:
        return "none"
    
    # Check open-ended response quality
    total_open_ended = sum(len(w.open_ended_responses) for w in weekly_responses)
    avg_response_length = sum(
        len(response) 
        for w in weekly_responses 
        for response in w.open_ended_responses.values()
    ) / max(total_open_ended, 1)
    
    if avg_response_length >= 200:
        return "detailed"
    elif avg_response_length >= 100:
        return "moderate"
    else:
        return "brief"


def calculate_persona_consistency(
    self,
    persona_type: str,
    weekly_responses: List[WeeklyResponse]
) -> float:
    """Calculate how consistent responses are with persona type"""
    if not weekly_responses:
        return 0.0
    
    # Check key indicators
    consistency_score = 0.0
    checks = 0
    
    # Check trust progression
    if persona_type == "health_aware_avoider":
        # Should have lower trust levels
        avg_trust = sum(w.trust_level for w in weekly_responses) / len(weekly_responses)
        if avg_trust <= 6:
            consistency_score += 1
        checks += 1
    elif persona_type == "healthcare_professional":
        # Should have higher trust levels
        avg_trust = sum(w.trust_level for w in weekly_responses) / len(weekly_responses)
        if avg_trust >= 7:
            consistency_score += 1
        checks += 1
    
    # Check completion patterns
    if persona_type == "structured_system_seeker":
        # Should complete most weeks
        if len(weekly_responses) >= 8:
            consistency_score += 1
        checks += 1
    elif persona_type == "overlooked_risk_group":
        # Lower completion expected
        if len(weekly_responses) <= 6:
            consistency_score += 1
        checks += 1
    
    return consistency_score / checks if checks > 0 else 0.5