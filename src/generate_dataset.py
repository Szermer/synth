import json
from pathlib import Path
from typing import Dict, List

from data_generation.generator import CustomerDataGenerator


def save_dataset(customers: List[Dict], output_path: str) -> None:
    """Save the generated dataset to a JSON file."""
    with open(output_path, "w") as f:
        json.dump(customers, f, indent=2)


def print_dataset_stats(customers: List[Dict]) -> None:
    """Print statistics about the generated dataset."""
    # Count customers by persona type
    persona_counts = {}
    for customer in customers:
        persona_type = customer["personaType"]
        persona_counts[persona_type] = persona_counts.get(persona_type, 0) + 1
    
    print("\nDataset Statistics:")
    print("-" * 50)
    print(f"Total customers: {len(customers)}")
    print("\nCustomers by persona type:")
    for persona_type, count in persona_counts.items():
        percentage = (count / len(customers)) * 100
        print(f"  {persona_type}: {count} ({percentage:.1f}%)")
    
    # Calculate average age by persona type
    print("\nAverage age by persona type:")
    age_sums = {}
    age_counts = {}
    for customer in customers:
        persona_type = customer["personaType"]
        age = customer["coreProfile"]["age"]
        age_sums[persona_type] = age_sums.get(persona_type, 0) + age
        age_counts[persona_type] = age_counts.get(persona_type, 0) + 1
    
    for persona_type in age_sums:
        avg_age = age_sums[persona_type] / age_counts[persona_type]
        print(f"  {persona_type}: {avg_age:.1f} years")
    
    # Calculate average screening completion by persona type
    print("\nAverage screening completion by persona type:")
    screening_sums = {}
    screening_counts = {}
    for customer in customers:
        persona_type = customer["personaType"]
        screening = customer["healthProfile"]["preventiveCare"]["screeningCompletion"]
        screening_sums[persona_type] = screening_sums.get(persona_type, 0) + screening
        screening_counts[persona_type] = screening_counts.get(persona_type, 0) + 1
    
    for persona_type in screening_sums:
        avg_screening = screening_sums[persona_type] / screening_counts[persona_type]
        print(f"  {persona_type}: {avg_screening:.2%}")


def main():
    """Generate and save the synthetic customer dataset."""
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate dataset
    print("Generating synthetic customer dataset...")
    generator = CustomerDataGenerator(total_customers=500)
    customers = generator.generate()
    
    # Save dataset
    output_path = output_dir / "synthetic_customers.json"
    save_dataset(customers, str(output_path))
    print(f"\nDataset saved to {output_path}")
    
    # Print statistics
    print_dataset_stats(customers)


if __name__ == "__main__":
    main() 