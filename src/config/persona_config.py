from typing import Dict, List, Tuple

# Persona distribution percentages
PERSONA_DISTRIBUTION = {
    "health_aware_avoider": 0.30,  # 150 profiles
    "structured_system_seeker": 0.25,  # 125 profiles
    "balanced_life_integrator": 0.20,  # 100 profiles
    "healthcare_professional": 0.15,  # 75 profiles
    "overlooked_risk_group": 0.10,  # 50 profiles
}

# Breast cancer risk probabilities by age group (10-year probabilities)
BREAST_CANCER_RISKS = {
    "20-29": {"diagnosis": 0.001, "death": 0.000},  # 0.1% diagnosis, <0.1% death
    "30-39": {"diagnosis": 0.005, "death": 0.000},  # 0.5% diagnosis, <0.1% death
    "40-49": {"diagnosis": 0.016, "death": 0.001},  # 1.6% diagnosis, 0.1% death
    "50-59": {"diagnosis": 0.025, "death": 0.003},  # 2.5% diagnosis, 0.3% death
    "60-69": {"diagnosis": 0.036, "death": 0.005},  # 3.6% diagnosis, 0.5% death
    "70-79": {"diagnosis": 0.042, "death": 0.007},  # 4.2% diagnosis, 0.7% death
    "80+": {"diagnosis": 0.031, "death": 0.010},    # 3.1% diagnosis, 1.0% death
}

# Race/ethnicity lifetime risk percentages
RACE_ETHNICITY_RISKS = {
    "Non-Hispanic White": 0.14,  # 14%
    "Non-Hispanic Black": 0.12,  # 12%
    "Non-Hispanic Asian/Pacific Islander": 0.12,  # 12%
    "Hispanic": 0.11,  # 11%
    "Non-Hispanic American Indian/Alaska Native": 0.10,  # 10%
}

# Persona templates with their characteristics
PERSONA_TEMPLATES: Dict[str, Dict] = {
    "health_aware_avoider": {
        "age_range": (25, 45),
        "gender_distribution": {"female": 0.95, "male": 0.05},
        "education_distribution": {
            "bachelor": 0.5,
            "master": 0.3,
            "high_school": 0.2,
        },
        "prevention_completion": (0.1, 0.4),
        "anxiety_level": (0.6, 0.9),
        "engagement_pattern": ["sporadic", "infrequent", "rare"],
        "avoidance_triggers": [
            "family_cancer_discussions",
            "screening_scheduling",
            "healthcare_admin",
        ],
        "health_awareness": (0.7, 0.9),
        "action_tendency": (0.1, 0.3),
        "risk_factors": [
            "family_history",
            "age",
            "hormonal_factors",
            "lifestyle"
        ],
        "pain_points": [
            "emotional_barriers",
            "system_complexity",
            "vague_risk_info",
            "care_relationship_difficulty"
        ],
        "primary_motivations": [
            "anxiety_reduction",
            "simplicity",
            "convenience"
        ],
        "prevention_approach": "symptom_triggered",
        "family_history_anxiety": (0.7, 1.0),
        "life_transitions": {
            "frequency": "high",
            "types": ["job_changes", "relocations", "relationship_changes"]
        }
    },
    "structured_system_seeker": {
        "age_range": (30, 50),
        "gender_distribution": {"female": 0.98, "male": 0.02},
        "education_distribution": {
            "bachelor": 0.4,
            "master": 0.5,
            "phd": 0.1,
        },
        "prevention_completion": (0.7, 0.95),
        "anxiety_level": (0.3, 0.6),
        "engagement_pattern": ["consistent", "scheduled", "regular"],
        "organization_level": "high",
        "health_awareness": (0.8, 1.0),
        "action_tendency": (0.7, 0.9),
        "risk_factors": [
            "age",
            "genetic_factors",
            "screening_history"
        ],
        "pain_points": [
            "routine_disruption",
            "fragmented_tracking",
            "time_constraints",
            "geographic_consistency"
        ],
        "primary_motivations": [
            "organization",
            "efficiency",
            "milestone_achievement"
        ],
        "prevention_approach": "systematic_tracking",
        "family_history_anxiety": (0.4, 0.7),
        "life_transitions": {
            "frequency": "very_high",
            "types": ["relocations", "career_changes", "family_changes"]
        }
    },
    "balanced_life_integrator": {
        "age_range": (28, 48),
        "gender_distribution": {"female": 0.97, "male": 0.03},
        "education_distribution": {
            "bachelor": 0.6,
            "master": 0.3,
            "high_school": 0.1,
        },
        "prevention_completion": (0.5, 0.8),
        "anxiety_level": (0.4, 0.7),
        "engagement_pattern": ["regular", "occasional", "planned"],
        "work_life_balance": "high",
        "health_awareness": (0.6, 0.8),
        "action_tendency": (0.5, 0.7),
        "risk_factors": [
            "age",
            "lifestyle",
            "environmental_factors"
        ],
        "pain_points": [
            "intrusive_technology",
            "metrics_overwhelm",
            "preference_disrespect",
            "holistic_provider_finding"
        ],
        "primary_motivations": [
            "quality_of_life",
            "lifestyle_integration",
            "holistic_wellness"
        ],
        "prevention_approach": "lifestyle_focused",
        "family_history_anxiety": (0.2, 0.4),
        "life_transitions": {
            "frequency": "low",
            "types": ["relationship_changes", "career_advancement"]
        }
    },
    "healthcare_professional": {
        "age_range": (25, 45),
        "gender_distribution": {"female": 0.90, "male": 0.10},
        "education_distribution": {
            "master": 0.4,
            "phd": 0.4,
            "bachelor": 0.2,
        },
        "prevention_completion": (0.8, 1.0),
        "anxiety_level": (0.2, 0.5),
        "engagement_pattern": ["consistent", "professional", "analytical"],
        "healthcare_expertise": "high",
        "health_awareness": (0.9, 1.0),
        "action_tendency": (0.8, 1.0),
        "risk_factors": [
            "occupational_exposure",
            "age",
            "genetic_factors"
        ],
        "pain_points": [
            "research_clinical_gap",
            "system_limitations",
            "data_overload",
            "professional_pressure"
        ],
        "primary_motivations": [
            "evidence_based_practice",
            "influencing_others",
            "clinical_expertise"
        ],
        "prevention_approach": "data_driven",
        "family_history_anxiety": (0.3, 0.6),
        "life_transitions": {
            "frequency": "moderate",
            "types": ["career_advancement", "specialization_changes"]
        }
    },
    "overlooked_risk_group": {
        "age_range": (30, 50),
        "gender_distribution": {"female": 0.92, "male": 0.08},
        "education_distribution": {
            "high_school": 0.5,
            "bachelor": 0.3,
            "master": 0.2,
        },
        "prevention_completion": (0.1, 0.3),
        "anxiety_level": (0.5, 0.8),
        "engagement_pattern": ["rare", "reactive", "infrequent"],
        "risk_factors": ["age", "family_history", "lifestyle", "socioeconomic"],
        "health_awareness": (0.3, 0.5),
        "action_tendency": (0.1, 0.3),
        "pain_points": [
            "standard_prevention_mismatch",
            "provider_dismissal",
            "social_stigma",
            "demographic_guidance_lack"
        ],
        "primary_motivations": [
            "recognition",
            "inclusivity",
            "clear_guidance"
        ],
        "prevention_approach": "protocol_seeking",
        "family_history_anxiety": (0.7, 1.0),
        "life_transitions": {
            "frequency": "moderate",
            "types": ["retirement_planning", "healthcare_access_changes"]
        }
    }
}

