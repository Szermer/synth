import json
import pytest
from pathlib import Path
from typing import Dict, List, Any

from src.data_generation.conversation_generator import ConversationFlowGenerator
from src.config.stage_zero_personas import STAGE_ZERO_PERSONAS

class TestStageZeroConversationGeneration:
    """Test suite for Stage Zero Health conversation generation"""
    
    def setup_method(self):
        """Setup test environment"""
        self.generator = ConversationFlowGenerator()
        self.test_personas = list(STAGE_ZERO_PERSONAS.keys())
    
    def test_persona_distribution_accuracy(self):
        """Test that generated cohort matches expected persona distribution"""
        cohort = self.generator.generate_cohort_dataset(1000)
        
        # Count personas
        persona_counts = {}
        for journey in cohort:
            persona = journey["user_profile"]["persona_type"]
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
        
        # Expected distribution (allowing 5% variance)
        expected = {
            "healthcare_professional_consumer_bridge": (0.10, 0.20),  # 15% ±5%
            "structured_system_seeker": (0.20, 0.30),                # 25% ±5%
            "health_aware_avoider": (0.25, 0.35),                    # 30% ±5%
            "balanced_life_integrator": (0.15, 0.25),                # 20% ±5%
            "overlooked_risk_group": (0.05, 0.15)                    # 10% ±5%
        }
        
        for persona, (min_pct, max_pct) in expected.items():
            actual_pct = persona_counts[persona] / 1000
            assert min_pct <= actual_pct <= max_pct, f"{persona}: {actual_pct} not in [{min_pct}, {max_pct}]"
    
    def test_10_week_journey_completeness(self):
        """Test that 10-week journeys are complete and properly structured"""
        for persona in self.test_personas:
            journey = self.generator.generate_10_week_journey(persona)
            
            # Check journey structure
            assert "user_profile" in journey
            assert "weekly_conversations" in journey
            assert "journey_analytics" in journey
            
            # Check all 10 weeks are present
            assert len(journey["weekly_conversations"]) == 10
            
            # Check week sequence
            for i, week_data in enumerate(journey["weekly_conversations"]):
                assert week_data["week"] == i + 1
                assert week_data["persona_type"] == persona
    
    def test_clinical_data_extraction_by_week(self):
        """Test that appropriate clinical data is extracted each week"""
        
        expected_clinical_data = {
            1: ["age", "ethnicity", "primary_motivation"],
            2: ["family_cancer_history", "maternal_history", "paternal_history"],
            3: ["age_at_menarche", "pregnancy_history", "hormone_use"],
            4: ["healthcare_relationships", "screening_history"],
            5: ["lifestyle_factors", "work_environment"],
            6: ["extended_family_history", "ethnic_background"],
            7: ["current_symptoms", "body_awareness"],
            8: ["support_systems", "financial_resources"],
            9: ["health_values", "detection_preferences"],
            10: ["plan_integration", "implementation_readiness"]
        }
        
        journey = self.generator.generate_10_week_journey("structured_system_seeker")
        
        for week, expected_fields in expected_clinical_data.items():
            week_data = journey["weekly_conversations"][week - 1]
            clinical_data = week_data["conversation_data"]["clinical_data_captured"]
            
            for field in expected_fields:
                assert field in clinical_data, f"Week {week} missing {field}"
    
    def test_narrative_response_quality_by_persona(self):
        """Test that narrative responses match persona characteristics"""
        
        persona_expectations = {
            "healthcare_professional_consumer_bridge": {
                "analytical_markers": ["evidence", "research", "clinical"],
                "professional_references": True,
                "detail_level": "high"
            },
            "structured_system_seeker": {
                "organization_markers": ["timeline", "plan", "system"],
                "systematic_approach": True,
                "detail_level": "comprehensive"
            },
            "health_aware_avoider": {
                "uncertainty_markers": ["maybe", "not sure", "think"],
                "gradual_disclosure": True,
                "detail_level": "variable"
            },
            "balanced_life_integrator": {
                "holistic_markers": ["balance", "integrate", "wellness"],
                "life_context": True,
                "detail_level": "contextual"
            },
            "overlooked_risk_group": {
                "learning_markers": ["understand", "learn", "explain"],
                "validation_seeking": True,
                "detail_level": "educational"
            }
        }
        
        for persona, expectations in persona_expectations.items():
            journey = self.generator.generate_10_week_journey(persona)
            
            # Analyze narrative responses across all weeks
            all_responses = []
            for week_data in journey["weekly_conversations"]:
                responses = week_data["conversation_data"]["narrative_responses"]
                all_responses.extend([r["content"] for r in responses.values()])
            
            # Test persona-specific patterns
            self._validate_persona_patterns(all_responses, expectations, persona)
    
    def test_emotional_progression_consistency(self):
        """Test that emotional progression is consistent and realistic"""
        
        for persona in self.test_personas:
            journey = self.generator.generate_10_week_journey(persona)
            
            # Extract emotional states across weeks
            emotional_progression = []
            trust_progression = []
            
            for week_data in journey["weekly_conversations"]:
                emotional_data = week_data["conversation_data"]["emotional_progression"]
                emotional_progression.append(emotional_data["primary_emotional_state"])
                trust_progression.append(emotional_data["trust_level"])
            
            # Test trust generally increases over time (allowing for some variance)
            self._validate_trust_progression(trust_progression, persona)
            
            # Test emotional states are appropriate for persona
            self._validate_emotional_states(emotional_progression, persona)
    
    def test_clinical_model_integration(self):
        """Test that clinical risk models can be properly populated"""
        
        # Test with personas likely to provide complete data
        for persona in ["healthcare_professional_consumer_bridge", "structured_system_seeker"]:
            journey = self.generator.generate_10_week_journey(persona)
            
            # Extract all clinical data
            all_clinical_data = {}
            for week_data in journey["weekly_conversations"]:
                clinical_data = week_data["conversation_data"]["clinical_data_captured"]
                all_clinical_data.update(clinical_data)
            
            # Test GAIL model requirements
            gail_requirements = ["age", "ethnicity", "family_cancer_history", "age_at_menarche", "pregnancy_history"]
            for req in gail_requirements:
                assert req in all_clinical_data, f"GAIL requirement {req} not captured for {persona}"
            
            # Test Tyrer-Cuzick requirements
            tc_requirements = ["hormone_use", "family_cancer_history", "reproductive_history"]
            for req in tc_requirements:
                assert any(req in key for key in all_clinical_data.keys()), f"Tyrer-Cuzick requirement {req} not captured for {persona}"
    
    def test_trust_building_milestones(self):
        """Test that trust building follows expected patterns"""
        
        expected_milestones = {
            3: "basic_comfort_established",
            5: "personal_sharing_increased", 
            7: "emotional_openness_present",
            10: "implementation_confidence"
        }
        
        for persona in self.test_personas:
            journey = self.generator.generate_10_week_journey(persona)
            
            for milestone_week, expected_milestone in expected_milestones.items():
                week_data = journey["weekly_conversations"][milestone_week - 1]
                trust_indicators = week_data["conversation_data"]["trust_indicators"]
                
                # Test that trust indicators show appropriate progression
                assert trust_indicators["overall_trust_score"] > 0.3, f"Week {milestone_week} trust too low for {persona}"
                
                if milestone_week == 10:
                    # Final week should show high implementation readiness
                    readiness = week_data["week_outcomes"]["readiness_for_next_week"]
                    assert readiness > 0.6, f"Implementation readiness too low for {persona}"
    
    def test_conversation_time_investment_realism(self):
        """Test that conversation time investments are realistic"""
        
        for persona in self.test_personas:
            journey = self.generator.generate_10_week_journey(persona)
            
            total_time = 0
            for week_data in journey["weekly_conversations"]:
                time_investment = week_data["conversation_data"]["time_investment"]
                week_time = time_investment.get("total_minutes", 0)
                
                # Each week should take 10-25 minutes (realistic for busy users)
                assert 8 <= week_time <= 30, f"Week time {week_time} unrealistic for {persona}"
                total_time += week_time
            
            # Total program should be 2-4 hours over 10 weeks
            assert 100 <= total_time <= 300, f"Total time {total_time} unrealistic for {persona}"
    
    def test_engagement_pattern_differentiation(self):
        """Test that different personas show different engagement patterns"""
        
        persona_journeys = {}
        for persona in self.test_personas:
            persona_journeys[persona] = self.generator.generate_10_week_journey(persona)
        
        # Compare engagement patterns between personas
        for metric in ["response_length", "detail_depth", "question_frequency"]:
            persona_metrics = {}
            
            for persona, journey in persona_journeys.items():
                metrics = []
                for week_data in journey["weekly_conversations"]:
                    engagement = week_data["conversation_data"]["engagement_metrics"]
                    metrics.append(engagement.get(metric, 0))
                persona_metrics[persona] = sum(metrics) / len(metrics)
            
            # Verify personas show different patterns
            metric_values = list(persona_metrics.values())
            assert max(metric_values) - min(metric_values) > 0.1, f"Personas not differentiated on {metric}"
    
    def test_weekly_dashboard_data_completeness(self):
        """Test that weekly dashboard data is complete and valid"""
        
        for persona in self.test_personas:
            journey = self.generator.generate_10_week_journey(persona)
            
            for week_data in journey["weekly_conversations"]:
                week = week_data["week"]
                
                # Test required dashboard components
                required_components = [
                    "narrative_responses",
                    "clinical_data_captured", 
                    "emotional_progression",
                    "engagement_metrics",
                    "trust_indicators"
                ]
                
                conversation_data = week_data["conversation_data"]
                for component in required_components:
                    assert component in conversation_data, f"Week {week} missing {component} for {persona}"
                
                # Test week outcomes
                outcomes = week_data["week_outcomes"]
                required_outcomes = [
                    "clinical_objectives_met",
                    "emotional_objectives_met", 
                    "trust_building_progress",
                    "readiness_for_next_week"
                ]
                
                for outcome in required_outcomes:
                    assert outcome in outcomes, f"Week {week} missing {outcome} for {persona}"
    
    # Helper methods for validation
    def _validate_persona_patterns(self, responses: List[str], expectations: Dict, persona: str):
        """Validate that responses match persona patterns"""
        combined_text = " ".join(responses).lower()
        
        if "analytical_markers" in expectations:
            markers_found = sum(1 for marker in expectations["analytical_markers"] if marker in combined_text)
            assert markers_found > 0, f"No analytical markers found for {persona}"
        
        if "uncertainty_markers" in expectations:
            markers_found = sum(1 for marker in expectations["uncertainty_markers"] if marker in combined_text)
            if persona == "health_aware_avoider":
                assert markers_found > 0, f"No uncertainty markers found for {persona}"
    
    def _validate_trust_progression(self, trust_progression: List[float], persona: str):
        """Validate that trust generally increases over time"""
        # Allow for some fluctuation but overall trend should be upward
        early_avg = sum(trust_progression[:3]) / 3
        late_avg = sum(trust_progression[-3:]) / 3
        
        assert late_avg > early_avg, f"Trust did not increase over time for {persona}"
        assert trust_progression[-1] > 0.5, f"Final trust level too low for {persona}"
    
    def _validate_emotional_states(self, emotional_states: List[str], persona: str):
        """Validate that emotional states are appropriate for persona"""
        # Each persona should show progression toward more positive states
        positive_states = ["engaged", "motivated", "determined", "stable", "confident"]
        
        final_states = emotional_states[-3:]  # Last 3 weeks
        positive_count = sum(1 for state in final_states if any(pos in state for pos in positive_states))
        
        assert positive_count >= 1, f"Not enough positive emotional states for {persona} in final weeks"

class TestNarrativeDataQuality:
    """Test narrative data quality and realism"""
    
    def test_response_length_distribution(self):
        """Test that response lengths follow realistic distributions"""
        generator = ConversationFlowGenerator()
        
        response_lengths = []
        for persona in STAGE_ZERO_PERSONAS.keys():
            journey = generator.generate_10_week_journey(persona)
            
            for week_data in journey["weekly_conversations"]:
                for response_data in week_data["conversation_data"]["narrative_responses"].values():
                    length = len(response_data["content"].split())
                    response_lengths.append(length)
        
        # Test realistic response length distribution
        avg_length = sum(response_lengths) / len(response_lengths)
        assert 20 <= avg_length <= 150, f"Average response length {avg_length} unrealistic"
        
        # Test range of responses
        min_length = min(response_lengths)
        max_length = max(response_lengths)
        assert min_length >= 5, "Some responses too short"
        assert max_length <= 500, "Some responses too long"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
