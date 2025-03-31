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
│   ├── test_scenarios/
│   │   ├── generate_test_scenarios.py    # Generate test scenarios
│   │   ├── analyze_journeys.py           # Analyze persona journeys
│   │   ├── visualize_journeys.py         # Create journey visualizations
│   │   ├── test_execution_framework.py   # Test execution framework
│   │   └── validate_journey_phases.py    # Journey phase validation
│   └── generate_dataset.py      # Script to run data generation
├── output/                      # Generated dataset output directory
│   └── test_scenarios/         # Test results and visualizations
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
- Test execution framework for validation
- Journey analysis and visualization capabilities
- Journey phase validation framework

## Customer Journey Framework

The project implements a comprehensive customer journey framework with four key phases:

### 1. Awareness Phase
- Initial discovery and connection
- Emotional state validation
- Initial concern and curiosity assessment
- Marketing content alignment

### 2. Engagement Phase
- Risk assessment completion
- Narrative capture
- Life events timeline creation
- Progressive engagement tracking

### 3. Action Phase
- Prevention plan development
- Support plan creation
- Action planning
- Motivation assessment

### 4. Continuity Phase
- Follow-up engagement
- Risk awareness maintenance
- Barrier identification
- Stability monitoring

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

### Generate Dataset

Run the data generation script:
```bash
PYTHONPATH=src python3 src/generate_dataset.py
```

### Generate Test Scenarios

Generate test scenarios for different persona types:
```bash
PYTHONPATH=src python3 src/test_scenarios/generate_test_scenarios.py
```

### Analyze Journeys

Analyze persona journeys and generate insights:
```bash
PYTHONPATH=src python3 src/test_scenarios/analyze_journeys.py
```

### Visualize Journeys

Create visualizations of journey patterns:
```bash
PYTHONPATH=src python3 src/test_scenarios/visualize_journeys.py
```

### Run Test Framework

Execute the test framework to validate data quality:
```bash
PYTHONPATH=src python3 src/test_scenarios/test_execution_framework.py
```

### Validate Journey Phases

Run the journey phase validation:
```bash
PYTHONPATH=src python3 src/test_scenarios/validate_journey_phases.py
```

## Test Framework

The project includes a comprehensive test execution framework that validates:

1. **Persona Distribution**
   - Validates correct distribution of persona types
   - Ensures adherence to target percentages
   - Checks consistency across scenario types

2. **Emotional States**
   - Validates emotional state patterns
   - Ensures appropriate distribution of emotions
   - Checks consistency in emotional profiles

3. **Journey Completion**
   - Validates completion rates for each step
   - Ensures logical progression through journeys
   - Checks consistency in completion patterns

4. **Risk Levels**
   - Validates risk level distribution
   - Ensures appropriate risk profiles per persona
   - Checks consistency in risk assessment

5. **Scenario Consistency**
   - Validates consistency across scenario types
   - Ensures persona type consistency
   - Checks data structure integrity

6. **Journey Phase Validation**
   - Validates Awareness phase emotional progression
   - Checks Engagement phase completion rates
   - Monitors Action phase motivation levels
   - Tracks Continuity phase stability
   - Analyzes phase transitions

## Output Format

The generated dataset is saved in JSON format with the following structure:

```json
{
  "scenario_type": "first_time_user",
  "user": {
    "name": "string",
    "age": number,
    "persona_type": "string",
    "risk_level": "string",
    "screening_history": {
      "has_history": boolean,
      "frequency": "string",
      "last_screening": "string|null",
      "completion_rate": number
    }
  },
  "journey": [
    {
      "step": "string",
      "timestamp": "string",
      "actions": ["string"],
      "emotional_state": "string",
      "completion_status": "string"
    }
  ]
}
```

## Customization

You can customize the following aspects:

1. **Persona Characteristics**
   - Modify persona types and their characteristics
   - Adjust distribution percentages
   - Update emotional state patterns

2. **Journey Steps**
   - Add or modify journey steps
   - Update completion criteria
   - Modify emotional state transitions

3. **Risk Assessment**
   - Adjust risk level criteria
   - Modify risk distribution
   - Update risk factors

4. **Journey Phases**
   - Customize phase validation criteria
   - Modify phase transition rules
   - Update emotional state requirements

## Development

The project uses:
- Python 3.8+
- Pandas for data manipulation
- Faker for generating realistic data
- Type hints for better code maintainability

To extend or modify the data generation:

1. **Add New Persona Types**
   - Update `persona_config.py`
   - Add new persona characteristics
   - Update distribution percentages

2. **Modify Journey Steps**
   - Update `generator.py`
   - Add new step types
   - Modify step logic

3. **Add New Test Cases**
   - Update `test_execution_framework.py`
   - Add new validation rules
   - Create custom test scenarios

