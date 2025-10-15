import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from pathlib import Path

from config.stage_zero_personas import (
    STAGE_ZERO_PERSONAS,
    WEEKLY_FRAMEWORK,
    CONVERSATION_RESPONSE_PATTERNS
)

class ConversationFlowGenerator:
    """Generate realistic 10-week conversation flows for Stage Zero Health"""
    
    def __init__(self):
        self.clinical_data_templates = self._load_clinical_templates()
        self.narrative_patterns = self._load_narrative_patterns()
        self.emotional_progression = self._define_emotional_progression()
    
    def _load_clinical_templates(self) -> Dict:
        """Clinical data templates for each week"""
        return {
            "week_1": {
                "required_fields": ["age", "ethnicity", "primary_motivation", "healthcare_access"],
                "narrative_elements": ["health_story_beginning", "family_influence", "current_concerns"]
            },
            "week_2": {
                "required_fields": ["family_cancer_history", "maternal_history", "paternal_history"],
                "narrative_elements": ["family_health_communication", "emotional_impact", "health_legacy"]
            },
            "week_3": {
                "required_fields": ["age_at_menarche", "pregnancy_history", "hormone_use"],
                "narrative_elements": ["reproductive_journey", "body_relationship", "health_timeline"]
            },
            "week_4": {
                "required_fields": ["healthcare_relationships", "screening_history", "access_barriers"],
                "narrative_elements": ["provider_experiences", "navigation_patterns", "advocacy_comfort"]
            },
            "week_5": {
                "required_fields": ["lifestyle_factors", "work_environment", "stress_management"],
                "narrative_elements": ["daily_life_context", "health_integration", "barrier_identification"]
            },
            "week_6": {
                "required_fields": ["extended_family_history", "ethnic_background", "genetic_patterns"],
                "narrative_elements": ["family_health_culture", "broader_patterns", "genetic_considerations"]
            },
            "week_7": {
                "required_fields": ["current_symptoms", "body_awareness", "exam_comfort"],
                "narrative_elements": ["current_health_status", "detection_readiness", "comfort_assessment"]
            },
            "week_8": {
                "required_fields": ["support_systems", "financial_resources", "cultural_factors"],
                "narrative_elements": ["support_network_mapping", "resource_assessment", "barrier_mitigation"]
            },
            "week_9": {
                "required_fields": ["health_values", "detection_preferences", "future_vision"],
                "narrative_elements": ["value_clarification", "preference_articulation", "goal_alignment"]
            },
            "week_10": {
                "required_fields": ["plan_integration", "implementation_readiness", "ongoing_support"],
                "narrative_elements": ["plan_personalization", "implementation_strategy", "future_planning"]
            }
        }
    
    def _load_narrative_patterns(self) -> Dict:
        """Narrative response patterns by persona and week"""
        return {
            "healthcare_professional_consumer_bridge": {
                "response_style": "analytical_personal",
                "detail_patterns": ["clinical_context", "personal_experience", "professional_insight"],
                "question_asking": "high",
                "evidence_references": True
            },
            "structured_system_seeker": {
                "response_style": "organized_comprehensive",
                "detail_patterns": ["systematic_timeline", "milestone_tracking", "integration_planning"],
                "question_asking": "moderate",
                "evidence_references": False
            },
            "health_aware_avoider": {
                "response_style": "cautious_gradual",
                "detail_patterns": ["uncertainty_acknowledgment", "emotional_processing", "gradual_disclosure"],
                "question_asking": "low",
                "evidence_references": False
            },
            "balanced_life_integrator": {
                "response_style": "reflective_holistic",
                "detail_patterns": ["life_context", "wisdom_sharing", "value_integration"],
                "question_asking": "moderate",
                "evidence_references": False
            },
            "overlooked_risk_group": {
                "response_style": "learning_engaged",
                "detail_patterns": ["knowledge_gaps", "advocacy_development", "validation_seeking"],
                "question_asking": "high",
                "evidence_references": False
            }
        }
    
    def _define_emotional_progression(self) -> Dict:
        """Emotional progression patterns through 10 weeks"""
        return {
            "healthcare_professional_consumer_bridge": {
                "weeks_1_3": ["professional_curiosity", "analytical_engagement", "boundary_setting"],
                "weeks_4_6": ["deepening_trust", "personal_sharing", "integration_thinking"],
                "weeks_7_9": ["comprehensive_engagement", "advocacy_preparation", "influence_planning"],
                "week_10": ["confident_implementation", "professional_integration", "peer_influence"]
            },
            "structured_system_seeker": {
                "weeks_1_3": ["systematic_approach", "information_gathering", "framework_building"],
                "weeks_4_6": ["detailed_planning", "timeline_development", "integration_focus"],
                "weeks_7_9": ["optimization_thinking", "milestone_preparation", "efficiency_planning"],
                "week_10": ["systematic_implementation", "tracking_setup", "routine_integration"]
            },
            "health_aware_avoider": {
                "weeks_1_3": ["cautious_exploration", "anxiety_acknowledgment", "gradual_trust"],
                "weeks_4_6": ["increasing_comfort", "story_sharing", "barrier_identification"],
                "weeks_7_9": ["growing_confidence", "support_seeking", "preparation_anxiety"],
                "week_10": ["empowered_planning", "supported_implementation", "ongoing_support"]
            },
            "balanced_life_integrator": {
                "weeks_1_3": ["holistic_consideration", "life_context_sharing", "value_exploration"],
                "weeks_4_6": ["integration_thinking", "balance_assessment", "priority_clarification"],
                "weeks_7_9": ["alignment_focus", "sustainable_planning", "quality_emphasis"],
                "week_10": ["integrated_approach", "life_aligned_implementation", "sustainable_practices"]
            },
            "overlooked_risk_group": {
                "weeks_1_3": ["initial_uncertainty", "learning_engagement", "validation_seeking"],
                "weeks_4_6": ["growing_awareness", "advocacy_development", "confidence_building"],
                "weeks_7_9": ["empowerment_growth", "preparation_focus", "support_identification"],
                "week_10": ["confident_advocacy", "prepared_implementation", "ongoing_learning"]
            }
        }
    
    def generate_weekly_conversation(self, persona_type: str, week: int, 
                                   previous_weeks_context: Optional[Dict] = None) -> Dict:
        """Generate conversation data for a specific week"""
        
        week_key = f"week_{week}"
        clinical_template = self.clinical_data_templates[week_key]
        persona_config = STAGE_ZERO_PERSONAS[persona_type]
        response_pattern = self.narrative_patterns[persona_type]
        
        # Generate narrative responses
        narrative_responses = self._generate_narrative_responses(
            persona_type, week, clinical_template, previous_weeks_context
        )
        
        # Extract clinical data
        clinical_data = self._extract_clinical_data(
            persona_type, week, narrative_responses
        )
        
        # Track emotional progression
        emotional_state = self._get_emotional_state(persona_type, week)
        
        # Measure engagement patterns
        engagement_metrics = self._calculate_engagement_metrics(
            persona_type, week, narrative_responses
        )
        
        # Trust building indicators
        trust_indicators = self._assess_trust_building(
            persona_type, week, narrative_responses, previous_weeks_context
        )
        
        return {
            "week": week,
            "persona_type": persona_type,
            "conversation_data": {
                "narrative_responses": narrative_responses,
                "clinical_data_captured": clinical_data,
                "emotional_progression": emotional_state,
                "engagement_metrics": engagement_metrics,
                "trust_indicators": trust_indicators,
                "completion_status": self._determine_completion_status(persona_type, week),
                "time_investment": self._calculate_time_investment(persona_type, week),
                "question_patterns": self._generate_question_patterns(persona_type, week)
            },
            "week_outcomes": {
                "clinical_objectives_met": self._assess_clinical_objectives(clinical_data, week),
                "emotional_objectives_met": self._assess_emotional_objectives(emotional_state, week),
                "trust_building_progress": trust_indicators["overall_trust_score"],
                "readiness_for_next_week": self._assess_readiness(persona_type, week, engagement_metrics)
            }
        }
    
    def _generate_narrative_responses(self, persona_type: str, week: int, 
                                    clinical_template: Dict, previous_context: Optional[Dict]) -> Dict:
        """Generate realistic narrative responses for the week"""
        
        response_style = self.narrative_patterns[persona_type]["response_style"]
        detail_patterns = self.narrative_patterns[persona_type]["detail_patterns"]
        
        responses = {}
        
        # Generate responses for each narrative element
        for element in clinical_template["narrative_elements"]:
            responses[element] = self._create_narrative_response(
                persona_type, week, element, response_style, detail_patterns, previous_context
            )
        
        return responses
    
    def _create_narrative_response(self, persona_type: str, week: int, element: str,
                                 response_style: str, detail_patterns: List[str],
                                 previous_context: Optional[Dict]) -> Dict:
        """Create a specific narrative response"""
        
        # Response length based on persona and week
        length_factor = self._calculate_response_length(persona_type, week, element)
        
        # Response content based on element and persona
        content = self._generate_response_content(persona_type, week, element, length_factor)
        
        # Response metadata
        metadata = {
            "response_length": length_factor,
            "detail_level": self._assess_detail_level(content),
            "emotional_content": self._detect_emotional_content(content),
            "clinical_relevance": self._assess_clinical_relevance(content, week),
            "trust_indicators": self._detect_trust_indicators(content),
            "follow_up_questions": self._generate_follow_up_questions(persona_type, content)
        }
        
        return {
            "content": content,
            "metadata": metadata
        }
    
    def _extract_clinical_data(self, persona_type: str, week: int, narrative_responses: Dict) -> Dict:
        """Extract clinical data from narrative responses"""
        
        clinical_data = {}
        week_template = self.clinical_data_templates[f"week_{week}"]
        
        for field in week_template["required_fields"]:
            clinical_data[field] = self._extract_field_data(
                field, narrative_responses, persona_type, week
            )
        
        return clinical_data
    
    def _get_emotional_state(self, persona_type: str, week: int) -> Dict:
        """Get emotional state for the week"""
        
        progression = self.emotional_progression[persona_type]
        
        if week <= 3:
            states = progression["weeks_1_3"]
        elif week <= 6:
            states = progression["weeks_4_6"]
        elif week <= 9:
            states = progression["weeks_7_9"]
        else:
            states = progression["week_10"]
        
        # Select appropriate state based on week position within phase
        if week <= 3:
            state_index = min(week - 1, len(states) - 1)
        elif week <= 6:
            state_index = min(week - 4, len(states) - 1)
        elif week <= 9:
            state_index = min(week - 7, len(states) - 1)
        else:
            state_index = 0
        
        primary_state = states[state_index]
        
        return {
            "primary_emotional_state": primary_state,
            "emotional_intensity": self._calculate_emotional_intensity(persona_type, week),
            "emotional_progression": self._assess_emotional_progression(persona_type, week),
            "anxiety_level": self._calculate_anxiety_level(persona_type, week),
            "trust_level": self._calculate_trust_level(persona_type, week),
            "engagement_comfort": self._calculate_engagement_comfort(persona_type, week)
        }
    
    def generate_10_week_journey(self, persona_type: str) -> Dict:
        """Generate a complete 10-week conversation journey"""
        
        journey = {
            "user_profile": {
                "persona_type": persona_type,
                "user_id": str(uuid.uuid4()),
                "journey_start": datetime.now().isoformat(),
                "persona_characteristics": STAGE_ZERO_PERSONAS[persona_type]
            },
            "weekly_conversations": [],
            "journey_analytics": {
                "overall_engagement": 0,
                "trust_progression": [],
                "clinical_data_completeness": 0,
                "narrative_richness": 0,
                "implementation_readiness": 0
            }
        }
        
        previous_context = None
        
        for week in range(1, 11):
            week_conversation = self.generate_weekly_conversation(
                persona_type, week, previous_context
            )
            
            journey["weekly_conversations"].append(week_conversation)
            
            # Update context for next week
            previous_context = {
                "previous_weeks": journey["weekly_conversations"],
                "trust_level": week_conversation["conversation_data"]["trust_indicators"]["overall_trust_score"],
                "engagement_trend": week_conversation["conversation_data"]["engagement_metrics"]["overall_engagement"]
            }
        
        # Calculate journey analytics
        journey["journey_analytics"] = self._calculate_journey_analytics(journey["weekly_conversations"])
        
        return journey
    
    def generate_cohort_dataset(self, cohort_size: int = 500) -> List[Dict]:
        """Generate a cohort of users with 10-week journeys"""
        
        # Persona distribution based on Stage Zero Health documentation
        persona_distribution = {
            "healthcare_professional_consumer_bridge": 0.15,  # 15%
            "structured_system_seeker": 0.25,                # 25%
            "health_aware_avoider": 0.30,                    # 30%
            "balanced_life_integrator": 0.20,                # 20%
            "overlooked_risk_group": 0.10                    # 10%
        }
        
        cohort = []
        
        for _ in range(cohort_size):
            # Select persona type based on distribution
            persona_type = random.choices(
                list(persona_distribution.keys()),
                weights=list(persona_distribution.values())
            )[0]
            
            # Generate journey
            journey = self.generate_10_week_journey(persona_type)
            
            cohort.append(journey)
        
        return cohort
    
    def save_cohort_dataset(self, cohort: List[Dict], filename: str = "stage_zero_cohort.json"):
        """Save the generated cohort to a JSON file"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / filename, "w") as f:
            json.dump(cohort, f, indent=2, default=str)
        
        print(f"Generated {len(cohort)} user journeys and saved to output/{filename}")
    
    # Helper methods for calculations and assessments
    def _calculate_response_length(self, persona_type: str, week: int, element: str) -> str:
        """Calculate appropriate response length"""
        # Implementation details...
        pass
    
    def _generate_response_content(self, persona_type: str, week: int, element: str, length_factor: str) -> str:
        """Generate actual response content"""
        # Implementation details...
        pass
    
    def _assess_detail_level(self, content: str) -> str:
        """Assess the detail level of response"""
        # Implementation details...
        pass
    
    def _detect_emotional_content(self, content: str) -> Dict:
        """Detect emotional content in response"""
        # Implementation details...
        pass
    
    def _assess_clinical_relevance(self, content: str, week: int) -> float:
        """Assess clinical relevance of response"""
        # Implementation details...
        pass
    
    def _detect_trust_indicators(self, content: str) -> Dict:
        """Detect trust indicators in response"""
        # Implementation details...
        pass
    
    def _generate_follow_up_questions(self, persona_type: str, content: str) -> List[str]:
        """Generate appropriate follow-up questions"""
        # Implementation details...
        pass
    
    def _extract_field_data(self, field: str, responses: Dict, persona_type: str, week: int) -> Any:
        """Extract specific clinical field data"""
        # Implementation details...
        pass
    
    def _calculate_emotional_intensity(self, persona_type: str, week: int) -> float:
        """Calculate emotional intensity"""
        # Implementation details...
        pass
    
    def _assess_emotional_progression(self, persona_type: str, week: int) -> Dict:
        """Assess emotional progression"""
        # Implementation details...
        pass
    
    def _calculate_anxiety_level(self, persona_type: str, week: int) -> float:
        """Calculate anxiety level"""
        # Implementation details...
        pass
    
    def _calculate_trust_level(self, persona_type: str, week: int) -> float:
        """Calculate trust level"""
        # Implementation details...
        pass
    
    def _calculate_engagement_comfort(self, persona_type: str, week: int) -> float:
        """Calculate engagement comfort"""
        # Implementation details...
        pass
    
    def _calculate_engagement_metrics(self, persona_type: str, week: int, responses: Dict) -> Dict:
        """Calculate engagement metrics"""
        # Implementation details...
        pass
    
    def _assess_trust_building(self, persona_type: str, week: int, responses: Dict, previous_context: Optional[Dict]) -> Dict:
        """Assess trust building indicators"""
        # Implementation details...
        pass
    
    def _determine_completion_status(self, persona_type: str, week: int) -> str:
        """Determine completion status for the week"""
        # Implementation details...
        pass
    
    def _calculate_time_investment(self, persona_type: str, week: int) -> Dict:
        """Calculate time investment for the week"""
        # Implementation details...
        pass
    
    def _generate_question_patterns(self, persona_type: str, week: int) -> List[str]:
        """Generate question patterns for the persona"""
        # Implementation details...
        pass
    
    def _assess_clinical_objectives(self, clinical_data: Dict, week: int) -> Dict:
        """Assess whether clinical objectives were met"""
        # Implementation details...
        pass
    
    def _assess_emotional_objectives(self, emotional_state: Dict, week: int) -> Dict:
        """Assess whether emotional objectives were met"""
        # Implementation details...
        pass
    
    def _assess_readiness(self, persona_type: str, week: int, engagement_metrics: Dict) -> float:
        """Assess readiness for next week"""
        # Implementation details...
        pass
    
    def _calculate_journey_analytics(self, weekly_conversations: List[Dict]) -> Dict:
        """Calculate overall journey analytics"""
        # Implementation details...
        pass

if __name__ == "__main__":
    generator = ConversationFlowGenerator()
    cohort = generator.generate_cohort_dataset(500)
    generator.save_cohort_dataset(cohort)
