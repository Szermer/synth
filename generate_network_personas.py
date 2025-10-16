#!/usr/bin/env python3
"""
Generate Network Effect Personas (Students, Teaching Assistants, Knowledge Consumers)

This script generates:
- 3 student_apprentice personas (linked to master_educators)
- 2 teaching_assistant personas (linked to master_educators)
- 2 knowledge_consumer personas (marketplace users)

Plus: Enhanced journeys with weekly synthesis and export events for ALL users.
"""

import json
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
from core.generators.journey_generator import JourneyGenerator
from core.models.journey import JourneyType
from core.models.persona import Persona
from core.utils.config_loader import ConfigLoader


def load_existing_users():
    """Load existing user cohort"""
    users_file = Path("output/private_language_synthetic_users_llm.json")
    with open(users_file) as f:
        return json.load(f)


def select_master_educators(users, count=2):
    """Select master educators to link TAs and students to"""
    educators = [u for u in users if u['persona_type'] == 'master_educator']

    # Prioritize educators with high engagement and teaching load
    scored_educators = []
    for edu in educators:
        attrs = edu.get('attributes', {})
        score = (
            edu.get('engagement_level', 0.5) * 0.4 +
            (attrs.get('students_per_year', 100) / 500) * 0.3 +  # Normalize
            (attrs.get('teaching_experience_years', 15) / 30) * 0.3
        )
        scored_educators.append((score, edu))

    scored_educators.sort(key=lambda x: x[0], reverse=True)
    return [edu for _, edu in scored_educators[:count]]


def generate_student_persona(instructor, student_num, config_loader):
    """Generate a student linked to an instructor"""

    # Load persona config (use PersonaConfig object)
    personas_config = config_loader.load_personas()
    student_config = personas_config['student_apprentice']

    # Generate demographics (access PersonaConfig properties directly)
    age = random.randint(student_config.age_range[0], student_config.age_range[1])

    gender_dist = student_config.gender_distribution
    gender = random.choices(list(gender_dist.keys()),
                           weights=list(gender_dist.values()))[0]

    edu_dist = student_config.education_distribution
    education = random.choices(list(edu_dist.keys()),
                              weights=list(edu_dist.values()))[0]

    # Generate behavioral traits
    engagement_level = random.uniform(
        student_config.action_tendency[0],
        student_config.action_tendency[1]
    )
    action_tendency = random.uniform(
        student_config.action_tendency[0],
        student_config.action_tendency[1]
    )
    anxiety_level = random.uniform(
        student_config.anxiety_level[0],
        student_config.anxiety_level[1]
    )

    # Generate attributes (access from PersonaConfig.attributes dict)
    attrs = student_config.attributes
    learning_stage_dist = attrs['learning_stage_distribution']
    learning_stage = random.choices(list(learning_stage_dist.keys()),
                                   weights=list(learning_stage_dist.values()))[0]

    # Tech comfort - check if it's a range or fixed
    tech_comfort_range = attrs.get('tech_comfort', [0.7, 0.95])
    if isinstance(tech_comfort_range, list):
        tech_comfort = random.uniform(tech_comfort_range[0], tech_comfort_range[1])
    else:
        tech_comfort = tech_comfort_range

    search_usage = random.choice(attrs['search_usage'])
    self_service_success = random.uniform(attrs['self_service_success_rate'][0],
                                          attrs['self_service_success_rate'][1])
    office_hours_reduction = random.uniform(attrs['office_hours_reduction'][0],
                                           attrs['office_hours_reduction'][1])

    question_frequency = random.randint(attrs['question_frequency'][0],
                                       attrs['question_frequency'][1])

    preferred_learning_mode = random.choice(attrs['preferred_learning_mode'])
    learning_goal = random.choice(attrs['learning_goal'])
    time_pressure = random.choice(attrs['time_pressure'])
    grades_motivation = random.uniform(attrs['grades_motivation'][0],
                                       attrs['grades_motivation'][1])
    intrinsic_curiosity = random.uniform(attrs['intrinsic_curiosity'][0],
                                         attrs['intrinsic_curiosity'][1])

    # Create student user
    student_id = f"student_apprentice_user_{student_num}"

    return {
        "id": f"student-{instructor['id']}-{student_num}",
        "persona_type": "student_apprentice",
        "created_at": datetime.now().isoformat(),
        "name": student_id,
        "age": age,
        "gender": gender,
        "education": education,
        "engagement_level": engagement_level,
        "action_tendency": action_tendency,
        "anxiety_level": anxiety_level,
        "attributes": {
            "learning_stage": learning_stage,
            "instructor_id": instructor['id'],
            "instructor_name": instructor['name'],
            "access_type": "student_view",
            "course_enrolled": True,
            "question_frequency": question_frequency,
            "search_usage": search_usage,
            "self_service_success_rate": self_service_success,
            "office_hours_reduction": office_hours_reduction,
            "preferred_learning_mode": preferred_learning_mode,
            "learning_goal": learning_goal,
            "time_pressure": time_pressure,
            "grades_motivation": grades_motivation,
            "intrinsic_curiosity": intrinsic_curiosity,
            "tech_comfort": tech_comfort,
            "engagement_tier": random.choices(['high', 'standard'], weights=[0.4, 0.6])[0],
            "capture_behavior": "n/a"  # Students don't capture, they consume
        },
        "metadata": {
            "linked_to_educator": True,
            "network_effect": True
        }
    }


