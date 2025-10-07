Stage Zero Health Synthetic User Generator
Generates 500 credible synthetic users with full 10-week assessment data

import json
import random
import uuid
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import numpy as np
from faker import Faker

fake = Faker()

# Persona distribution based on Stage Zero Master Plan
PERSONA_DISTRIBUTION = {
    "health_aware_avoider": 0.30,
    "structured_system_seeker": 0.25,
    "balanced_life_integrator": 0.20,
    "healthcare_professional": 0.15,
    "overlooked_risk_group": 0.10
}

# Target completion rates by week
COMPLETION_TARGETS = {
    1: 0.85,
    2: 0.75,
    3: 0.70,
    4: 0.65,
    5: 0.60,
    6: 0.55,
    7: 0.50,
    8: 0.45,
    9: 0.40,
    10: 0.35
}

# Emotional states progression
EMOTIONAL_STATES = {
    "early": ["curious", "hopeful", "anxious", "uncertain"],
    "middle": ["engaged", "thoughtful", "overwhelmed", "committed"],
    "late": ["confident", "empowered", "concerned", "determined"]
}

# Race/ethnicity distribution (US demographics)
RACE_ETHNICITY_DISTRIBUTION = {
    "Non-Hispanic White": 0.60,
    "Hispanic": 0.18,
    "Non-Hispanic Black": 0.12,
    "Non-Hispanic Asian/Pacific Islander": 0.06,
    "Non-Hispanic American Indian/Alaska Native": 0.02,
    "Other/Mixed": 0.02
}

# Education distribution
EDUCATION_DISTRIBUTION = {
    "high_school": 0.25,
    "some_college": 0.20,
    "bachelors": 0.35,
    "masters": 0.15,
    "doctorate": 0.05
}

# Geographic distribution
LOCATION_DISTRIBUTION = {
    "urban": 0.55,
    "suburban": 0.30,
    "rural": 0.15
}

# Insurance types
INSURANCE_TYPES = {
    "employer": 0.50,
    "marketplace": 0.15,
    "medicare": 0.10,
    "medicaid": 0.15,
    "uninsured": 0.10
}


@dataclass
class Demographics:
    """User demographic information"""
    user_id: str
    persona_type: str
    preferred_name: str
    legal_name: str
    date_of_birth: str
    age: int
    biological_sex: str
    race_ethnicity: str
    education_level: str
    location_type: str
    zip_code: str
    insurance_type: str
    insurance_status: str


@dataclass
class FamilyHistory:
    """Family cancer history"""
    mother_cancer: Optional[Dict[str, Any]] = None
    father_cancer: Optional[Dict[str, Any]] = None
    siblings_cancer: List[Dict[str, Any]] = field(default_factory=list)
    grandparents_cancer: List[Dict[str, Any]] = field(default_factory=list)
    aunts_uncles_cancer: List[Dict[str, Any]] = field(default_factory=list)
    family_communication: str = "somewhat_open"
    family_patterns_recognized: List[str] = field(default_factory=list)


@dataclass
class ReproductiveHistory:
    """Reproductive and hormonal history"""
    age_at_menarche: Optional[int] = None
    pregnancies: int = 0
    age_at_first_birth: Optional[int] = None
    breastfeeding_months: int = 0
    menopause_age: Optional[int] = None
    hormone_use: Dict[str, Any] = field(default_factory=dict)
    reproductive_procedures: List[str] = field(default_factory=list)


@dataclass
class HealthcareAccess:
    """Healthcare access and experience"""
    has_primary_care: bool = False
    has_obgyn: bool = False
    provider_relationship_quality: str = "neutral"
    healthcare_comfort: int = 5  # 1-10 scale
    last_mammogram_age: Optional[int] = None
    mammogram_experience: Optional[str] = None
    screening_barriers: List[str] = field(default_factory=list)
    healthcare_navigation_confidence: int = 5  # 1-10 scale


@dataclass
class LifestyleFactors:
    """Lifestyle and environmental factors"""
    physical_activity_level: str = "moderate"
    alcohol_frequency: str = "occasional"
    smoking_status: str = "never"
    stress_level: int = 5  # 1-10 scale
    sleep_quality: str = "fair"
    occupation_type: str = "office"
    environmental_exposures: List[str] = field(default_factory=list)


@dataclass
class CurrentHealth:
    """Current health status"""
    overall_health: str = "good"
    chronic_conditions: List[str] = field(default_factory=list)
    breast_health_awareness: int = 5  # 1-10 scale
    current_symptoms: List[str] = field(default_factory=list)
    mental_health_status: str = "stable"
    medications: List[str] = field(default_factory=list)


