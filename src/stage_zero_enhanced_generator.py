"""
Enhanced Stage Zero Synthetic User Generator
Generates comprehensive synthetic users with all Stage Zero MVP features
"""

import random
import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import faker

# Initialize faker
fake = faker.Faker()

# Stage Zero specific persona distribution (matching ADR-052)
PERSONA_DISTRIBUTION = {
    "health_aware_avoider": 0.30,      # 30%
    "structured_system_seeker": 0.25,   # 25%
    "balanced_life_integrator": 0.20,   # 20%
    "healthcare_professional": 0.15,    # 15%
    "overlooked_risk_group": 0.10       # 10%
}

# Realistic completion rates by week (from Stage Zero requirements)
COMPLETION_RATES = {
    1: 0.85,   # 85% complete week 1
    2: 0.75,   # 75% continue to week 2
    3: 0.70,
    4: 0.65,
    5: 0.60,   # 60% reach mid-journey
    6: 0.55,
    7: 0.50,
    8: 0.45,
    9: 0.40,
    10: 0.35   # 35% complete full journey
}

# Emotional state progressions by journey phase
EMOTIONAL_STATES = {
    "early": ["curious", "hopeful", "anxious", "uncertain", "motivated"],
    "middle": ["engaged", "thoughtful", "overwhelmed", "committed", "processing"],
    "late": ["confident", "empowered", "concerned", "determined", "ready"]
}

# Trust level progression patterns by persona
TRUST_PATTERNS = {
    "health_aware_avoider": {"start": 4, "increment": 0.4, "max": 7},
    "structured_system_seeker": {"start": 6, "increment": 0.5, "max": 9},
    "balanced_life_integrator": {"start": 5, "increment": 0.5, "max": 8},
    "healthcare_professional": {"start": 7, "increment": 0.3, "max": 9},
    "overlooked_risk_group": {"start": 3, "increment": 0.6, "max": 7}
}

@dataclass
class Demographics:
    """Enhanced demographics with Stage Zero requirements"""
    user_id: str
    persona_type: str
    preferred_name: str
    legal_name: str
    date_of_birth: str
    age: int
    biological_sex: str
    race_ethnicity: str
    education: str
    location_type: str
    insurance_type: str
    language_preference: str = "english"
    timezone: str = "America/New_York"
    
@dataclass
class FamilyHistory:
    """Comprehensive family cancer history"""
    mother_cancer: bool
    father_cancer: bool
    siblings_cancer: bool
    mother_cancer_type: Optional[str] = None
    mother_cancer_age: Optional[int] = None
    father_cancer_type: Optional[str] = None
    father_cancer_age: Optional[int] = None
    siblings_cancer_details: List[Dict] = field(default_factory=list)
    grandparents_cancer: Dict[str, bool] = field(default_factory=dict)
    aunts_uncles_cancer: int = 0
    family_communication: str = "somewhat_open"
    genetic_testing_done: bool = False
    genetic_counseling_indicated: bool = False
    ashkenazi_jewish: bool = False

@dataclass
class ReproductiveHistory:
    """Detailed reproductive and hormonal history"""
    age_at_menarche: Optional[int] = None
    pregnancies: int = 0
    live_births: int = 0
    age_at_first_birth: Optional[int] = None
    breastfeeding_months: int = 0
    miscarriages: int = 0
    fertility_treatments: bool = False
    hormone_use: bool = False
    hormone_type: Optional[str] = None
    hormone_duration_years: int = 0
    menopause_status: str = "premenopausal"
    age_at_menopause: Optional[int] = None
    
@dataclass
class HealthcareAccess:
    """Healthcare system navigation and access"""
    has_primary_care: bool
    provider_name: Optional[str] = None
    provider_relationship: str = "neutral"
    healthcare_comfort: int = 5  # 1-10 scale
    navigation_confidence: int = 5  # 1-10 scale
    last_checkup: Optional[str] = None
    last_mammogram: Optional[int] = None
    last_clinical_exam: Optional[str] = None
    screening_barriers: List[str] = field(default_factory=list)
    preferred_communication: str = "email"
    telehealth_comfort: int = 5
    insurance_type: Optional[str] = None

@dataclass
class LifestyleFactors:
    """Comprehensive lifestyle and environmental factors"""
    physical_activity: str
    alcohol_use: str
    smoking: str
    exercise_minutes_weekly: int = 0
    drinks_per_week: int = 0
    pack_years: float = 0.0
    stress_level: int = 5  # 1-10
    sleep_quality: str = "fair"
    sleep_hours: float = 7.0
    diet_quality: str = "moderate"
    bmi: float = 25.0
    occupational_exposures: List[str] = field(default_factory=list)
    environmental_concerns: List[str] = field(default_factory=list)

@dataclass
class CurrentHealth:
    """Current health status and concerns"""
    overall_health: str = "good"
    chronic_conditions: List[str] = field(default_factory=list)
    current_medications: List[str] = field(default_factory=list)
    recent_symptoms: List[str] = field(default_factory=list)
    mental_health_status: str = "stable"
    health_anxiety_level: int = 5  # 1-10
    body_awareness: str = "moderate"
    self_exam_frequency: str = "rarely"

@dataclass
class SupportSystem:
    """Support network and resources"""
    family_support: str = "moderate"
    partner_support: Optional[str] = None
    friend_support: str = "moderate"
    community_resources: List[str] = field(default_factory=list)
    financial_stability: str = "stable"
    transportation_access: str = "reliable"
    childcare_needs: bool = False
    eldercare_responsibilities: bool = False
    work_flexibility: str = "moderate"

@dataclass
class RiskAssessment:
    """Multi-model risk assessment scores"""
    # GAIL Model (Week 1-2)
    gail_score: float = 0.0
    gail_category: str = "average"
    gail_lifetime_risk: float = 0.0
    gail_five_year_risk: float = 0.0
    
    # Tyrer-Cuzick Model (Week 3+)
    tyrer_cuzick_score: float = 0.0
    tyrer_cuzick_category: str = "average"
    tyrer_cuzick_ten_year_risk: float = 0.0
    
    # BOADICEA Model (Week 6+)
    boadicea_score: float = 0.0
    boadicea_category: str = "average"
    boadicea_genetic_risk: float = 0.0
    
    # Aggregate assessment
    risk_factors_count: int = 0
    genetic_counseling_indicated: bool = False
    high_risk_criteria_met: List[str] = field(default_factory=list)
    recommended_screening_age: int = 40

@dataclass
class WeeklyAssessment:
    """Enhanced weekly journey data with responses"""
    week: int
    completed: bool
    completion_status: str  # "completed", "partial", "skipped"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    time_spent_minutes: int = 0
    emotional_state: str = "neutral"
    trust_level: float = 5.0  # 1-10 scale
    response_quality: float = 0.0  # 0-1 scale
    
    # Assessment-specific responses
    responses: Dict[str, Any] = field(default_factory=dict)
    open_ended_responses: Dict[str, str] = field(default_factory=dict)
    
    # Engagement metrics
    sessions_count: int = 1
    abandonment_points: List[str] = field(default_factory=list)
    help_requests: int = 0
    
    # Week-specific features
    risk_model_used: Optional[str] = None
    educational_content_viewed: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)

@dataclass
class LifeEvent:
    """Life events with journey impact"""
    event_id: str
    event_type: str  # health, career, family, financial, social
    event_name: str
    event_date: str
    days_ago: int
    impact_level: str  # high, moderate, low
    status: str  # ongoing, resolved, processing
    requires_support: bool
    journey_impact: Dict[str, Any] = field(default_factory=dict)
    specialized_path_triggered: bool = False

