#!/usr/bin/env python3
"""
Scenario Analyzer for Private Language Synthetic Users

Analyzes generated synthetic users for specific product scenarios like
first capture sessions, onboarding patterns, and engagement behaviors.
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any
import statistics


class ScenarioAnalyzer:
    """Analyze synthetic users for product scenarios"""

    def __init__(self, data_file: str):
        """Load synthetic user data"""
        with open(data_file, 'r') as f:
            self.users = json.load(f)

    def analyze_first_capture_session(self) -> Dict[str, Any]:
        """Analyze first knowledge capture session scenario"""

        print("\n" + "="*80)
        print("📊 FIRST KNOWLEDGE CAPTURE SESSION ANALYSIS")
        print("="*80)

        # Filter users in discovery/onboarding phases
        early_users = [
            u for u in self.users
            if u['journey']['steps'] and
            any(step['phase_id'] in ['phase_1', 'phase_2'] for step in u['journey']['steps'][:3])
        ]

        print(f"\n👥 Analyzing {len(early_users)} users in early journey phases")

        # Analyze by persona
        persona_behaviors = defaultdict(lambda: {
            'users': [],
            'first_sessions': [],
            'emotional_states': [],
            'completion_rates': [],
            'time_invested': []
        })

        for user in early_users:
            persona = user['persona_type']
            journey = user['journey']

            # Get first 1-3 steps (representing first capture session)
            first_steps = journey['steps'][:3] if journey['steps'] else []

            if first_steps:
                persona_behaviors[persona]['users'].append(user)
                persona_behaviors[persona]['first_sessions'].append(first_steps)

                # Collect emotional states from first session
                for step in first_steps:
                    persona_behaviors[persona]['emotional_states'].append(
                        step['emotional_state']
                    )
                    if step.get('time_invested'):
                        persona_behaviors[persona]['time_invested'].append(
                            step['time_invested']
                        )

                # Calculate completion rate
                completed = sum(
                    1 for s in first_steps
                    if s['completion_status'] == 'completed'
                )
                persona_behaviors[persona]['completion_rates'].append(
                    completed / len(first_steps)
                )

        # Print persona-specific insights
        for persona, data in sorted(persona_behaviors.items()):
            if not data['users']:
                continue

            print(f"\n{'─'*80}")
            print(f"🎭 {persona.upper().replace('_', ' ')}")
            print(f"{'─'*80}")

            # User count
            print(f"   Sample Size: {len(data['users'])} users")

            # Average completion rate
            avg_completion = statistics.mean(data['completion_rates']) * 100
            print(f"   First Session Completion: {avg_completion:.1f}%")

            # Time investment
            if data['time_invested']:
                avg_time = statistics.mean(data['time_invested'])
                print(f"   Average Time Investment: {avg_time:.1f} minutes")

            # Most common emotional states
            emotion_counts = defaultdict(int)
            for emotion in data['emotional_states']:
                emotion_counts[emotion] += 1

            top_emotions = sorted(
                emotion_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

            print(f"   Top Emotional States:")
            for emotion, count in top_emotions:
                pct = (count / len(data['emotional_states'])) * 100
                print(f"      • {emotion}: {pct:.1f}%")

            # Journey progress
            avg_steps = statistics.mean([len(s) for s in data['first_sessions']])
            print(f"   Average Steps in First Session: {avg_steps:.1f}")

        return self._create_product_insights(persona_behaviors)

    def _create_product_insights(self, persona_behaviors: Dict) -> Dict[str, Any]:
        """Generate product-specific insights"""

        print(f"\n{'='*80}")
        print("💡 PRODUCT INSIGHTS: First Capture Session")
        print(f"{'='*80}\n")

        insights = {
            'onboarding_recommendations': [],
            'ux_considerations': [],
            'support_needed': [],
            'success_patterns': []
        }

        # Analyze success patterns
        high_performers = []
        struggling_personas = []

        for persona, data in persona_behaviors.items():
            if not data['completion_rates']:
                continue

            avg_completion = statistics.mean(data['completion_rates'])

            if avg_completion > 0.7:
                high_performers.append(persona)
            elif avg_completion < 0.5:
                struggling_personas.append(persona)

        # Generate insights
        if high_performers:
            print("✅ HIGH ENGAGEMENT PERSONAS:")
            for persona in high_performers:
                print(f"   • {persona.replace('_', ' ').title()}")
                insights['success_patterns'].append(
                    f"{persona} shows high first-session completion"
                )
            print("\n   → These users need minimal hand-holding")
            print("   → Focus on accelerating to value (gap detection)")
            insights['onboarding_recommendations'].append(
                "Fast-track high-engagement personas to advanced features"
            )

        if struggling_personas:
            print(f"\n⚠️  NEEDS SUPPORT:")
            for persona in struggling_personas:
                print(f"   • {persona.replace('_', ' ').title()}")
                insights['support_needed'].append(
                    f"{persona} may need additional onboarding support"
                )
            print("\n   → These users need more guidance")
            print("   → Consider interactive tutorials or live demos")
            insights['onboarding_recommendations'].append(
                "Add extra support for cautious/learning personas"
            )

        # Time investment insights
        print(f"\n⏱️  TIME INVESTMENT PATTERNS:")
        for persona, data in sorted(persona_behaviors.items()):
            if data['time_invested']:
                avg_time = statistics.mean(data['time_invested'])
                print(f"   • {persona.replace('_', ' ').title()}: {avg_time:.1f} min")

        print("\n   → Ensure onboarding can be completed in 15-20 min")
        print("   → Break longer sessions into resumable chunks")
        insights['ux_considerations'].append(
            "Design for 15-20 minute first sessions with save points"
        )

        # Emotional journey insights
        print(f"\n🎭 EMOTIONAL JOURNEY INSIGHTS:")

        # Find personas with negative emotions
        negative_emotions = ['skeptical', 'anxious', 'frustrated', 'uncertain']
        personas_with_anxiety = []

        for persona, data in persona_behaviors.items():
            negative_count = sum(
                1 for e in data['emotional_states']
                if any(neg in e.lower() for neg in negative_emotions)
            )
            if negative_count / max(len(data['emotional_states']), 1) > 0.3:
                personas_with_anxiety.append(persona)

        if personas_with_anxiety:
            print("   ⚠️  Anxiety-prone personas:")
            for persona in personas_with_anxiety:
                print(f"      • {persona.replace('_', ' ').title()}")
            print("\n   → Add reassurance messaging during capture")
            print("   → Show immediate value (knowledge atoms generated)")
            insights['ux_considerations'].append(
                "Add real-time feedback during capture to reduce anxiety"
            )

        return insights

    def generate_scenario_report(self) -> None:
        """Generate comprehensive scenario report"""

        print("\n" + "="*80)
        print("📄 SCENARIO ANALYSIS REPORT")
        print("="*80)

        # First capture analysis
        insights = self.analyze_first_capture_session()

        # Summary recommendations
        print(f"\n{'='*80}")
        print("🎯 RECOMMENDATIONS FOR PRODUCT TEAM")
        print(f"{'='*80}\n")

        print("1️⃣  ONBOARDING OPTIMIZATION:")
        for rec in insights['onboarding_recommendations']:
            print(f"   • {rec}")

        print("\n2️⃣  UX IMPROVEMENTS:")
        for ux in insights['ux_considerations']:
            print(f"   • {ux}")

        print("\n3️⃣  SUPPORT STRATEGY:")
        for support in insights['support_needed']:
            print(f"   • {support}")

        print("\n4️⃣  SUCCESS PATTERNS:")
        for pattern in insights['success_patterns']:
            print(f"   • {pattern}")

        print("\n" + "="*80)
        print("✅ Analysis Complete!")
        print("="*80 + "\n")


def main():
    """Run scenario analysis"""
    data_file = "output/private_language_synthetic_users.json"

    if not Path(data_file).exists():
        print(f"❌ Data file not found: {data_file}")
        print("   Run: python cli.py generate private_language --count 100")
        return

    analyzer = ScenarioAnalyzer(data_file)
    analyzer.generate_scenario_report()


if __name__ == "__main__":
    main()
