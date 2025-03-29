import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

import faker
from faker.providers import person, address, job, company, date_time

from config.persona_config import (
    PERSONA_DISTRIBUTION,
    PERSONA_TEMPLATES,
    HEALTH_CONDITIONS,
    LIFE_EVENTS,
    LOCATION_TYPES,
    ENGAGEMENT_METRICS,
    BREAST_CANCER_RISKS,
    RACE_ETHNICITY_RISKS,
)

fake = faker.Faker()
fake.add_provider(person)
fake.add_provider(address)
fake.add_provider(job)
fake.add_provider(company)
fake.add_provider(date_time)


class CustomerDataGenerator:
    def __init__(self, total_customers: int = 500):
        self.total_customers = total_customers
        self.customers: List[Dict] = []

    def generate(self) -> List[Dict]:
        """Generate the complete synthetic customer dataset."""
        # Generate customers based on persona distribution
        for persona_type, percentage in PERSONA_DISTRIBUTION.items():
            num_customers = int(self.total_customers * percentage)
            for _ in range(num_customers):
                customer = self._generate_customer(persona_type)
                self.customers.append(customer)
        
        return self.customers

    def _generate_customer(self, persona_type: str) -> Dict:
        """Generate a single customer profile based on persona type."""
        template = PERSONA_TEMPLATES[persona_type]
        
        # Generate core profile
        core_profile = self._generate_core_profile(template)
        
        # Generate health profile
        health_profile = self._generate_health_profile(core_profile["age"], persona_type)
        
        # Generate life events
        life_events = self._generate_life_events(core_profile["age"], persona_type)
        
        # Generate engagement data
        engagement_data = self._generate_engagement_data(persona_type)
        
        # Generate narrative elements
        narrative_elements = self._generate_narrative_elements(persona_type, health_profile)
        
        # Generate SDoH context
        sdoh_context = self._generate_sdoh_context(core_profile["location"])
        
        return {
            "id": str(uuid.uuid4()),
            "personaType": persona_type,
            "coreProfile": core_profile,
            "healthProfile": health_profile,
            "lifeEvents": life_events,
            "engagementData": engagement_data,
            "narrativeElements": narrative_elements,
            "sdohContext": sdoh_context,
        }

    def _generate_core_profile(self, template: Dict) -> Dict:
        """Generate core demographic profile."""
        age = random.randint(template["age_range"][0], template["age_range"][1])
        
        # Select gender based on distribution
        gender = random.choices(
            list(template["gender_distribution"].keys()),
            weights=list(template["gender_distribution"].values())
        )[0]
        
        # Select education based on distribution
        education = random.choices(
            list(template["education_distribution"].keys()),
            weights=list(template["education_distribution"].values())
        )[0]
        
        # Generate location
        location_type = random.choice(list(LOCATION_TYPES.keys()))
        location = self._generate_location(location_type)
        
        # Select race/ethnicity based on risk distribution
        race_ethnicity = random.choices(
            list(RACE_ETHNICITY_RISKS.keys()),
            weights=list(RACE_ETHNICITY_RISKS.values())
        )[0]
        
        return {
            "name": fake.name(),
            "age": age,
            "gender": gender,
            "education": education,
            "occupation": fake.job(),
            "location": location,
            "maritalStatus": random.choice(["single", "married", "divorced", "in relationship"]),
            "raceEthnicity": race_ethnicity,
        }

    def _generate_health_profile(self, age: int, persona_type: str) -> Dict:
        """Generate health profile based on age and persona type."""
        template = PERSONA_TEMPLATES[persona_type]
        
        # Determine age group for health conditions
        age_group = self._get_age_group(age)
        
        # Generate health conditions based on age group probabilities
        conditions = []
        for condition, probability in HEALTH_CONDITIONS[age_group].items():
            if random.random() < probability:
                conditions.append(condition)
        
        # Generate prevention completion rate based on persona
        prevention_completion = random.uniform(
            template["prevention_completion"][0],
            template["prevention_completion"][1]
        )
        
        # Calculate breast cancer risk based on age group
        breast_cancer_risk = self._calculate_breast_cancer_risk(age, template)
        
        return {
            "height": random.randint(150, 190),
            "weight": random.randint(50, 100),
            "chronicConditions": conditions,
            "preventiveCare": {
                "screeningCompletion": prevention_completion,
                "lastScreening": self._generate_past_date(0, 2) if prevention_completion > 0.5 else None,
                "mammogramHistory": self._generate_mammogram_history(age, prevention_completion),
            },
            "anxietyLevel": random.uniform(
                template["anxiety_level"][0],
                template["anxiety_level"][1]
            ),
            "breastCancerRisk": breast_cancer_risk,
            "riskFactors": template["risk_factors"],
        }

    def _calculate_breast_cancer_risk(self, age: int, template: Dict) -> Dict:
        """Calculate breast cancer risk based on age and persona characteristics."""
        # Get base risk from age group
        age_group = self._get_age_group(age)
        base_risk = BREAST_CANCER_RISKS[age_group]["diagnosis"]
        
        # Adjust risk based on persona type and characteristics
        risk_multiplier = 1.0
        
        # Adjust based on prevention completion
        prevention_completion = random.uniform(
            template["prevention_completion"][0],
            template["prevention_completion"][1]
        )
        if prevention_completion < 0.3:
            risk_multiplier *= 1.2  # 20% higher risk for low prevention completion
        
        # Adjust based on risk factors
        risk_factors = template["risk_factors"]
        if "family_history" in risk_factors:
            risk_multiplier *= 1.5  # 50% higher risk with family history
        if "genetic_factors" in risk_factors:
            risk_multiplier *= 1.3  # 30% higher risk with genetic factors
        
        # Calculate final risk
        final_risk = min(base_risk * risk_multiplier, 0.5)  # Cap at 50%
        
        return {
            "baseRisk": base_risk,
            "adjustedRisk": final_risk,
            "riskFactors": risk_factors,
            "riskLevel": self._get_risk_level(final_risk),
        }

    def _get_risk_level(self, risk: float) -> str:
        """Convert numerical risk to risk level category."""
        if risk < 0.02:
            return "low"
        elif risk < 0.05:
            return "moderate"
        elif risk < 0.15:
            return "high"
        else:
            return "very_high"

    def _generate_mammogram_history(self, age: int, prevention_completion: float) -> Dict:
        """Generate mammogram history based on age and prevention completion."""
        if prevention_completion < 0.3:
            return {
                "hasHistory": False,
                "lastMammogram": None,
                "frequency": "never",
            }
        
        # Generate history based on age and prevention completion
        has_history = random.random() < prevention_completion
        if not has_history:
            return {
                "hasHistory": False,
                "lastMammogram": None,
                "frequency": "never",
            }
        
        # Generate frequency based on prevention completion
        if prevention_completion > 0.8:
            frequency = "annual"
            max_years = 5
        elif prevention_completion > 0.5:
            frequency = "biennial"
            max_years = 3
        else:
            frequency = "irregular"
            max_years = 2
        
        # Generate last mammogram date
        last_date = self._generate_past_date(0, max_years)
        
        return {
            "hasHistory": True,
            "lastMammogram": last_date,
            "frequency": frequency,
        }

    def _generate_life_events(self, age: int, persona_type: str) -> Dict:
        """Generate life events based on age and persona type."""
        events = []
        birth_year = datetime.now().year - age
        
        # Generate past events based on age
        for event_type, subtypes in LIFE_EVENTS.items():
            for subtype, characteristics in subtypes.items():
                if random.random() < self._get_event_probability(characteristics["frequency"]):
                    event = {
                        "id": str(uuid.uuid4()),
                        "type": event_type,
                        "subCategory": subtype,
                        "timestamp": self._generate_past_date(0, age),
                        "title": self._generate_event_title(event_type, subtype),
                        "impact": {
                            "riskImpact": self._get_impact_level(characteristics["impact"]),
                            "preventionOpportunity": random.choice(["high", "medium", "low"]),
                            "supportNeeds": self._generate_support_needs(event_type, subtype),
                        },
                        "status": "completed",
                    }
                    events.append(event)
        
        # Generate anticipated events
        anticipated_events = self._generate_anticipated_events(age, persona_type)
        
        return {
            "lifeEvents": sorted(events, key=lambda x: x["timestamp"]),
            "anticipatedEvents": anticipated_events,
        }

    def _generate_engagement_data(self, persona_type: str) -> Dict:
        """Generate engagement data based on persona type."""
        template = PERSONA_TEMPLATES[persona_type]
        engagement_pattern = random.choice(template["engagement_pattern"])
        
        # Map persona engagement patterns to visit frequency patterns
        pattern_mapping = {
            "sporadic": "sporadic",
            "infrequent": "infrequent",
            "rare": "sporadic",
            "regular": "regular",
            "consistent": "consistent",
            "occasional": "infrequent",
            "planned": "regular",
            "professional": "consistent",
            "analytical": "consistent",
            "reactive": "sporadic"
        }
        
        visit_frequency = pattern_mapping.get(engagement_pattern, "regular")
        
        # Get visit frequency metrics
        visit_metrics = ENGAGEMENT_METRICS["visit_frequency"][visit_frequency]
        
        # Generate visit history
        visits = []
        num_visits = random.randint(visit_metrics["min_visits"], visit_metrics["max_visits"])
        
        for _ in range(num_visits):
            visit = {
                "timestamp": self._generate_past_date(0, 365),
                "duration": random.randint(*random.choice(list(ENGAGEMENT_METRICS["session_duration"].values()))),
                "features": random.choice(list(ENGAGEMENT_METRICS["feature_usage"].values())),
            }
            visits.append(visit)
        
        return {
            "platformEngagement": {
                "visitFrequency": visit_frequency,
                "sessionDuration": {
                    "average": sum(v["duration"] for v in visits) / len(visits) if visits else 0,
                    "pattern": engagement_pattern,
                },
                "visitHistory": sorted(visits, key=lambda x: x["timestamp"]),
            }
        }

    def _generate_narrative_elements(self, persona_type: str, health_profile: Dict) -> Dict:
        """Generate narrative elements based on persona type and health profile."""
        template = PERSONA_TEMPLATES[persona_type]
        
        # Generate health narrative based on persona characteristics
        health_awareness = random.uniform(
            template["health_awareness"][0],
            template["health_awareness"][1]
        )
        
        action_tendency = random.uniform(
            template["action_tendency"][0],
            template["action_tendency"][1]
        )
        
        return {
            "healthNarrative": {
                "selfDescription": self._generate_self_description(
                    persona_type, health_awareness, action_tendency
                ),
                "relationshipToHealthcare": self._generate_healthcare_relationship(
                    persona_type, health_profile
                ),
            }
        }

    def _generate_sdoh_context(self, location: Dict) -> Dict:
        """Generate social determinants of health context."""
        location_type = location["type"]
        location_characteristics = LOCATION_TYPES[location_type]
        
        return {
            "areaLevel": {
                "currentLocation": {
                    "censusTract": fake.numerify("########"),
                    "indices": {
                        "adi": random.randint(20, 80),  # Area Deprivation Index
                    },
                },
                "characteristics": location_characteristics,
            },
            "individualLevel": {
                "financialStability": {
                    "incomeCategory": random.choice(["low", "middle", "high"]),
                    "insuranceStatus": random.choice(["insured", "uninsured", "underinsured"]),
                },
                "socialSupport": {
                    "networkSize": random.randint(1, 10),
                    "supportLevel": random.choice(["low", "medium", "high"]),
                },
            },
        }

    def _generate_location(self, location_type: str) -> Dict:
        """Generate location data based on type."""
        if location_type == "urban":
            city = fake.city()
            state = fake.state_abbr()
            zip_code = fake.zipcode()
        elif location_type == "suburban":
            city = fake.city()
            state = fake.state_abbr()
            zip_code = fake.zipcode()
        else:  # rural
            city = fake.city()
            state = fake.state_abbr()
            zip_code = fake.zipcode()
        
        return {
            "city": city,
            "state": state,
            "zipCode": zip_code,
            "type": location_type,
        }

    def _get_age_group(self, age: int) -> str:
        """Determine age group for health conditions."""
        if age < 30:
            return "20-29"
        elif age < 40:
            return "30-39"
        elif age < 50:
            return "40-49"
        elif age < 60:
            return "50-59"
        elif age < 70:
            return "60-69"
        elif age < 80:
            return "70-79"
        else:
            return "80+"

    def _generate_past_date(self, min_years: int, max_years: int) -> str:
        """Generate a random date in the past."""
        days = random.randint(min_years * 365, max_years * 365)
        return (datetime.now() - timedelta(days=days)).isoformat()

    def _get_event_probability(self, frequency: str) -> float:
        """Get probability for event generation based on frequency."""
        probabilities = {
            "rare": 0.1,
            "regular": 0.3,
            "frequent": 0.5,
        }
        return probabilities.get(frequency, 0.2)

    def _get_impact_level(self, impact: str) -> str:
        """Convert impact string to standardized format."""
        return f"{impact}_increase" if impact != "low" else "neutral"

    def _generate_support_needs(self, event_type: str, subtype: str) -> List[str]:
        """Generate support needs based on event type and subtype."""
        support_needs = []
        if event_type == "health":
            support_needs.extend(["medical_guidance", "emotional_support"])
        elif event_type == "career":
            support_needs.extend(["professional_development", "work_life_balance"])
        elif event_type == "family":
            support_needs.extend(["family_support", "counseling"])
        
        return random.sample(support_needs, random.randint(1, len(support_needs)))

    def _generate_event_title(self, event_type: str, subtype: str) -> str:
        """Generate a title for a life event."""
        if event_type == "health":
            return f"{subtype.title()} Event"
        elif event_type == "career":
            return f"Career {subtype.title()}"
        else:
            return f"Family {subtype.title()}"

    def _generate_anticipated_events(self, age: int, persona_type: str) -> List[Dict]:
        """Generate anticipated future events."""
        events = []
        template = PERSONA_TEMPLATES[persona_type]
        
        # Generate 1-3 anticipated events
        num_events = random.randint(1, 3)
        
        for _ in range(num_events):
            event_type = random.choice(list(LIFE_EVENTS.keys()))
            subtype = random.choice(list(LIFE_EVENTS[event_type].keys()))
            
            event = {
                "id": str(uuid.uuid4()),
                "type": event_type,
                "subCategory": subtype,
                "timestamp": self._generate_future_date(1, 12),
                "title": self._generate_event_title(event_type, subtype),
                "impact": {
                    "riskImpact": "neutral",
                    "preventionOpportunity": random.choice(["high", "medium", "low"]),
                    "supportNeeds": self._generate_support_needs(event_type, subtype),
                },
                "status": "planned",
            }
            events.append(event)
        
        return events

    def _generate_future_date(self, min_months: int, max_months: int) -> str:
        """Generate a random date in the future."""
        days = random.randint(min_months * 30, max_months * 30)
        return (datetime.now() + timedelta(days=days)).isoformat()

    def _generate_self_description(self, persona_type: str, health_awareness: float, action_tendency: float) -> str:
        """Generate self-description based on persona characteristics."""
        if persona_type == "health_aware_avoider":
            return "I'm aware of health issues but often struggle to take action."
        elif persona_type == "structured_system_seeker":
            return "I prefer organized approaches to health management."
        elif persona_type == "balanced_life_integrator":
            return "I try to maintain a balanced approach to health and wellness."
        elif persona_type == "healthcare_professional":
            return "I have professional expertise in healthcare and take a systematic approach."
        else:  # overlooked_risk_group
            return "I have some health concerns but often prioritize other aspects of life."

    def _generate_healthcare_relationship(self, persona_type: str, health_profile: Dict) -> str:
        """Generate description of relationship with healthcare system."""
        if persona_type == "health_aware_avoider":
            return "I have a complex relationship with healthcare, often feeling anxious about appointments."
        elif persona_type == "structured_system_seeker":
            return "I maintain a regular schedule of preventive care and follow-ups."
        elif persona_type == "balanced_life_integrator":
            return "I engage with healthcare when needed while maintaining work-life balance."
        elif persona_type == "healthcare_professional":
            return "I have a professional understanding of healthcare systems and processes."
        else:  # overlooked_risk_group
            return "I tend to seek healthcare only when necessary." 