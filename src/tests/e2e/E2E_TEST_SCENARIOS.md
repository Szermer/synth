# E2E Test Scenarios - Private Language

**Based on Synthetic User Framework (500-user cohort)**

This document maps the 10 persona types to specific E2E test scenarios for Private Language platform validation.

## Overview

- **500 synthetic users** with realistic behavioral patterns
- **10 persona types** covering core users (80%) and edge cases (20%)
- **3 engagement tiers** (high, standard, low) within each persona
- **4 capture behaviors** (systematic, opportunistic, crisis-driven, experimental)

## Test Scenario Matrix

| Persona | Distribution | Priority | Critical Paths | Edge Cases |
|---------|--------------|----------|----------------|------------|
| Master Educator | 30% | P0 | Curriculum upload, student queries | Retirement urgency, accreditation |
| Studio Practitioner | 20% | P0 | Multi-modal capture, technique docs | Low tech comfort, dropout |
| Department Head | 15% | P1 | Institution setup, faculty mgmt | Budget justification, ROI |
| Early Adopter | 10% | P1 | Feature exploration, community | Bleeding-edge requests, feedback |
| Skeptical Veteran | 5% | P2 | Privacy flows, onboarding friction | AI resistance, dropout |
| Cross-Domain | 6% | P2 | Multi-role workflows, context switching | Complex integrations |
| International | 5% | P2 | GDPR compliance, language support | Time zones, payments |
| Industry Trainer | 4% | P2 | Compliance docs, certification | Audit trails, bulk operations |
| Graduate Student | 3% | P3 | Advisor capture, dissertation | Budget constraints, sharing |
| Outlier/Stress | 2% | P3 | System boundaries, extreme usage | Accessibility, edge cases |

---

## Core Personas (80% - P0/P1)

### 1. Master Educator (30% - 150 users) - P0

**Persona Characteristics:**
- Age: 40-65
- Tech Comfort: 0.5-0.8 (functional user)
- AI Attitude: Pragmatic/Cautious (correlated with tech comfort)
- Career Stage: 60% late-career (retirement urgency)
- Subject Domain: 35% STEM, 25% Liberal Arts, 20% Vocational
- Institution: 30% Research Uni, 25% Liberal Arts, 20% Community College

**Engagement Patterns:**
- High (20%): Daily uploads, comprehensive curriculum docs, active community
- Standard (60%): 2-3x weekly, course material focus, occasional queries
- Low (20%): Weekly sporadic, minimal docs, passive

**Capture Behavior:**
- Systematic (25%): Scheduled weekly curriculum updates
- Opportunistic (35%): After lectures, during grading
- Crisis-Driven (25%): Before accreditation, retirement deadline
- Experimental (15%): Testing different capture methods

**Critical Test Scenarios:**

#### **T-ME-001: First Curriculum Upload** (P0)
```
Given: New Master Educator account (tech_comfort: 0.6)
When: Uploads first lecture recording (45 min, video + slides)
Then:
  - Upload completes within 2 minutes
  - Extraction identifies: concepts, teaching methodology, student interactions
  - Preview shows semantic entities with 85%+ confidence
  - User can review low-confidence extractions
Expected Time: 15 minutes (matches synthetic data)
```

#### **T-ME-002: Systematic Weekly Pattern** (P0)
```
Given: Established educator with systematic capture behavior
When: Uploads weekly lectures for 8 weeks (simulated)
Then:
  - Platform suggests scheduling (detected pattern)
  - Curriculum structure auto-generated
  - Student question variations identified across weeks
  - Evolution of teaching approach tracked
Journey: 8-20 sessions over 8-16 weeks
```

#### **T-ME-003: Retirement Urgency - Crisis Upload** (P1)
```
Given: Late-career educator (age: 62, retirement_timeline: 2 years)
When: Uploads 20 years of course materials in 2-week burst
Then:
  - Batch upload handling (up to 50 files)
  - Processing queue management
  - Progress tracking and resumability
  - Extraction quality maintained under load
Pattern: Crisis-driven (3 uploads/day for 14 days, then gap)
```

