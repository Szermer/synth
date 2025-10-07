# Stage Zero Health Persona Configuration
# Aligned with the documented user segments and narrative approach

STAGE_ZERO_PERSONAS = {
    "healthcare_professional_consumer_bridge": {
        "profile": "Jessica Rivera, NP (32)",
        "age_range": (28, 45),
        "characteristics": {
            "professional_knowledge": (0.8, 0.95),
            "personal_boundaries": (0.7, 0.9),
            "evidence_seeking": (0.85, 0.95),
            "influence_potential": (0.7, 0.9)
        },
        "narrative_preferences": {
            "scientific_transparency": True,
            "evidence_based_validation": True,
            "professional_terminology_comfort": (0.8, 0.95),
            "clinical_integration_focus": True
        },
        "conversation_patterns": {
            "detail_seeking": "high",
            "skepticism_level": "moderate",
            "story_sharing_comfort": (0.6, 0.8),
            "family_history_completeness": (0.8, 0.95)
        },
        "weekly_engagement": {
            "completion_likelihood": (0.85, 0.95),
            "depth_preference": "comprehensive",
            "trust_building_speed": "moderate",
            "clinical_integration": "high"
        }
    },
    
    "structured_system_seeker": {
        "profile": "Rebecca Chen (29) - MBA Student",
        "age_range": (25, 40),
        "characteristics": {
            "organization_preference": (0.85, 0.95),
            "goal_orientation": (0.8, 0.95),
            "system_integration": (0.7, 0.9),
            "disruption_sensitivity": (0.6, 0.8)
        },
        "narrative_preferences": {
            "timeline_visualization": True,
            "milestone_tracking": True,
            "integration_planning": True,
            "achievement_recognition": True
        },
        "conversation_patterns": {
            "systematic_responses": "high",
            "completionist_tendency": (0.8, 0.95),
            "calendar_integration_need": True,
            "progress_metrics_desire": (0.8, 0.9)
        },
        "life_transition_factors": {
            "geographic_mobility": "high",
            "career_transitions": "frequent",
            "routine_disruption": "challenging",
            "adaptation_strategies": ["detailed_planning", "backup_systems"]
        }
    },
    
    "health_aware_avoider": {
        "profile": "Laura Martinez (31) - Marketing Manager",
        "age_range": (25, 45),
        "characteristics": {
            "health_awareness": (0.7, 0.9),
            "action_avoidance": (0.6, 0.8),
            "anxiety_management": (0.4, 0.7),
            "system_complexity_aversion": (0.7, 0.9)
        },
        "narrative_preferences": {
            "anxiety_acknowledgment": True,
            "simplified_pathways": True,
            "gradual_disclosure": True,
            "emotional_support": "high"
        },
        "conversation_patterns": {
            "hesitation_markers": ["I'm not sure", "Maybe", "I think"],
            "story_sharing_comfort": (0.3, 0.6),
            "completion_pace": "slower",
            "support_seeking": (0.6, 0.8)
        },
        "barriers_and_motivations": {
            "emotional_barriers": ["family_anxiety", "system_complexity"],
            "motivations": ["simplicity", "convenience", "anxiety_reduction"],
            "trust_building_needs": "high",
            "validation_requirements": "frequent"
        }
    },
    
    "balanced_life_integrator": {
        "profile": "Betsy Langford (55) - Semi-retired Consultant",
        "age_range": (45, 65),
        "characteristics": {
            "holistic_approach": (0.8, 0.95),
            "life_balance_priority": (0.85, 0.95),
            "quality_focus": (0.8, 0.9),
            "simplicity_preference": (0.7, 0.9)
        },
        "narrative_preferences": {
            "lifestyle_integration": True,
            "minimal_disruption": True,
            "quality_over_quantity": True,
            "community_connection": (0.6, 0.8)
        },
        "conversation_patterns": {
            "wisdom_sharing": (0.7, 0.9),
            "life_context_emphasis": "high",
            "value_alignment": "critical",
            "wellbeing_focus": "holistic"
        },
        "detection_preferences": {
            "life_integrated_options": True,
            "minimal_medical_focus": (0.6, 0.8),
            "sustainable_practices": True,
            "community_support": (0.5, 0.7)
        }
    },
    
    "overlooked_risk_group": {
        "profile": "Michael Reynolds (62) - Construction Project Manager",
        "age_range": (35, 70),
        "characteristics": {
            "demographic_invisibility": (0.7, 0.9),
            "healthcare_navigation": (0.3, 0.6),
            "family_history_awareness": (0.2, 0.5),
            "advocacy_skill_need": (0.6, 0.9)
        },
        "narrative_preferences": {
            "inclusive_representation": True,
            "validation_emphasis": "high",
            "stigma_reduction": True,
            "clear_protocols": True
        },
        "conversation_patterns": {
            "initial_uncertainty": (0.6, 0.8),
            "learning_engagement": (0.4, 0.7),
            "advocacy_development": "progressive",
            "provider_preparation": "needed"
        },
        "unique_considerations": {
            "gender_specific_content": True,
            "cultural_barriers": ["masculine_health_norms", "professional_culture"],
            "education_needs": ["risk_recognition", "provider_communication"],
            "support_requirements": ["advocacy_tools", "inclusive_guidance"]
        }
    }
}

# Weekly conversation themes and clinical objectives
WEEKLY_FRAMEWORK = {
    "week_1": {
        "theme": "foundation_setting",
        "clinical_objectives": ["demographics", "motivation", "healthcare_status"],
        "emotional_objectives": ["trust_building", "anxiety_reduction", "partnership_establishment"],
        "persona_adaptations": {
            "healthcare_professional_consumer_bridge": {
                "approach": "professional_validation",
                "content_depth": "detailed",
                "terminology": "clinical_comfortable"
            },
            "structured_system_seeker": {
                "approach": "systematic_explanation",
                "content_depth": "organized",
                "terminology": "clear_framework"
            },
            "health_aware_avoider": {
                "approach": "gentle_introduction",
                "content_depth": "essential",
                "terminology": "accessible"
            },
            "balanced_life_integrator": {
                "approach": "holistic_context",
                "content_depth": "integrated",
                "terminology": "life_focused"
            },
            "overlooked_risk_group": {
                "approach": "inclusive_validation",
                "content_depth": "explanatory",
                "terminology": "educational"
            }
        }
    },
    # Continue for weeks 2-10...
}

# Conversation response patterns by persona
CONVERSATION_RESPONSE_PATTERNS = {
    "healthcare_professional_consumer_bridge": {
        "question_style": "analytical",
        "detail_level": "comprehensive",
        "professional_references": True,
        "evidence_seeking": True,
        "boundary_setting": True
    },
    "structured_system_seeker": {
        "question_style": "systematic",
        "detail_level": "organized",
        "timeline_focus": True,
        "milestone_tracking": True,
        "integration_planning": True
    },
    "health_aware_avoider": {
        "question_style": "cautious",
        "detail_level": "gradual",
        "uncertainty_markers": True,
        "emotional_processing": True,
        "support_seeking": True
    },
    "balanced_life_integrator": {
        "question_style": "reflective",
        "detail_level": "contextual",
        "wisdom_sharing": True,
        "life_integration": True,
        "value_emphasis": True
    },
    "overlooked_risk_group": {
        "question_style": "learning",
        "detail_level": "educational",
        "uncertainty_acknowledgment": True,
        "advocacy_development": True,
        "validation_seeking": True
    }
}