@dataclass
class SupportSystem:
    """Support systems and resources"""
    family_support_level: str = "moderate"
    partner_support: bool = False
    community_connections: List[str] = field(default_factory=list)
    financial_stability: str = "moderate"
    transportation_access: str = "reliable"
    childcare_needs: bool = False
    work_flexibility: str = "some"


@dataclass
class ValuesPreferences:
    """Health values and detection preferences"""
    health_philosophy: str = "balanced"
    prevention_approach: str = "guideline_based"
    information_preference: str = "sufficient"
    control_preference: str = "collaborative"
    screening_comfort_levels: Dict[str, int] = field(default_factory=dict)
    provider_gender_preference: Optional[str] = None
    decision_priorities: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    """Calculated risk scores"""
    gail_score: float = 0.0
    gail_risk_category: str = "average"
    tyrer_cuzick_score: float = 0.0
    tyrer_cuzick_category: str = "average"
    boadicea_score: float = 0.0
    boadicea_category: str = "average"
    genetic_counseling_indicated: bool = False
    risk_factors_identified: List[str] = field(default_factory=list)


@dataclass
class WeeklyResponse:
    """Response data for a specific week"""
    week_number: int
    completion_status: str  # completed, partial, skipped
    completion_timestamp: Optional[str] = None
    time_spent_minutes: int = 0
    emotional_state: str = "neutral"
    trust_level: int = 5  # 1-10 scale
    responses: Dict[str, Any] = field(default_factory=dict)
    open_ended_responses: Dict[str, str] = field(default_factory=dict)


@dataclass
class PersonalizedPlan:
    """Final personalized detection plan"""
    plan_id: str
    created_date: str
    risk_summary: str
    immediate_actions: List[Dict[str, Any]] = field(default_factory=list)
    ongoing_schedule: Dict[str, Any] = field(default_factory=dict)
    provider_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    support_resources: List[Dict[str, Any]] = field(default_factory=list)
    plan_satisfaction_score: int = 0  # 1-10 scale
    implementation_commitment: int = 0  # 1-10 scale


@dataclass
class SyntheticUser:
    """Complete synthetic user with 10-week journey"""
    demographics: Demographics
    family_history: FamilyHistory
    reproductive_history: ReproductiveHistory
    healthcare_access: HealthcareAccess
    lifestyle_factors: LifestyleFactors
    current_health: CurrentHealth
    support_system: SupportSystem
    values_preferences: ValuesPreferences
    risk_assessment: RiskAssessment
    weekly_responses: List[WeeklyResponse] = field(default_factory=list)
    personalized_plan: Optional[PersonalizedPlan] = None
    journey_metadata: Dict[str, Any] = field(default_factory=dict)


