# Recent Changes

## Version 2.1.0 - Synthetic User Framework Integration (2025-10-07)

### 🎯 Framework Enhancements

**Aligned with Synthetic User Generation Framework**
- Integrated comprehensive framework from Private Language research
- 500-user target distribution validated with perfect accuracy
- Statistical realism through correlation matrices and behavioral modeling

**Expanded Persona Set** ([ADR-0004](architecture/decisions/0004-synthetic-user-framework-integration.md))
- Added 3 new core personas:
  - Early Adopter (10%) - Innovation champions driving word-of-mouth
  - Skeptical Veteran (5%) - AI resistance and adoption barriers
  - Department Head expanded to 15% (was 3%) - Key decision makers
- Added 5 edge case personas (20% total):
  - Cross-Domain Practitioner (6%)
  - International User (5%)
  - Industry Trainer (4%)
  - Graduate Student (3%)
  - Outlier/Stress Case (2%)

**Correlation Matrices**
- Age → Tech Comfort (-0.3 correlation): Older users less comfortable with tech
- Tech Comfort → AI Attitude (0.7 correlation): Higher comfort = more positive attitude
- Age → Years Experience (0.85 correlation): Strong positive relationship
- Automatic correlation application in persona generation

**Engagement Stratification**
- Within-persona variation: 20% high, 60% standard, 20% low
- Affects journey generation:
  - High: 15-25 sessions, +20% completion boost
  - Standard: 10-20 sessions, normal patterns
  - Low: 5-12 sessions, -20% completion, higher dropout

**Knowledge Capture Behaviors**
- Systematic (25%): Regular 2-7 day intervals
- Opportunistic (35%): Variable 1-14 day intervals
- Crisis-Driven (25%): Burst patterns (1-3 days then 10-30 day gaps)
- Experimental (15%): Very irregular 1-21 day intervals
- Affects session timing in journey generation

**Persona-Specific Distributions**
- Extended YAML schema with `*_distribution` pattern
- Master Educators: Career stage distributions (60% late-career, 30% mid-late, 10% exceptional)
- Studio Practitioners: Medium distributions (ceramics, visual arts, textile, woodworking, etc.)
- Department Heads: Sector and concern distributions

### 🧪 Validation

**Generated and Validated 500-User Cohort**
- Perfect persona distribution accuracy (all within 0.0%)
- Engagement stratification within 2% of targets
- Capture behaviors within 4% of targets
- Journey patterns validated:
  - High engagement: avg 20.2 sessions (15-25 range) ✓
  - Standard: avg 15.1 sessions (10-20 range) ✓
  - Low: avg 8.0 sessions (5-12 range) ✓

**New Analysis Tool**
- `analyze_framework_validation.py` - Comprehensive validation of distributions and correlations
- Validates personas, engagement, behaviors, correlations, and journey patterns
- 8-section validation report with statistical analysis

### 📚 Documentation

**New ADR**
- ADR-0004: Synthetic User Generation Framework Integration
- Documents correlation matrices, engagement stratification, capture behaviors
- Validation results and alternatives considered

**Updated Files**
- Decision Registry with ADR-0004
- personas.yaml expanded to 10 personas with detailed distributions
- PersonaGenerator and JourneyGenerator enhanced

### 🔧 Technical Changes

**Core Generators Enhanced**
- `PersonaGenerator`:
  - Correlation matrices with `_apply_correlation()` method
  - Engagement tier assignment
  - Knowledge capture behavior assignment
  - Weighted distribution support for persona attributes
  - Tech Comfort → AI Attitude bias logic

- `JourneyGenerator`:
  - Engagement-tier-aware session generation
  - Capture-behavior-based timing patterns
  - Dropout logic based on engagement tier
  - Systematic, opportunistic, crisis-driven, experimental patterns

### 📊 Results

- **Realism**: Age-tech comfort correlation measured at -0.607 (stronger than -0.3 target)
- **Accuracy**: Master Educator career stages 62.7% late-career (vs 60% target)
- **Diversity**: 10 persona types covering full adoption curve and edge cases
- **Scale**: Successfully generated and validated 500-user cohort

---

## Version 2.0.0 - Multi-Domain Refactor (2025-10-07)

### 🔴 Breaking Changes

**Architecture Overhaul**
- Refactored from single-purpose (Stage Zero Health) to multi-domain framework
- Moved domain logic from code to YAML configuration files
- Stage Zero code archived to `archive/stage_zero/`
- New project structure: `projects/{project_name}/`

**Migration Required**
- Existing Stage Zero users need to create new project configs
- Original functionality preserved in archive
- Follow migration guide in ADR-0001

### ✨ New Features

**Multi-Domain Support** ([ADR-0001](architecture/decisions/0001-multi-domain-architecture-refactor.md))
- Domain-agnostic core engine
- YAML-based project configuration system
- Support for unlimited domains via config files
- First new project: Private Language (knowledge sovereignty platform)

