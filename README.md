# Synthetic Customer Dataset Generator

This project generates a synthetic dataset of 500 customers based on defined persona types and their characteristics. The dataset includes detailed profiles with demographic information, health data, life events, engagement patterns, and social determinants of health context.

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

2. **Structured System-Seekers (25%)**
   - Highly organized approach to health
   - Regular engagement with healthcare systems
   - Strong preference for systematic processes

3. **Balanced Life Integrators (20%)**
   - Balanced approach to health and wellness
   - Moderate engagement with healthcare
   - Focus on work-life balance

4. **Healthcare Professionals (15%)**
   - Professional healthcare expertise
   - High engagement with healthcare systems
   - Systematic approach to health management

5. **Overlooked Risk Group (10%)**
   - Lower engagement with healthcare
   - Multiple risk factors
   - Often prioritize other aspects of life

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the data generation script:
```bash
python src/generate_dataset.py
```

This will:
1. Generate 500 synthetic customer profiles
2. Save the dataset to `output/synthetic_customers.json`
3. Print statistics about the generated dataset

## Output Format

The generated dataset is saved as a JSON file with the following structure:

```json
[
  {
    "id": "uuid",
    "personaType": "persona_type",
    "coreProfile": {
      "name": "string",
      "age": number,
      "gender": "string",
      "education": "string",
      "occupation": "string",
      "location": {
        "city": "string",
        "state": "string",
        "zipCode": "string",
        "type": "string"
      },
      "maritalStatus": "string"
    },
    "healthProfile": {
      "height": number,
      "weight": number,
      "chronicConditions": ["string"],
      "preventiveCare": {
        "screeningCompletion": number,
        "lastScreening": "string"
      },
      "anxietyLevel": number
    },
    "lifeEvents": {
      "lifeEvents": [
        {
          "id": "uuid",
          "type": "string",
          "subCategory": "string",
          "timestamp": "string",
          "title": "string",
          "impact": {
            "riskImpact": "string",
            "preventionOpportunity": "string",
            "supportNeeds": ["string"]
          },
          "status": "string"
        }
      ],
      "anticipatedEvents": [...]
    },
    "engagementData": {
      "platformEngagement": {
        "visitFrequency": "string",
        "sessionDuration": {
          "average": number,
          "pattern": "string"
        },
        "visitHistory": [...]
      }
    },
    "narrativeElements": {
      "healthNarrative": {
        "selfDescription": "string",
        "relationshipToHealthcare": "string"
      }
    },
    "sdohContext": {
      "areaLevel": {
        "currentLocation": {
          "censusTract": "string",
          "indices": {
            "adi": number
          }
        },
        "characteristics": {
          "populationDensity": "string",
          "healthcareAccess": "string",
          "stressLevel": "string"
        }
      },
      "individualLevel": {
        "financialStability": {
          "incomeCategory": "string",
          "insuranceStatus": "string"
        },
        "socialSupport": {
          "networkSize": number,
          "supportLevel": "string"
        }
      }
    }
  }
]
```

## Customization

You can modify the persona characteristics and distributions in `src/config/persona_config.py`. The configuration includes:

- Persona distribution percentages
- Age ranges for each persona
- Gender and education distributions
- Health condition probabilities
- Life event types and characteristics
- Location types and their characteristics
- Engagement metrics

## Development

To modify or extend the data generation:

1. Update the persona templates in `persona_config.py`
2. Modify the generation logic in `generator.py`
3. Add new validation or analysis in `generate_dataset.py`

## License

MIT License