4. **Extend Journey Phase Validation**
   - Update `validate_journey_phases.py`
   - Add new phase-specific validation rules
   - Modify transition criteria

## License

This project is licensed under the MIT License.

# Engagement Pattern System

A sophisticated React component system for creating adaptive, persona-responsive user experiences. This system implements four key engagement patterns: Value Articulation, Progressive Disclosure, Emotional Scaffolding, and Persona Adaptation.

## Features

- **Value-First Architecture**: Emphasizes the "why" behind each step
- **Progressive Disclosure**: Adapts content visibility based on user engagement
- **Emotional Scaffolding**: Provides contextual emotional support
- **Persona Adaptation**: Tailors content to user personas
- **Dynamic Content Loading**: Progressive loading of content tiers
- **Interaction-Based Adaptation**: Real-time content adaptation
- **Progress Preservation**: Saves and restores user progress
- **Development Tools**: Pattern visualization and metrics tracking

## Installation

```bash
npm install @kit/engagement-patterns
# or
yarn add @kit/engagement-patterns
```

## Dependencies

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "zod": "^3.0.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  }
}
```

## Usage

### Basic Implementation

```tsx
import { JourneyStepComponent } from '@kit/engagement-patterns';

function JourneyPage() {
  const step = {
    id: 'step-1',
    type: 'essential',
    content: 'Your step content here...',
    visibility: 'visible'
  };

  const user = {
    id: 'user-1',
    persona: 'health_aware_avoider',
    email: 'user@example.com',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  return (
    <JourneyStepComponent
      step={step}
      user={user}
      onComplete={(stepId, metrics) => {
        console.log('Step completed:', stepId, metrics);
      }}
    />
  );
}
```

### Step Types

The system supports three types of steps:

1. **Essential**: Core information that should be immediately visible
2. **Extended**: Additional context and details
3. **Comprehensive**: Deep dive content with detailed information

```tsx
const essentialStep = {
  type: 'essential',
  content: 'Core information...'
};

const extendedStep = {
  type: 'extended',
  content: 'Core + extended content...'
};

const comprehensiveStep = {
  type: 'comprehensive',
  content: 'Core + extended + comprehensive content...'
};
```

### User Personas

The system supports various user personas:

- `health_aware_avoider`: Cautious, detail-oriented users
- `structured_system_seeker`: Analytical, organized users
- `balanced_life_integrator`: Practical, holistic users
- `healthcare_professional`: Professional, knowledgeable users
- `overlooked_risk_group`: Pragmatic, resourceful users

```tsx
const user = {
  persona: 'health_aware_avoider',
  // ... other user properties
};
```

### Pattern Components

Each step can include various pattern components:

```tsx
const step = {
  // ... basic step properties
  valueComponents: {
    preview: 'Why this matters...',
    confirmation: 'You've made great progress!',
    contextual: 'Additional context...'
  },
  emotionalComponents: {
    type: 'reassurance',
    intensity: 0.8,
    message: 'You're doing great!'
  },
  personaComponents: {
    approach: 'direct',
    intensity: 0.7,
    adaptations: ['Adapted content...']
  }
};
```

### Development Tools

In development mode, the component displays pattern metrics and visualization:

```tsx
// Pattern metrics are automatically tracked
const metrics = {
  valueArticulation: 0.85,
  emotionalScaffolding: 0.72,
  progressiveDisclosure: 0.68,
  personaAlignment: 0.91
};
```

## Hooks

### useDynamicContentLoading

Manages progressive content loading:

```tsx
const { contentState } = useDynamicContentLoading(step, user);
```

### useInteractionAdaptation

Adapts content based on user interactions:

```tsx
const adaptedStep = useInteractionAdaptation(measurements, enhancedStep);
```

### useProgressPreservation

Manages progress saving and restoration:

```tsx
const { calculateProgress } = useProgressPreservation(step, user, interactions);
```

## Styling

The component uses Tailwind CSS for styling. Custom styles can be applied using the `cn` utility:

```tsx
<div className={cn(
  "base-styles",
  {
    'essential-styles': step.type === 'essential',
    'extended-styles': step.type === 'extended',
    'comprehensive-styles': step.type === 'comprehensive'
  }
)}>
```

## Best Practices

1. **Content Structure**
   - Start with essential content
   - Layer extended content progressively
   - Provide comprehensive details when needed

2. **Persona Adaptation**
   - Match content style to user persona
   - Adjust emotional support intensity
   - Use appropriate communication approach

3. **Progress Tracking**
   - Save progress regularly
   - Restore from last known state
   - Track completion metrics

4. **Performance**
   - Load content progressively
   - Cache extended content
   - Optimize for user interactions

## Development

### Running Tests

```bash
npm test
# or
yarn test
```

### Building

```bash
npm run build
# or
yarn build
```

### Development Mode

```bash
npm run dev
# or
yarn dev
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT