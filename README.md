# Synth - Multi-Domain Synthetic User Data Generator

**Generate realistic synthetic user data across different domains using persona archetypes and journey phase modeling.**

Synth is a flexible framework for creating synthetic user datasets based on configurable personas and user journeys. Originally built for healthcare applications, it now supports any domain through YAML-based project configurations.

## ✨ Features

- **Multi-Domain Support** - Configure different projects with domain-specific personas and journeys
- **Persona-Driven Generation** - Create users based on realistic behavioral archetypes
- **Journey Phase Modeling** - Simulate user progression through discovery, onboarding, active use, and maturity
- **Emotional State Tracking** - Model emotional progression throughout user journeys
- **Narrative Generation** - Create realistic conversational responses based on persona characteristics
- **Flexible Journey Types** - Support for time-based, session-based, or milestone-based journeys
- **YAML Configuration** - Human-readable, version-controllable project definitions

## 🏗️ Architecture

```
synth/
├── core/                       # Domain-agnostic engine
│   ├── models/                # Data models (Persona, Journey, UserProfile)
│   ├── generators/            # Generation engines
│   ├── validation/            # Validation framework
│   └── utils/                 # Config loaders and utilities
│
├── projects/                   # Project-specific configurations
│   └── private_language/      # Example: Knowledge sovereignty platform
│       ├── config.yaml        # Project metadata
│       ├── personas.yaml      # Persona definitions
│       ├── journey_phases.yaml # Journey structure
│       ├── emotional_states.yaml # Emotional progressions
│       ├── data_schema.yaml   # Data fields
│       └── narrative_patterns.yaml # Response styles
│
├── cli.py                     # Command-line interface
└── output/                    # Generated datasets
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Szermer/synth.git
cd synth

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Synthetic Users

```bash
# List available projects
python cli.py list-projects

# Generate 1000 users for Private Language
python cli.py generate private_language --count 1000

# Validate project configuration
python cli.py validate private_language
```

### Output

Generated data is saved to `output/<project_name>_synthetic_users.json`:

```json
{
  "id": "uuid",
  "persona_type": "studio_practitioner",
  "name": "Sarah Martinez",
  "age": 42,
  "gender": "female",
  "education": "bachelors",
  "attributes": {
    "expertise_domain": "ceramics",
    "years_in_craft": 15,
    "tech_comfort": 0.65
  },
  "journey": {
    "journey_type": "session_based",
    "phases": [...],
    "steps": [...],
    "overall_completion": 0.73
  }
}
```

## 📋 Creating a New Project

### 1. Create Project Directory

```bash
mkdir -p projects/your_project
```

### 2. Define Configuration Files

#### `config.yaml` - Project Metadata

```yaml
name: "Your Project"
description: "Description of your domain"
version: "1.0"
domain: "your_domain"

default_count: 1000
journey_type: "session_based"  # or "time_based" or "milestone_based"

journey:
  type: "session_based"
  phases:
    - discovery
    - onboarding
    - active_use
```

#### `personas.yaml` - Define Your Personas

```yaml
personas:
  persona_type_1:
    name: "Persona Name"
    description: "Who they are"
    distribution: 0.30  # 30% of users

    demographics:
      age_range: [25, 55]
      gender_distribution:
        female: 0.50
        male: 0.50
      education_distribution:
        bachelors: 0.60
        masters: 0.40

    behavioral:
      engagement_pattern: "cautious_gradual"
      action_tendency: [0.5, 0.7]
      anxiety_level: [0.3, 0.6]

    completion_thresholds:
      discovery: [0.6, 0.8]
      onboarding: [0.5, 0.7]
```

#### `journey_phases.yaml` - Define User Journey

```yaml
phases:
  - name: "discovery"
    order: 0
    description: "User discovers your product"
    objectives:
      - "understand_value_proposition"
      - "evaluate_fit"
    emotional_objectives:
      - "reduce_skepticism"
      - "build_curiosity"
    data_to_collect:
      - "discovery_source"
      - "primary_pain_point"
```

#### `emotional_states.yaml` - Define Emotional Progression

```yaml
emotional_progressions:
  persona_type_1:
    discovery:
      - "skeptical"
      - "curious"
    onboarding:
      - "learning"
      - "confident"
```

#### `narrative_patterns.yaml` - Define Response Styles

```yaml
patterns:
  persona_type_1:
    response_style: "cautious_practical"
    detail_level: "moderate"
    linguistic_markers:
      - "I think"
      - "maybe"
```

### 3. Generate Data

```bash
python cli.py validate your_project
python cli.py generate your_project --count 500
```

## 💡 Example Projects

### Private Language
A knowledge sovereignty platform for craft expertise preservation. Demonstrates:
- 7 distinct personas (Studio Practitioner, Educator, Master Craftsperson, etc.)
- Session-based journey progression
- Tacit knowledge capture and documentation patterns
- Legacy preservation motivations

## 🛠️ Development

### Project Structure

- **Core Engine** (`core/`) - Domain-agnostic generation logic
- **Models** (`core/models/`) - Data structures for personas, journeys, users
- **Generators** (`core/generators/`) - Persona, journey, and narrative generation
- **Utils** (`core/utils/`) - Configuration loading and helpers
- **Projects** (`projects/`) - Domain-specific configurations

### Architecture

- [C4 Architecture Diagram](docs/architecture/C4_ARCHITECTURE.md) - System architecture overview
- [Decision Registry](docs/architecture/DECISION_REGISTRY.md) - All architectural decisions
- [Architecture Decision Records](docs/architecture/decisions/) - Detailed ADRs
  - [ADR-0001: Multi-Domain Architecture Refactor](docs/architecture/decisions/0001-multi-domain-architecture-refactor.md)
  - [ADR-0002: YAML Configuration Schema](docs/architecture/decisions/0002-yaml-configuration-schema.md)
  - [ADR-0003: Session-Based Journey Modeling](docs/architecture/decisions/0003-session-based-journey-modeling.md)

### Adding Features

The core engine is designed to be extended without modification. Add new capabilities by:
1. Extending YAML schemas in project configs
2. Adding custom attributes to persona configs
3. Defining new journey phases
4. Creating domain-specific narrative patterns

### Testing

```bash
# Run tests
PYTHONPATH=. pytest

# Run specific test
PYTHONPATH=. pytest src/tests/test_file.py::test_name
```

## 📚 Documentation

### Concepts
- **Personas** - Behavioral archetypes with demographic and psychological traits
- **Journey Phases** - Stages users progress through (discovery → mature use)
- **Journey Types**:
  - **Time-Based**: Weekly/daily progression (e.g., 10-week program)
  - **Session-Based**: Variable capture sessions (e.g., knowledge logging)
  - **Milestone-Based**: Achievement-triggered progression
- **Emotional States** - How user emotions evolve through journey
- **Narrative Patterns** - How personas communicate and respond

### Documentation
- [Recent Changes](docs/RECENT_CHANGES.md) - Version 2.0 migration guide
- [TODO](TODO.md) - Roadmap and planned features
- [Architecture](docs/architecture/) - System design and ADRs
- [Decision Registry](docs/architecture/DECISION_REGISTRY.md) - All architectural decisions

## 🗃️ Archive

Previous domain-specific implementations are archived in `archive/`:
- `stage_zero/` - Healthcare risk assessment synthetic users (10-week conversation flows)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Related Projects

- **Private Language** - Knowledge sovereignty platform ([/Szermer/PrivateLanguage](https://github.com/Szermer/PrivateLanguage))

---

**Version 2.0** - Multi-domain refactor | Originally built for Stage Zero Health