# Health condition probabilities by age group
HEALTH_CONDITIONS = {
    "20-29": {
        "hypertension": 0.05,
        "diabetes": 0.02,
        "asthma": 0.15,
        "anxiety": 0.2,
        "depression": 0.15,
        "benign_breast_conditions": 0.1,
    },
    "30-39": {
        "hypertension": 0.1,
        "diabetes": 0.05,
        "asthma": 0.15,
        "anxiety": 0.2,
        "depression": 0.15,
        "benign_breast_conditions": 0.15,
        "fibrocystic_breast_changes": 0.1,
    },
    "40-49": {
        "hypertension": 0.2,
        "diabetes": 0.1,
        "asthma": 0.12,
        "anxiety": 0.25,
        "depression": 0.2,
        "arthritis": 0.1,
        "benign_breast_conditions": 0.2,
        "fibrocystic_breast_changes": 0.15,
    },
    "50-59": {
        "hypertension": 0.3,
        "diabetes": 0.15,
        "asthma": 0.1,
        "anxiety": 0.3,
        "depression": 0.25,
        "arthritis": 0.2,
        "heart_disease": 0.1,
        "benign_breast_conditions": 0.25,
        "fibrocystic_breast_changes": 0.2,
    },
    "60-69": {
        "hypertension": 0.4,
        "diabetes": 0.2,
        "asthma": 0.1,
        "anxiety": 0.3,
        "depression": 0.25,
        "arthritis": 0.3,
        "heart_disease": 0.15,
        "benign_breast_conditions": 0.25,
        "fibrocystic_breast_changes": 0.2,
    },
    "70-79": {
        "hypertension": 0.5,
        "diabetes": 0.25,
        "asthma": 0.1,
        "anxiety": 0.3,
        "depression": 0.25,
        "arthritis": 0.4,
        "heart_disease": 0.2,
        "benign_breast_conditions": 0.2,
        "fibrocystic_breast_changes": 0.15,
    },
    "80+": {
        "hypertension": 0.6,
        "diabetes": 0.3,
        "asthma": 0.1,
        "anxiety": 0.3,
        "depression": 0.25,
        "arthritis": 0.5,
        "heart_disease": 0.25,
        "benign_breast_conditions": 0.15,
        "fibrocystic_breast_changes": 0.1,
    },
}

# Life event types and their characteristics
LIFE_EVENTS = {
    "health": {
        "diagnosis": {"impact": "high", "frequency": "rare"},
        "screening": {"impact": "medium", "frequency": "regular"},
        "treatment": {"impact": "high", "frequency": "rare"},
        "prevention": {"impact": "medium", "frequency": "regular"},
        "genetic_testing": {"impact": "high", "frequency": "rare"},
        "biopsy": {"impact": "high", "frequency": "rare"},
    },
    "career": {
        "job_change": {"impact": "medium", "frequency": "rare"},
        "promotion": {"impact": "low", "frequency": "rare"},
        "retirement": {"impact": "high", "frequency": "rare"},
    },
    "family": {
        "marriage": {"impact": "medium", "frequency": "rare"},
        "divorce": {"impact": "high", "frequency": "rare"},
        "child_birth": {"impact": "high", "frequency": "rare"},
        "family_loss": {"impact": "high", "frequency": "rare"},
        "family_cancer_diagnosis": {"impact": "high", "frequency": "rare"},
    },
}

# Location types and their characteristics
LOCATION_TYPES = {
    "urban": {
        "population_density": "high",
        "healthcare_access": "high",
        "stress_level": "high",
        "screening_facilities": "high",
    },
    "suburban": {
        "population_density": "medium",
        "healthcare_access": "medium",
        "stress_level": "medium",
        "screening_facilities": "medium",
    },
    "rural": {
        "population_density": "low",
        "healthcare_access": "low",
        "stress_level": "low",
        "screening_facilities": "low",
    },
}