**Journey Type Flexibility** ([ADR-0003](architecture/decisions/0003-session-based-journey-modeling.md))
- Time-Based: Fixed intervals (e.g., weekly check-ins)
- Session-Based: Variable capture sessions (e.g., knowledge logging)
- Milestone-Based: Achievement-triggered progression

**CLI Interface**
```bash
python cli.py generate <project> --count N
python cli.py validate <project>
python cli.py list-projects
```

**Project Templates**
- Complete Private Language project config
- 7 detailed personas with distributions
- 4-phase session-based journey
- Emotional state progressions
- Narrative response patterns

**Analysis Tools**
- `analyze_scenarios.py` - Analyze user cohorts
- `generate_persona_scenarios.py` - Create user stories
- `example_generate.py` - Programmatic usage reference

### 🏗️ Architecture Changes

**New Structure**
```
synth/
├── core/                    # Domain-agnostic engine
│   ├── models/             # Persona, Journey, UserProfile
│   ├── generators/         # Core generation logic
│   └── utils/              # ConfigLoader, helpers
├── projects/               # Project configurations
│   └── private_language/  # Example project
├── archive/stage_zero/    # Original implementation
└── docs/                  # Documentation & ADRs
```

**Core Components**
- `PersonaGenerator`: Generate persona instances from configs
- `JourneyGenerator`: Create user journeys with phases/steps
- `NarrativeGenerator`: Generate persona-specific responses
- `ConfigLoader`: YAML configuration parser

**Data Models**
- `Persona`: User archetype with behavioral traits
- `Journey`: User progression through phases
- `JourneyStep`: Individual session/week in journey
- `UserProfile`: Complete user with persona + journey

### 📚 Documentation

**New ADRs**
- ADR-0001: Multi-Domain Architecture Refactor
- ADR-0002: YAML Configuration Schema
- ADR-0003: Session-Based Journey Modeling

**Updated Docs**
- Complete README rewrite
- Architecture decision registry
- Project creation guide
- Configuration schema reference

### 🧪 Testing

**Private Language Validation**
- Generated 100-user test cohort
- Validated persona distributions (perfect match)
- Tested session-based journey generation
- Analyzed first capture session patterns
- Created realistic user scenarios

**Test Results**
- ✅ Persona distribution: Exact match to configuration
- ✅ Journey generation: 5-20 sessions with variable intervals
- ✅ Emotional progression: Phase-appropriate states
- ✅ Time investment: 13-15 min average (realistic)

### 🛠️ Technical Details

**Dependencies**
- Added: `pyyaml>=6.0.0` for configuration parsing
- Retained: `faker`, `pandas`, `numpy` for data generation
- Dev: `pytest`, `black`, `isort`, `mypy`

**Removed**
- Stage Zero-specific generators (10 files)
- Hardcoded persona configurations
- Healthcare domain models
- Time-based-only journey logic

**File Changes**
```
73 files changed
4,119 insertions(+)
84,166 deletions(-)
```

### 🔗 Related Projects

**Private Language Integration**
- First multi-domain project using Synth
- Knowledge sovereignty platform for craft expertise
- 7 personas mapped from user research
- Session-based knowledge capture journeys
- Realistic first-session scenarios generated

## Migration Guide

### From v1.x (Stage Zero) to v2.0

**Option 1: Use Archived Code**
Original Stage Zero code preserved in `archive/stage_zero/`
```bash
python archive/stage_zero/stage_zero_generator.py
```

**Option 2: Create New Config**
1. Create `projects/stage_zero/` directory
2. Copy YAML templates from `projects/private_language/`
3. Adapt personas to healthcare domain
4. Use time-based journey type
5. Run `python cli.py generate stage_zero --count 500`

**Option 3: Continue with Archive**
No migration needed - archived version still functional

### Breaking Changes Checklist

- [ ] Review ADR-0001 for architecture changes
- [ ] Decide: Archive or migrate?
- [ ] If migrating: Create project configs
- [ ] Update any automation scripts to use new CLI
- [ ] Test generation with new system

## Previous Versions

### Version 1.x - Stage Zero Health (2025-03 to 2025-06)

**Features**
- Healthcare-focused synthetic user generation
- 10-week conversation flow modeling
- 5 health awareness personas
- Journey phase validation framework
- Test execution framework

**Archived:** All v1.x code preserved in `archive/stage_zero/`

---

**For detailed architectural decisions, see:**
- [ADR-0001: Multi-Domain Architecture](architecture/decisions/0001-multi-domain-architecture-refactor.md)
- [Decision Registry](architecture/DECISION_REGISTRY.md)
- [C4 Architecture](architecture/C4_ARCHITECTURE.md)