class StageZeroGenerator:
    """Generator for Stage Zero Health synthetic users"""
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        self.fake = Faker()
        if seed:
            Faker.seed(seed)
        
    def generate_users(self, count: int = 500) -> List[SyntheticUser]:
        """Generate specified number of synthetic users"""
        users = []
        
        # Calculate persona distribution
        persona_counts = {}
        for persona, ratio in PERSONA_DISTRIBUTION.items():
            persona_counts[persona] = int(count * ratio)
        
        # Adjust for rounding
        total = sum(persona_counts.values())
        if total < count:
            persona_counts["health_aware_avoider"] += count - total
            
        # Generate users by persona
        for persona_type, persona_count in persona_counts.items():
            for i in range(persona_count):
                user = self.generate_user(persona_type)
                users.append(user)
                
        return users
    
    def generate_user(self, persona_type: str) -> SyntheticUser:
        """Generate a single synthetic user"""
        # Generate demographics first
        demographics = self.generate_demographics(persona_type)
        
        # Generate components based on demographics and persona
        family_history = self.generate_family_history(demographics)
        reproductive_history = self.generate_reproductive_history(demographics)
        healthcare_access = self.generate_healthcare_access(demographics, persona_type)
        lifestyle_factors = self.generate_lifestyle_factors(persona_type)
        current_health = self.generate_current_health(demographics)
        support_system = self.generate_support_system(persona_type)
        values_preferences = self.generate_values_preferences(persona_type)
        
        # Calculate risk assessment
        risk_assessment = self.calculate_risk_assessment(
            demographics, family_history, reproductive_history, lifestyle_factors
        )
        
        # Generate weekly responses with progressive completion
        weekly_responses = self.generate_weekly_journey(
            demographics, persona_type, family_history, reproductive_history,
            healthcare_access, lifestyle_factors, current_health, support_system,
            values_preferences
        )
        
        # Generate personalized plan if user completed week 10
        personalized_plan = None
        if weekly_responses and weekly_responses[-1].completion_status == "completed":
            personalized_plan = self.generate_personalized_plan(
                demographics, risk_assessment, healthcare_access, values_preferences
            )
        
        # Create user object
        user = SyntheticUser(
            demographics=demographics,
            family_history=family_history,
            reproductive_history=reproductive_history,
            healthcare_access=healthcare_access,
            lifestyle_factors=lifestyle_factors,
            current_health=current_health,
            support_system=support_system,
            values_preferences=values_preferences,
            risk_assessment=risk_assessment,
            weekly_responses=weekly_responses,
            personalized_plan=personalized_plan,
            journey_metadata=self.generate_journey_metadata(persona_type, weekly_responses)
        )
        
        return user
    
    def generate_demographics(self, persona_type: str) -> Demographics:
        """Generate demographic information"""
        # Age based on persona
        age_ranges = {
            "health_aware_avoider": (25, 45),
            "structured_system_seeker": (30, 50),
            "balanced_life_integrator": (28, 48),
            "healthcare_professional": (25, 45),
            "overlooked_risk_group": (30, 50)
        }
        
        age_range = age_ranges[persona_type]
        age = random.randint(age_range[0], age_range[1])
        
        # Generate names
        is_female = random.random() < 0.95  # 95% female for breast cancer focus
        if is_female:
            legal_name = self.fake.name_female()
            preferred_name = legal_name.split()[0]
        else:
            legal_name = self.fake.name_male()
            preferred_name = legal_name.split()[0]
        
        # Calculate date of birth
        today = date.today()
        birth_year = today.year - age
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Avoid month-end issues
        date_of_birth = date(birth_year, birth_month, birth_day).isoformat()
        
        # Other demographics
        race_ethnicity = self.weighted_choice(RACE_ETHNICITY_DISTRIBUTION)
        education_level = self.weighted_choice(EDUCATION_DISTRIBUTION)
        location_type = self.weighted_choice(LOCATION_DISTRIBUTION)
        insurance_type = self.weighted_choice(INSURANCE_TYPES)
        
        return Demographics(
            user_id=str(uuid.uuid4()),
            persona_type=persona_type,
            preferred_name=preferred_name,
            legal_name=legal_name,
            date_of_birth=date_of_birth,
            age=age,
            biological_sex="female" if is_female else "male",
            race_ethnicity=race_ethnicity,
            education_level=education_level,
            location_type=location_type,
            zip_code=self.fake.zipcode(),
            insurance_type=insurance_type,
            insurance_status="active" if insurance_type != "uninsured" else "none"
        )
    
    def weighted_choice(self, distribution: Dict[str, float]) -> str:
        """Make a weighted random choice"""
        choices = list(distribution.keys())
        weights = list(distribution.values())
        return random.choices(choices, weights=weights)[0]
    
    # Additional methods to be implemented...
    # (Continuing in next part due to length)"""
Stage Zero Generator - Part 2: Core generation methods


def generate_family_history(self, demographics: Demographics) -> FamilyHistory:
    """Generate family cancer history"""
    family_history = FamilyHistory()
    
    # Base family cancer probability
    base_prob = 0.20 if demographics.race_ethnicity == "Non-Hispanic White" else 0.15
    
    # Mother's cancer history
    if random.random() < base_prob * 1.2:  # Slightly higher for mother
        family_history.mother_cancer = {
            "type": random.choice(["breast", "ovarian", "colon", "lung", "other"]),
            "age_at_diagnosis": random.randint(45, 70),
            "user_age_at_diagnosis": max(0, demographics.age - random.randint(10, 30))
        }
    
    # Father's cancer history
    if random.random() < base_prob:
        family_history.father_cancer = {
            "type": random.choice(["prostate", "colon", "lung", "pancreatic", "other"]),
            "age_at_diagnosis": random.randint(50, 75),
            "user_age_at_diagnosis": max(0, demographics.age - random.randint(10, 30))
        }
    
    # Siblings
    num_siblings = random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.3, 0.15, 0.05])[0]
    for i in range(num_siblings):
        if random.random() < base_prob * 0.5:  # Lower probability for siblings
            family_history.siblings_cancer.append({
                "sibling_number": i + 1,
                "type": random.choice(["breast", "colon", "thyroid", "melanoma", "other"]),
                "age_at_diagnosis": random.randint(30, 60)
            })
    
    # Extended family
    # Grandparents
    for side in ["maternal", "paternal"]:
        for grandparent in ["grandmother", "grandfather"]:
            if random.random() < base_prob * 0.8:
                family_history.grandparents_cancer.append({
                    "relation": f"{side}_{grandparent}",
                    "type": random.choice(["breast", "colon", "stomach", "liver", "other"]),
                    "age_at_diagnosis": random.randint(60, 85)
                })
    
    # Aunts/Uncles
    num_aunts_uncles = random.randint(2, 8)
    for i in range(num_aunts_uncles):
        if random.random() < base_prob * 0.6:
            family_history.aunts_uncles_cancer.append({
                "side": random.choice(["maternal", "paternal"]),
                "type": random.choice(["breast", "ovarian", "colon", "lung", "other"]),
                "age_at_diagnosis": random.randint(40, 70)
            })
    
    # Family communication style
    family_history.family_communication = random.choice([
        "very_open", "somewhat_open", "private", "very_private", "complicated"
    ])
    
    # Pattern recognition
    if len([h for h in [family_history.mother_cancer] + family_history.aunts_uncles_cancer 
            if h and h.get("type") == "breast"]) >= 2:
        family_history.family_patterns_recognized.append("breast_cancer_maternal")
    
    if len([h for h in [family_history.father_cancer] + family_history.siblings_cancer 
            if h and h.get("type") == "colon"]) >= 2:
        family_history.family_patterns_recognized.append("colon_cancer_pattern")
    
    return family_history