# Engagement metrics
ENGAGEMENT_METRICS = {
    "visit_frequency": {
        "sporadic": {"min_visits": 1, "max_visits": 3, "interval_days": (30, 90)},
        "infrequent": {"min_visits": 2, "max_visits": 5, "interval_days": (15, 45)},
        "regular": {"min_visits": 4, "max_visits": 8, "interval_days": (7, 21)},
        "consistent": {"min_visits": 6, "max_visits": 12, "interval_days": (3, 10)},
    },
    "session_duration": {
        "short": (1, 5),
        "medium": (5, 15),
        "long": (15, 30),
    },
    "feature_usage": {
        "basic": ["profile", "view_history", "screening_reminders"],
        "intermediate": ["profile", "view_history", "schedule", "reminders", "risk_assessment"],
        "advanced": ["profile", "view_history", "schedule", "reminders", "analytics", "community", "genetic_risk"],
    },
}

"""Persona configuration settings."""

PERSONA_CONFIG = {
    "health_aware_avoider": {
        "age_range": (30, 60),
        "gender_distribution": {"female": 0.7, "male": 0.3},
        "education_distribution": {
            "high_school": 0.2,
            "some_college": 0.3,
            "bachelors": 0.3,
            "graduate": 0.2
        },
        "prevention_completion": (0.3, 0.7),
        "anxiety_level": (0.6, 0.9),
        "risk_factors": ["family_history", "lifestyle"],
        "health_awareness": (0.7, 0.9),
        "action_tendency": (0.3, 0.6),
        "engagement_pattern": ["sporadic", "infrequent", "rare"]
    },
    "structured_system_seeker": {
        "age_range": (35, 65),
        "gender_distribution": {"female": 0.6, "male": 0.4},
        "education_distribution": {
            "bachelors": 0.4,
            "graduate": 0.4,
            "professional": 0.2
        },
        "prevention_completion": (0.7, 0.95),
        "anxiety_level": (0.3, 0.6),
        "risk_factors": ["genetic_factors", "lifestyle"],
        "health_awareness": (0.8, 0.95),
        "action_tendency": (0.7, 0.9),
        "engagement_pattern": ["regular", "consistent", "planned"]
    },
    "balanced_life_integrator": {
        "age_range": (30, 55),
        "gender_distribution": {"female": 0.65, "male": 0.35},
        "education_distribution": {
            "some_college": 0.3,
            "bachelors": 0.4,
            "graduate": 0.3
        },
        "prevention_completion": (0.5, 0.8),
        "anxiety_level": (0.4, 0.7),
        "risk_factors": ["lifestyle", "environmental"],
        "health_awareness": (0.6, 0.8),
        "action_tendency": (0.5, 0.7),
        "engagement_pattern": ["regular", "occasional", "planned"]
    },
    "healthcare_professional": {
        "age_range": (35, 70),
        "gender_distribution": {"female": 0.6, "male": 0.4},
        "education_distribution": {
            "bachelors": 0.3,
            "graduate": 0.4,
            "professional": 0.3
        },
        "prevention_completion": (0.8, 0.98),
        "anxiety_level": (0.2, 0.5),
        "risk_factors": ["genetic_factors", "professional_exposure"],
        "health_awareness": (0.9, 0.98),
        "action_tendency": (0.8, 0.95),
        "engagement_pattern": ["consistent", "professional", "analytical"]
    },
    "overlooked_risk_group": {
        "age_range": (25, 50),
        "gender_distribution": {"female": 0.75, "male": 0.25},
        "education_distribution": {
            "high_school": 0.3,
            "some_college": 0.4,
            "bachelors": 0.3
        },
        "prevention_completion": (0.2, 0.5),
        "anxiety_level": (0.5, 0.8),
        "risk_factors": ["lifestyle", "environmental", "socioeconomic"],
        "health_awareness": (0.4, 0.6),
        "action_tendency": (0.2, 0.4),
        "engagement_pattern": ["sporadic", "reactive", "infrequent"]
    }
}

