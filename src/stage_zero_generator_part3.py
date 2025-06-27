"""
Stage Zero Generator - Part 3: Health, support, and journey generation
"""

# Additional methods for the StageZeroGenerator class

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
    
    return assessment