def generate_ta_persona(instructor, ta_num, config_loader):
    """Generate a teaching assistant linked to an instructor"""

    # Load persona config
    personas_config = config_loader.load_personas()
    ta_config = personas_config['teaching_assistant']

    # Generate demographics
    age = random.randint(ta_config.age_range[0], ta_config.age_range[1])

    gender_dist = ta_config.gender_distribution
    gender = random.choices(list(gender_dist.keys()),
                           weights=list(gender_dist.values()))[0]

    edu_dist = ta_config.education_distribution
    education = random.choices(list(edu_dist.keys()),
                              weights=list(edu_dist.values()))[0]

    # Generate behavioral traits
    engagement_level = random.uniform(
        ta_config.action_tendency[0],
        ta_config.action_tendency[1]
    )
    action_tendency = random.uniform(
        ta_config.action_tendency[0],
        ta_config.action_tendency[1]
    )
    anxiety_level = random.uniform(
        ta_config.anxiety_level[0],
        ta_config.anxiety_level[1]
    )

    # Generate attributes
    attrs = ta_config.attributes
    tech_comfort_range = attrs.get('tech_comfort', [0.75, 0.95])
    if isinstance(tech_comfort_range, list):
        tech_comfort = random.uniform(tech_comfort_range[0], tech_comfort_range[1])
    else:
        tech_comfort = tech_comfort_range

    student_interaction_volume = random.randint(attrs['student_interaction_volume'][0],
                                                attrs['student_interaction_volume'][1])
    sections_taught = random.randint(attrs['sections_taught'][0],
                                     attrs['sections_taught'][1])
    students_per_section = random.randint(attrs['students_per_section'][0],
                                          attrs['students_per_section'][1])
    knowledge_base_contribution = random.randint(attrs['knowledge_base_contribution'][0],
                                                 attrs['knowledge_base_contribution'][1])
    ta_experience_years = random.randint(attrs['ta_experience_years'][0],
                                         attrs['ta_experience_years'][1])
    career_goal = random.choice(attrs['career_goal'])
    time_savings_per_week = random.randint(attrs['time_savings_per_week'][0],
                                           attrs['time_savings_per_week'][1])
    repeat_question_handling = random.uniform(attrs['repeat_question_handling'][0],
                                              attrs['repeat_question_handling'][1])
    collaboration_frequency = random.choice(attrs['collaboration_frequency'])

    # Create TA user
    ta_id = f"teaching_assistant_user_{ta_num}"

    return {
        "id": f"ta-{instructor['id']}-{ta_num}",
        "persona_type": "teaching_assistant",
        "created_at": datetime.now().isoformat(),
        "name": ta_id,
        "age": age,
        "gender": gender,
        "education": education,
        "engagement_level": engagement_level,
        "action_tendency": action_tendency,
        "anxiety_level": anxiety_level,
        "attributes": {
            "supervising_instructor_id": instructor['id'],
            "instructor_name": instructor['name'],
            "permission_level": "editor",
            "collaboration_frequency": collaboration_frequency,
            "student_interaction_volume": student_interaction_volume,
            "sections_taught": sections_taught,
            "students_per_section": students_per_section,
            "primary_activities": random.sample(attrs['primary_activities'], 3),
            "knowledge_base_contribution": knowledge_base_contribution,
            "ta_experience_years": ta_experience_years,
            "career_goal": career_goal,
            "learning_from_instructor": True,
            "time_savings_per_week": time_savings_per_week,
            "repeat_question_handling": repeat_question_handling,
            "tech_comfort": tech_comfort,
            "engagement_tier": random.choices(['high', 'standard'], weights=[0.6, 0.4])[0],
            "capture_behavior": "systematic"
        },
        "metadata": {
            "linked_to_educator": True,
            "network_effect": True
        }
    }