#### **T-ME-004: Student Query Workflow** (P0)
```
Given: Educator with 12 weeks of captured lectures
When: Student asks "Why does centering fail with soft clay?"
Then:
  - Query finds relevant teaching moments across sessions
  - Answer includes: materials (clay type), process (centering), conditions (humidity)
  - Response cites specific lecture timestamps
  - Confidence scores shown for causal relationships
Response Time: <10s for complex query
```

#### **T-ME-005: Accreditation Documentation** (P1)
```
Given: Department head persona with accreditation_involvement: true
When: Generates accreditation report for curriculum
Then:
  - Learning objectives extracted and mapped
  - Teaching methodology documented
  - Student outcome patterns identified
  - Export to PDF with citations
Use Case: 30% have accreditation as primary concern
```

**Edge Cases:**
- Very low tech comfort (0.2-0.4): Needs simplified onboarding
- PhD with publication pressure: Wants citable knowledge base
- K-12 educator: Different terminology, FERPA considerations

---

### 2. Studio Practitioner (20% - 100 users) - P0

**Persona Characteristics:**
- Age: 25-65 (wide range)
- Tech Comfort: 0.3-0.7 (cautious)
- Medium: 25% ceramics, 20% visual arts, 15% textile/woodworking
- Practice Type: 40% teaching artist, 35% studio+workshops
- Career Stage: 50% mid-career, 25% established

**Critical Test Scenarios:**

#### **T-SP-001: First Ceramics Session - Multi-Modal** (P0 - Beta Test Scenario)
```
Given: Ceramicist (3+ years experience, tech_comfort: 0.55)
When: Uploads first throwing session (video: 22 min)
  - Shows centering → opening → pulling → shaping
  - Verbal commentary on humidity, clay consistency
  - Visible tool usage and hand positions
Then:
  - Kinetic dimension: Hand positions, tool movements extracted
  - Dynamic dimension: Clay state changes identified
  - Temporal dimension: Process steps sequenced correctly
  - Social dimension: Teaching explanations recognized
  - Contextual dimension: Studio conditions noted
Validation: Matches beta testing plan criteria
Expected Time: 13-15 minutes (per framework data)
```

#### **T-SP-002: Low Tech Comfort - Error Recovery** (P0)
```
Given: Studio practitioner (tech_comfort: 0.35, age: 58)
When: Encounters upload error (file format, size limit)
Then:
  - Clear, non-technical error messages
  - Suggested fixes (convert video, compress file)
  - Option to request white-glove support
  - Session state preserved (can retry)
Dropout Risk: High if not handled well
```

#### **T-SP-003: Technique Evolution Tracking** (P1)
```
Given: Mid-career ceramicist with 15 sessions over 6 months
When: Queries "How has my glazing technique changed?"
Then:
  - Timeline visualization of technique evolution
  - Success/failure patterns identified
  - Environmental factor correlations (seasonal humidity)
  - Confidence improvements tracked
Pattern: Opportunistic capture (1-14 day intervals)
```

#### **T-SP-004: Teaching Workshop Capture** (P0)
```
Given: Teaching artist with 5 students (different skill levels)
When: Uploads workshop session (90 min, multi-person)
Then:
  - Social dimension: Individual student adaptations extracted
  - Teaching moments differentiated (beginner vs advanced)
  - Student questions and responses captured
  - Skill-level-specific explanations identified
Use Case: 40% are teaching artists
```

**Edge Cases:**
- Pure studio artist (no teaching): Different motivation, value prop
- Digital arts: Different capture needs (screen recording, process files)
- Commercial pressure (high): Needs ROI validation, client work separation

---

### 3. Department Head (15% - 75 users) - P1

**Persona Characteristics:**
- Age: 45-65
- Education: 80% PhD
- Department Size: 40% small (5-10), 35% medium (11-25)
- Primary Concern: 35% faculty turnover, 30% accreditation
- Decision Authority: 50% influence/recommendation, 30% full budget

**Critical Test Scenarios:**

#### **T-DH-001: Institution Setup - Multi-Faculty** (P1)
```
Given: Department head (department_size: medium_11_25)
When: Sets up institutional account for 15 faculty members
Then:
  - Department structure configuration
  - Faculty onboarding workflow
  - Permission and access controls
  - Billing and budget tracking
  - Usage analytics dashboard
Budget Authority: $50K-$500K range
```