# Location types and their characteristics
LOCATION_TYPES = {
    "urban": {
        "population_density": "high",
        "healthcare_access": "high",
        "support_services": "high"
    },
    "suburban": {
        "population_density": "medium",
        "healthcare_access": "medium",
        "support_services": "medium"
    },
    "rural": {
        "population_density": "low",
        "healthcare_access": "low",
        "support_services": "low"
    }
}

# Life events and their characteristics
LIFE_EVENTS = {
    "health": {
        "diagnosis": {
            "frequency": "rare",
            "impact": "high"
        },
        "surgery": {
            "frequency": "rare",
            "impact": "high"
        },
        "recovery": {
            "frequency": "regular",
            "impact": "medium"
        }
    },
    "career": {
        "job_change": {
            "frequency": "regular",
            "impact": "medium"
        },
        "promotion": {
            "frequency": "rare",
            "impact": "high"
        },
        "retirement": {
            "frequency": "rare",
            "impact": "high"
        }
    },
    "family": {
        "marriage": {
            "frequency": "rare",
            "impact": "high"
        },
        "divorce": {
            "frequency": "rare",
            "impact": "high"
        },
        "birth": {
            "frequency": "rare",
            "impact": "high"
        }
    }
}

# Engagement metrics
ENGAGEMENT_METRICS = {
    "visit_frequency": {
        "sporadic": {"min_visits": 1, "max_visits": 3},
        "infrequent": {"min_visits": 2, "max_visits": 4},
        "regular": {"min_visits": 3, "max_visits": 6},
        "consistent": {"min_visits": 4, "max_visits": 8}
    },
    "session_duration": {
        "short": (5, 15),
        "medium": (15, 30),
        "long": (30, 60)
    },
    "feature_usage": {
        "basic": ["profile", "risk_assessment"],
        "standard": ["profile", "risk_assessment", "prevention_plan"],
        "advanced": ["profile", "risk_assessment", "prevention_plan", "support_network"]
    }
}

# Health conditions by age group
HEALTH_CONDITIONS = {
    "20-29": {
        "anxiety": 0.2,
        "depression": 0.15,
        "hypertension": 0.05
    },
    "30-39": {
        "anxiety": 0.25,
        "depression": 0.2,
        "hypertension": 0.1,
        "diabetes": 0.05
    },
    "40-49": {
        "anxiety": 0.3,
        "depression": 0.25,
        "hypertension": 0.2,
        "diabetes": 0.1,
        "arthritis": 0.05
    },
    "50-59": {
        "anxiety": 0.35,
        "depression": 0.3,
        "hypertension": 0.3,
        "diabetes": 0.15,
        "arthritis": 0.1,
        "heart_disease": 0.05
    },
    "60-69": {
        "anxiety": 0.4,
        "depression": 0.35,
        "hypertension": 0.4,
        "diabetes": 0.2,
        "arthritis": 0.15,
        "heart_disease": 0.1
    },
    "70-79": {
        "anxiety": 0.45,
        "depression": 0.4,
        "hypertension": 0.5,
        "diabetes": 0.25,
        "arthritis": 0.2,
        "heart_disease": 0.15
    },
    "80+": {
        "anxiety": 0.5,
        "depression": 0.45,
        "hypertension": 0.6,
        "diabetes": 0.3,
        "arthritis": 0.25,
        "heart_disease": 0.2
    }
}

# Breast cancer risks by age group
BREAST_CANCER_RISKS = {
    "20-29": {"diagnosis": 0.0001},
    "30-39": {"diagnosis": 0.004},
    "40-49": {"diagnosis": 0.02},
    "50-59": {"diagnosis": 0.03},
    "60-69": {"diagnosis": 0.04},
    "70-79": {"diagnosis": 0.05},
    "80+": {"diagnosis": 0.06}
}

# Race/ethnicity risk factors
RACE_ETHNICITY_RISKS = {
    "white": 0.7,
    "black": 0.15,
    "hispanic": 0.1,
    "asian": 0.05
} 