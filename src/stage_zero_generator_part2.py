"""
Stage Zero Generator - Part 2: Core generation methods
"""

# This file contains the remaining methods for the StageZeroGenerator class
# These should be added to the main stage_zero_generator.py file

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
    
    return factors