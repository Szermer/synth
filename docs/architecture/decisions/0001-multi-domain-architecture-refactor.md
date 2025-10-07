# ADR-0001: Multi-Domain Architecture Refactor

## Status
Accepted

## Context
The Synth project was originally built as a single-purpose synthetic user data generator for Stage Zero Health, a healthcare risk assessment application. The codebase had:
- Hardcoded healthcare-specific personas and journey phases
- Domain logic mixed with generation engine
- Stage Zero-specific data models and narrative patterns
- No separation between framework and domain

We needed to support multiple domains (Private Language being the first new use case) without duplicating code or maintaining separate generators.

## Decision
Refactor Synth into a **multi-domain synthetic user data generation framework** with:

### 1. **Core Engine (Domain-Agnostic)**
```
core/
├── models/          # Persona, Journey, UserProfile data models
├── generators/      # PersonaGenerator, JourneyGenerator, NarrativeGenerator
├── validation/      # Generic validation framework
└── utils/          # ConfigLoader, helpers
```

**Key Principles:**
- No domain-specific logic in core
- All generators work with any YAML configuration
- Data models are flexible with `attributes` dictionaries
- Type-safe with dataclasses and type hints

### 2. **Project-Based Configuration System**
```
projects/
└── {project_name}/
    ├── config.yaml             # Project metadata, journey type
    ├── personas.yaml           # Persona definitions with distributions
    ├── journey_phases.yaml     # Phase objectives and progression
    ├── emotional_states.yaml   # Emotional progressions by persona
    ├── data_schema.yaml        # Domain-specific fields
    └── narrative_patterns.yaml # Response styles by persona
```

**Configuration-Driven:**
- YAML for human readability and version control
- Hot-swappable project configs
- No code changes needed for new domains
- Validation on config load

### 3. **CLI Interface**
```bash
python cli.py generate <project_name> --count N
python cli.py validate <project_name>
python cli.py list-projects
```

**Benefits:**
- Simple, intuitive usage
- Self-documenting with `--help`
- Extensible for future commands

### 4. **Journey Type Flexibility**
Support three journey patterns:
- **Time-Based**: Fixed intervals (e.g., 10 weeks, daily check-ins)
- **Session-Based**: Variable capture sessions (e.g., knowledge logging)
- **Milestone-Based**: Achievement-triggered progression

**Implementation:**
```python
class JourneyType(Enum):
    TIME_BASED = "time_based"
    SESSION_BASED = "session_based"
    MILESTONE_BASED = "milestone_based"
```

### 5. **Archive Strategy**
Move Stage Zero code to `archive/stage_zero/` to:
- Preserve original implementation
- Provide reference for time-based journeys
- Enable regeneration of Stage Zero data if needed

## Consequences

### Positive ✅
- **Reusable**: Add new domains by creating config files, not code
- **Maintainable**: Single engine, multiple configs
- **Scalable**: Easy to support dozens of projects
- **Type-Safe**: Dataclasses and Zod-like validation
- **Version-Controllable**: YAML configs in Git
- **Self-Documenting**: Configs describe domain clearly

### Negative ⚠️
- **Migration Required**: Existing Stage Zero users need new configs
- **Config Complexity**: YAML files can get large for complex domains
- **Validation Overhead**: Config errors only caught at runtime
- **Learning Curve**: Users need to understand YAML structure

### Risks Mitigated 🛡️
- **Code Duplication**: Eliminated need for domain-specific generators
- **Technical Debt**: Clear separation of concerns
- **Extensibility**: Can add new journey types without breaking changes

## Implementation Details

### Phase 1: Core Engine (Completed)
- ✅ Extract domain-agnostic models
- ✅ Build flexible generators
- ✅ Create ConfigLoader for YAML parsing
- ✅ Implement journey type enum

### Phase 2: Private Language Project (Completed)
- ✅ Define 7 personas with distributions
- ✅ Create 4-phase session-based journey
- ✅ Map emotional progressions
- ✅ Define narrative patterns
- ✅ Test generation with 100 users

### Phase 3: Tooling (Completed)
- ✅ CLI with generate/validate/list commands
- ✅ Example programmatic usage script
- ✅ Scenario analysis tools

## Related Documents
- [ADR-0002: YAML Configuration Schema](0002-yaml-configuration-schema.md)
- [ADR-0003: Session-Based Journey Modeling](0003-session-based-journey-modeling.md)
- [README.md](../../../README.md)
- [DECISION_REGISTRY.md](../DECISION_REGISTRY.md)

## References
- Original Stage Zero implementation: `archive/stage_zero/`
- Private Language personas: `/Users/stephenszermer/Dev/PrivateLanguage/docs/personas/USER_PERSONAS.md`
- Awesome Synthetic Data: https://github.com/statice/awesome-synthetic-data

## Migration Notes

### From Stage Zero to Multi-Domain
**Before:**
```python
# Hardcoded in generator.py
PERSONA_CONFIG = {
    "health_aware_avoider": {...}
}
```

**After:**
```yaml
# projects/stage_zero/personas.yaml
personas:
  health_aware_avoider:
    distribution: 0.30
    demographics: {...}
```

### Adding New Projects
1. Create `projects/your_project/`
2. Copy YAML templates from `projects/private_language/`
3. Customize personas, journeys, emotions
4. Run `python cli.py validate your_project`
5. Generate: `python cli.py generate your_project --count 1000`

## Date
2025-10-07

## Authors
- Stephen Szermer (with Claude Code assistance)
