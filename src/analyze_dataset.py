import json
from collections import Counter
from pathlib import Path
import statistics

def load_dataset(file_path: str) -> list:
    with open(file_path, 'r') as f:
        return json.load(f)

def analyze_dataset(customers: list) -> None:
    print("\nDetailed Dataset Analysis")
    print("-" * 50)
    
    # Gender distribution
    genders = Counter(c['coreProfile']['gender'] for c in customers)
    print("\nGender Distribution:")
    for gender, count in genders.items():
        print(f"  {gender}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Race/Ethnicity distribution
    race_ethnicity = Counter(c['coreProfile']['raceEthnicity'] for c in customers)
    print("\nRace/Ethnicity Distribution:")
    for race, count in race_ethnicity.items():
        print(f"  {race}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Age distribution by decade
    ages = [c['coreProfile']['age'] for c in customers]
    age_decades = Counter((age // 10) * 10 for age in ages)
    print("\nAge Distribution by Decade:")
    for decade, count in sorted(age_decades.items()):
        print(f"  {decade}s: {count} ({count/len(customers)*100:.1f}%)")
    
    # Education distribution
    education = Counter(c['coreProfile']['education'] for c in customers)
    print("\nEducation Distribution:")
    for edu, count in education.items():
        print(f"  {edu}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Location type distribution
    locations = Counter(c['coreProfile']['location']['type'] for c in customers)
    print("\nLocation Type Distribution:")
    for loc, count in locations.items():
        print(f"  {loc}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Breast cancer risk analysis
    risk_levels = Counter(c['healthProfile']['breastCancerRisk']['riskLevel'] for c in customers)
    print("\nBreast Cancer Risk Level Distribution:")
    for level, count in risk_levels.items():
        print(f"  {level}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Average risk by age group
    print("\nAverage Breast Cancer Risk by Age Group:")
    age_groups = {
        "20-39": [],
        "40-49": [],
        "50-59": [],
        "60-69": [],
        "70+": []
    }
    
    for customer in customers:
        age = customer['coreProfile']['age']
        risk = customer['healthProfile']['breastCancerRisk']['adjustedRisk']
        
        if age < 40:
            age_groups["20-39"].append(risk)
        elif age < 50:
            age_groups["40-49"].append(risk)
        elif age < 60:
            age_groups["50-59"].append(risk)
        elif age < 70:
            age_groups["60-69"].append(risk)
        else:
            age_groups["70+"].append(risk)
    
    for group, risks in age_groups.items():
        if risks:
            print(f"  {group}: {statistics.mean(risks)*100:.1f}%")
    
    # Mammogram screening analysis
    mammogram_stats = {
        "has_history": 0,
        "annual": 0,
        "biennial": 0,
        "irregular": 0,
        "never": 0
    }
    
    for customer in customers:
        mammogram = customer['healthProfile']['preventiveCare']['mammogramHistory']
        mammogram_stats["has_history"] += 1 if mammogram["hasHistory"] else 0
        mammogram_stats[mammogram["frequency"]] += 1
    
    print("\nMammogram Screening Distribution:")
    print(f"  Has History: {mammogram_stats['has_history']} ({mammogram_stats['has_history']/len(customers)*100:.1f}%)")
    print(f"  Annual: {mammogram_stats['annual']} ({mammogram_stats['annual']/len(customers)*100:.1f}%)")
    print(f"  Biennial: {mammogram_stats['biennial']} ({mammogram_stats['biennial']/len(customers)*100:.1f}%)")
    print(f"  Irregular: {mammogram_stats['irregular']} ({mammogram_stats['irregular']/len(customers)*100:.1f}%)")
    print(f"  Never: {mammogram_stats['never']} ({mammogram_stats['never']/len(customers)*100:.1f}%)")
    
    # Risk factors analysis
    all_risk_factors = []
    for customer in customers:
        all_risk_factors.extend(customer['healthProfile']['riskFactors'])
    risk_factors = Counter(all_risk_factors)
    
    print("\nTop Risk Factors:")
    for factor, count in risk_factors.most_common(5):
        print(f"  {factor}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Chronic conditions analysis
    all_conditions = []
    for customer in customers:
        all_conditions.extend(customer['healthProfile']['chronicConditions'])
    conditions = Counter(all_conditions)
    
    print("\nTop Chronic Conditions:")
    for condition, count in conditions.most_common(5):
        print(f"  {condition}: {count} ({count/len(customers)*100:.1f}%)")
    
    # Anxiety level analysis
    anxiety_levels = [c['healthProfile']['anxietyLevel'] for c in customers]
    print("\nAnxiety Level Statistics:")
    print(f"  Mean: {statistics.mean(anxiety_levels):.2f}")
    print(f"  Median: {statistics.median(anxiety_levels):.2f}")
    print(f"  Std Dev: {statistics.stdev(anxiety_levels):.2f}")
    
    # Life events analysis
    events_per_person = [len(c['lifeEvents']['lifeEvents']) for c in customers]
    print("\nLife Events Statistics:")
    print(f"  Average events per person: {statistics.mean(events_per_person):.1f}")
    print(f"  Max events: {max(events_per_person)}")
    print(f"  Min events: {min(events_per_person)}")

def main():
    dataset_path = Path('output/synthetic_customers.json')
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {dataset_path}")
        return
    
    customers = load_dataset(dataset_path)
    analyze_dataset(customers)

if __name__ == '__main__':
    main() 