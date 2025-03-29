# Synthetic Customer Dataset Generator

This project generates a synthetic dataset of 500 customers based on defined persona types and their characteristics. The dataset focuses on early risk detection and prevention, with a particular emphasis on younger demographics and life transitions. The dataset includes detailed profiles with demographic information, health data, life events, engagement patterns, and social determinants of health context.

## Project Structure

```
.
├── src/
│   ├── config/
│   │   └── persona_config.py    # Persona templates and configuration
│   ├── data_generation/
│   │   └── generator.py         # Core data generation logic
│   └── generate_dataset.py      # Script to run data generation
├── output/                      # Generated dataset output directory
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## Features

- Generates 500 synthetic customer profiles
- Five distinct persona types with realistic characteristics
- Focus on early risk detection and prevention
- Comprehensive profile data including:
  - Core demographic information
  - Health profiles and conditions
  - Life events and timeline
  - Platform engagement data
  - Narrative elements
  - Social determinants of health context

## Persona Types

1. **Health-Aware Avoiders (30%)**
   - High health awareness but low action tendency
   - Tend to avoid healthcare interactions
   - Often experience anxiety about health matters
   - Age range: 25-45 years

2. **Structured System-Seekers (25%)**
   - Highly organized approach to health
   - Regular engagement with healthcare systems
   - Strong preference for systematic processes
   - Age range: 30-50 years

3. **Balanced Life Integrators (20%)**
   - Balanced approach to health and wellness
   - Moderate engagement with healthcare
   - Focus on work-life balance
   - Age range: 28-48 years

4. **Healthcare Professionals (15%)**
   - Professional healthcare expertise
   - High engagement with healthcare systems
   - Systematic approach to health management
   - Age range: 25-45 years

5. **Overlooked Risk Group (10%)**
   - Lower engagement with healthcare
   - Multiple risk factors
   - Often prioritize other aspects of life
   - Age range: 30-50 years

## Age Distribution

The dataset focuses on early risk detection with the following age distribution:
- 20s: ~14%
- 30s: ~50%
- 40s: ~33%
- 50s: ~3%

This distribution emphasizes the "30-year threshold" where health awareness typically increases and early prevention becomes crucial.

## Risk Level Distribution

- Low Risk: ~71%
- Moderate Risk: ~29%

This distribution reflects the early detection focus, with most customers in lower risk categories where prevention is most impactful.

## Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the data generation script:
```bash
PYTHONPATH=src python3 src/generate_dataset.py
```

The script will:
1. Generate 500 synthetic customer profiles
2. Save the dataset to `output/synthetic_customers.json`
3. Print statistics about the generated dataset

## Output Format

The generated dataset is saved in JSON format with the following structure:

```json
{
  "customer_id": "uuid",
  "persona_type": "string",
  "core_profile": {
    "age": "integer",
    "gender": "string",
    "education": "string",
    "location": "object"
  },
  "health_profile": {
    "risk_level": "string",
    "conditions": "array",
    "screening_history": "object"
  },
  "life_events": "array",
  "engagement_data": "object",
  "narrative_elements": "object",
  "sdoh_context": "object"
}
```

## Customization

You can modify the following aspects of the data generation:

1. Persona characteristics in `src/config/persona_config.py`
2. Risk probabilities and distributions
3. Life event types and frequencies
4. Engagement patterns and metrics

## Development

The project uses:
- Python 3.8+
- Pandas for data manipulation
- Faker for generating realistic data
- Type hints for better code maintainability

## License

MIT License