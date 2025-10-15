# Decision Registry

This document tracks all Architecture Decision Records (ADRs) for the Synth project.

## Overview

Synth is a multi-domain synthetic user data generation framework that creates realistic user personas, journey progressions, and behavioral patterns for product development, UX research, and testing.

## Decision Records

| ID | Title | Status | Date | Impact |
|----|-------|--------|------|--------|
| [ADR-0001](decisions/0001-multi-domain-architecture-refactor.md) | Multi-Domain Architecture Refactor | ✅ Accepted | 2025-10-07 | 🔴 High |
| [ADR-0002](decisions/0002-yaml-configuration-schema.md) | YAML Configuration Schema | ✅ Accepted | 2025-10-07 | 🟡 Medium |
| [ADR-0003](decisions/0003-session-based-journey-modeling.md) | Session-Based Journey Modeling | ✅ Accepted | 2025-10-07 | 🟡 Medium |
| [ADR-0004](decisions/0004-synthetic-user-framework-integration.md) | Synthetic User Generation Framework Integration | ✅ Accepted | 2025-10-07 | 🟡 Medium |
| [ADR-0005](decisions/0005-e2e-testing-framework-persona-based.md) | Persona-Based E2E Testing Framework | ✅ Accepted | 2025-10-07 | 🟡 Medium |

## Status Legend

- ✅ **Accepted** - Decision is approved and implemented
- 🚧 **Proposed** - Under discussion, not yet implemented
- ⚠️ **Deprecated** - No longer recommended, superseded
- ❌ **Rejected** - Considered but not adopted

## Impact Legend

- 🔴 **High** - Fundamental architectural changes, affects entire system
- 🟡 **Medium** - Significant component changes, affects multiple areas
- 🟢 **Low** - Localized changes, minimal system impact

## Key Decisions Summary

### ADR-0001: Multi-Domain Architecture Refactor 🔴
**Problem:** Single-purpose tool (Stage Zero Health) couldn't support new domains
**Solution:** Extract core engine, move domain logic to YAML configs
**Impact:** Complete architectural refactor, enables unlimited domains

### ADR-0002: YAML Configuration Schema 🟡
**Problem:** Need human-readable, version-controllable config format
**Solution:** Standardized YAML schema for personas, journeys, emotions
**Impact:** Non-developers can create new projects without coding

### ADR-0003: Session-Based Journey Modeling 🟡
**Problem:** Time-based journeys too rigid for variable user behaviors
**Solution:** Support 3 journey types: time-based, session-based, milestone-based
**Impact:** Realistic modeling of irregular engagement patterns

### ADR-0004: Synthetic User Generation Framework Integration 🟡
**Problem:** Initial personas lacked statistical realism and behavioral diversity
**Solution:** Implement correlation matrices, engagement stratification, and capture behaviors
**Impact:** 500-user cohorts with realistic distributions and behavioral patterns

### ADR-0005: Persona-Based E2E Testing Framework 🟡
**Problem:** Traditional E2E tests lack behavioral diversity and realistic user patterns
**Solution:** Playwright tests that adapt to persona attributes from synthetic cohort
**Impact:** 50+ test scenarios with realistic behaviors, beta test simulation, comprehensive coverage

## Cross-Project Decisions

### Private Language Integration
- **ADR-0001**: Enabled Private Language as first multi-domain project
- **ADR-0003**: Session-based journeys model knowledge capture sessions
- **ADR-0004**: 500-user cohort with engagement patterns and capture behaviors
- **ADR-0005**: E2E testing framework leveraging synthetic data for realistic tests

### Stage Zero Archive
- **ADR-0001**: Original code preserved in `archive/stage_zero/`
- Migration path documented for existing users

## Future Decisions

Potential upcoming ADRs:

- **Statistical Realism**: Integration with SDV or similar libraries
- **Privacy Preservation**: Synthetic data generation from real user samples
- **Multi-Project Analytics**: Cross-project pattern detection
- **API Layer**: RESTful API for on-demand generation
- **Validation Framework**: Enhanced config validation with JSON Schema

## Related Documents

- [C4 Architecture](C4_ARCHITECTURE.md) - System architecture overview
- [README.md](../../README.md) - Project overview and quick start
- [RECENT_CHANGES.md](../RECENT_CHANGES.md) - Recent updates and migrations

## ADR Process

### Creating New ADRs

1. Copy `docs/architecture/decisions/template.md`
2. Number sequentially (next: ADR-0006)
3. Fill in all sections
4. Link related ADRs
5. Update this registry
6. Submit PR for review

### ADR Template Sections

- **Status**: Proposed, Accepted, Deprecated, Rejected
- **Context**: What problem are we solving?
- **Decision**: What did we decide and why?
- **Consequences**: Positive/negative impacts
- **Implementation**: How is it built?
- **Related Documents**: Cross-references

## Maintenance

This registry is updated whenever:
- New ADRs are created
- Existing ADRs change status
- Major architectural changes occur
- Cross-ADR relationships are identified

**Last Updated:** 2025-10-07
**Maintainer:** Stephen Szermer