#### **T-DH-002: Retiring Faculty Knowledge Capture** (P0)
```
Given: Faculty member retiring in 6 months
When: Department head initiates legacy capture project
Then:
  - White-glove onboarding for retiring faculty
  - Accelerated capture workflow
  - Department knowledge graph integration
  - Successor training materials generated
Urgency: 35% cite faculty turnover as primary concern
```

#### **T-DH-003: ROI Metrics Dashboard** (P1)
```
Given: Department head needs budget justification
When: Accesses ROI dashboard after 6 months
Then:
  - Knowledge assets quantified (hours saved, techniques documented)
  - Faculty time investment tracked
  - Student query resolution metrics
  - Comparison to manual documentation costs
Decision Driver: 15% cite budget efficiency as concern
```

**Edge Cases:**
- K-12 department head: FERPA compliance, parent communication
- Arts organization (non-academic): Different structure, funding models
- Full budget control: Wants enterprise features, SSO, custom contracts

---

### 4. Early Adopter (10% - 50 users) - P1

**Persona Characteristics:**
- Age: 30-50 (younger)
- Tech Comfort: 0.85-0.98 (very high)
- AI Attitude: Enthusiastic/Pragmatic
- Primary Role: 40% educator+technologist, 30% pure educator
- Influence: 40% department-wide, 25% institution-wide

**Critical Test Scenarios:**

#### **T-EA-001: Feature Exploration - Bleeding Edge** (P1)
```
Given: Early adopter (tech_comfort: 0.92, innovation_focus: ai_integration)
When: Explores all platform features in first week
Then:
  - All features accessible and documented
  - Advanced features (API, integrations, analytics)
  - Community features (sharing, collaboration)
  - Feedback mechanism prominent
  - Feature request tracking
Expected: 20-25 sessions in first month (high engagement)
```

#### **T-EA-002: API Integration Test** (P2)
```
Given: Educational technologist wants LMS integration
When: Attempts to integrate with Canvas/Moodle
Then:
  - API documentation clear and complete
  - OAuth flow works seamlessly
  - Webhook support for real-time updates
  - Rate limits documented and reasonable
Use Case: 35% focused on AI integration
```

#### **T-EA-003: Community Contribution** (P1)
```
Given: Institution-wide thought leader
When: Creates shareable knowledge templates
Then:
  - Template creation workflow
  - Public sharing options
  - Attribution and licensing
  - Discovery by other users
Influence: 25% are external thought leaders
```

**Edge Cases:**
- IT support role: Infrastructure concerns, SSO, data residency
- Wants to build on platform: API extensibility, webhooks, custom UI

---

### 5. Skeptical Veteran (5% - 25 users) - P2

**Persona Characteristics:**
- Age: 50-70 (older)
- Tech Comfort: 0.2-0.5 (low)
- AI Attitude: Skeptical/Fearful/Cautious
- Skepticism Type: 40% AI replacement fear, 30% privacy concerns
- Conversion Potential: 40% high with proof, 35% medium with peers

**Critical Test Scenarios:**

#### **T-SV-001: Privacy-First Onboarding** (P2)
```
Given: Skeptical veteran (ai_attitude: fearful, privacy_concerns: high)
When: First login and data upload
Then:
  - Prominent privacy controls
  - Data sovereignty explained clearly
  - "How AI is used" transparency
  - Option to exclude data from training
  - Granular sharing controls
Dropout Risk: Very high if trust not established
```

#### **T-SV-002: Peer Proof - Success Stories** (P2)
```
Given: Veteran with medium_with_peers conversion potential
When: Views case studies from similar users
Then:
  - Testimonials from respected peers
  - Specific ROI examples
  - "It won't replace you" messaging
  - Human-in-the-loop workflows highlighted
Conversion: 35% need peer validation
```