def generate_reproductive_history(self, demographics: Demographics) -> ReproductiveHistory:
    """Generate reproductive and hormonal history"""
    history = ReproductiveHistory()
    
    if demographics.biological_sex != "female":
        return history
    
    # Age at menarche
    history.age_at_menarche = random.choices(
        [10, 11, 12, 13, 14, 15, 16],
        weights=[0.05, 0.10, 0.25, 0.30, 0.20, 0.08, 0.02]
    )[0]
    
    # Pregnancy history based on age and persona
    if demographics.age >= 25:
        pregnancy_prob = 0.7 if demographics.persona_type != "healthcare_professional" else 0.5
        if random.random() < pregnancy_prob:
            history.pregnancies = random.choices(
                [1, 2, 3, 4, 5],
                weights=[0.25, 0.40, 0.25, 0.08, 0.02]
            )[0]
            history.age_at_first_birth = random.randint(20, min(35, demographics.age - 1))
            
            # Breastfeeding
            if random.random() < 0.75:
                history.breastfeeding_months = random.randint(1, 24) * history.pregnancies
    
    # Menopause
    if demographics.age >= 45:
        menopause_prob = (demographics.age - 45) / 10  # Increases with age
        if random.random() < menopause_prob:
            history.menopause_age = random.randint(45, min(55, demographics.age))
    
    # Hormone use
    # Birth control
    if demographics.age >= 18 and random.random() < 0.65:
        bc_start = random.randint(18, 25)
        bc_duration = random.randint(1, 10)
        history.hormone_use["birth_control"] = {
            "start_age": bc_start,
            "duration_years": bc_duration,
            "type": random.choice(["pill", "iud_hormonal", "injection", "patch"])
        }
    
    # HRT (if menopausal)
    if history.menopause_age and random.random() < 0.3:
        history.hormone_use["hrt"] = {
            "start_age": history.menopause_age,
            "duration_years": random.randint(1, 5),
            "type": "combined"
        }
    
    # Reproductive procedures
    if random.random() < 0.15:
        history.reproductive_procedures.append("tubal_ligation")
    if random.random() < 0.10:
        history.reproductive_procedures.append("hysterectomy")
    
    return history