@dataclass
class PersonalizedPlan:
    """Week 10 personalized detection plan"""
    plan_id: str
    created_at: str
    
    # Risk communication
    risk_summary: str
    risk_interpretation: str
    personalized_factors: List[str]
    
    # Detection recommendations
    screening_schedule: Dict[str, Any]
    immediate_actions: List[Dict[str, Any]]
    lifestyle_modifications: List[Dict[str, Any]]
    
    # Implementation support
    provider_talking_points: List[str]
    insurance_navigation: Dict[str, Any]
    barrier_solutions: Dict[str, List[str]]
    
    # Follow-up
    check_in_schedule: List[Dict[str, Any]]
    support_resources: List[Dict[str, Any]]
    
    # User feedback
    plan_satisfaction: Optional[int] = None  # 1-10
    implementation_commitment: Optional[float] = None  # 0-1
    likelihood_to_recommend: Optional[int] = None  # NPS score

@dataclass
class NarrativeElements:
    """Enhanced narrative and qualitative responses"""
    # Identity and motivation
    self_description: str
    health_philosophy: str
    motivation_for_joining: str
    
    # Health relationship
    healthcare_story: str
    screening_hesitations: str
    ideal_healthcare_experience: str
    
    # Values and preferences
    health_priorities: List[str]
    detection_comfort_level: str
    decision_making_style: str
    information_preferences: str
    
    # Goals and barriers
    health_goals: List[str]
    perceived_barriers: List[str]
    success_definitions: List[str]
    
    # Support needs
    support_preferences: str
    communication_style: str
    learning_style: str

@dataclass
class PrivacyIndicators:
    """Data privacy and PHI indicators"""
    contains_phi: bool = True
    contains_pii: bool = True
    sensitive_conditions: List[str] = field(default_factory=list)
    genetic_information_present: bool = False
    mental_health_information: bool = False
    substance_use_information: bool = False
    consent_date: Optional[str] = None
    data_sharing_preferences: Dict[str, bool] = field(default_factory=dict)
    deletion_requested: bool = False

@dataclass
class StageZeroUser:
    """Complete Stage Zero synthetic user profile"""
    # Core identity
    demographics: Demographics
    
    # Health data
    family_history: FamilyHistory
    reproductive_history: ReproductiveHistory
    healthcare_access: HealthcareAccess
    lifestyle_factors: LifestyleFactors
    current_health: CurrentHealth
    support_system: SupportSystem
    
    # Risk assessment
    risk_assessment: RiskAssessment
    
    # Journey data
    weekly_assessments: List[WeeklyAssessment]
    life_events: List[LifeEvent]
    
    # Personalization
    narrative_elements: NarrativeElements
    personalized_plan: Optional[PersonalizedPlan] = None
    
    # Metadata
    privacy_indicators: PrivacyIndicators = field(default_factory=PrivacyIndicators)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: Optional[str] = None
    journey_status: str = "active"  # active, paused, completed, abandoned
    total_time_invested_minutes: int = 0
    overall_completion_rate: float = 0.0


