# TODO

## Active Development

### 🚀 In Progress
- [ ] None - v2.4 complete!

### 📋 Next Up (High Priority)
- [ ] Add JSON Schema for YAML validation
- [ ] Create project template generator CLI command
- [ ] Add unit tests for core generators
- [ ] Document migration path for Stage Zero users
- [ ] Implement QueryPage and ReviewPage objects for E2E tests
- [ ] Create mock upload files (videos, documents) for E2E tests
- [ ] Add E2E tests to CI/CD pipeline

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
- [x] Export to testing frameworks (Playwright, Cypress)
- [ ] API layer for on-demand generation
- [ ] Database seeding utilities

### Semantic Similarity Rating (SSR)
- [x] Core SSR integration with PyMC Labs implementation
- [x] 8 predefined reference scales
- [x] Optional SSR in journey generation
- [x] Real LLM integration (Claude Sonnet 4.5 API)
- [x] Cost estimation tool for batch generation
- [x] Graceful fallback to simulated responses
- [ ] Prompt caching for cost reduction (90% savings potential)
- [ ] Parallel API calls for 4x faster generation
- [ ] Multi-provider support (OpenAI, local LLM)
- [ ] Response caching for common persona/stimulus combinations
- [ ] Dynamic scale generation from descriptions
- [ ] Batch embedding computation for performance
- [ ] Distribution comparison visualizations
- [ ] Cohort segmentation by response patterns
- [ ] SSR caching for repeated stimuli

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

### v2.5 Release (2025-10-16)
- [x] Network Effect Personas for Private Language validation
- [x] Student/apprentice persona (Jordan) - student-facing UI validation
- [x] Knowledge consumer persona (Alex) - marketplace & pay-per-query model
- [x] Teaching assistant persona (Maya) - team collaboration & permissions
- [x] Intelligent user linking (students→educators, TAs→educators)
- [x] Smart educator selection algorithm (engagement + teaching load + experience)
- [x] Journey enhancements: weekly synthesis steps
- [x] Journey enhancements: export event tracking
- [x] generate_network_personas.py script (649 lines)
- [x] PRIVATE_LANGUAGE_ALIGNMENT_REPORT.md (600+ lines, 9/10 alignment score)
- [x] ADR-0008: Private Language Network Effect Personas
- [x] Enhanced personas.yaml with 3 new persona types (240 lines)
- [x] Updated DECISION_REGISTRY, RECENT_CHANGES, and C4_ARCHITECTURE

### v2.4 Release (2025-10-15)
- [x] Real LLM integration with Claude Sonnet 4.5
- [x] LLMResponseGenerator for authentic persona-specific responses
- [x] Optional real LLM parameter in JourneyGenerator
- [x] Persona context injection (age, tech_comfort, ai_attitude, craft experience)
- [x] Scale-specific prompting (engagement, satisfaction, progress, relevance)
- [x] Emotional state awareness in prompts
- [x] Temperature control (0.8) for natural variation
- [x] 200-token response limit for cost optimization
- [x] Cost estimation tool (estimate_llm_costs.py)
- [x] Graceful fallback to simulated on API error
- [x] Environment variable security (.env with ANTHROPIC_API_KEY)
- [x] Test scripts (quick_llm_test.py, test_focused_llm.py, test_one_journey.py, generate_llm_cohort.py)
- [x] ADR-0007: Real LLM Integration
- [x] Updated README with Real LLM Integration section
- [x] Updated DECISION_REGISTRY and C4_ARCHITECTURE

### v2.3 Release (2025-10-15)
- [x] Semantic Similarity Rating (SSR) integration
- [x] SSRResponseGenerator for realistic Likert-scale distributions
- [x] 8 reference scales (engagement, satisfaction, difficulty, progress, relevance, completion, confidence, interest)
- [x] YAML-driven reference scale configuration
- [x] Optional SSR support in JourneyGenerator
- [x] Temperature control for distribution sharpness
- [x] Survey aggregation for cohort-level statistics
- [x] Example script with 6 comprehensive demonstrations
- [x] ADR-0006: Semantic Similarity Rating Integration
- [x] SSR documentation in README

### v2.2 Release (2025-10-07)
- [x] Persona-based E2E testing framework
- [x] Beta test simulation cohort (5 ceramicists matching screening criteria)
- [x] E2E test scenarios catalog (50+ scenarios across all personas)
- [x] Persona-aware Playwright page objects (BasePage, UploadPage)
- [x] Test fixtures from synthetic data
- [x] First capture session tests (12 Playwright tests)
- [x] Beta cohort selector (generate_beta_test_cohort.py)
- [x] E2E framework documentation (README, test scenarios)
- [x] ADR-0005: E2E Testing Framework
- [x] User story mapping to test scenarios

### v2.1 Release (2025-10-07)
- [x] Synthetic User Generation Framework integration
- [x] Correlation matrices (age ↔ tech_comfort, etc.)
- [x] Engagement stratification (high/standard/low)
- [x] Knowledge capture behaviors (systematic, opportunistic, crisis-driven, experimental)
- [x] Expanded persona set (10 personas: core 80%, edge cases 20%)
- [x] Enhanced PersonaGenerator with correlations
- [x] Enhanced JourneyGenerator with engagement/behavior patterns
- [x] 500-user cohort generation and validation
- [x] Framework validation tool (analyze_framework_validation.py)
- [x] ADR-0004: Framework Integration
- [x] Updated documentation (RECENT_CHANGES, README, DECISION_REGISTRY)

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

**Last Updated:** 2025-10-16
**Maintainer:** Stephen Szermer