#### **T-SV-003: Gradual Adoption Path** (P2)
```
Given: Veteran with low completion rates (discovery: 0.4-0.6)
When: Onboards with minimal features
Then:
  - Progressive disclosure of features
  - "Manual mode" for all AI features
  - Clear value before asking for more data
  - Support hotline prominently displayed
Journey: 5-8 sessions, high dropout risk
```

**Edge Cases:**
- Active resistor (5%): May never convert, test graceful exit flow
- Time investment worry: Needs quick wins, minimal setup
- Change resistance: Familiar UI patterns, minimal innovation

---

## Edge Cases (20% - P2/P3)

### 6. Cross-Domain Practitioner (6% - 30 users) - P2

**Test Scenarios:**

#### **T-CD-001: Multi-Role Knowledge Streams** (P2)
```
Given: Artist-educator-researcher with 3 distinct roles
When: Uploads content across all domains
Then:
  - Context switching without data loss
  - Unified knowledge graph with role separation
  - Cross-domain insights (teaching informs art practice)
  - Audience-specific views (students vs gallery vs journal)
Complexity: High workflow integration needs
```

---

### 7. International User (5% - 25 users) - P2

**Test Scenarios:**

#### **T-IU-001: GDPR Compliance Flow** (P2)
```
Given: European user (regulatory_context: gdpr)
When: Signs up and uploads data
Then:
  - GDPR consent banners and controls
  - Right to deletion prominent
  - Data portability (export all data)
  - EU data residency confirmed
  - DPA available for institutional users
Requirement: 50% are subject to GDPR
```

#### **T-IU-002: Non-English Content** (P3)
```
Given: User with primary_language: non_english
When: Uploads French lecture
Then:
  - Language detection automatic
  - Extraction quality maintained
  - Query responses in French
  - UI language switcher
Support: Medium-high language needs
```

---

### 8. Industry Trainer (4% - 20 users) - P2

**Test Scenarios:**

#### **T-IT-001: Compliance Audit Trail** (P2)
```
Given: OSHA compliance trainer
When: Documents safety training program
Then:
  - Audit trail for all training sessions
  - Certification tracking
  - Compliance report generation
  - Timestamp and versioning
Use Case: 25% have compliance requirements
```

---

### 9. Graduate Student (3% - 15 users) - P3

**Test Scenarios:**

#### **T-GS-001: Budget-Constrained User** (P3)
```
Given: PhD student (budget_tier: low, payment_source: personal)
When: Evaluates platform
Then:
  - Student discount clearly offered
  - Freemium tier with meaningful functionality
  - Academic pricing transparent
  - Advisor group billing option
Conversion: Price-sensitive segment
```

---

### 10. Outlier/Stress Case (2% - 10 users) - P3

**Test Scenarios:**

#### **T-OS-001: Extreme Volume Upload** (P3)
```
Given: Power user (documentation_volume: 1000 pages/month)
When: Uploads massive knowledge base
Then:
  - Batch processing handles scale
  - No degradation in quality
  - Progress visibility
  - Graceful handling of limits
Pattern: Stress test system boundaries
```

#### **T-OS-002: Accessibility Requirements** (P3)
```
Given: User with accessibility needs
When: Uses platform with screen reader
Then:
  - WCAG 2.1 AA compliance
  - Keyboard navigation functional
  - Alt text for all images
  - High contrast mode
  - Transcript generation automatic
Use Case: Edge case but critical
```

---

## Engagement Tier Testing

### High Engagement (20% of each persona)

**Test Pattern:**
- **Sessions**: 15-25 over 2-4 months
- **Completion Rate**: +20% above persona baseline
- **Features Used**: Community, advanced analytics, API
- **Support Needs**: Feature requests, collaboration

**Key Tests:**
- T-ENG-HIGH-001: Community participation workflow
- T-ENG-HIGH-002: Advanced analytics dashboard
- T-ENG-HIGH-003: Collaboration and sharing features

### Standard Engagement (60% of each persona)

**Test Pattern:**
- **Sessions**: 10-20 over 2-4 months
- **Completion Rate**: Persona baseline
- **Features Used**: Core capture and query workflows
- **Support Needs**: Occasional how-to questions

**Key Tests:**
- T-ENG-STD-001: Standard upload and query workflow
- T-ENG-STD-002: Email notifications and reminders
- T-ENG-STD-003: Progress tracking

