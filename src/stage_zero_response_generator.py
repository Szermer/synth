"""
Stage Zero Response Generator - Generates credible open-ended responses
"""

import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


class ResponseGenerator:
    """Generates credible open-ended responses based on persona and context"""
    
    def __init__(self):
        self.load_response_templates()
    
    def load_response_templates(self):
        """Load response templates for different personas and questions"""
        
        # Week 1: What brought you here today?
        self.motivation_templates = {
            "health_aware_avoider": [
                "My sister was just diagnosed with breast cancer at 42. I've been putting this off for years but I can't ignore it anymore.",
                "I turned {age} last month and my doctor keeps mentioning I should think about this. I'm terrified but I know I need to face it.",
                "My mom had breast cancer and I've been too scared to look into my own risk. But avoiding it isn't making the fear go away.",
                "I've been having anxiety about cancer for months. Maybe knowing my actual risk will help me sleep better.",
                "My best friend is going through treatment right now. It made me realize I've been in denial about my family history."
            ],
            "structured_system_seeker": [
                "I just relocated for work and need to establish a new healthcare routine. This seems like a logical starting point.",
                "I'm {age} now and want a comprehensive understanding of my health risks so I can plan accordingly.",
                "I track everything about my health and realized I have a gap in understanding my cancer risk. Time to fix that.",
                "My company offers a health benefit that covers this assessment. I like to maximize my benefits and stay on top of preventive care.",
                "I'm updating all my health records and screenings. This is the next item on my checklist."
            ],
            "balanced_life_integrator": [
                "I've been focusing on my overall wellness and realized I should understand my cancer risk as part of that journey.",
                "A friend mentioned how helpful this was for her. I like the holistic approach to understanding health risks.",
                "I'm trying to be more proactive about my health without letting it take over my life. This seems balanced.",
                "I want to model good health habits for my daughters. Understanding my risk seems like responsible self-care.",
                "I've been working on reducing stress and taking better care of myself. This feels like a natural next step."
            ],
            "healthcare_professional": [
                "I recommend cancer screening to my patients daily but realized I don't fully understand my own risk profile.",
                "As a {occupation}, I see the importance of early detection. Time to practice what I preach.",
                "I'm interested in how you present risk information to patients. Plus, I should know my own risk factors.",
                "Professionally, I know the statistics. Personally, I've been avoiding thinking about my own risk. Time to change that.",
                "I want to experience what my patients go through with risk assessment so I can better support them."
            ],
            "overlooked_risk_group": [
                "My cousin told me about this. I don't usually do these health things but she said it was really helpful.",
                "I'm not sure if this is for someone like me, but I figured I'd try. My family doesn't really talk about cancer.",
                "My new doctor suggested I look into this. I don't know much about my risk but I guess it's time to learn.",
                "I saw an ad and thought maybe I should check it out. No one in my family really does preventive care.",
                "A coworker was talking about her experience and it made me think maybe I should know more about my health."
            ]
        }
        
        # Week 2: How did family cancer experience affect you?
        self.family_impact_templates = {
            "health_aware_avoider": [
                "Watching my mom go through chemo when I was {young_age} was traumatic. I've been terrified of doctors ever since.",
                "It made me hyperaware of every little change in my body. Sometimes I think ignorance would be easier.",
                "My family doesn't talk about it. We just pretend it didn't happen, but the fear is always there.",
                "I became the family caretaker at a young age. Now thinking about my own health feels selfish somehow.",
                "It's complicated. Part of me wants to know everything, part of me wants to know nothing."
            ],
            "structured_system_seeker": [
                "It motivated me to be very organized about health records and screening schedules. Information is power.",
                "I started researching everything I could about cancer prevention. I keep detailed family health histories.",
                "It made me realize the importance of being proactive rather than reactive with health management.",
                "I became the family health coordinator, tracking everyone's screening dates and medical information.",
                "It taught me that knowledge and early detection are our best tools. I approach it very systematically now."
            ],
            "balanced_life_integrator": [
                "It showed me that health is important but you can't let fear control your life. Balance is key.",
                "I learned to appreciate each day while still being responsible about prevention. It's about finding middle ground.",
                "It brought our family closer but also taught us not to let cancer define us. We focus on living well.",
                "I saw how stress affected my mom's recovery. It made me prioritize mental health alongside physical health.",
                "It made me more conscious about health choices without becoming obsessed. Moderation in everything."
            ],
            "healthcare_professional": [
                "It influenced my career choice. I wanted to help other families navigate what we went through.",
                "Professionally, I understood the medical side. Emotionally, it was completely different being the family member.",
                "It gave me empathy for my patients that textbooks never could. Personal experience changes perspective.",
                "I saw gaps in how healthcare systems support families. It drives my patient advocacy work now.",
                "It made me realize how much medical knowledge doesn't prepare you for the emotional reality."
            ],
            "overlooked_risk_group": [
                "We didn't really understand what was happening. The doctors used big words and we just nodded along.",
                "My family kind of fell apart after. We don't really talk about health stuff since then.",
                "It was confusing and scary. I was young and no one explained anything to me.",
                "Honestly, I'm not sure it did affect me. We just moved on and didn't discuss it much.",
                "It made me feel like cancer is just something that happens to people like us. Like we don't have control."
            ]
        }
        
        # Week 3: Relationship with body/reproductive choices
        self.body_relationship_templates = {
            "health_aware_avoider": [
                "Having kids made me more anxious about my health. What if something happens to me?",
                "I've always had a complicated relationship with my body. Medical exams make me very uncomfortable.",
                "Pregnancy was the only time I felt connected to my body. Otherwise, I try not to think about it much.",
                "I chose not to have children partly because of my family cancer history. Sometimes I wonder if that was fear talking.",
                "Breastfeeding was difficult and made me realize how little control I have over my body. It's unsettling."
            ],
            "structured_system_seeker": [
                "I tracked everything during pregnancy - very data-driven. I approach all health decisions this way.",
                "My reproductive choices were carefully planned. I researched all the health implications thoroughly.",
                "I keep detailed records of my cycles and hormonal changes. Data helps me feel in control.",
                "Having children made me more committed to preventive care. I need to be here for them.",
                "I've always been very aware of my body and track changes systematically. It helps with health management."
            ],
            "balanced_life_integrator": [
                "Pregnancy taught me to trust my body more. I learned to balance medical advice with intuition.",
                "I try to appreciate what my body can do rather than worry about what might go wrong.",
                "Motherhood shifted my priorities. Health is important but not worth obsessing over.",
                "I've learned to listen to my body without overanalyzing every sensation. It's about balance.",
                "My reproductive journey taught me that planning is good but flexibility is essential."
            ],
            "healthcare_professional": [
                "My medical knowledge was both helpful and anxiety-inducing during pregnancy. Sometimes knowing less is easier.",
                "I understand the clinical aspects but the personal experience is entirely different. It's humbling.",
                "Working in healthcare made me very aware of everything that could go wrong. I had to learn to separate work from personal life.",
                "My reproductive choices were informed by medical knowledge but ultimately came down to personal values.",
                "I counsel patients about these issues daily, but my own journey was more emotional than clinical."
            ],
            "overlooked_risk_group": [
                "I had my kids young. Didn't really think about how it might affect my health later.",
                "No one ever explained how pregnancy and stuff could relate to cancer risk. This is all new to me.",
                "I just did what felt natural. Never really thought about tracking things or keeping records.",
                "My body is my body. I don't spend much time thinking about it unless something hurts.",
                "Having kids just happened. We didn't plan it out like some people do."
            ]
        }
        
        # Week 4: Healthcare provider relationships
        self.provider_relationship_templates = {
            "health_aware_avoider": [
                "I tend to downplay symptoms because I don't want to be seen as a hypochondriac. Then I worry I'm not being taken seriously.",
                "I get so anxious before appointments that I forget half of what I wanted to ask. It's frustrating.",
                "My doctor is nice but always seems rushed. I don't feel like there's time to really discuss my concerns.",
                "I've switched providers several times looking for someone who understands my anxiety about health issues.",
                "I often leave appointments feeling unheard. Maybe it's me not communicating well, but it's discouraging."
            ],
            "structured_system_seeker": [
                "I come prepared with written questions and expect detailed answers. Some doctors appreciate it, others seem annoyed.",
                "I maintain spreadsheets of my health data to share with providers. I need them to see the full picture.",
                "My ideal provider is someone who respects that I've done my research and wants to have an informed discussion.",
                "I've found a great primary care doctor who appreciates my organized approach. We work well together.",
                "I expect evidence-based recommendations and clear explanations. Vague advice doesn't work for me."
            ],
            "balanced_life_integrator": [
                "I look for providers who see health holistically, not just individual symptoms or test results.",
                "My best healthcare experiences have been with providers who take time to understand my lifestyle and values.",
                "I prefer collaborative relationships where my input is valued alongside medical expertise.",
                "I've learned to advocate for what I need while respecting the provider's expertise. It's about partnership.",
                "Good communication is key. I need providers who can explain things clearly without being condescending."
            ],
            "healthcare_professional": [
                "Being a healthcare provider myself sometimes complicates the dynamic. Some colleagues assume I know everything.",
                "I have high standards for my care team because I know what good care looks like. That can make me a challenging patient.",
                "I appreciate providers who treat me as a partner, acknowledging my knowledge while filling in gaps.",
                "It's actually hard to be the patient when you're used to being the provider. Role reversal is uncomfortable.",
                "I've learned to explicitly state when I'm speaking as a patient versus a colleague. It helps clarify the relationship."
            ],
            "overlooked_risk_group": [
                "I feel like doctors don't always take me seriously. Maybe it's how I talk or dress, I don't know.",
                "I mostly go to urgent care when something's really wrong. Don't really have a regular doctor.",
                "Sometimes I feel like they're judging me for not knowing medical terms or asking 'dumb' questions.",
                "My last doctor retired and I haven't found a new one. It's hard to start over with someone new.",
                "I wish doctors would explain things in normal words. Sometimes I just nod even when I don't understand."
            ]
        }
        
        # Week 5: What helps you stay active?
        self.activity_templates = {
            "health_aware_avoider": [
                "I go through phases. When I'm anxious about health, I exercise obsessively. Then I burn out and stop completely.",
                "Walking my dog is the only consistent exercise I get. At least she forces me outside every day.",
                "I know I should exercise more but gym environments make me self-conscious. I prefer activities where I can be alone.",
                "Honestly, anxiety is what drives most of my activity. Nervous energy has to go somewhere.",
                "I've tried so many fitness programs but nothing sticks. The mental barriers are harder than the physical ones."
            ],
            "structured_system_seeker": [
                "I have a detailed workout schedule that I track in my fitness app. Data and goals keep me motivated.",
                "I've been doing the same morning routine for 5 years. Consistency is key for me.",
                "I schedule exercise like any other appointment. If it's on my calendar, it happens.",
                "I respond well to structured programs with clear progressions. Random workouts don't work for me.",
                "Tracking metrics like steps, heart rate, and calories helps me stay accountable and motivated."
            ],
            "balanced_life_integrator": [
                "I focus on activities I enjoy rather than what burns the most calories. Happiness is part of health.",
                "I integrate movement into daily life - bike commuting, walking meetings, active family time.",
                "Variety keeps me engaged. I do yoga for stress, hiking for nature, and dance for fun.",
                "I've learned to be flexible. Some weeks are more active than others and that's okay.",
                "Finding activities I can do with friends or family helps me stay consistent. It's social time too."
            ],
            "healthcare_professional": [
                "I know all the recommendations but struggle with the time. 12-hour shifts don't leave much energy for exercise.",
                "I try to model healthy behaviors for my patients, which keeps me accountable even when I'm tired.",
                "I've learned to do quick, efficient workouts. 20 minutes of HIIT is better than skipping entirely.",
                "Shift work wreaks havoc on routine. I've had to get creative about when and how I exercise.",
                "Understanding the science behind exercise benefits motivates me even when I don't feel like it."
            ],
            "overlooked_risk_group": [
                "I get exercise at work - I'm on my feet all day. Don't really have time or energy for more.",
                "Gym memberships are expensive. I try to walk when I can but it's not always safe in my neighborhood.",
                "Taking care of kids is my exercise. I don't have time for fancy workout routines.",
                "I've never been athletic. PE class was torture and I've avoided exercise ever since.",
                "When I have free time, I'm too tired to exercise. Just surviving is enough activity for me."
            ]
        }
        
        # Week 8: What additional support would be helpful?
        self.support_needs_templates = {
            "health_aware_avoider": [
                "Someone to go with me to appointments. I get so anxious I can't process information alone.",
                "Clear, simple reminders that don't trigger my anxiety. Gentle nudges, not scary statistics.",
                "A support group for people who are anxious about health. Sometimes I feel like I'm the only one who worries this much.",
                "Help finding providers who understand medical anxiety and won't dismiss my concerns as 'just anxiety'.",
                "Resources for managing health anxiety while still being appropriately proactive about screening."
            ],
            "structured_system_seeker": [
                "Integration with my existing health tracking apps would be helpful. I want all my data in one place.",
                "Detailed timelines and checklists for all recommended screenings based on my specific risk factors.",
                "Access to the latest research and guidelines so I can stay informed about best practices.",
                "A provider who appreciates prepared patients and will engage in detailed discussions about options.",
                "Automated scheduling that syncs with my calendar and sends appropriate advance reminders."
            ],
            "balanced_life_integrator": [
                "Flexible scheduling options that work with my varied schedule. Traditional 9-5 appointments are challenging.",
                "Resources that consider whole-person wellness, not just disease prevention.",
                "Child care assistance during appointments would remove a major barrier for me.",
                "Providers who understand that health is just one part of a full life, not the only priority.",
                "Community programs that make prevention feel less medical and more like self-care."
            ],
            "healthcare_professional": [
                "Colleagues who understand the unique challenges of being both a healthcare provider and a patient.",
                "Expedited scheduling that works with my unpredictable work hours. It's hard to plan appointments weeks out.",
                "CME credit for completing comprehensive health assessments. Make it professionally beneficial too.",
                "Peer support from other healthcare professionals navigating their own health journeys.",
                "Evidence-based resources I can share with my patients based on my own experience."
            ],
            "overlooked_risk_group": [
                "Help understanding what my insurance actually covers. The paperwork is so confusing.",
                "Transportation assistance to get to appointments. The bus routes don't always work for medical centers.",
                "Someone who can explain medical stuff in plain language. I want to understand but it's overwhelming.",
                "Financial help for screenings. Even with insurance, the copays add up quickly.",
                "Appointments outside regular work hours. I can't afford to take time off for preventive care."
            ]
        }
        
        # Week 9: What gives you peace of mind about health?
        self.peace_of_mind_templates = {
            "health_aware_avoider": [
                "Honestly, I'm not sure anything gives me real peace of mind. But having a plan might help with the constant worry.",
                "When my test results are normal, I feel relief for about a week. Then the anxiety creeps back.",
                "Knowing I'm doing something proactive helps a little. At least I'm not just worrying without action.",
                "Having doctors who take my concerns seriously, even if they seem excessive to others.",
                "Meditation and therapy help more than medical tests. I'm working on the anxiety alongside the screening."
            ],
            "structured_system_seeker": [
                "Having complete, up-to-date health records and knowing I'm following all recommended guidelines.",
                "Data gives me peace of mind. When I can track trends and see that things are stable, I feel in control.",
                "Knowing I have a comprehensive plan and I'm executing it properly. Uncertainty is what causes stress.",
                "Regular check-ins and screenings on schedule. Consistency and routine are calming for me.",
                "Understanding the why behind recommendations. When things make logical sense, I feel more at peace."
            ],
            "balanced_life_integrator": [
                "Knowing I'm doing reasonable prevention without letting it dominate my life gives me peace.",
                "Trusting my body while also being appropriately vigilant. It's about finding that sweet spot.",
                "Having a support system that will help me navigate whatever comes. I don't have to face things alone.",
                "Focusing on what I can control - lifestyle choices - rather than worrying about what I can't.",
                "Regular check-ins that don't disrupt my life too much. Prevention that fits into living."
            ],
            "healthcare_professional": [
                "Using my medical knowledge appropriately without letting it fuel anxiety. Knowledge as power, not fear.",
                "Having colleagues I trust for my own care. Sometimes you need to be the patient, not the expert.",
                "Evidence-based screening at appropriate intervals. Not over-testing but not under-vigilant either.",
                "Separating my professional knowledge from personal health anxiety. They're different skills.",
                "Quality providers who respect my knowledge but still provide thorough care. Partnership model."
            ],
            "overlooked_risk_group": [
                "Just knowing someone is paying attention to my health. Sometimes I feel invisible in the healthcare system.",
                "When doctors explain things so I actually understand. Knowledge helps even if it's scary.",
                "Having a plan I can actually follow. Recommendations that work with my real life, not some ideal.",
                "Knowing there's help available if I need it. Financial assistance, transportation, translation - practical support.",
                "Feeling like I matter, like my health is important even if I'm not rich or educated."
            ]
        }
        
        # Week 10: What's most valuable about this journey?
        self.journey_value_templates = {
            "health_aware_avoider": [
                "I finally faced something I've been avoiding for years. That alone feels like a huge accomplishment.",
                "Learning that my anxiety about cancer risk was actually worse than knowing my real risk. Knowledge really is power.",
                "Having someone guide me through this gradually made it manageable. I couldn't have done it all at once.",
                "Realizing I'm not alone in my fears. Hearing that others struggle with health anxiety too was validating.",
                "Getting a plan that acknowledges my anxiety and works with it, not against it. That's new for me."
            ],
            "structured_system_seeker": [
                "The comprehensive nature of the assessment. Finally, something that looks at all the factors, not just age and family history.",
                "Having data-driven recommendations specific to my situation. Generic guidelines never felt sufficient.",
                "The systematic approach resonated with how I think. Step by step, building a complete picture.",
                "Being able to track progress and see how each week built on the last. The structure was perfect for me.",
                "Getting a plan I can actually implement with clear timelines and metrics. Actionable intelligence."
            ],
            "balanced_life_integrator": [
                "The holistic approach that considered my whole life, not just medical risk factors. That was refreshing.",
                "Learning how to balance being health-conscious with living fully. That's always been my struggle.",
                "Seeing how my values and preferences could shape my prevention plan. It's not one-size-fits-all.",
                "The pace allowed me to integrate this into my life without overwhelming everything else. Sustainable approach.",
                "Feeling heard and understood, not just assessed. The personal touch made all the difference."
            ],
            "healthcare_professional": [
                "Experiencing the patient perspective in such depth. This will definitely influence how I practice.",
                "The integration of multiple risk models was sophisticated. I appreciate evidence-based approaches.",
                "Being reminded that even with all my knowledge, the emotional journey is what matters for patients.",
                "Getting personalized recommendations despite my tendency to think I already know everything. Humbling and helpful.",
                "The way complex medical information was presented. I'm taking notes for my own patient communications."
            ],
            "overlooked_risk_group": [
                "Someone finally taking time to explain everything in ways I could understand. That's rare in healthcare.",
                "Feeling like my concerns and barriers were heard, not judged. Usually I feel dismissed.",
                "Getting a plan that actually works with my life situation. Not just ideal world recommendations.",
                "Learning that I have more control over my health than I thought. It's not just luck or genetics.",
                "Being treated like my health matters. Sometimes it feels like preventive care is only for certain people."
            ]
        }
    
    def generate_response(
        self,
        question_type: str,
        persona_type: str,
        context: Dict[str, Any]
    ) -> str:
        """Generate a credible open-ended response"""
        
        # Map question types to template sets
        template_map = {
            "motivation": self.motivation_templates,
            "family_impact": self.family_impact_templates,
            "body_relationship": self.body_relationship_templates,
            "provider_relationship": self.provider_relationship_templates,
            "activity": self.activity_templates,
            "support_needs": self.support_needs_templates,
            "peace_of_mind": self.peace_of_mind_templates,
            "journey_value": self.journey_value_templates
        }
        
        # Get appropriate templates
        templates = template_map.get(question_type, {}).get(persona_type, [])
        if not templates:
            return "I prefer not to answer this question in detail."
        
        # Select and customize template
        template = random.choice(templates)
        
        # Replace placeholders with context
        response = template.format(
            age=context.get("age", "40"),
            young_age=random.randint(8, 16),
            occupation=context.get("occupation", "nurse")
        )
        
        # Add personal touches based on context
        if context.get("has_children") and random.random() < 0.3:
            response += " Having kids definitely changes how I think about this."
        
        if context.get("high_anxiety") and random.random() < 0.4:
            response += " I know I worry too much, but I can't help it."
        
        return response
    
    def generate_week_responses(
        self,
        week_number: int,
        persona_type: str,
        user_context: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate all open-ended responses for a specific week"""
        
        responses = {}
        
        # Week-specific questions
        week_questions = {
            1: [("motivation", "What brought you here today?")],
            2: [("family_impact", "How did family cancer experience affect you?")],
            3: [("body_relationship", "How did pregnancy/reproductive choices affect your health relationship?")],
            4: [("provider_relationship", "Describe your healthcare provider relationships")],
            5: [("activity", "What helps you stay active?")],
            8: [("support_needs", "What additional support would be helpful?")],
            9: [("peace_of_mind", "What gives you peace of mind about health?")],
            10: [("journey_value", "What was most valuable about this journey?")]
        }
        
        week_qs = week_questions.get(week_number, [])
        
        for question_type, question_text in week_qs:
            response = self.generate_response(question_type, persona_type, user_context)
            responses[question_text] = response
        
        return responses