def generate_knowledge_consumer_persona(consumer_num, config_loader):
    """Generate a knowledge consumer (marketplace user)"""

    # Load persona config
    personas_config = config_loader.load_personas()
    consumer_config = personas_config['knowledge_consumer']

    # Generate demographics
    age = random.randint(consumer_config.age_range[0], consumer_config.age_range[1])

    gender_dist = consumer_config.gender_distribution
    gender = random.choices(list(gender_dist.keys()),
                           weights=list(gender_dist.values()))[0]

    edu_dist = consumer_config.education_distribution
    education = random.choices(list(edu_dist.keys()),
                              weights=list(edu_dist.values()))[0]

    # Generate behavioral traits
    engagement_level = random.uniform(
        consumer_config.action_tendency[0],
        consumer_config.action_tendency[1]
    )
    action_tendency = random.uniform(
        consumer_config.action_tendency[0],
        consumer_config.action_tendency[1]
    )
    anxiety_level = random.uniform(
        consumer_config.anxiety_level[0],
        consumer_config.anxiety_level[1]
    )

    # Generate attributes
    attrs = consumer_config.attributes
    tech_comfort_range = attrs.get('tech_comfort', [0.6, 0.9])
    if isinstance(tech_comfort_range, list):
        tech_comfort = random.uniform(tech_comfort_range[0], tech_comfort_range[1])
    else:
        tech_comfort = tech_comfort_range

    query_specificity = random.choice(attrs['query_specificity'])
    query_complexity = random.choice(attrs['query_complexity'])
    query_frequency = random.randint(attrs['query_frequency'][0],
                                     attrs['query_frequency'][1])
    willingness_to_pay = random.randint(attrs['willingness_to_pay'][0],
                                        attrs['willingness_to_pay'][1])

    price_sensitivity_dist = attrs['price_sensitivity_distribution']
    price_sensitivity = random.choices(list(price_sensitivity_dist.keys()),
                                      weights=list(price_sensitivity_dist.values()))[0]

    use_case_dist = attrs['use_case_distribution']
    use_case = random.choices(list(use_case_dist.keys()),
                             weights=list(use_case_dist.values()))[0]

    discovery_source = random.choice(attrs['discovery_source'])
    subscription_conversion_potential = random.uniform(
        attrs['subscription_conversion_potential'][0],
        attrs['subscription_conversion_potential'][1]
    )

    # Create consumer user
    consumer_id = f"knowledge_consumer_user_{consumer_num}"

    return {
        "id": f"consumer-{consumer_num}",
        "persona_type": "knowledge_consumer",
        "created_at": datetime.now().isoformat(),
        "name": consumer_id,
        "age": age,
        "gender": gender,
        "education": education,
        "engagement_level": engagement_level,
        "action_tendency": action_tendency,
        "anxiety_level": anxiety_level,
        "attributes": {
            "usage_pattern": "one_time_query",
            "payment_model": "pay_per_query",
            "subscription_conversion_potential": subscription_conversion_potential,
            "query_specificity": query_specificity,
            "query_complexity": query_complexity,
            "query_frequency": query_frequency,
            "willingness_to_pay": willingness_to_pay,
            "verification_requirement": "expert_verified",
            "price_sensitivity": price_sensitivity,
            "use_case": use_case,
            "discovery_source": discovery_source,
            "tech_comfort": tech_comfort,
            "engagement_tier": "standard",
            "capture_behavior": "n/a"
        },
        "metadata": {
            "marketplace_user": True,
            "transactional": True
        }
    }


def add_weekly_synthesis_steps(journey_steps, persona_type):
    """Add weekly synthesis review steps to a journey"""

    # Find steps that should have synthesis reviews (every ~7 steps in active_use phase)
    active_use_steps = [s for s in journey_steps if s.get('phase_id') == 'phase_3']

    if not active_use_steps:
        return journey_steps

    # Add synthesis review every ~7 days
    synthesis_steps = []
    for i, step in enumerate(active_use_steps):
        if i > 0 and i % 7 == 0:  # Every 7th step
            synthesis_step = {
                "id": f"synthesis-{step['id']}",
                "phase_id": "phase_3",
                "step_number": step['step_number'] + 0.5,  # Insert between steps
                "timestamp": step['timestamp'],
                "actions": ["review_weekly_synthesis"],
                "emotional_state": "reflective",
                "completion_status": "completed",
                "data_captured": {
                    "patterns_discovered": random.randint(5, 15),
                    "gaps_identified": random.randint(3, 10),
                    "clarifying_questions_answered": random.randint(2, 8),
                    "time_saved_minutes": random.randint(20, 90),
                    "surprise_insights": random.randint(1, 4)
                },
                "time_invested": random.randint(10, 30),
                "engagement_score": random.uniform(0.7, 0.95),
                "synthesis_engagement": {
                    "reviewed": True,
                    "value_rating": random.randint(4, 5)  # High value
                }
            }
            synthesis_steps.append((step['step_number'], synthesis_step))

    # Insert synthesis steps
    all_steps = journey_steps.copy()
    for _, syn_step in synthesis_steps:
        all_steps.append(syn_step)

    # Re-sort by step_number
    all_steps.sort(key=lambda x: x['step_number'])

    return all_steps


