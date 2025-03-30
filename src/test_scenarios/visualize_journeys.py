import json
from pathlib import Path
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def load_analysis_results() -> Dict[str, Any]:
    """Load the journey analysis results."""
    with open("output/test_scenarios/journey_analysis.json", "r") as f:
        return json.load(f)

def create_emotional_state_heatmap(analysis_results: Dict[str, Any]) -> None:
    """Create a heatmap of emotional states across persona types."""
    # Prepare data
    emotional_data = []
    for persona_type, states in analysis_results["emotional_states"].items():
        total = sum(states.values())
        row = {
            "Persona Type": persona_type.replace("_", " ").title(),
            **{state: (count/total)*100 for state, count in states.items()}
        }
        emotional_data.append(row)
    
    df = pd.DataFrame(emotional_data)
    
    # Create heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        df.set_index("Persona Type"),
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        cbar_kws={"label": "Percentage"}
    )
    plt.title("Emotional State Distribution by Persona Type")
    plt.tight_layout()
    plt.savefig("output/test_scenarios/emotional_states_heatmap.png")
    plt.close()

def create_completion_rates_barplot(analysis_results: Dict[str, Any]) -> None:
    """Create a bar plot of completion rates across steps and persona types."""
    # Prepare data
    completion_data = []
    for persona_type, steps in analysis_results["completion_rates"].items():
        for step, stats in steps.items():
            completion_data.append({
                "Persona Type": persona_type.replace("_", " ").title(),
                "Step": step.replace("_", " ").title(),
                "Completion Rate": (stats["completed"]/stats["total"])*100
            })
    
    df = pd.DataFrame(completion_data)
    
    # Create bar plot
    plt.figure(figsize=(15, 8))
    sns.barplot(
        data=df,
        x="Step",
        y="Completion Rate",
        hue="Persona Type",
        palette="Set3"
    )
    plt.xticks(rotation=45, ha="right")
    plt.title("Step Completion Rates by Persona Type")
    plt.tight_layout()
    plt.savefig("output/test_scenarios/completion_rates_barplot.png")
    plt.close()

def create_journey_duration_boxplot(analysis_results: Dict[str, Any]) -> None:
    """Create a box plot of journey durations across persona types."""
    # Prepare data
    duration_data = []
    for persona_type, stats in analysis_results["journey_durations"].items():
        duration_data.append({
            "Persona Type": persona_type.replace("_", " ").title(),
            "Average Duration (days)": float(stats["avg_days"])
        })
    
    df = pd.DataFrame(duration_data)
    
    # Create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x="Persona Type",
        y="Average Duration (days)",
        hue="Persona Type",
        legend=False
    )
    plt.xticks(rotation=45, ha="right")
    plt.title("Average Journey Duration by Persona Type")
    plt.tight_layout()
    plt.savefig("output/test_scenarios/journey_duration_barplot.png")
    plt.close()

def create_risk_level_distribution(analysis_results: Dict[str, Any]) -> None:
    """Create a stacked bar chart of risk level distribution."""
    # Prepare data
    risk_data = []
    for persona_type, risks in analysis_results["risk_levels"].items():
        total = sum(risks.values())
        risk_data.append({
            "Persona Type": persona_type.replace("_", " ").title(),
            "Low Risk": (risks["low"]/total)*100,
            "Moderate Risk": (risks["moderate"]/total)*100
        })
    
    df = pd.DataFrame(risk_data)
    
    # Create stacked bar chart
    plt.figure(figsize=(10, 6))
    df.plot(
        x="Persona Type",
        kind="bar",
        stacked=True,
        colormap="RdYlGn"
    )
    plt.xticks(rotation=45, ha="right")
    plt.title("Risk Level Distribution by Persona Type")
    plt.ylabel("Percentage")
    plt.legend(title="Risk Level")
    plt.tight_layout()
    plt.savefig("output/test_scenarios/risk_level_distribution.png")
    plt.close()

def create_expected_outcomes_heatmap(analysis_results: Dict[str, Any]) -> None:
    """Create a heatmap of expected outcomes across persona types."""
    # Prepare data
    outcome_data = []
    for persona_type, outcomes in analysis_results["expected_outcomes"].items():
        row = {
            "Persona Type": persona_type.replace("_", " ").title(),
            **{outcome.replace("_", " ").title(): int(count) 
               for outcome, count in outcomes.items()}
        }
        outcome_data.append(row)
    
    df = pd.DataFrame(outcome_data)
    
    # Create heatmap
    plt.figure(figsize=(15, 8))
    sns.heatmap(
        df.set_index("Persona Type"),
        annot=True,
        fmt="g",
        cmap="YlOrRd",
        cbar_kws={"label": "Count"}
    )
    plt.title("Expected Outcomes by Persona Type")
    plt.tight_layout()
    plt.savefig("output/test_scenarios/expected_outcomes_heatmap.png")
    plt.close()

def create_journey_patterns_dashboard(analysis_results: Dict[str, Any]) -> None:
    """Create a comprehensive dashboard of journey patterns."""
    # Create output directory if it doesn't exist
    output_dir = Path("output/test_scenarios")
    output_dir.mkdir(exist_ok=True)
    
    # Generate all visualizations
    create_emotional_state_heatmap(analysis_results)
    create_completion_rates_barplot(analysis_results)
    create_journey_duration_boxplot(analysis_results)
    create_risk_level_distribution(analysis_results)
    create_expected_outcomes_heatmap(analysis_results)
    
    print("Visualizations have been generated and saved to output/test_scenarios/")

def main():
    """Generate visualizations of journey patterns."""
    analysis_results = load_analysis_results()
    create_journey_patterns_dashboard(analysis_results)

if __name__ == "__main__":
    main() 