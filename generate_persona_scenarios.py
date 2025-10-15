#!/usr/bin/env python3
"""
Generate detailed persona-specific scenarios for Private Language

Creates realistic user stories showing how different personas experience
their first knowledge capture session.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import random


class PersonaScenarioGenerator:
    """Generate realistic user scenarios by persona"""

    def __init__(self, data_file: str):
        with open(data_file, 'r') as f:
            self.users = json.load(f)

    def generate_scenarios(self):
        """Generate persona-specific first capture scenarios"""

        print("\n" + "="*80)
        print("📖 FIRST CAPTURE SESSION: PERSONA SCENARIOS")
        print("="*80)
        print("\nRealistic user stories showing how different personas experience")
        print("their first knowledge capture session with Private Language.\n")

        personas_to_showcase = [
            'studio_practitioner',
            'master_craftsperson',
            'educator_instructor',
            'student_apprentice'
        ]

        for persona_type in personas_to_showcase:
            # Find a representative user
            persona_users = [
                u for u in self.users
                if u['persona_type'] == persona_type and u['journey']['steps']
            ]

            if not persona_users:
                continue

            user = random.choice(persona_users)
            self._print_persona_scenario(user)

        self._print_usage_recommendations()

    def _print_persona_scenario(self, user: Dict[str, Any]):
        """Print a detailed scenario for a persona"""

        persona_type = user['persona_type']
        journey = user['journey']
        first_steps = journey['steps'][:3] if journey['steps'] else []

        # Persona mapping
        persona_info = {
            'studio_practitioner': {
                'name': 'Sarah',
                'title': 'Studio Practitioner',
                'craft': 'Ceramicist',
                'age': user['age'],
                'experience': user.get('attributes', {}).get('craft_experience_years', 15)
            },
            'master_craftsperson': {
                'name': 'Elena',
                'title': 'Master Craftsperson',
                'craft': 'Luthier',
                'age': user['age'],
                'experience': user.get('attributes', {}).get('craft_experience_years', 42)
            },
            'educator_instructor': {
                'name': 'Marcus',
                'title': 'Educator/Instructor',
                'craft': 'Woodworking Professor',
                'age': user['age'],
                'experience': user.get('attributes', {}).get('teaching_experience_years', 25)
            },
            'student_apprentice': {
                'name': 'Jordan',
                'title': 'Student/Apprentice',
                'craft': 'Ceramics Student',
                'age': user['age'],
                'experience': user.get('attributes', {}).get('craft_experience_years', 2)
            }
        }

        info = persona_info.get(persona_type, {
            'name': 'User',
            'title': persona_type.replace('_', ' ').title(),
            'craft': 'Craftsperson',
            'age': user['age'],
            'experience': 10
        })

        print("\n" + "─"*80)
        print(f"👤 {info['name']} - {info['title']}")
        print("─"*80)
        print(f"   {info['craft']}, {info['age']} years old")
        print(f"   {info['experience']} years experience")
        print(f"   Engagement Level: {user['engagement_level']:.0%}")
        print()

        # Discovery phase
        print("📍 DISCOVERY")
        print(f"   • Heard about Private Language from {'a colleague' if persona_type in ['educator_instructor', 'master_craftsperson'] else 'Instagram'}")
        print(f"   • Primary pain point: {self._get_pain_point(persona_type)}")
        print(f"   • Initial emotional state: {first_steps[0]['emotional_state'] if first_steps else 'curious'}")
        print()

        # First capture session
        if first_steps:
            total_time = sum(s.get('time_invested', 0) for s in first_steps)

            print("🎙️  FIRST CAPTURE SESSION")
            print(f"   • Duration: {total_time} minutes")
            print(f"   • Capture method: {self._get_capture_method(persona_type)}")
            print()

            # Step-by-step narrative
            for i, step in enumerate(first_steps, 1):
                print(f"   Step {i}: {self._get_step_narrative(step, persona_type, i)}")
                print(f"           Emotional: {step['emotional_state']}")
                print(f"           Time: {step.get('time_invested', 0)} min")
                print(f"           Status: {step['completion_status']}")
                print()

        # Outcome
        completion = sum(1 for s in first_steps if s['completion_status'] == 'completed') / len(first_steps) if first_steps else 0

        print("📊 SESSION OUTCOME")
        print(f"   • Completion Rate: {completion:.0%}")
        print(f"   • Next Step: {self._get_next_step(persona_type, completion)}")
        print()

        # Key insight
        print("💡 KEY INSIGHT")
        print(f"   {self._get_insight(persona_type, completion)}")
        print()

    def _get_pain_point(self, persona: str) -> str:
        """Get primary pain point by persona"""
        pain_points = {
            'studio_practitioner': "Knowledge lives in my head - can't explain my glaze techniques",
            'master_craftsperson': "Need to preserve 40 years of expertise before retirement",
            'educator_instructor': "Students keep making the same mistakes every semester",
            'student_apprentice': "Can't access my instructor's knowledge at midnight"
        }
        return pain_points.get(persona, "Documentation takes too much time")

    def _get_capture_method(self, persona: str) -> str:
        """Get likely capture method by persona"""
        methods = {
            'studio_practitioner': "Voice memo while working (Omi pendant)",
            'master_craftsperson': "Recorded workshop session (Shadow)",
            'educator_instructor': "Lecture recording + annotations",
            'student_apprentice': "Smartphone voice notes"
        }
        return methods.get(persona, "Voice recording")

    def _get_step_narrative(self, step: Dict, persona: str, step_num: int) -> str:
        """Generate narrative for a step"""
        narratives = {
            1: {
                'studio_practitioner': "Talks through reduction firing process",
                'master_craftsperson': "Demonstrates wood selection for violin",
                'educator_instructor': "Explains joinery fundamentals",
                'student_apprentice': "Describes first centering attempt"
            },
            2: {
                'studio_practitioner': "Reviews glaze mixing ratios",
                'master_craftsperson': "Discusses arching technique",
                'educator_instructor': "Shares common student mistakes",
                'student_apprentice': "Questions about wedging technique"
            },
            3: {
                'studio_practitioner': "Notes kiln temperature curves",
                'master_craftsperson': "Explains wood grain reading",
                'educator_instructor': "Outlines semester progression",
                'student_apprentice': "Captures instructor feedback"
            }
        }
        return narratives.get(step_num, {}).get(persona, f"Captures knowledge (step {step_num})")

    def _get_next_step(self, persona: str, completion: float) -> str:
        """Determine next step based on completion"""
        if completion > 0.8:
            return "✅ Received weekly synthesis report → Exploring gap detection"
        elif completion > 0.5:
            return "⏸️  Paused session → Will resume tomorrow"
        else:
            return "❌ Dropped off → Needs re-engagement email"

    def _get_insight(self, persona: str, completion: float) -> str:
        """Generate persona-specific insight"""
        if completion > 0.8:
            insights = {
                'studio_practitioner': "Sarah was surprised to see gaps in her firing process explanation - never realized she skipped the humidity step when teaching",
                'master_craftsperson': "Elena felt relief seeing her tacit knowledge captured - 'This is exactly what I needed to preserve'",
                'educator_instructor': "Marcus immediately saw how this could reduce office hours - 'Students can search this instead of asking me'",
                'student_apprentice': "Jordan loved having searchable access to technique explanations - 'Better than my messy notebook'"
            }
        else:
            insights = {
                'studio_practitioner': "Sarah felt overwhelmed by the interface - needs simpler onboarding with just voice capture",
                'master_craftsperson': "Elena struggled with tech complexity - would benefit from white-glove onboarding",
                'educator_instructor': "Marcus wanted to see ROI before investing time - needs success metrics upfront",
                'student_apprentice': "Jordan got distracted - mobile-first experience would help"
            }

        return insights.get(persona, f"Completion rate {completion:.0%} indicates {['needs support', 'good fit'][int(completion > 0.7)]}")

    def _print_usage_recommendations(self):
        """Print how to use these scenarios"""

        print("\n" + "="*80)
        print("🎯 HOW TO USE THESE SCENARIOS")
        print("="*80)
        print()
        print("1️⃣  PRODUCT DEVELOPMENT")
        print("   • Use Sarah's scenario to test onboarding for anxious users")
        print("   • Use Elena's scenario to design white-glove enterprise onboarding")
        print("   • Test gap detection surprise factor with all personas")
        print()
        print("2️⃣  UX DESIGN")
        print("   • Map emotional states to UI feedback mechanisms")
        print("   • Design different paths for high-engagement vs cautious users")
        print("   • Create resumable sessions for Studio Practitioners")
        print()
        print("3️⃣  MARKETING COPY")
        print("   • Turn these into case study narratives")
        print("   • Use persona-specific pain points in landing pages")
        print("   • Create testimonials matching emotional progression")
        print()
        print("4️⃣  SALES ENABLEMENT")
        print("   • Marcus's scenario = academic sales pitch")
        print("   • Elena's scenario = legacy preservation service")
        print("   • Show realistic time investment (15min sessions)")
        print()
        print("="*80)
        print()


def main():
    data_file = "output/private_language_synthetic_users.json"

    if not Path(data_file).exists():
        print(f"❌ Data file not found: {data_file}")
        return

    generator = PersonaScenarioGenerator(data_file)
    generator.generate_scenarios()


if __name__ == "__main__":
    main()