def generate_healthcare_access(self, demographics: Demographics, persona_type: str) -> HealthcareAccess:
    """Generate healthcare access information"""
    access = HealthcareAccess()
    
    # Access based on insurance and location
    if demographics.insurance_type != "uninsured":
        access.has_primary_care = random.random() < 0.85
        access.has_obgyn = random.random() < 0.70 if demographics.biological_sex == "female" else False
    else:
        access.has_primary_care = random.random() < 0.30
        access.has_obgyn = random.random() < 0.20 if demographics.biological_sex == "female" else False
    
    # Provider relationship quality based on persona
    relationship_probs = {
        "health_aware_avoider": {"excellent": 0.1, "good": 0.2, "neutral": 0.4, "poor": 0.3},
        "structured_system_seeker": {"excellent": 0.4, "good": 0.4, "neutral": 0.15, "poor": 0.05},
        "balanced_life_integrator": {"excellent": 0.2, "good": 0.5, "neutral": 0.25, "poor": 0.05},
        "healthcare_professional": {"excellent": 0.5, "good": 0.35, "neutral": 0.1, "poor": 0.05},
        "overlooked_risk_group": {"excellent": 0.05, "good": 0.15, "neutral": 0.4, "poor": 0.4}
    }
    
    probs = relationship_probs[persona_type]
    access.provider_relationship_quality = random.choices(
        list(probs.keys()), weights=list(probs.values())
    )[0]
    
    # Healthcare comfort
    comfort_ranges = {
        "health_aware_avoider": (2, 5),
        "structured_system_seeker": (6, 9),
        "balanced_life_integrator": (5, 8),
        "healthcare_professional": (7, 10),
        "overlooked_risk_group": (3, 6)
    }
    
    range_min, range_max = comfort_ranges[persona_type]
    access.healthcare_comfort = random.randint(range_min, range_max)
    
    # Mammogram history (if female and age appropriate)
    if demographics.biological_sex == "female" and demographics.age >= 40:
        mammogram_prob = {
            "health_aware_avoider": 0.4,
            "structured_system_seeker": 0.9,
            "balanced_life_integrator": 0.7,
            "healthcare_professional": 0.95,
            "overlooked_risk_group": 0.3
        }
        
        if random.random() < mammogram_prob[persona_type]:
            access.last_mammogram_age = demographics.age - random.randint(1, 3)
            access.mammogram_experience = random.choice([
                "very_positive", "positive", "neutral", "uncomfortable", "very_uncomfortable"
            ])
    
    # Screening barriers
    barrier_options = {
        "cost": 0.4 if demographics.insurance_type == "uninsured" else 0.1,
        "time": 0.6 if persona_type == "structured_system_seeker" else 0.3,
        "fear": 0.7 if persona_type == "health_aware_avoider" else 0.2,
        "access": 0.8 if demographics.location_type == "rural" else 0.2,
        "childcare": 0.3 if demographics.age < 45 else 0.1,
        "work_schedule": 0.5,
        "transportation": 0.4 if demographics.location_type == "rural" else 0.1
    }
    
    for barrier, prob in barrier_options.items():
        if random.random() < prob:
            access.screening_barriers.append(barrier)
    
    # Navigation confidence
    nav_ranges = {
        "health_aware_avoider": (3, 5),
        "structured_system_seeker": (7, 9),
        "balanced_life_integrator": (5, 7),
        "healthcare_professional": (8, 10),
        "overlooked_risk_group": (2, 5)
    }
    
    nav_min, nav_max = nav_ranges[persona_type]
    access.healthcare_navigation_confidence = random.randint(nav_min, nav_max)
    
    return access


