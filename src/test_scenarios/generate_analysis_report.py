import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from datetime import datetime

def load_analysis_results() -> Dict[str, Any]:
    """Load the journey analysis results."""
    with open("output/test_scenarios/journey_analysis.json", "r") as f:
        return json.load(f)

def generate_persona_insights(analysis_results: Dict[str, Any]) -> str:
    """Generate detailed insights for each persona type."""
    insights = []
    
    for persona_type, data in analysis_results.items():
        if persona_type in ["emotional_states", "completion_rates", "journey_durations", "risk_levels", "expected_outcomes"]:
            continue
            
        persona_name = persona_type.replace("_", " ").title()
        insights.append(f"\n## {persona_name} Analysis")
        
        # Emotional Profile
        emotional_states = analysis_results["emotional_states"][persona_type]
        total_emotional = sum(emotional_states.values())
        primary_emotion = max(emotional_states.items(), key=lambda x: x[1])[0]
        primary_percentage = (emotional_states[primary_emotion] / total_emotional) * 100
        
        insights.append(f"\n### Emotional Profile")
        insights.append(f"- Primary emotional state: {primary_emotion.replace('_', ' ').title()} ({primary_percentage:.1f}%)")
        insights.append(f"- Key emotional patterns:")
        for emotion, count in emotional_states.items():
            percentage = (count / total_emotional) * 100
            insights.append(f"  * {emotion.replace('_', ' ').title()}: {percentage:.1f}%")
        
        # Journey Completion
        completion_rates = analysis_results["completion_rates"][persona_type]
        insights.append(f"\n### Journey Completion")
        for step, stats in completion_rates.items():
            rate = (stats["completed"] / stats["total"]) * 100
            insights.append(f"- {step.replace('_', ' ').title()}: {rate:.1f}% completion rate")
        
        # Journey Duration
        duration_stats = analysis_results["journey_durations"][persona_type]
        insights.append(f"\n### Journey Duration")
        insights.append(f"- Average duration: {duration_stats['avg_days']:.1f} days")
        
        # Risk Levels
        risk_levels = analysis_results["risk_levels"][persona_type]
        total_risks = sum(risk_levels.values())
        insights.append(f"\n### Risk Profile")
        for risk, count in risk_levels.items():
            percentage = (count / total_risks) * 100
            insights.append(f"- {risk.replace('_', ' ').title()}: {percentage:.1f}%")
        
        # Expected Outcomes
        outcomes = analysis_results["expected_outcomes"][persona_type]
        total_outcomes = sum(outcomes.values())
        insights.append(f"\n### Expected Outcomes")
        for outcome, count in outcomes.items():
            percentage = (count / total_outcomes) * 100
            insights.append(f"- {outcome.replace('_', ' ').title()}: {percentage:.1f}%")
    
    return "\n".join(insights)

def generate_key_findings(analysis_results: Dict[str, Any]) -> str:
    """Generate key findings and patterns across all personas."""
    findings = ["## Key Findings and Patterns"]
    
    # Emotional Patterns
    findings.append("\n### Emotional Patterns")
    emotional_patterns = []
    for persona_type, states in analysis_results["emotional_states"].items():
        total = sum(states.values())
        primary_emotion = max(states.items(), key=lambda x: x[1])[0]
        percentage = (states[primary_emotion] / total) * 100
        emotional_patterns.append(f"- {persona_type.replace('_', ' ').title()}: {primary_emotion.replace('_', ' ').title()} ({percentage:.1f}%)")
    findings.extend(emotional_patterns)
    
    # Completion Patterns
    findings.append("\n### Journey Completion Patterns")
    completion_patterns = []
    for persona_type, steps in analysis_results["completion_rates"].items():
        avg_completion = sum((s["completed"] / s["total"]) * 100 for s in steps.values()) / len(steps)
        completion_patterns.append(f"- {persona_type.replace('_', ' ').title()}: {avg_completion:.1f}% average completion rate")
    findings.extend(completion_patterns)
    
    # Duration Patterns
    findings.append("\n### Journey Duration Patterns")
    duration_patterns = []
    for persona_type, stats in analysis_results["journey_durations"].items():
        duration_patterns.append(f"- {persona_type.replace('_', ' ').title()}: {stats['avg_days']:.1f} days average")
    findings.extend(duration_patterns)
    
    # Risk Patterns
    findings.append("\n### Risk Level Patterns")
    risk_patterns = []
    for persona_type, risks in analysis_results["risk_levels"].items():
        total = sum(risks.values())
        moderate_risk = (risks["moderate"] / total) * 100
        risk_patterns.append(f"- {persona_type.replace('_', ' ').title()}: {moderate_risk:.1f}% moderate risk")
    findings.extend(risk_patterns)
    
    return "\n".join(findings)