class StageZeroEnhancedGenerator:
    """Enhanced generator for Stage Zero synthetic users"""
    
    def __init__(self):
        self.fake = faker.Faker()
        self.current_date = datetime.now()
        
    def generate_users(self, count: int = 500) -> List[StageZeroUser]:
        """Generate specified number of synthetic users"""
        users = []
        
        # Calculate persona counts based on distribution
        persona_counts = {}
        remaining = count
        
        for persona, percentage in PERSONA_DISTRIBUTION.items():
            if persona == list(PERSONA_DISTRIBUTION.keys())[-1]:
                # Last persona gets remaining to avoid rounding issues
                persona_counts[persona] = remaining
            else:
                persona_count = int(count * percentage)
                persona_counts[persona] = persona_count
                remaining -= persona_count
        
        # Generate users for each persona
        for persona_type, persona_count in persona_counts.items():
            for _ in range(persona_count):
                user = self.generate_single_user(persona_type)
                users.append(user)
        
        # Shuffle to mix personas
        random.shuffle(users)
        return users
    
    def generate_single_user(self, persona_type: str) -> StageZeroUser:
        """Generate a single complete user profile"""
        
        # Generate core components
        demographics = self.generate_demographics(persona_type)
        family_history = self.generate_family_history(persona_type, demographics)
        reproductive_history = self.generate_reproductive_history(demographics)
        healthcare_access = self.generate_healthcare_access(persona_type, demographics)
        lifestyle_factors = self.generate_lifestyle_factors(persona_type)
        current_health = self.generate_current_health(persona_type)
        support_system = self.generate_support_system(persona_type)
        
        # Generate life events
        life_events = self.generate_life_events(persona_type, demographics)
        
        # Generate narrative elements
        narrative_elements = self.generate_narrative_elements(
            persona_type, demographics, family_history, healthcare_access
        )
        
        # Generate weekly journey with realistic completion
        weekly_assessments = self.generate_weekly_journey(
            persona_type, demographics, family_history, reproductive_history,
            healthcare_access, lifestyle_factors, current_health, life_events
        )
        
        # Calculate risk assessments based on completed weeks
        risk_assessment = self.calculate_risk_assessments(
            demographics, family_history, reproductive_history,
            lifestyle_factors, weekly_assessments
        )
        
        # Generate personalized plan if journey completed
        personalized_plan = None
        if len(weekly_assessments) >= 10 and weekly_assessments[-1].completed:
            personalized_plan = self.generate_personalized_plan(
                demographics, risk_assessment, healthcare_access,
                narrative_elements, support_system, lifestyle_factors
            )
        
        # Calculate metadata
        total_time = sum(w.time_spent_minutes for w in weekly_assessments)
        completion_rate = len([w for w in weekly_assessments if w.completed]) / 10
        last_active = weekly_assessments[-1].completed_at if weekly_assessments else None
        
        # Determine journey status
        if len(weekly_assessments) >= 10 and weekly_assessments[-1].completed:
            journey_status = "completed"
        elif last_active and (self.current_date - datetime.fromisoformat(last_active)).days > 14:
            journey_status = "abandoned"
        elif last_active and (self.current_date - datetime.fromisoformat(last_active)).days > 7:
            journey_status = "paused"
        else:
            journey_status = "active"
        
        # Create privacy indicators
        privacy_indicators = PrivacyIndicators(
            contains_phi=True,
            contains_pii=True,
            sensitive_conditions=current_health.chronic_conditions,
            genetic_information_present=family_history.genetic_testing_done,
            mental_health_information=current_health.mental_health_status != "stable",
            consent_date=(self.current_date - timedelta(days=random.randint(1, 90))).isoformat(),
            data_sharing_preferences={
                "research": random.choice([True, False]),
                "provider_sharing": True,
                "family_sharing": random.choice([True, False])
            }
        )
        
        return StageZeroUser(
            demographics=demographics,
            family_history=family_history,
            reproductive_history=reproductive_history,
            healthcare_access=healthcare_access,
            lifestyle_factors=lifestyle_factors,
            current_health=current_health,
            support_system=support_system,
            risk_assessment=risk_assessment,
            weekly_assessments=weekly_assessments,
            life_events=life_events,
            narrative_elements=narrative_elements,
            personalized_plan=personalized_plan,
            privacy_indicators=privacy_indicators,
            created_at=(self.current_date - timedelta(days=random.randint(0, 70))).isoformat(),
            last_active=last_active,
            journey_status=journey_status,
            total_time_invested_minutes=total_time,
            overall_completion_rate=completion_rate
        )
    
    def generate_demographics(self, persona_type: str) -> Demographics:
        """Generate demographic data based on persona"""
        # Age ranges by persona
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
            preferred_name = random.choice([
                legal_name.split()[0],  # Use first name
                self.fake.first_name_female()  # Different preferred name
            ])
        else:
            legal_name = self.fake.name_male()
            preferred_name = legal_name.split()[0]
        
        # Date of birth
        dob = self.current_date - timedelta(days=age*365 + random.randint(0, 364))
        
        # Race/ethnicity distribution
        race_ethnicity_options = [
            "Non-Hispanic White",
            "Non-Hispanic Black",
            "Hispanic/Latino",
            "Non-Hispanic Asian/Pacific Islander",
            "Non-Hispanic American Indian/Alaska Native",
            "Multiple races"
        ]
        
        # Education by persona
        education_map = {
            "health_aware_avoider": ["high_school", "some_college", "bachelors"],
            "structured_system_seeker": ["bachelors", "masters", "doctorate"],
            "balanced_life_integrator": ["some_college", "bachelors", "masters"],
            "healthcare_professional": ["bachelors", "masters", "doctorate"],
            "overlooked_risk_group": ["high_school", "some_college"]
        }
        
        return Demographics(
            user_id=str(uuid.uuid4()),
            persona_type=persona_type,
            preferred_name=preferred_name,
            legal_name=legal_name,
            date_of_birth=dob.isoformat(),
            age=age,
            biological_sex="female" if is_female else "male",
            race_ethnicity=random.choice(race_ethnicity_options),
            education=random.choice(education_map[persona_type]),
            location_type=random.choice(["urban", "suburban", "rural"]),
            insurance_type=random.choice(["employer", "marketplace", "medicare", "medicaid", "uninsured"]),
            language_preference=random.choice(["english", "spanish", "other"]) if random.random() < 0.1 else "english",
            timezone=random.choice(["America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles"])
        )
    
    def generate_family_history(self, persona_type: str, demographics: Demographics) -> FamilyHistory:
        """Generate family cancer history with emotional context"""
        # Higher family history for certain personas
        family_risk = {
            "health_aware_avoider": 0.4,
            "structured_system_seeker": 0.3,
            "balanced_life_integrator": 0.2,
            "healthcare_professional": 0.25,
            "overlooked_risk_group": 0.35
        }
        
        has_family_history = random.random() < family_risk[persona_type]
        
        family_history = FamilyHistory(
            mother_cancer=has_family_history and random.random() < 0.3,
            father_cancer=random.random() < 0.1,
            siblings_cancer=has_family_history and random.random() < 0.2,
            family_communication=random.choice(["very_open", "somewhat_open", "limited", "none"]),
            genetic_testing_done=random.random() < 0.1,
            ashkenazi_jewish=demographics.race_ethnicity == "Non-Hispanic White" and random.random() < 0.025
        )
        
        # Add details if cancer present
        if family_history.mother_cancer:
            family_history.mother_cancer_type = random.choice(["breast", "ovarian", "other"])
            family_history.mother_cancer_age = random.randint(35, 70)
        
        if family_history.father_cancer:
            family_history.father_cancer_type = random.choice(["prostate", "colon", "other"])
            family_history.father_cancer_age = random.randint(45, 75)
        
        if family_history.siblings_cancer:
            num_siblings = random.randint(1, 3)
            for _ in range(num_siblings):
                family_history.siblings_cancer_details.append({
                    "relation": random.choice(["sister", "brother"]),
                    "cancer_type": random.choice(["breast", "ovarian", "other"]),
                    "age_at_diagnosis": random.randint(30, 60)
                })
        
        # Extended family
        family_history.grandparents_cancer = {
            "maternal_grandmother": has_family_history and random.random() < 0.3,
            "maternal_grandfather": random.random() < 0.1,
            "paternal_grandmother": random.random() < 0.2,
            "paternal_grandfather": random.random() < 0.1
        }
        
        family_history.aunts_uncles_cancer = random.randint(0, 4) if has_family_history else 0
        
        # Genetic counseling indicated if strong family history
        family_history.genetic_counseling_indicated = (
            family_history.mother_cancer or 
            family_history.siblings_cancer or
            family_history.aunts_uncles_cancer >= 2 or
            family_history.ashkenazi_jewish
        )
        
        return family_history
    
    def generate_reproductive_history(self, demographics: Demographics) -> ReproductiveHistory:
        """Generate reproductive history for risk assessment"""
        if demographics.biological_sex != "female":
            return ReproductiveHistory()
        
        reproductive = ReproductiveHistory()
        
        # Age at menarche
        reproductive.age_at_menarche = random.randint(9, 16)
        
        # Pregnancy history based on age
        if demographics.age > 20:
            reproductive.pregnancies = random.choices([0, 1, 2, 3, 4], weights=[30, 25, 25, 15, 5])[0]
            reproductive.live_births = random.randint(0, reproductive.pregnancies)
            reproductive.miscarriages = reproductive.pregnancies - reproductive.live_births
            
            if reproductive.live_births > 0:
                min_age = max(18, demographics.age - 30)
                reproductive.age_at_first_birth = random.randint(min_age, demographics.age - 1)
                reproductive.breastfeeding_months = random.randint(0, 24) if random.random() < 0.6 else 0
        
        # Fertility treatments
        reproductive.fertility_treatments = random.random() < 0.1
        
        # Hormone use
        reproductive.hormone_use = random.random() < 0.3
        if reproductive.hormone_use:
            reproductive.hormone_type = random.choice(["birth_control", "hrt", "fertility"])
            reproductive.hormone_duration_years = random.randint(1, 10)
        
        # Menopause status
        if demographics.age < 45:
            reproductive.menopause_status = "premenopausal"
        elif demographics.age < 55:
            reproductive.menopause_status = random.choice(["premenopausal", "perimenopausal", "postmenopausal"])
            if reproductive.menopause_status == "postmenopausal":
                reproductive.age_at_menopause = random.randint(45, demographics.age)
        else:
            reproductive.menopause_status = "postmenopausal"
            reproductive.age_at_menopause = random.randint(45, 55)
        
        return reproductive
    
    def generate_healthcare_access(self, persona_type: str, demographics: Demographics) -> HealthcareAccess:
        """Generate healthcare access and navigation data"""
        # Access patterns by persona
        access_patterns = {
            "health_aware_avoider": {
                "has_pcp": 0.6,
                "comfort": (3, 6),
                "confidence": (2, 5),
                "barriers": ["fear", "anxiety", "cost", "time"]
            },
            "structured_system_seeker": {
                "has_pcp": 0.95,
                "comfort": (7, 10),
                "confidence": (7, 10),
                "barriers": ["time", "scheduling"]
            },
            "balanced_life_integrator": {
                "has_pcp": 0.8,
                "comfort": (5, 8),
                "confidence": (5, 8),
                "barriers": ["time", "cost", "childcare"]
            },
            "healthcare_professional": {
                "has_pcp": 0.99,
                "comfort": (8, 10),
                "confidence": (9, 10),
                "barriers": ["time"]
            },
            "overlooked_risk_group": {
                "has_pcp": 0.4,
                "comfort": (2, 5),
                "confidence": (2, 4),
                "barriers": ["cost", "insurance", "transportation", "language"]
            }
        }
        
        pattern = access_patterns[persona_type]
        
        healthcare = HealthcareAccess(
            has_primary_care=random.random() < pattern["has_pcp"],
            provider_relationship=random.choice(["excellent", "good", "neutral", "poor"]),
            healthcare_comfort=random.randint(*pattern["comfort"]),
            navigation_confidence=random.randint(*pattern["confidence"]),
            screening_barriers=random.sample(pattern["barriers"], k=random.randint(1, len(pattern["barriers"]))),
            preferred_communication=random.choice(["email", "phone", "patient_portal", "text"]),
            telehealth_comfort=random.randint(3, 9)
        )
        
        if healthcare.has_primary_care:
            healthcare.provider_name = f"Dr. {self.fake.last_name()}"
            healthcare.last_checkup = (self.current_date - timedelta(days=random.randint(30, 730))).isoformat()
        
        # Mammogram history for women over 40
        if demographics.biological_sex == "female" and demographics.age >= 40:
            if random.random() < 0.7:
                healthcare.last_mammogram = demographics.age - random.randint(0, 5)
        
        return healthcare
    
    def generate_lifestyle_factors(self, persona_type: str) -> LifestyleFactors:
        """Generate lifestyle and environmental factors"""
        lifestyle_patterns = {
            "health_aware_avoider": {
                "activity": ["sedentary", "light", "moderate"],
                "stress": (6, 9),
                "sleep": ["poor", "fair"]
            },
            "structured_system_seeker": {
                "activity": ["moderate", "vigorous"],
                "stress": (4, 7),
                "sleep": ["fair", "good"]
            },
            "balanced_life_integrator": {
                "activity": ["light", "moderate"],
                "stress": (5, 7),
                "sleep": ["fair", "good"]
            },
            "healthcare_professional": {
                "activity": ["moderate", "vigorous"],
                "stress": (6, 8),
                "sleep": ["poor", "fair"]
            },
            "overlooked_risk_group": {
                "activity": ["sedentary", "light"],
                "stress": (7, 9),
                "sleep": ["poor", "fair"]
            }
        }
        
        pattern = lifestyle_patterns[persona_type]
        
        activity = random.choice(pattern["activity"])
        activity_minutes = {
            "sedentary": random.randint(0, 30),
            "light": random.randint(30, 90),
            "moderate": random.randint(90, 200),
            "vigorous": random.randint(150, 300)
        }
        
        lifestyle = LifestyleFactors(
            physical_activity=activity,
            exercise_minutes_weekly=activity_minutes[activity],
            alcohol_use=random.choice(["never", "occasional", "moderate", "heavy"]),
            smoking=random.choice(["never", "former", "current"]),
            stress_level=random.randint(*pattern["stress"]),
            sleep_quality=random.choice(pattern["sleep"]),
            sleep_hours=random.uniform(5, 9),
            diet_quality=random.choice(["poor", "fair", "moderate", "good", "excellent"]),
            bmi=random.uniform(18, 35)
        )
        
        # Add details
        if lifestyle.alcohol_use == "occasional":
            lifestyle.drinks_per_week = random.randint(1, 3)
        elif lifestyle.alcohol_use == "moderate":
            lifestyle.drinks_per_week = random.randint(4, 7)
        elif lifestyle.alcohol_use == "heavy":
            lifestyle.drinks_per_week = random.randint(8, 20)
        
        if lifestyle.smoking == "current":
            lifestyle.pack_years = random.uniform(0.5, 20)
        elif lifestyle.smoking == "former":
            lifestyle.pack_years = random.uniform(0.1, 10)
        
        # Occupational/environmental exposures
        if random.random() < 0.2:
            lifestyle.occupational_exposures = random.sample(
                ["chemicals", "radiation", "night_shift", "stress"], 
                k=random.randint(1, 2)
            )
        
        return lifestyle
    
    def generate_current_health(self, persona_type: str) -> CurrentHealth:
        """Generate current health status"""
        health_patterns = {
            "health_aware_avoider": {
                "overall": ["fair", "good"],
                "anxiety": (6, 9),
                "awareness": "high"
            },
            "structured_system_seeker": {
                "overall": ["good", "excellent"],
                "anxiety": (3, 6),
                "awareness": "high"
            },
            "balanced_life_integrator": {
                "overall": ["good"],
                "anxiety": (4, 6),
                "awareness": "moderate"
            },
            "healthcare_professional": {
                "overall": ["good", "excellent"],
                "anxiety": (2, 5),
                "awareness": "very_high"
            },
            "overlooked_risk_group": {
                "overall": ["poor", "fair"],
                "anxiety": (5, 8),
                "awareness": "low"
            }
        }
        
        pattern = health_patterns[persona_type]
        
        current = CurrentHealth(
            overall_health=random.choice(pattern["overall"]),
            health_anxiety_level=random.randint(*pattern["anxiety"]),
            body_awareness=pattern["awareness"],
            self_exam_frequency=random.choice(["never", "rarely", "occasionally", "monthly"]),
            mental_health_status=random.choice(["stable", "mild_anxiety", "moderate_anxiety", "depression"])
        )
        
        # Chronic conditions
        if random.random() < 0.3:
            current.chronic_conditions = random.sample(
                ["hypertension", "diabetes", "hypothyroid", "anxiety", "depression"],
                k=random.randint(1, 2)
            )
            
            # Add medications for conditions
            if "hypertension" in current.chronic_conditions:
                current.current_medications.append("lisinopril")
            if "diabetes" in current.chronic_conditions:
                current.current_medications.append("metformin")
        
        # Recent symptoms
        if random.random() < 0.2:
            current.recent_symptoms = random.sample(
                ["breast_pain", "lump_feeling", "skin_changes", "nipple_discharge"],
                k=random.randint(1, 2)
            )
        
        return current
    
    def generate_support_system(self, persona_type: str) -> SupportSystem:
        """Generate support network assessment"""
        support_patterns = {
            "health_aware_avoider": {
                "family": ["minimal", "moderate"],
                "financial": ["unstable", "stable"]
            },
            "structured_system_seeker": {
                "family": ["moderate", "strong"],
                "financial": ["stable", "comfortable"]
            },
            "balanced_life_integrator": {
                "family": ["moderate", "strong"],
                "financial": ["stable"]
            },
            "healthcare_professional": {
                "family": ["moderate", "strong"],
                "financial": ["stable", "comfortable"]
            },
            "overlooked_risk_group": {
                "family": ["minimal", "moderate"],
                "financial": ["unstable", "stretched"]
            }
        }
        
        pattern = support_patterns[persona_type]
        
        support = SupportSystem(
            family_support=random.choice(pattern["family"]),
            friend_support=random.choice(["minimal", "moderate", "strong"]),
            financial_stability=random.choice(pattern["financial"]),
            transportation_access=random.choice(["none", "limited", "reliable"]),
            work_flexibility=random.choice(["none", "minimal", "moderate", "high"])
        )
        
        # Partner support
        if random.random() < 0.6:
            support.partner_support = random.choice(["unsupportive", "neutral", "supportive", "very_supportive"])
        
        # Responsibilities
        support.childcare_needs = random.random() < 0.3
        support.eldercare_responsibilities = random.random() < 0.2
        
        # Community resources
        if random.random() < 0.4:
            support.community_resources = random.sample(
                ["support_group", "church", "community_center", "online_forum"],
                k=random.randint(1, 2)
            )
        
        return support
    
    def generate_life_events(self, persona_type: str, demographics: Demographics) -> List[LifeEvent]:
        """Generate recent life events with journey impact"""
        events = []
        
        # Event frequency by persona
        event_frequency = {
            "health_aware_avoider": 0.7,
            "structured_system_seeker": 0.5,
            "balanced_life_integrator": 0.6,
            "healthcare_professional": 0.4,
            "overlooked_risk_group": 0.8
        }
        
        if random.random() < event_frequency[persona_type]:
            num_events = random.randint(1, 3)
            
            event_types = [
                ("health", ["diagnosis", "surgery", "family_illness", "mental_health_crisis"]),
                ("career", ["job_loss", "promotion", "retirement", "career_change"]),
                ("family", ["marriage", "divorce", "birth", "death", "caregiving"]),
                ("financial", ["bankruptcy", "inheritance", "major_expense"]),
                ("social", ["relocation", "isolation", "relationship_change"])
            ]
            
            for _ in range(num_events):
                event_category, event_options = random.choice(event_types)
                event_name = random.choice(event_options)
                days_ago = random.randint(30, 365)
                
                event = LifeEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=event_category,
                    event_name=event_name,
                    event_date=(self.current_date - timedelta(days=days_ago)).isoformat(),
                    days_ago=days_ago,
                    impact_level=random.choice(["high", "moderate", "low"]),
                    status=random.choice(["ongoing", "resolved", "processing"]),
                    requires_support=random.random() < 0.5,
                    specialized_path_triggered=days_ago < 180 and random.random() < 0.3
                )
                
                # Journey impact
                if event.impact_level == "high":
                    event.journey_impact = {
                        "completion_modifier": -0.2,
                        "trust_modifier": -0.5,
                        "time_modifier": 1.5,
                        "support_needs": ["counseling", "flexibility", "resources"]
                    }
                elif event.impact_level == "moderate":
                    event.journey_impact = {
                        "completion_modifier": -0.1,
                        "trust_modifier": 0,
                        "time_modifier": 1.2,
                        "support_needs": ["understanding", "flexibility"]
                    }
                
                events.append(event)
        
        return events
    
    def generate_narrative_elements(self, persona_type: str, demographics: Demographics,
                                   family_history: FamilyHistory, 
                                   healthcare_access: HealthcareAccess) -> NarrativeElements:
        """Generate rich narrative responses"""
        
        # Persona-specific narratives
        narratives = {
            "health_aware_avoider": {
                "philosophy": "I believe in listening to my body but I also know that sometimes ignorance feels safer than knowing.",
                "motivation": "My friend was recently diagnosed and it made me realize I can't keep avoiding this forever.",
                "hesitation": "I'm terrified of what they might find. My mom went through treatment and it was so hard.",
                "ideal": "A provider who understands my fears and doesn't judge me for waiting so long."
            },
            "structured_system_seeker": {
                "philosophy": "Prevention is always better than treatment. I believe in being proactive with data-driven decisions.",
                "motivation": "I want to understand my exact risk level so I can create an optimal screening schedule.",
                "hesitation": "I worry about overscreening but also missing something important.",
                "ideal": "Clear protocols, consistent providers, and evidence-based recommendations."
            },
            "balanced_life_integrator": {
                "philosophy": "Health is important but it needs to fit into my whole life, not dominate it.",
                "motivation": "I want to be healthy for my family without letting fear control our lives.",
                "hesitation": "Finding time for appointments while juggling work and family is challenging.",
                "ideal": "Flexible scheduling, efficient visits, and practical advice that fits my lifestyle."
            },
            "healthcare_professional": {
                "philosophy": "I've seen what early detection can do. Knowledge truly is power in healthcare.",
                "motivation": "I know the statistics and I want to be on the right side of them.",
                "hesitation": "Sometimes knowing too much makes every symptom feel significant.",
                "ideal": "Colleague-to-colleague discussions with access to detailed data and latest research."
            },
            "overlooked_risk_group": {
                "philosophy": "I do the best I can with what I have. Health is important but not always accessible.",
                "motivation": "I want to take care of myself but the system isn't designed for people like me.",
                "hesitation": "Cost, time off work, finding childcare - there are so many barriers.",
                "ideal": "Affordable care, flexible hours, and providers who understand my situation."
            }
        }
        
        persona_narrative = narratives[persona_type]
        
        # Build narrative elements
        narrative = NarrativeElements(
            self_description=f"I'm {demographics.preferred_name}, {demographics.age} years old, and I work hard to balance everything in my life.",
            health_philosophy=persona_narrative["philosophy"],
            motivation_for_joining=persona_narrative["motivation"],
            healthcare_story=f"My relationship with healthcare has been {healthcare_access.provider_relationship}. "
                           f"{'I have a regular doctor' if healthcare_access.has_primary_care else 'I dont have a regular doctor'}.",
            screening_hesitations=persona_narrative["hesitation"],
            ideal_healthcare_experience=persona_narrative["ideal"],
            health_priorities=random.sample(["prevention", "family", "longevity", "quality_of_life", "peace_of_mind"], k=3),
            detection_comfort_level=random.choice(["very_uncomfortable", "uncomfortable", "neutral", "comfortable"]),
            decision_making_style=random.choice(["analytical", "intuitive", "collaborative", "delegating"]),
            information_preferences=random.choice(["detailed", "summary", "visual", "verbal"]),
            health_goals=random.sample(["regular_screening", "reduce_risk", "understand_genetics", "lifestyle_change"], k=2),
            perceived_barriers=healthcare_access.screening_barriers,
            success_definitions=["completing_assessment", "getting_screened", "peace_of_mind"],
            support_preferences=random.choice(["independent", "family_involved", "provider_guided", "peer_support"]),
            communication_style=random.choice(["direct", "gentle", "detailed", "brief"]),
            learning_style=random.choice(["reading", "video", "interactive", "discussion"])
        )
        
        # Add family context if relevant
        if family_history.mother_cancer:
            narrative.healthcare_story += f" My mother had {family_history.mother_cancer_type} cancer, which affects how I think about screening."
        
        return narrative
    
    def generate_weekly_journey(self, persona_type: str, demographics: Demographics,
                               family_history: FamilyHistory, reproductive_history: ReproductiveHistory,
                               healthcare_access: HealthcareAccess, lifestyle_factors: LifestyleFactors,
                               current_health: CurrentHealth, life_events: List[LifeEvent]) -> List[WeeklyAssessment]:
        """Generate realistic weekly journey with completion patterns"""
        
        assessments = []
        trust_pattern = TRUST_PATTERNS[persona_type]
        current_trust = trust_pattern["start"]
        
        # Calculate completion modifier based on life events
        completion_modifier = 1.0
        for event in life_events:
            if event.impact_level == "high" and event.days_ago < 90:
                completion_modifier *= 0.8
            elif event.impact_level == "moderate" and event.days_ago < 60:
                completion_modifier *= 0.9
        
        # Generate each week
        for week in range(1, 11):
            # Check if user continues based on completion rates
            base_rate = COMPLETION_RATES[week]
            adjusted_rate = min(1.0, base_rate * completion_modifier)
            
            # Persona-specific completion adjustments
            if persona_type == "health_aware_avoider":
                adjusted_rate *= 0.95
            elif persona_type == "structured_system_seeker":
                adjusted_rate = min(1.0, adjusted_rate * 1.3)
            elif persona_type == "healthcare_professional":
                adjusted_rate = min(1.0, adjusted_rate * 1.4)
            elif persona_type == "balanced_life_integrator":
                adjusted_rate = min(1.0, adjusted_rate * 1.1)
            elif persona_type == "overlooked_risk_group":
                adjusted_rate *= 0.8
            
            # Use cumulative probability for more realistic distribution
            continue_probability = random.random()
            if week == 1:
                # Most users complete week 1
                if continue_probability > adjusted_rate:
                    break
            else:
                # For later weeks, use stricter continuation
                if continue_probability > adjusted_rate * 1.2:
                    break
            
            # Determine completion status
            if random.random() < 0.9:  # 90% fully complete
                completion_status = "completed"
                completed = True
            else:
                completion_status = "partial"
                completed = False
            
            # Calculate time spent
            base_time = {
                1: 15, 2: 12, 3: 25, 4: 20, 5: 18,
                6: 22, 7: 15, 8: 17, 9: 20, 10: 30
            }
            time_spent = base_time[week] + random.randint(-5, 10)
            
            # Determine emotional state
            if week <= 3:
                emotional_state = random.choice(EMOTIONAL_STATES["early"])
            elif week <= 7:
                emotional_state = random.choice(EMOTIONAL_STATES["middle"])
            else:
                emotional_state = random.choice(EMOTIONAL_STATES["late"])
            
            # Create assessment
            started_at = self.current_date - timedelta(days=70-week*7) + timedelta(hours=random.randint(0, 23))
            completed_at = started_at + timedelta(minutes=time_spent) if completed else None
            
            assessment = WeeklyAssessment(
                week=week,
                completed=completed,
                completion_status=completion_status,
                started_at=started_at.isoformat(),
                completed_at=completed_at.isoformat() if completed_at else None,
                time_spent_minutes=time_spent,
                emotional_state=emotional_state,
                trust_level=min(trust_pattern["max"], current_trust),
                response_quality=random.uniform(0.7, 1.0) if completed else random.uniform(0.3, 0.7),
                sessions_count=random.randint(1, 3),
                help_requests=random.randint(0, 2) if week > 3 else 0
            )
            
            # Add week-specific responses
            assessment.responses = self.generate_week_responses(
                week, demographics, family_history, reproductive_history,
                healthcare_access, lifestyle_factors, current_health
            )
            
            # Add open-ended responses
            assessment.open_ended_responses = self.generate_week_open_ended(
                week, persona_type, emotional_state
            )
            
            # Risk model used
            if week >= 1:
                assessment.risk_model_used = "GAIL"
            if week >= 3:
                assessment.risk_model_used = "Tyrer-Cuzick"
            if week >= 6:
                assessment.risk_model_used = "BOADICEA"
            
            # Educational content viewed
            if random.random() < 0.6:
                assessment.educational_content_viewed = random.sample(
                    [f"week_{week}_intro", f"risk_factors_{week}", f"prevention_tips_{week}"],
                    k=random.randint(1, 2)
                )
            
            assessments.append(assessment)
            
            # Update trust level
            current_trust += trust_pattern["increment"]
        
        return assessments
    
    def generate_week_responses(self, week: int, demographics: Demographics,
                               family_history: FamilyHistory, reproductive_history: ReproductiveHistory,
                               healthcare_access: HealthcareAccess, lifestyle_factors: LifestyleFactors,
                               current_health: CurrentHealth) -> Dict[str, Any]:
        """Generate specific responses for each week's assessment"""
        
        responses = {}
        
        if week == 1:
            # Zero Assessment - Foundation
            responses = {
                "age": demographics.age,
                "biological_sex": demographics.biological_sex,
                "race_ethnicity": demographics.race_ethnicity,
                "preferred_name": demographics.preferred_name,
                "legal_name": demographics.legal_name
            }
        
        elif week == 2:
            # Family History
            responses = {
                "mother_cancer": family_history.mother_cancer,
                "mother_cancer_type": family_history.mother_cancer_type,
                "mother_cancer_age": family_history.mother_cancer_age,
                "siblings_cancer": family_history.siblings_cancer,
                "family_communication": family_history.family_communication
            }
        
        elif week == 3:
            # Reproductive History
            responses = {
                "age_at_menarche": reproductive_history.age_at_menarche,
                "pregnancies": reproductive_history.pregnancies,
                "age_at_first_birth": reproductive_history.age_at_first_birth,
                "breastfeeding_months": reproductive_history.breastfeeding_months,
                "hormone_use": reproductive_history.hormone_use
            }
        
        elif week == 4:
            # Healthcare Access
            responses = {
                "has_primary_care": healthcare_access.has_primary_care,
                "provider_relationship": healthcare_access.provider_relationship,
                "screening_barriers": healthcare_access.screening_barriers,
                "healthcare_comfort": healthcare_access.healthcare_comfort
            }
        
        elif week == 5:
            # Lifestyle Factors
            responses = {
                "physical_activity": lifestyle_factors.physical_activity,
                "alcohol_use": lifestyle_factors.alcohol_use,
                "smoking": lifestyle_factors.smoking,
                "stress_level": lifestyle_factors.stress_level,
                "sleep_quality": lifestyle_factors.sleep_quality
            }
        
        elif week == 6:
            # Extended Family
            responses = {
                "grandparents_cancer": family_history.grandparents_cancer,
                "aunts_uncles_cancer": family_history.aunts_uncles_cancer,
                "genetic_testing_interest": random.choice(["yes", "no", "maybe"]),
                "ashkenazi_jewish": family_history.ashkenazi_jewish
            }
        
        elif week == 7:
            # Current Health
            responses = {
                "overall_health": current_health.overall_health,
                "chronic_conditions": current_health.chronic_conditions,
                "recent_symptoms": current_health.recent_symptoms,
                "self_exam_frequency": current_health.self_exam_frequency
            }
        
        elif week == 8:
            # Support Systems
            responses = {
                "family_support": "moderate",
                "financial_stability": "stable",
                "transportation_access": "reliable",
                "work_flexibility": "moderate"
            }
        
        elif week == 9:
            # Values and Preferences
            responses = {
                "health_priorities": ["prevention", "family", "quality_of_life"],
                "detection_comfort": "moderate",
                "decision_style": "collaborative",
                "information_preference": "summary"
            }
        
        elif week == 10:
            # Plan Review and Commitment
            responses = {
                "plan_understood": True,
                "implementation_ready": random.random() < 0.7,
                "barriers_identified": random.randint(1, 3),
                "support_needed": random.choice(["minimal", "moderate", "significant"])
            }
        
        return responses
    
    def generate_week_open_ended(self, week: int, persona_type: str, 
                                emotional_state: str) -> Dict[str, str]:
        """Generate open-ended responses for each week"""
        
        responses = {}
        
        # Week-specific prompts and responses
        week_prompts = {
            1: {
                "motivation": "What brought you to Stage Zero today?",
                "concerns": "What are your main health concerns?"
            },
            2: {
                "family_impact": "How has your family's cancer history affected you?",
                "communication": "How does your family talk about cancer?"
            },
            3: {
                "reproductive_reflection": "How do you feel about these reproductive factors?",
                "body_changes": "How have hormonal changes affected you?"
            },
            4: {
                "healthcare_experience": "Describe your healthcare experiences.",
                "ideal_provider": "What would your ideal provider be like?"
            },
            5: {
                "lifestyle_challenges": "What makes healthy habits difficult?",
                "stress_sources": "What are your main sources of stress?"
            },
            6: {
                "genetic_feelings": "How do you feel about genetic risk?",
                "testing_thoughts": "What are your thoughts on genetic testing?"
            },
            7: {
                "health_narrative": "How would you describe your health journey?",
                "symptom_worries": "What symptoms concern you most?"
            },
            8: {
                "support_needs": "What kind of support do you need?",
                "resource_gaps": "What resources are you missing?"
            },
            9: {
                "values_reflection": "What matters most in your health decisions?",
                "fear_vs_action": "How do you balance fear with action?"
            },
            10: {
                "plan_reaction": "How do you feel about your personalized plan?",
                "next_steps": "What will you do first?"
            }
        }
        
        # Generate responses based on persona and emotional state
        if week in week_prompts:
            for prompt_key, prompt_text in week_prompts[week].items():
                responses[prompt_key] = self.generate_persona_response(
                    persona_type, emotional_state, prompt_text, week
                )
        
        return responses
    
    def generate_persona_response(self, persona_type: str, emotional_state: str,
                                 prompt: str, week: int) -> str:
        """Generate persona-appropriate response to prompt"""
        
        # Simplified response generation - in production, use more sophisticated NLG
        response_templates = {
            "health_aware_avoider": [
                "I've been putting this off for too long, but I know I need to face it.",
                "It's scary but I'm trying to be brave about understanding my risk.",
                "My anxiety makes this hard, but I'm taking it one step at a time."
            ],
            "structured_system_seeker": [
                "I want to understand all the data so I can make informed decisions.",
                "Having a clear plan and timeline helps me feel in control.",
                "I appreciate the systematic approach to risk assessment."
            ],
            "balanced_life_integrator": [
                "I'm trying to find a way to prioritize health without letting it consume me.",
                "This needs to work with my life, not against it.",
                "Balance is key - I want to be informed but not obsessed."
            ],
            "healthcare_professional": [
                "As someone in healthcare, I know the importance of early detection.",
                "I want to see the evidence and understand the recommendations.",
                "My medical knowledge helps but also makes me hyper-aware."
            ],
            "overlooked_risk_group": [
                "The system hasn't always worked for people like me.",
                "I'm doing my best with limited resources and time.",
                "I hope this program understands my situation."
            ]
        }
        
        return random.choice(response_templates[persona_type])
    
    def calculate_risk_assessments(self, demographics: Demographics, family_history: FamilyHistory,
                                  reproductive_history: ReproductiveHistory, lifestyle_factors: LifestyleFactors,
                                  weekly_assessments: List[WeeklyAssessment]) -> RiskAssessment:
        """Calculate comprehensive risk scores based on completed assessments"""
        
        assessment = RiskAssessment()
        
        # Count risk factors
        risk_factors = 0
        
        # Age risk
        if demographics.age > 50:
            risk_factors += 1
        
        # Family history risk
        if family_history.mother_cancer or family_history.siblings_cancer:
            risk_factors += 2
        if family_history.aunts_uncles_cancer >= 2:
            risk_factors += 1
        
        # Reproductive risk factors
        if reproductive_history.age_at_menarche and reproductive_history.age_at_menarche < 12:
            risk_factors += 1
        if reproductive_history.age_at_first_birth and reproductive_history.age_at_first_birth > 30:
            risk_factors += 1
        if reproductive_history.live_births == 0:
            risk_factors += 1
        
        # Lifestyle risk factors
        if lifestyle_factors.alcohol_use in ["moderate", "heavy"]:
            risk_factors += 1
        if lifestyle_factors.bmi > 30:
            risk_factors += 1
        
        assessment.risk_factors_count = risk_factors
        
        # Calculate GAIL score (simplified)
        assessment.gail_score = 1.0 + (risk_factors * 0.3)
        if assessment.gail_score < 1.3:
            assessment.gail_category = "low"
        elif assessment.gail_score < 1.67:
            assessment.gail_category = "average"
        else:
            assessment.gail_category = "elevated"
        
        assessment.gail_five_year_risk = min(0.3, assessment.gail_score * 0.015)
        assessment.gail_lifetime_risk = min(0.5, assessment.gail_score * 0.08)
        
        # Calculate Tyrer-Cuzick if week 3+ completed
        if len(weekly_assessments) >= 3:
            assessment.tyrer_cuzick_score = assessment.gail_score * random.uniform(0.9, 1.1)
            assessment.tyrer_cuzick_category = assessment.gail_category
            assessment.tyrer_cuzick_ten_year_risk = min(0.4, assessment.tyrer_cuzick_score * 0.02)
        
        # Calculate BOADICEA if week 6+ completed
        if len(weekly_assessments) >= 6:
            genetic_modifier = 1.2 if family_history.genetic_counseling_indicated else 1.0
            assessment.boadicea_score = assessment.gail_score * genetic_modifier
            assessment.boadicea_category = "elevated" if assessment.boadicea_score > 1.67 else "average"
            assessment.boadicea_genetic_risk = min(0.2, genetic_modifier * 0.1)
        
        # High risk criteria
        if assessment.gail_score >= 1.67:
            assessment.high_risk_criteria_met.append("GAIL >= 1.67")
        if family_history.genetic_counseling_indicated:
            assessment.high_risk_criteria_met.append("Strong family history")
        if reproductive_history.age_at_menarche and reproductive_history.age_at_menarche < 12:
            assessment.high_risk_criteria_met.append("Early menarche")
        
        # Genetic counseling indication
        assessment.genetic_counseling_indicated = (
            family_history.genetic_counseling_indicated or
            len(assessment.high_risk_criteria_met) >= 2
        )
        
        # Recommended screening age
        if assessment.gail_category == "elevated" or assessment.genetic_counseling_indicated:
            assessment.recommended_screening_age = 35
        elif assessment.gail_category == "average" and family_history.mother_cancer:
            assessment.recommended_screening_age = 40
        else:
            assessment.recommended_screening_age = 45
        
        return assessment
    
    def generate_personalized_plan(self, demographics: Demographics, risk_assessment: RiskAssessment,
                                  healthcare_access: HealthcareAccess, narrative_elements: NarrativeElements,
                                  support_system: SupportSystem, lifestyle_factors: LifestyleFactors) -> PersonalizedPlan:
        """Generate comprehensive personalized detection plan"""
        
        plan = PersonalizedPlan(
            plan_id=str(uuid.uuid4()),
            created_at=self.current_date.isoformat(),
            risk_summary=f"Based on your 10-week assessment, your breast cancer risk is {risk_assessment.gail_category}.",
            risk_interpretation=self.generate_risk_interpretation(risk_assessment, demographics),
            personalized_factors=[],
            screening_schedule={},
            immediate_actions=[],
            lifestyle_modifications=[],
            provider_talking_points=[],
            insurance_navigation={},
            barrier_solutions={},
            check_in_schedule=[],
            support_resources=[]
        )
        
        # Personalized factors
        if risk_assessment.risk_factors_count > 0:
            plan.personalized_factors = [
                f"You have {risk_assessment.risk_factors_count} identified risk factors",
                f"Your GAIL score is {risk_assessment.gail_score:.2f}",
                f"Recommended screening should begin at age {risk_assessment.recommended_screening_age}"
            ]
        
        # Screening schedule
        current_age = demographics.age
        if current_age >= risk_assessment.recommended_screening_age:
            plan.screening_schedule = {
                "mammogram": "Annual",
                "clinical_exam": "Every 6 months",
                "self_exam": "Monthly"
            }
        else:
            years_until = risk_assessment.recommended_screening_age - current_age
            plan.screening_schedule = {
                "mammogram": f"Begin in {years_until} years",
                "clinical_exam": "Annual",
                "self_exam": "Monthly"
            }
        
        # Immediate actions based on risk and access
        if risk_assessment.gail_category == "elevated":
            plan.immediate_actions.append({
                "action": "Schedule mammogram",
                "timeline": "Within 30 days",
                "priority": "high"
            })
        
        if risk_assessment.genetic_counseling_indicated:
            plan.immediate_actions.append({
                "action": "Genetic counseling consultation",
                "timeline": "Within 60 days",
                "priority": "high"
            })
        
        if not healthcare_access.has_primary_care:
            plan.immediate_actions.append({
                "action": "Find primary care provider",
                "timeline": "Within 2 weeks",
                "priority": "high"
            })
        
        # Lifestyle modifications
        if lifestyle_factors.physical_activity in ["sedentary", "light"]:
            plan.lifestyle_modifications.append({
                "area": "Physical Activity",
                "recommendation": "Increase to 150 minutes moderate exercise weekly",
                "impact": "Can reduce risk by up to 20%"
            })
        
        if lifestyle_factors.alcohol_use in ["moderate", "heavy"]:
            plan.lifestyle_modifications.append({
                "area": "Alcohol",
                "recommendation": "Limit to less than 1 drink per day",
                "impact": "Can reduce risk by 10-15%"
            })
        
        # Provider talking points
        plan.provider_talking_points = [
            f"My GAIL risk score is {risk_assessment.gail_score:.2f}",
            f"I have a family history of cancer" if risk_assessment.genetic_counseling_indicated else "No significant family history",
            f"I want to discuss screening options for my risk level"
        ]
        
        # Insurance navigation
        plan.insurance_navigation = {
            "coverage_type": demographics.insurance_type,
            "preventive_coverage": "Most plans cover annual mammograms after 40",
            "genetic_testing": "May be covered if criteria met",
            "resources": ["insurance_advocate", "patient_financial_services"]
        }
        
        # Barrier solutions
        for barrier in healthcare_access.screening_barriers:
            solutions = {
                "cost": ["Payment plans available", "Free screening programs", "Insurance coverage review"],
                "time": ["Weekend appointments", "Mobile mammography", "Workplace screening"],
                "fear": ["Support group", "Gradual exposure", "Companion allowed"],
                "transportation": ["Mobile units", "Ride services", "Telehealth options"]
            }
            if barrier in solutions:
                plan.barrier_solutions[barrier] = solutions[barrier]
        
        # Follow-up schedule
        plan.check_in_schedule = [
            {"timeframe": "2 weeks", "action": "Confirm first appointment scheduled"},
            {"timeframe": "1 month", "action": "Review plan progress"},
            {"timeframe": "3 months", "action": "Assess implementation"},
            {"timeframe": "6 months", "action": "Update risk assessment"}
        ]
        
        # Support resources
        plan.support_resources = [
            {"type": "educational", "name": "Stage Zero Learning Library", "url": "stagezero.com/learn"},
            {"type": "support", "name": "Peer Support Network", "url": "stagezero.com/community"},
            {"type": "tools", "name": "Risk Calculator", "url": "stagezero.com/tools"}
        ]
        
        # User feedback (simulate for completed journeys)
        if random.random() < 0.8:  # 80% provide feedback
            plan.plan_satisfaction = random.randint(7, 10)
            plan.implementation_commitment = random.uniform(0.6, 0.95)
            plan.likelihood_to_recommend = random.randint(7, 10)
        
        return plan
    
    def generate_risk_interpretation(self, risk_assessment: RiskAssessment, 
                                    demographics: Demographics) -> str:
        """Generate personalized risk interpretation"""
        
        if risk_assessment.gail_category == "low":
            return (f"At age {demographics.age}, your risk is below average. This doesn't mean zero risk, "
                   "but it does mean you can follow standard screening guidelines with confidence.")
        elif risk_assessment.gail_category == "average":
            return (f"Your risk level is similar to most women your age. Regular screening starting at "
                   f"{risk_assessment.recommended_screening_age} is important for early detection.")
        else:
            return (f"Your risk is higher than average, which means earlier and more frequent screening "
                   "could benefit you. This doesn't mean you will develop cancer, but vigilance is important.")