def generate_lifestyle_factors(self, persona_type: str) -> LifestyleFactors:
    """Generate lifestyle and environmental factors"""
    factors = LifestyleFactors()
    
    # Physical activity by persona
    activity_probs = {
        "health_aware_avoider": {"high": 0.2, "moderate": 0.3, "low": 0.5},
        "structured_system_seeker": {"high": 0.5, "moderate": 0.4, "low": 0.1},
        "balanced_life_integrator": {"high": 0.3, "moderate": 0.5, "low": 0.2},
        "healthcare_professional": {"high": 0.4, "moderate": 0.4, "low": 0.2},
        "overlooked_risk_group": {"high": 0.1, "moderate": 0.3, "low": 0.6}
    }
    
    probs = activity_probs[persona_type]
    factors.physical_activity_level = random.choices(
        list(probs.keys()), weights=list(probs.values())
    )[0]
    
    # Alcohol use
    alcohol_probs = {
        "never": 0.25,
        "rare": 0.20,
        "occasional": 0.30,
        "moderate": 0.20,
        "frequent": 0.05
    }
    factors.alcohol_frequency = random.choices(
        list(alcohol_probs.keys()), weights=list(alcohol_probs.values())
    )[0]
    
    # Smoking
    smoking_probs = {
        "never": 0.70,
        "former": 0.20,
        "current": 0.10
    }
    factors.smoking_status = random.choices(
        list(smoking_probs.keys()), weights=list(smoking_probs.values())
    )[0]
    
    # Stress level by persona
    stress_ranges = {
        "health_aware_avoider": (6, 9),
        "structured_system_seeker": (4, 7),
        "balanced_life_integrator": (3, 6),
        "healthcare_professional": (5, 8),
        "overlooked_risk_group": (6, 9)
    }
    
    stress_min, stress_max = stress_ranges[persona_type]
    factors.stress_level = random.randint(stress_min, stress_max)
    
    # Sleep quality
    sleep_options = ["excellent", "good", "fair", "poor"]
    if factors.stress_level >= 7:
        factors.sleep_quality = random.choices(
            sleep_options, weights=[0.05, 0.15, 0.40, 0.40]
        )[0]
    else:
        factors.sleep_quality = random.choices(
            sleep_options, weights=[0.20, 0.40, 0.30, 0.10]
        )[0]
    
    # Occupation
    factors.occupation_type = random.choice([
        "office", "healthcare", "education", "retail", "manual_labor",
        "remote", "shift_work", "unemployed", "retired"
    ])
    
    # Environmental exposures
    if factors.occupation_type in ["healthcare", "manual_labor"]:
        if random.random() < 0.3:
            factors.environmental_exposures.append("occupational_chemicals")
    
    if random.random() < 0.1:
        factors.environmental_exposures.append("secondhand_smoke")
    
    return factors"""
Stage Zero Generator - Part 3: Health, support, and journey generation


def generate_current_health(self, demographics: Demographics) -> CurrentHealth:
    """Generate current health status"""
    health = CurrentHealth()
    
    # Overall health perception
    age_factor = (demographics.age - 25) / 50  # 0 at age 25, 1 at age 75
    health_probs = {
        "excellent": max(0.05, 0.20 - age_factor * 0.15),
        "good": 0.40,
        "fair": 0.30 + age_factor * 0.10,
        "poor": 0.05 + age_factor * 0.05
    }
    
    # Normalize probabilities
    total = sum(health_probs.values())
    health_probs = {k: v/total for k, v in health_probs.items()}
    
    health.overall_health = random.choices(
        list(health_probs.keys()), weights=list(health_probs.values())
    )[0]
    
    # Chronic conditions by age
    condition_probs = {
        "hypertension": 0.10 + age_factor * 0.30,
        "diabetes": 0.05 + age_factor * 0.15,
        "anxiety": 0.20 + random.gauss(0, 0.05),
        "depression": 0.15 + random.gauss(0, 0.05),
        "arthritis": age_factor * 0.30,
        "asthma": 0.12,
        "thyroid_disorder": 0.08 if demographics.biological_sex == "female" else 0.02,
        "high_cholesterol": 0.10 + age_factor * 0.20
    }
    
    for condition, prob in condition_probs.items():
        if random.random() < prob:
            health.chronic_conditions.append(condition)
    
    # Breast health awareness (for females)
    if demographics.biological_sex == "female":
        awareness_ranges = {
            "health_aware_avoider": (3, 6),
            "structured_system_seeker": (7, 10),
            "balanced_life_integrator": (5, 8),
            "healthcare_professional": (8, 10),
            "overlooked_risk_group": (2, 5)
        }
        
        range_min, range_max = awareness_ranges.get(demographics.persona_type, (4, 7))
        health.breast_health_awareness = random.randint(range_min, range_max)
    
    # Current symptoms (rare but important for triage)
    if random.random() < 0.02:  # 2% have concerning symptoms
        health.current_symptoms.append(random.choice([
            "breast_lump", "breast_pain", "nipple_discharge", "skin_changes"
        ]))
    
    # Mental health
    if "anxiety" in health.chronic_conditions or "depression" in health.chronic_conditions:
        health.mental_health_status = random.choice(["managing", "struggling", "improving"])
    else:
        health.mental_health_status = "stable"
    
    # Medications based on conditions
    med_map = {
        "hypertension": ["lisinopril", "amlodipine", "metoprolol"],
        "diabetes": ["metformin", "glipizide"],
        "anxiety": ["sertraline", "escitalopram"],
        "depression": ["fluoxetine", "bupropion"],
        "high_cholesterol": ["atorvastatin", "simvastatin"]
    }
    
    for condition in health.chronic_conditions:
        if condition in med_map:
            health.medications.append(random.choice(med_map[condition]))
    
    return health


def generate_support_system(self, persona_type: str) -> SupportSystem:
    """Generate support system information"""
    support = SupportSystem()
    
    # Family support by persona
    support_levels = {
        "health_aware_avoider": ["low", "moderate", "moderate", "high"],
        "structured_system_seeker": ["moderate", "high", "high", "very_high"],
        "balanced_life_integrator": ["moderate", "high", "high", "moderate"],
        "healthcare_professional": ["low", "moderate", "high", "high"],
        "overlooked_risk_group": ["low", "low", "moderate", "moderate"]
    }
    
    support.family_support_level = random.choice(support_levels[persona_type])
    
    # Partner support
    partner_probs = {
        "health_aware_avoider": 0.6,
        "structured_system_seeker": 0.7,
        "balanced_life_integrator": 0.75,
        "healthcare_professional": 0.65,
        "overlooked_risk_group": 0.5
    }
    support.partner_support = random.random() < partner_probs[persona_type]
    
    # Community connections
    community_options = [
        "religious_community", "exercise_group", "book_club", "volunteer_org",
        "professional_network", "neighborhood_group", "online_community"
    ]
    num_connections = random.choices([0, 1, 2, 3], weights=[0.2, 0.3, 0.3, 0.2])[0]
    support.community_connections = random.sample(community_options, num_connections)
    
    # Financial stability
    financial_probs = {
        "struggling": 0.15,
        "moderate": 0.50,
        "stable": 0.30,
        "comfortable": 0.05
    }
    support.financial_stability = random.choices(
        list(financial_probs.keys()), weights=list(financial_probs.values())
    )[0]
    
    # Transportation
    transport_probs = {
        "no_access": 0.05,
        "limited": 0.15,
        "reliable": 0.60,
        "very_reliable": 0.20
    }
    support.transportation_access = random.choices(
        list(transport_probs.keys()), weights=list(transport_probs.values())
    )[0]
    
    # Childcare needs (age-dependent)
    if 25 <= demographics.age <= 45:
        support.childcare_needs = random.random() < 0.4
    else:
        support.childcare_needs = False
    
    # Work flexibility
    work_flex_probs = {
        "none": 0.25,
        "minimal": 0.25,
        "some": 0.30,
        "significant": 0.20
    }
    support.work_flexibility = random.choices(
        list(work_flex_probs.keys()), weights=list(work_flex_probs.values())
    )[0]
    
    return support


def generate_values_preferences(self, persona_type: str) -> ValuesPreferences:
    """Generate health values and detection preferences"""
    values = ValuesPreferences()
    
    # Health philosophy by persona
    philosophy_map = {
        "health_aware_avoider": ["reactive", "minimal", "anxiety_driven"],
        "structured_system_seeker": ["proactive", "comprehensive", "data_driven"],
        "balanced_life_integrator": ["balanced", "holistic", "lifestyle_focused"],
        "healthcare_professional": ["evidence_based", "comprehensive", "clinical"],
        "overlooked_risk_group": ["uncertain", "seeking_guidance", "reactive"]
    }
    values.health_philosophy = random.choice(philosophy_map[persona_type])
    
    # Prevention approach
    prevention_map = {
        "health_aware_avoider": ["minimal", "symptom_based"],
        "structured_system_seeker": ["maximum", "guideline_based", "comprehensive"],
        "balanced_life_integrator": ["balanced", "personalized"],
        "healthcare_professional": ["evidence_based", "comprehensive"],
        "overlooked_risk_group": ["uncertain", "minimal", "barrier_limited"]
    }
    values.prevention_approach = random.choice(prevention_map[persona_type])
    
    # Information preference
    info_map = {
        "health_aware_avoider": ["minimal", "essential"],
        "structured_system_seeker": ["maximum", "detailed"],
        "balanced_life_integrator": ["sufficient", "practical"],
        "healthcare_professional": ["maximum", "clinical"],
        "overlooked_risk_group": ["guided", "simple"]
    }
    values.information_preference = random.choice(info_map[persona_type])
    
    # Control preference
    control_map = {
        "health_aware_avoider": ["provider_led", "guided"],
        "structured_system_seeker": ["full", "collaborative"],
        "balanced_life_integrator": ["collaborative", "flexible"],
        "healthcare_professional": ["full", "evidence_based"],
        "overlooked_risk_group": ["guided", "provider_led"]
    }
    values.control_preference = random.choice(control_map[persona_type])
    
    # Screening comfort levels (1-10 scale)
    comfort_ranges = {
        "health_aware_avoider": (2, 5),
        "structured_system_seeker": (6, 9),
        "balanced_life_integrator": (5, 8),
        "healthcare_professional": (7, 10),
        "overlooked_risk_group": (3, 6)
    }
    
    range_min, range_max = comfort_ranges[persona_type]
    screening_types = ["mammography", "clinical_exam", "self_exam", "genetic_testing", "mri"]
    
    for screening in screening_types:
        base_comfort = random.randint(range_min, range_max)
        # Adjust for specific screening types
        if screening == "self_exam":
            base_comfort = min(10, base_comfort + 2)
        elif screening == "genetic_testing" and persona_type == "health_aware_avoider":
            base_comfort = max(1, base_comfort - 2)
        
        values.screening_comfort_levels[screening] = base_comfort
    
    # Provider gender preference
    if random.random() < 0.4:  # 40% have preference
        values.provider_gender_preference = "female" if random.random() < 0.8 else "no_preference"
    
    # Decision priorities
    priority_options = [
        "effectiveness", "comfort", "cost", "convenience", "family_input",
        "provider_recommendation", "evidence_base", "lifestyle_fit"
    ]
    
    # Select top 3-5 priorities
    num_priorities = random.randint(3, 5)
    values.decision_priorities = random.sample(priority_options, num_priorities)
    
    return values


def calculate_risk_assessment(
    self,
    demographics: Demographics,
    family_history: FamilyHistory,
    reproductive_history: ReproductiveHistory,
    lifestyle_factors: LifestyleFactors
) -> RiskAssessment:
    """Calculate risk scores based on user data"""
    assessment = RiskAssessment()
    
    # Simplified GAIL score calculation
    gail_factors = 0.0
    
    # Age factor
    if demographics.age >= 50:
        gail_factors += 0.5
    elif demographics.age >= 40:
        gail_factors += 0.3
    
    # Family history factor
    if family_history.mother_cancer and family_history.mother_cancer.get("type") == "breast":
        gail_factors += 1.0
    if len([s for s in family_history.siblings_cancer if s.get("type") == "breast"]) > 0:
        gail_factors += 0.5
    
    # Reproductive factors
    if reproductive_history.age_at_menarche and reproductive_history.age_at_menarche < 12:
        gail_factors += 0.3
    if reproductive_history.age_at_first_birth is None or reproductive_history.age_at_first_birth > 30:
        gail_factors += 0.3
    
    # Calculate GAIL score (simplified)
    assessment.gail_score = 1.0 + gail_factors * 0.5
    
    # Categorize GAIL risk
    if assessment.gail_score < 1.3:
        assessment.gail_risk_category = "low"
    elif assessment.gail_score < 1.67:
        assessment.gail_risk_category = "average"
    else:
        assessment.gail_risk_category = "elevated"
    
    # Tyrer-Cuzick (includes more factors)
    tc_factors = gail_factors
    
    # Additional hormonal factors
    if reproductive_history.hormone_use.get("birth_control"):
        tc_factors += 0.2
    if reproductive_history.hormone_use.get("hrt"):
        tc_factors += 0.3
    
    # Lifestyle factors
    if lifestyle_factors.alcohol_frequency in ["moderate", "frequent"]:
        tc_factors += 0.3
    if lifestyle_factors.physical_activity_level == "low":
        tc_factors += 0.2
    
    assessment.tyrer_cuzick_score = 1.0 + tc_factors * 0.4
    
    # Categorize Tyrer-Cuzick
    if assessment.tyrer_cuzick_score < 1.5:
        assessment.tyrer_cuzick_category = "low"
    elif assessment.tyrer_cuzick_score < 2.0:
        assessment.tyrer_cuzick_category = "average"
    else:
        assessment.tyrer_cuzick_category = "elevated"
    
    # BOADICEA (includes genetic patterns)
    boadicea_factors = tc_factors
    
    # Extended family patterns
    breast_cancer_count = len([
        h for h in ([family_history.mother_cancer] + 
                   family_history.siblings_cancer + 
                   family_history.aunts_uncles_cancer)
        if h and h.get("type") == "breast"
    ])
    
    if breast_cancer_count >= 3:
        boadicea_factors += 2.0
    elif breast_cancer_count >= 2:
        boadicea_factors += 1.0
    
    assessment.boadicea_score = 1.0 + boadicea_factors * 0.3
    
    # Categorize BOADICEA
    if assessment.boadicea_score < 1.5:
        assessment.boadicea_category = "low"
    elif assessment.boadicea_score < 2.5:
        assessment.boadicea_category = "average"
    else:
        assessment.boadicea_category = "elevated"
    
    # Genetic counseling indication
    assessment.genetic_counseling_indicated = (
        breast_cancer_count >= 2 or
        (family_history.mother_cancer and 
         family_history.mother_cancer.get("age_at_diagnosis", 100) < 50) or
        assessment.boadicea_category == "elevated"
    )
    
    # Risk factors identified
    if demographics.age >= 40:
        assessment.risk_factors_identified.append("age")
    if breast_cancer_count > 0:
        assessment.risk_factors_identified.append("family_history")
    if lifestyle_factors.alcohol_frequency in ["moderate", "frequent"]:
        assessment.risk_factors_identified.append("alcohol_use")
    if lifestyle_factors.physical_activity_level == "low":
        assessment.risk_factors_identified.append("sedentary_lifestyle")
    if reproductive_history.age_at_first_birth is None:
        assessment.risk_factors_identified.append("nulliparity")
    
    return assessment"""
Stage Zero Generator - Part 4: Journey simulation and personalized plans

from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional


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
    
    return responses"""
Stage Zero Generator - Part 5: Personalized plan generation and journey metadata

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
