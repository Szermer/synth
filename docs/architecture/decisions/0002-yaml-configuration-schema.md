# ADR-0002: YAML Configuration Schema

## Status
Accepted

## Context
After deciding to refactor Synth into a multi-domain framework ([ADR-0001](0001-multi-domain-architecture-refactor.md)), we needed a configuration format that:
- Is human-readable and editable
- Supports version control (Git-friendly)
- Allows complex nested structures
- Enables validation before runtime
- Works well with Python dataclasses

## Decision
Use **YAML** as the primary configuration format with a standardized schema across all projects.

### Configuration Structure
```
projects/{project_name}/
├── config.yaml             # Project metadata
├── personas.yaml           # Persona archetypes
├── journey_phases.yaml     # Journey progression
├── emotional_states.yaml   # Emotional modeling
├── data_schema.yaml        # Domain fields (optional)
└── narrative_patterns.yaml # Response styles
```

### Schema Definitions

#### 1. `config.yaml` - Project Metadata
```yaml
name: "Project Name"
description: "Brief description"
version: "1.0"
domain: "domain_identifier"

default_count: 1000
journey_type: "session_based"  # time_based, session_based, milestone_based

journey:
  type: "session_based"
  phases:
    - discovery
    - onboarding
    - active_use
    - mature_use

metrics:
  - completion_rate
  - engagement_score
  - retention_rate
```

#### 2. `personas.yaml` - Persona Definitions
```yaml
personas:
  persona_identifier:
    name: "Human-Readable Name"
    description: "Who they are"
    distribution: 0.30  # Must sum to 1.0 across all personas
    priority: "tier_1_mvp"  # Optional prioritization

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
      action_tendency: [0.5, 0.7]  # Min-max range
      anxiety_level: [0.3, 0.6]    # Optional

    attributes:
      domain_specific_field: [min, max]
      another_field: ["option1", "option2"]

    completion_thresholds:
      phase_name: [0.6, 0.8]

    pain_points:
      - "description of pain point"

    motivations:
      - "what drives them"
```

**Validation Rules:**
- ✅ All persona distributions must sum to 1.0 (±0.01 tolerance)
- ✅ Age ranges: `min < max`
- ✅ Gender/education distributions sum to 1.0
- ✅ Action tendency ranges: `[0.0, 1.0]`
- ✅ Completion thresholds per journey phase

#### 3. `journey_phases.yaml` - Journey Structure
```yaml
phases:
  - name: "phase_identifier"
    order: 0
    description: "What happens in this phase"
    duration_estimate: "1-3 sessions"  # Optional
    completion_threshold: 0.7

    objectives:
      - "objective_1"
      - "objective_2"

    emotional_objectives:
      - "reduce_anxiety"
      - "build_confidence"

    data_to_collect:
      - "field_name"
      - "another_field"

    narrative_prompts:
      - "Question to ask user"

    verification_questions:
      - "Validation question"
```

**Journey Phase Ordering:**
- Phases are processed in `order` sequence
- Each phase can have variable duration based on journey type

#### 4. `emotional_states.yaml` - Emotional Progression
```yaml
emotional_progressions:
  persona_identifier:
    phase_name:
      - "initial_state"
      - "mid_state"
      - "final_state"

common_markers:
  positive:
    - "confident"
    - "engaged"
  negative:
    - "anxious"
    - "frustrated"
  transitional:
    - "curious"
    - "evaluating"
```

#### 5. `narrative_patterns.yaml` - Response Styles
```yaml
patterns:
  persona_identifier:
    response_style: "cautious_practical"
    detail_level: "moderate"  # brief, moderate, comprehensive

    linguistic_markers:
      - "I think"
      - "maybe"

    response_lengths:
      min_words: 20
      max_words: 100
      avg_words: 50
```

## Consequences

### Positive ✅
- **Human-Readable**: Non-developers can edit configs
- **Version Control**: Git-friendly, clear diffs
- **Nested Structures**: Easy to represent complex relationships
- **Comments**: YAML supports inline documentation
- **Validation**: PyYAML + Pydantic for schema validation
- **IDE Support**: Syntax highlighting, autocomplete

### Negative ⚠️
- **Runtime Errors**: YAML syntax errors only caught when loaded
- **Indentation-Sensitive**: Whitespace errors are common
- **No Schema Enforcement**: Requires custom validation
- **Size**: Large configs can be unwieldy

### Trade-offs Considered

**YAML vs JSON:**
- ✅ YAML: Comments, more readable
- ❌ JSON: No comments, verbose

**YAML vs TOML:**
- ✅ YAML: Better for nested structures
- ❌ TOML: Better for flat configs

**YAML vs Python:**
- ✅ YAML: Declarative, non-code
- ❌ Python: Programmatic, version-controlled code

## Implementation

### ConfigLoader Class
```python
class ConfigLoader:
    def __init__(self, project_path: Path):
        self.project_path = project_path

    def load_personas(self) -> Dict[str, PersonaConfig]:
        data = self._load_yaml("personas.yaml")
        return self._parse_personas(data)

    def _load_yaml(self, filename: str) -> Dict:
        with open(self.project_path / filename) as f:
            return yaml.safe_load(f)
```

### Validation Strategy
1. **Load-Time Validation**: Check YAML syntax and structure
2. **Schema Validation**: Validate against expected fields
3. **Business Logic Validation**: Check distributions sum to 1.0
4. **Cross-Reference Validation**: Ensure phase names match

### Error Handling
```python
try:
    loader = ConfigLoader(project_path)
    personas = loader.load_personas()
except FileNotFoundError:
    print("❌ Missing configuration file")
except yaml.YAMLError:
    print("❌ Invalid YAML syntax")
except ValueError as e:
    print(f"❌ Validation error: {e}")
```

## Best Practices

### 1. **Start with Templates**
Copy `projects/private_language/` as starting point

### 2. **Validate Early**
```bash
python cli.py validate your_project
```

### 3. **Use Comments**
```yaml
personas:
  studio_practitioner:
    distribution: 0.30  # 30% of cohort - primary ICP
```

### 4. **Organize by Priority**
```yaml
personas:
  # Tier 1: MVP Focus
  studio_practitioner: {...}
  educator_instructor: {...}

  # Tier 2: Growth Phase
  master_craftsperson: {...}
```

### 5. **Version Your Configs**
```yaml
# projects/my_project/config.yaml
name: "My Project"
version: "1.0"  # Increment on breaking changes
```

## Related Documents
- [ADR-0001: Multi-Domain Architecture Refactor](0001-multi-domain-architecture-refactor.md)
- [README.md](../../../README.md) - Usage examples
- [Example Project](../../../projects/private_language/) - Reference implementation

## Future Enhancements
- [ ] JSON Schema for IDE autocomplete
- [ ] YAML linting in pre-commit hooks
- [ ] Config migration tools for version upgrades
- [ ] Visual config editor/builder

## Date
2025-10-07

## Authors
- Stephen Szermer (with Claude Code assistance)