def add_export_events(journey_steps, persona_type):
    """Add export/teaching materials creation events to journeys"""

    # Find mature_use steps
    mature_steps = [s for s in journey_steps if s.get('phase_id') == 'phase_4']

    if not mature_steps or persona_type in ['student_apprentice', 'knowledge_consumer']:
        return journey_steps  # Only practitioners/educators export

    # Add 1-2 export events
    export_count = random.randint(1, 2)
    export_steps = []

    for i in range(export_count):
        if i < len(mature_steps):
            step = mature_steps[i * len(mature_steps) // export_count]

            export_formats = ['pdf', 'markdown', 'notion', 'docx']
            content_types = ['workshop_handout', 'course_syllabus', 'technique_guide', 'reference_sheet']

            export_step = {
                "id": f"export-{step['id']}",
                "phase_id": "phase_4",
                "step_number": step['step_number'] + 0.3,
                "timestamp": step['timestamp'],
                "actions": ["export_teaching_materials"],
                "emotional_state": "accomplished",
                "completion_status": "completed",
                "data_captured": {
                    "export_format": random.choice(export_formats),
                    "content_type": random.choice(content_types),
                    "knowledge_atoms_included": random.randint(15, 80),
                    "pages_generated": random.randint(3, 25),
                    "usage": random.choice(["shared_with_students", "workshop_use", "personal_reference"]),
                    "student_feedback": random.choice(["very_positive", "positive", "neutral"])
                },
                "time_invested": random.randint(5, 20),
                "engagement_score": random.uniform(0.8, 0.98),
                "export_outcome": {
                    "success": True,
                    "time_to_create_minutes": random.randint(15, 45),
                    "quality_self_rating": random.randint(4, 5)
                }
            }
            export_steps.append((step['step_number'], export_step))

    # Insert export steps
    all_steps = journey_steps.copy()
    for _, exp_step in export_steps:
        all_steps.append(exp_step)

    # Re-sort by step_number
    all_steps.sort(key=lambda x: x['step_number'])

    return all_steps


def main():
    """Main execution"""

    print("=" * 80)
    print("🌐 Network Effect Personas Generation")
    print("=" * 80)
    print()

    # Load existing users
    print("📂 Loading existing user cohort...")
    existing_users = load_existing_users()
    print(f"   Loaded {len(existing_users)} existing users")
    print()

    # Load project configs
    config_loader = ConfigLoader("projects/private_language")
    phases = config_loader.load_journey_phases()
    emotional_states = config_loader.load_emotional_states()

    # Select educators to link to
    print("🎓 Selecting master educators for linking...")
    selected_educators = select_master_educators(existing_users, count=2)
    print(f"   Selected {len(selected_educators)} educators:")
    for edu in selected_educators:
        print(f"     - {edu['name']} (engagement: {edu['engagement_level']:.2f}, "
              f"students/year: {edu['attributes'].get('students_per_year', 'N/A')})")
    print()

    # Generate new personas
    new_users = []

    # Generate students (3 total, distributed across selected educators)
    print("👨‍🎓 Generating student personas...")
    student_count = 0
    for edu in selected_educators:
        # 2 students for first educator, 1 for second
        num_students = 2 if student_count == 0 else 1
        for i in range(num_students):
            student_count += 1
            student = generate_student_persona(edu, student_count, config_loader)
            new_users.append(student)
            print(f"   ✓ {student['name']} → linked to {edu['name']}")
    print()

    # Generate TAs (2 total, one per educator)
    print("👩‍🏫 Generating teaching assistant personas...")
    for ta_num, edu in enumerate(selected_educators, 1):
        ta = generate_ta_persona(edu, ta_num, config_loader)
        new_users.append(ta)
        print(f"   ✓ {ta['name']} → linked to {edu['name']}")
    print()

    # Generate knowledge consumers (2 total, independent)
    print("🛒 Generating knowledge consumer personas...")
    for i in range(1, 3):
        consumer = generate_knowledge_consumer_persona(i, config_loader)
        new_users.append(consumer)
        print(f"   ✓ {consumer['name']} (marketplace user)")
    print()

    print(f"📊 Generated {len(new_users)} new personas:")
    print(f"   - 3 students (linked to educators)")
    print(f"   - 2 teaching assistants (linked to educators)")
    print(f"   - 2 knowledge consumers (marketplace)")
    print()

    # Initialize journey generator with REAL LLM
    print("🤖 Initializing journey generator with Claude Sonnet 4.5...")
    journey_gen = JourneyGenerator(
        journey_type=JourneyType.SESSION_BASED,
        phases_config=phases,
        emotional_states=emotional_states,
        ssr_config_path="projects/private_language/response_scales.yaml",
        enable_ssr=True,
        use_real_llm=True,
        llm_model="claude-sonnet-4-5-20250929"
    )
    print("✓ Generator ready")
    print()

    # Generate journeys for new users
    print("=" * 80)
    print("📝 Generating Journeys with Real LLM")
    print("=" * 80)
    print()

    completed_users = []
    start_time = time.time()

    for idx, user_data in enumerate(new_users, 1):
        user_start = time.time()

        print(f"Processing {idx}/{len(new_users)}: {user_data['name']} ({user_data['persona_type']})")

        # Create persona object
        persona = Persona(
            id=user_data["id"],
            persona_type=user_data["persona_type"],
            config=None,
            age=user_data["age"],
            gender=user_data["gender"],
            education=user_data["education"],
            engagement_level=user_data["engagement_level"],
            action_tendency=user_data["action_tendency"],
            anxiety_level=user_data.get("anxiety_level"),
            attributes=user_data["attributes"]
        )

        # Generate journey
        journey = journey_gen.generate(persona, user_data["id"])

        # Convert to dict
        journey_dict = {
            "id": journey.id,
            "user_id": journey.user_id,
            "persona_type": journey.persona_type,
            "journey_type": journey.journey_type.value,
            "started_at": journey.started_at.isoformat(),
            "completed_at": journey.completed_at.isoformat() if journey.completed_at else None,
            "overall_completion": journey.overall_completion,
            "steps": []
        }

        for step in journey.steps:
            step_dict = {
                "id": step.id,
                "phase_id": step.phase_id,
                "step_number": step.step_number,
                "timestamp": step.timestamp.isoformat(),
                "actions": step.actions,
                "emotional_state": step.emotional_state,
                "completion_status": step.completion_status.value,
                "data_captured": step.data_captured,
                "time_invested": step.time_invested,
                "engagement_score": step.engagement_score
            }

            if hasattr(step, 'ssr_responses'):
                step_dict['ssr_responses'] = step.ssr_responses

            journey_dict['steps'].append(step_dict)

        # Add weekly synthesis steps
        journey_dict['steps'] = add_weekly_synthesis_steps(
            journey_dict['steps'],
            user_data['persona_type']
        )

        # Add export events
        journey_dict['steps'] = add_export_events(
            journey_dict['steps'],
            user_data['persona_type']
        )

        # Combine user data with journey
        user_result = {
            **user_data,
            "journey": journey_dict,
            "llm_generated": True,
            "llm_model": "claude-sonnet-4-5-20250929",
            "generation_timestamp": datetime.now().isoformat(),
            "enhanced_with_synthesis_and_export": True
        }

        completed_users.append(user_result)

        user_time = time.time() - user_start
        print(f"  ✓ Journey generated: {len(journey.steps)} steps, {user_time:.1f}s")
        print()

    total_time = time.time() - start_time

    # Save new personas
    output_file = Path("output/network_effect_personas.json")
    with open(output_file, 'w') as f:
        json.dump(completed_users, f, indent=2)

    print("=" * 80)
    print("✅ Generation Complete")
    print("=" * 80)
    print()
    print(f"Generated {len(completed_users)} network effect personas with full journeys")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Saved to: {output_file}")
    print()
    print("📦 Persona Breakdown:")
    print(f"  • 3 students linked to educators (validates student-facing UI)")
    print(f"  • 2 TAs linked to educators (validates team collaboration)")
    print(f"  • 2 knowledge consumers (validates marketplace/pay-per-query)")
    print()
    print("🎯 Enhanced Features:")
    print(f"  • Weekly synthesis review steps added to all journeys")
    print(f"  • Export event outcomes added to practitioner/educator journeys")
    print(f"  • Full LLM-generated SSR responses for authentic persona voice")
    print()


if __name__ == "__main__":
    main()
