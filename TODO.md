# TODO

## Active Development

### 🚀 In Progress
- [ ] Complete documentation for v2.0 release

### 📋 Next Up (High Priority)
- [ ] Add JSON Schema for YAML validation
- [ ] Create project template generator CLI command
- [ ] Add unit tests for core generators
- [ ] Document migration path for Stage Zero users

## Features

### Core Engine
- [ ] Add support for hybrid journey types (time + milestone)
- [ ] Implement configurable interval distributions
- [ ] Add journey visualization tools
- [ ] Create validation framework with detailed error messages
- [ ] Support for conditional journey branching

### Configuration
- [ ] JSON Schema for IDE autocomplete
- [ ] YAML linting in pre-commit hooks
- [ ] Config migration tools for version upgrades
- [ ] Visual config editor/builder (web interface?)
- [ ] Config templates for common use cases

### Analysis & Reporting
- [x] Basic scenario analysis tool
- [x] Persona-specific user stories
- [ ] Journey flow visualization (Mermaid diagrams)
- [ ] Cohort comparison reports
- [ ] Export to common formats (CSV, Parquet, SQL)
- [ ] Statistical validation reports

### Integration
- [ ] SDV (Synthetic Data Vault) integration for demographics
- [ ] Faker provider customization per project
- [ ] Export to testing frameworks (Playwright, Cypress)
- [ ] API layer for on-demand generation
- [ ] Database seeding utilities

## Documentation

### User Guides
- [x] README with quick start
- [x] Architecture Decision Records
- [x] Configuration schema reference
- [ ] Video walkthrough of creating a project
- [ ] Cookbook with common patterns
- [ ] FAQ section

### Developer Docs
- [ ] Contributing guidelines
- [ ] Code architecture deep-dive
- [ ] Generator extension guide
- [ ] Custom validator tutorial
- [ ] Release process documentation

### Project Examples
- [x] Private Language (session-based)
- [ ] Stage Zero (time-based) - migrated from archive
- [ ] E-commerce onboarding (milestone-based)
- [ ] SaaS free trial (mixed journey type)

## Testing

### Test Coverage
- [ ] Unit tests for all generators
- [ ] Integration tests for CLI
- [ ] Config validation tests
- [ ] Journey progression tests
- [ ] Persona distribution tests
- [ ] Edge case handling

### CI/CD
- [ ] GitHub Actions workflow
- [ ] Automated testing on PR
- [ ] Linting and type checking
- [ ] YAML validation in CI
- [ ] Test coverage reporting

## Quality & Performance

### Code Quality
- [ ] Type hints for all functions
- [ ] Docstrings for public APIs
- [ ] Remove TODO comments from code
- [ ] Refactor long functions (>50 lines)
- [ ] Add logging throughout

### Performance
- [ ] Benchmark large cohort generation (10K+ users)
- [ ] Optimize persona distribution calculation
- [ ] Cache parsed YAML configs
- [ ] Parallelize journey generation
- [ ] Memory profiling for large datasets

## Community & Growth

### Adoption
- [ ] Publish to PyPI
- [ ] Create demo Jupyter notebooks
- [ ] Write blog post announcing v2.0
- [ ] Submit to awesome-synthetic-data list
- [ ] Create project website/landing page

### Examples & Templates
- [ ] E-commerce personas template
- [ ] SaaS onboarding template
- [ ] Education platform template
- [ ] Healthcare template (from Stage Zero)
- [ ] Fintech template

## Bugs & Issues

### Known Issues
- [ ] None currently tracked

### Technical Debt
- [ ] Consider switching from random to numpy.random for reproducibility
- [ ] Add seed parameter for deterministic generation
- [ ] Improve error messages in ConfigLoader
- [ ] Add progress bars for large generation runs

## Future Considerations

### Advanced Features
- [ ] Multi-project analytics (cross-project patterns)
- [ ] A/B testing for journey variations
- [ ] Machine learning for realistic distributions
- [ ] Privacy-preserving generation from real data
- [ ] Synthetic data marketplace integration

### Ecosystem
- [ ] VSCode extension for YAML editing
- [ ] Slack/Discord community
- [ ] Monthly synthetic data newsletter
- [ ] Annual conference/meetup

## Completed ✅

### v2.0 Release (2025-10-07)
- [x] Multi-domain architecture refactor
- [x] YAML configuration system
- [x] Session-based journey modeling
- [x] Private Language project setup
- [x] CLI interface (generate, validate, list)
- [x] Analysis tools (scenarios, cohorts)
- [x] Complete documentation suite
- [x] Architecture Decision Records
- [x] Archive Stage Zero code
- [x] 100-user test cohort generation

---

**Priority Legend:**
- 🔴 High - Blocking or high-impact
- 🟡 Medium - Important but not urgent
- 🟢 Low - Nice to have

**Last Updated:** 2025-10-07
**Maintainer:** Stephen Szermer