def main():
    """Generate and save enhanced synthetic users"""
    generator = StageZeroEnhancedGenerator()
    
    print("Generating 500 enhanced Stage Zero synthetic users...")
    users = generator.generate_users(500)
    
    # Convert to dict for JSON serialization
    users_data = []
    for user in users:
        user_dict = {
            "user_id": user.demographics.user_id,
            "persona_type": user.demographics.persona_type,
            "demographics": asdict(user.demographics),
            "family_history": asdict(user.family_history),
            "reproductive_history": asdict(user.reproductive_history),
            "healthcare_access": asdict(user.healthcare_access),
            "lifestyle_factors": asdict(user.lifestyle_factors),
            "current_health": asdict(user.current_health),
            "support_system": asdict(user.support_system),
            "risk_assessment": asdict(user.risk_assessment),
            "weekly_journey": [asdict(w) for w in user.weekly_assessments],
            "life_events": [asdict(e) for e in user.life_events],
            "narrative_elements": asdict(user.narrative_elements),
            "personalized_plan": asdict(user.personalized_plan) if user.personalized_plan else None,
            "privacy_indicators": asdict(user.privacy_indicators),
            "metadata": {
                "created_at": user.created_at,
                "last_active": user.last_active,
                "journey_status": user.journey_status,
                "total_time_invested_minutes": user.total_time_invested_minutes,
                "overall_completion_rate": user.overall_completion_rate
            }
        }
        users_data.append(user_dict)
    
    # Save to file
    output_path = Path("/Users/stephenszermer/Dev/synth/output/stage_zero_enhanced_500_users.json")
    with open(output_path, 'w') as f:
        json.dump(users_data, f, indent=2)
    
    print(f"✅ Generated {len(users)} enhanced users")
    print(f"📁 Saved to: {output_path}")
    
    # Print statistics
    print("\n=== Generation Statistics ===")
    
    # Persona distribution
    persona_counts = {}
    for user in users:
        persona = user.demographics.persona_type
        persona_counts[persona] = persona_counts.get(persona, 0) + 1
    
    print("\nPersona Distribution:")
    for persona, count in sorted(persona_counts.items()):
        print(f"  {persona}: {count} ({count/len(users)*100:.1f}%)")
    
    # Completion statistics
    completion_stats = {}
    for week in range(1, 11):
        completed = sum(1 for u in users if len(u.weekly_assessments) >= week 
                       and u.weekly_assessments[week-1].completed)
        completion_stats[week] = completed
    
    print("\nWeekly Completion Rates:")
    for week, count in completion_stats.items():
        print(f"  Week {week}: {count}/{len(users)} ({count/len(users)*100:.1f}%)")
    
    # Journey completion
    fully_completed = sum(1 for u in users if u.journey_status == "completed")
    print(f"\nFully Completed Journeys: {fully_completed}/{len(users)} ({fully_completed/len(users)*100:.1f}%)")
    
    # Risk distribution
    risk_categories = {"low": 0, "average": 0, "elevated": 0}
    for user in users:
        risk_categories[user.risk_assessment.gail_category] += 1
    
    print("\nRisk Distribution:")
    for category, count in risk_categories.items():
        print(f"  {category}: {count} ({count/len(users)*100:.1f}%)")
    
    # Life events
    users_with_events = sum(1 for u in users if u.life_events)
    print(f"\nUsers with Life Events: {users_with_events}/{len(users)} ({users_with_events/len(users)*100:.1f}%)")
    
    # Sample user details
    print("\n=== Sample User Details ===")
    completed_users = [u for u in users if u.journey_status == "completed"]
    if completed_users:
        sample_user = random.choice(completed_users)
    else:
        # If no completed users, pick the one who got furthest
        sample_user = max(users, key=lambda u: len(u.weekly_assessments))
    
    print(f"\nUser: {sample_user.demographics.preferred_name}")
    print(f"Age: {sample_user.demographics.age}")
    print(f"Persona: {sample_user.demographics.persona_type}")
    print(f"Risk Category: {sample_user.risk_assessment.gail_category}")
    print(f"GAIL Score: {sample_user.risk_assessment.gail_score:.2f}")
    print(f"Weeks Completed: {len(sample_user.weekly_assessments)}")
    print(f"Total Time Invested: {sample_user.total_time_invested_minutes} minutes")
    print(f"Journey Status: {sample_user.journey_status}")
    
    if sample_user.narrative_elements:
        print(f"\nMotivation: \"{sample_user.narrative_elements.motivation_for_joining}\"")
        print(f"Health Philosophy: \"{sample_user.narrative_elements.health_philosophy}\"")
    
    if sample_user.personalized_plan:
        if sample_user.personalized_plan.plan_satisfaction:
            print(f"\nPlan Satisfaction: {sample_user.personalized_plan.plan_satisfaction}/10")
        if sample_user.personalized_plan.implementation_commitment:
            print(f"Implementation Commitment: {sample_user.personalized_plan.implementation_commitment:.1%}")


if __name__ == "__main__":
    main()