def generate_recommendations(analysis_results: Dict[str, Any]) -> str:
    """Generate actionable recommendations based on the analysis."""
    recommendations = ["## Recommendations"]
    
    # Persona-specific recommendations
    recommendations.append("\n### Persona-Specific Recommendations")
    
    # Health Aware Avoider recommendations
    recommendations.append("\n#### Health Aware Avoider")
    recommendations.append("- Implement anxiety-reduction techniques in the user interface")
    recommendations.append("- Provide clear, step-by-step guidance with progress indicators")
    recommendations.append("- Offer educational content to build confidence")
    
    # Structured System Seeker recommendations
    recommendations.append("\n#### Structured System Seeker")
    recommendations.append("- Provide detailed scheduling and planning tools")
    recommendations.append("- Implement systematic progress tracking")
    recommendations.append("- Offer customizable organization features")
    
    # Balanced Life Integrator recommendations
    recommendations.append("\n#### Balanced Life Integrator")
    recommendations.append("- Design flexible scheduling options")
    recommendations.append("- Provide integration with existing calendar systems")
    recommendations.append("- Offer quick-access features for busy schedules")
    
    # Healthcare Professional recommendations
    recommendations.append("\n#### Healthcare Professional")
    recommendations.append("- Provide advanced analytics and reporting tools")
    recommendations.append("- Offer integration with professional healthcare systems")
    recommendations.append("- Implement time-saving automation features")
    
    # Overlooked Risk Group recommendations
    recommendations.append("\n#### Overlooked Risk Group")
    recommendations.append("- Implement proactive outreach and engagement features")
    recommendations.append("- Provide simplified, accessible interfaces")
    recommendations.append("- Offer personalized risk assessment tools")
    
    # General recommendations
    recommendations.append("\n### General Recommendations")
    recommendations.append("- Implement personalized journey paths based on persona type")
    recommendations.append("- Develop targeted support resources for each persona")
    recommendations.append("- Create flexible scheduling options to accommodate different journey durations")
    recommendations.append("- Design risk assessment tools that adapt to persona characteristics")
    recommendations.append("- Develop comprehensive outcome tracking and reporting systems")
    
    return "\n".join(recommendations)

def generate_report() -> None:
    """Generate a comprehensive analysis report."""
    analysis_results = load_analysis_results()
    
    # Create report content
    report = [
        "# Persona Journey Analysis Report",
        f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n## Executive Summary",
        "This report provides a comprehensive analysis of persona journeys across different user types, ",
        "including emotional patterns, completion rates, journey durations, risk levels, and expected outcomes. ",
        "The analysis is based on detailed journey data and provides actionable recommendations for optimization.",
        generate_key_findings(analysis_results),
        generate_persona_insights(analysis_results),
        generate_recommendations(analysis_results)
    ]
    
    # Save report
    output_dir = Path("output/test_scenarios")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "journey_analysis_report.md", "w") as f:
        f.write("\n".join(report))
    
    print("Analysis report has been generated and saved to output/test_scenarios/journey_analysis_report.md")

if __name__ == "__main__":
    generate_report() 