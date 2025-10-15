"""
Stage Zero Health Synthetic User Generator
Generates 500 credible synthetic users with full 10-week assessment data
"""

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
    # (Continuing in next part due to length)