### Low Engagement (20% of each persona)

**Test Pattern:**
- **Sessions**: 5-12 over 3-6 months
- **Completion Rate**: -20% below baseline
- **Features Used**: Minimal, may drop off
- **Support Needs**: Re-engagement campaigns

**Key Tests:**
- T-ENG-LOW-001: Dropout detection and recovery
- T-ENG-LOW-002: Re-engagement email campaigns
- T-ENG-LOW-003: Simplified return-to-platform flow

---

## Capture Behavior Testing

### Systematic (25%)

**Pattern**: Regular 2-7 day intervals

**Tests:**
- T-CB-SYS-001: Scheduled upload reminders
- T-CB-SYS-002: Pattern detection and suggestions
- T-CB-SYS-003: Calendar integration

### Opportunistic (35%)

**Pattern**: Variable 1-14 day intervals

**Tests:**
- T-CB-OPP-001: Mobile upload (capture in moment)
- T-CB-OPP-002: Quick capture workflow
- T-CB-OPP-003: Session timeout handling

### Crisis-Driven (25%)

**Pattern**: Bursts (1-3 days) then gaps (10-30 days)

**Tests:**
- T-CB-CRI-001: Batch upload handling (3-10 files/day)
- T-CB-CRI-002: Processing queue under load
- T-CB-CRI-003: Resumability after gaps

### Experimental (15%)

**Pattern**: Very irregular (1-21 days)

**Tests:**
- T-CB-EXP-001: Support for different file formats
- T-CB-EXP-002: Feature discovery and experimentation
- T-CB-EXP-003: Feedback loop for new patterns

---

## Test Data Requirements

### From 500-User Cohort

**Available Data:**
- 500 complete user profiles with journeys
- Realistic attribute distributions
- Engagement tier assignments
- Capture behavior patterns
- Journey step sequences with timestamps

**Test Fixture Generation:**
- Extract 5-10 users per persona type for test suite
- Generate realistic file metadata (duration, size, format)
- Create expected extraction outputs based on attributes
- Map queries to knowledge graph responses

### Beta Test Subset

**Criteria** (from beta testing plan):
- 3-5 Studio Practitioners
- Medium: ceramics or woodworking
- Practice experience: 3+ years
- Teaching experience: workshops or classes
- Tech comfort: moderate (0.4-0.7)
- Engagement tier: standard or high

**Use Cases:**
- First capture session validation
- Extraction quality benchmarking
- Query satisfaction testing
- Review interface usability

---

## Implementation Priority

### Phase 1: Core Personas - Critical Paths (P0)
1. Master Educator: First upload, query workflow, systematic pattern
2. Studio Practitioner: Multi-modal capture, low tech comfort, error recovery

### Phase 2: Institutional & Adoption (P1)
3. Department Head: Institution setup, ROI dashboard
4. Early Adopter: Feature exploration, API integration
5. Skeptical Veteran: Privacy flow, dropout recovery

### Phase 3: Edge Cases (P2/P3)
6-10. Remaining personas for comprehensive coverage

### Phase 4: Engagement & Behavior Patterns
- Engagement tier variations across all personas
- Capture behavior timing tests

---

## Metrics & Success Criteria

### Test Coverage
- ✅ All 10 personas have critical path tests
- ✅ Each engagement tier represented
- ✅ Each capture behavior validated
- ✅ Beta test scenarios match real user criteria

### Performance Baselines
- Upload: <2 min for 45-min video
- Query: <10s for complex queries
- Extraction: >85% accuracy (measured by user approval rate)
- Time investment: 13-15 min avg (matches framework data)

### Conversion & Retention
- Discovery completion: Per persona thresholds
- Onboarding completion: Per persona thresholds
- Low engagement dropout: <15% unplanned
- Re-engagement success: >30% return after 30 days

---

**Next Steps:**
1. Generate Playwright test suite from scenarios
2. Create test fixtures from synthetic cohort
3. Map to Private Language user stories (US001-US025)
4. Implement beta test simulation

**Maintained by:** Product & QA Teams
**Last Updated:** 2025-10-07
