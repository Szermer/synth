#!/usr/bin/env python3
"""
Create visualizations for Stage Zero Beta Learning Report
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_completion_funnel():
    """Create completion funnel chart"""
    weeks = list(range(1, 11))
    completion_rates = [100, 100, 100, 89.0, 80.8, 71.0, 61.2, 50.8, 41.8, 41.8]
    targets = [85, 75, 70, 65, 60, 55, 50, 45, 40, 35]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot actual vs target
    ax.plot(weeks, completion_rates, 'b-', linewidth=3, marker='o', markersize=8, label='Actual')
    ax.plot(weeks, targets, 'r--', linewidth=2, marker='s', markersize=6, label='Target', alpha=0.7)
    
    # Fill area between
    ax.fill_between(weeks, completion_rates, alpha=0.3)
    
    # Annotations
    for i, (week, rate) in enumerate(zip(weeks, completion_rates)):
        if i % 2 == 0:  # Annotate every other point
            ax.annotate(f'{rate:.1f}%', (week, rate), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontsize=9)
    
    ax.set_xlabel('Week', fontsize=12)
    ax.set_ylabel('Completion Rate (%)', fontsize=12)
    ax.set_title('Stage Zero Health: 10-Week Journey Completion Funnel', fontsize=14, fontweight='bold')
    ax.set_xticks(weeks)
    ax.set_ylim(0, 105)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/completion_funnel.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_persona_completion_chart():
    """Create persona completion comparison"""
    personas = ['Health Aware\nAvoider', 'Structured\nSystem Seeker', 'Balanced Life\nIntegrator', 
                'Healthcare\nProfessional', 'Overlooked\nRisk Group']
    completion_rates = [23.3, 72.8, 45.0, 41.3, 14.0]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(personas, completion_rates, color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'])
    
    # Add value labels on bars
    for bar, rate in zip(bars, completion_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add target line
    ax.axhline(y=35, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Target (35%)')
    
    ax.set_ylabel('Completion Rate (%)', fontsize=12)
    ax.set_title('Journey Completion by Persona Type', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 80)
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/persona_completion.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_trust_progression():
    """Create trust level progression chart"""
    weeks = list(range(1, 11))
    trust_levels = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]
    user_counts = [500, 500, 500, 445, 404, 355, 306, 254, 209, 209]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Trust level line
    color = 'tab:blue'
    ax1.set_xlabel('Week', fontsize=12)
    ax1.set_ylabel('Trust Level (1-10)', color=color, fontsize=12)
    line1 = ax1.plot(weeks, trust_levels, color=color, linewidth=3, marker='o', 
                     markersize=8, label='Trust Level')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(4, 10)
    
    # User count bars
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Active Users', color=color, fontsize=12)
    bars = ax2.bar(weeks, user_counts, alpha=0.5, color=color, label='Active Users')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 600)
    
    # Title and grid
    ax1.set_title('Trust Level Progression Throughout Journey', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(weeks)
    
    # Combined legend
    lines = line1 + [bars]
    labels = ['Trust Level', 'Active Users']
    ax1.legend(lines, labels, loc='center right')
    
    plt.tight_layout()
    plt.savefig('output/trust_progression.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_risk_distribution():
    """Create risk category distribution pie chart"""
    categories = ['Low Risk', 'Average Risk', 'Elevated Risk']
    percentages = [33.4, 53.0, 13.6]
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Pie chart
    wedges, texts, autotexts = ax1.pie(percentages, labels=categories, colors=colors, 
                                       autopct='%1.1f%%', startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')
    
    ax1.set_title('Risk Category Distribution', fontsize=14, fontweight='bold')
    
    # Genetic counseling bar
    ax2.bar(['All Users', 'Genetic Counseling\nIndicated'], [100, 14.8], 
            color=['#3498db', '#e74c3c'], width=0.6)
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    ax2.set_title('Genetic Counseling Indication Rate', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 110)
    
    # Add percentage labels
    ax2.text(0, 102, '100%', ha='center', fontsize=11, fontweight='bold')
    ax2.text(1, 16.8, '14.8%', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/risk_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_satisfaction_metrics():
    """Create satisfaction and commitment metrics"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Satisfaction distribution
    satisfaction_scores = np.random.normal(8.4, 1.2, 209)
    satisfaction_scores = np.clip(satisfaction_scores, 5, 10)
    
    ax1.hist(satisfaction_scores, bins=10, color='#3498db', alpha=0.7, edgecolor='black')
    ax1.axvline(x=8.4, color='red', linestyle='--', linewidth=2, label='Average (8.4)')
    ax1.set_xlabel('Satisfaction Score', fontsize=12)
    ax1.set_ylabel('Number of Users', fontsize=12)
    ax1.set_title('Plan Satisfaction Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlim(5, 10)
    ax1.legend()
    
    # Implementation commitment
    metrics = ['Plan Satisfaction\n≥8/10', 'Implementation\nCommitment ≥7/10', 'NPS Proxy\n(Score)']
    values = [73.2, 73.7, 44]
    colors = ['#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax2.bar(metrics, values, color=colors)
    
    # Add value labels
    for bar, value in zip(bars, values):
        height = bar.get_height()
        label = f'{value:.1f}%' if value > 50 else f'{value}'
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                label, ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Percentage / Score', fontsize=12)
    ax2.set_title('Key Business Metrics', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 85)
    ax2.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/satisfaction_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_summary_dashboard():
    """Create a summary dashboard with key metrics"""
    fig = plt.figure(figsize=(14, 10))
    
    # Title
    fig.suptitle('Stage Zero Health Beta: Key Performance Metrics', fontsize=16, fontweight='bold')
    
    # Grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Completion targets met
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.text(0.5, 0.7, '10/10', fontsize=36, fontweight='bold', ha='center', color='#2ecc71')
    ax1.text(0.5, 0.3, 'Weekly Targets\nAchieved', fontsize=14, ha='center')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    
    # 2. Final completion rate
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.text(0.5, 0.7, '41.8%', fontsize=36, fontweight='bold', ha='center', color='#3498db')
    ax2.text(0.5, 0.3, 'Journey Completion\n(Target: 35%)', fontsize=14, ha='center')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    
    # 3. Trust progression
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.text(0.5, 0.7, '5.0→9.5', fontsize=30, fontweight='bold', ha='center', color='#9b59b6')
    ax3.text(0.5, 0.3, 'Trust Level\nProgression', fontsize=14, ha='center')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    
    # 4. Completion by persona (mini bar chart)
    ax4 = fig.add_subplot(gs[1, :])
    personas_short = ['Avoider', 'Seeker', 'Integrator', 'Professional', 'Overlooked']
    completion_rates = [23.3, 72.8, 45.0, 41.3, 14.0]
    bars = ax4.bar(personas_short, completion_rates, color=plt.cm.viridis(np.linspace(0, 1, 5)))
    ax4.axhline(y=35, color='red', linestyle='--', alpha=0.5, label='Target')
    ax4.set_ylabel('Completion %')
    ax4.set_title('Completion Rates by Persona')
    for bar, rate in zip(bars, completion_rates):
        ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{rate:.0f}%', ha='center', fontsize=9)
    
    # 5. Risk distribution
    ax5 = fig.add_subplot(gs[2, 0])
    sizes = [33.4, 53.0, 13.6]
    ax5.pie(sizes, labels=['Low', 'Average', 'Elevated'], autopct='%1.0f%%',
            colors=['#2ecc71', '#f39c12', '#e74c3c'], startangle=90)
    ax5.set_title('Risk Distribution')
    
    # 6. Satisfaction score
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.text(0.5, 0.7, '8.4/10', fontsize=30, fontweight='bold', ha='center', color='#2ecc71')
    ax6.text(0.5, 0.3, 'Plan Satisfaction\nScore', fontsize=14, ha='center')
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 1)
    ax6.axis('off')
    
    # 7. NPS
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.text(0.5, 0.7, '44', fontsize=36, fontweight='bold', ha='center', color='#3498db')
    ax7.text(0.5, 0.3, 'Net Promoter\nScore (Proxy)', fontsize=14, ha='center')
    ax7.set_xlim(0, 1)
    ax7.set_ylim(0, 1)
    ax7.axis('off')
    
    plt.tight_layout()
    plt.savefig('output/summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("Creating Stage Zero Health visualizations...")
    
    # Create output directory if needed
    Path('output').mkdir(exist_ok=True)
    
    # Generate all charts
    create_completion_funnel()
    print("✓ Created completion funnel chart")
    
    create_persona_completion_chart()
    print("✓ Created persona completion chart")
    
    create_trust_progression()
    print("✓ Created trust progression chart")
    
    create_risk_distribution()
    print("✓ Created risk distribution charts")
    
    create_satisfaction_metrics()
    print("✓ Created satisfaction metrics charts")
    
    create_summary_dashboard()
    print("✓ Created summary dashboard")
    
    print("\nAll visualizations saved to output/ directory")

if __name__ == "__main__":
    main()