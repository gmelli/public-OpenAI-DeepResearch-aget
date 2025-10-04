# Research Plan: Spec-driven Release Hygiene for Agent Migrations (v2.4→v2.5)

**Agent:** my-OpenAI-DeepResearch-aget
**Date:** 2025-10-03
**Status:** Draft (Dry-run - No External Calls)
**Type:** Migration Hygiene Research

---

## Objectives

**Primary Objective:**
Establish a specification-driven release hygiene protocol for AGET framework migrations, specifically addressing the v2.4→v2.5 transition to prevent regression and ensure consistency across agent instances.

**Secondary Objectives:**
1. Identify critical contract points that must remain stable across minor versions
2. Define testable acceptance criteria for version migrations
3. Document migration risks specific to the v2.4→v2.5 transition
4. Create reusable migration validation checklist

**Scope:**
- Focus on AGET framework v2.4.x → v2.5.x migrations
- Include: wake/identity contracts, version metadata, routing/ownership labels
- Exclude: Major version transitions (3.x), agent-specific business logic

---

## Key Research Questions

1. **Contract Stability:** What behavioral contracts must remain unchanged across minor version bumps? [C1]
2. **Regression Vectors:** Which v2.4 features are most vulnerable to regression in v2.5? [C2]
3. **Test Coverage:** What CI test patterns effectively catch identity/wake/routing regressions? [C3]
4. **Migration Sequence:** What is the optimal migration path for a multi-agent system? [C4]
5. **Validation Gates:** At what checkpoints should migration be blocked if tests fail? [C5]

---

## Method Outline (Local-Only Sources)

### Step 1: Contract Identification
**Objective:** Catalog behavioral contracts in v2.4 that must persist in v2.5

**Local Sources:**
- `.aget/version.json` - Version metadata schema [C6]
- `AGENTS.md` - Agent identity and wake protocol [C7]
- `.aget/patterns/session/aget_wake_up.py` - Wake entrypoint implementation [C8]
- `Makefile` - Standard wake target configuration [C9]
- `.aget/schemas/` - Collaboration and session metadata schemas [C10]

**Analysis Method:**
- Extract version-agnostic vs version-specific behaviors
- Map dependencies between wake, identity, and version declarations
- Identify implicit contracts (e.g., case-sensitive agent names on Linux CI)

**Output:** Contract catalog with stability classifications (MUST-PRESERVE, SHOULD-PRESERVE, MAY-CHANGE)

---

### Step 2: Regression Surface Analysis
**Objective:** Identify high-risk areas where v2.5 changes could break v2.4 contracts

**Local Sources:**
- `sessions/SESSION_2025-10-03_v24_health_check.md` - Current v2.4 health baseline [C11]
- Git commit history for v2.3→v2.4 migration [C12]
- `.aget/migration_history` (if exists) [C13]
- Agent-specific configuration files [C14]

**Analysis Method:**
- Review v2.3→v2.4 migration issues as precedent
- Map contract points to potential failure modes
- Classify risks by severity (CRITICAL, HIGH, MEDIUM, LOW)

**Output:** Risk matrix with failure modes, affected contracts, detection methods

---

### Step 3: Test Strategy Design
**Objective:** Define CI test suite for v2.5 migration validation

**Local Sources:**
- Existing test suites (if present) [C15]
- `.github/workflows/` - CI pipeline configuration [C16]
- Migration checklist patterns from v2.4 health check [C17]

**Test Categories:**
1. **Identity Tests:** Assert agent_name matches across artifacts
2. **Wake Tests:** Verify Makefile wake → script → expected output chain
3. **Version Tests:** Validate version.json + AGENTS.md alignment
4. **Routing Tests:** Confirm hub labels exist and route correctly
5. **Metadata Tests:** Verify collaboration schemas load correctly

**Platform Requirements:**
- Must run on Linux (case-sensitive filesystem testing)
- Must validate against v2.5.0 specification
- Must fail fast with clear error messages

**Output:** Test specification with assertions, fixtures, expected outcomes

---

### Step 4: Migration Sequence Validation
**Objective:** Define safe migration path for multi-agent systems

**Local Sources:**
- `.aget/coordination/` - Handoff and collaboration infrastructure [C18]
- Agent dependency graph (derived from managed_by + handoff patterns) [C19]
- Version compatibility matrix (if exists) [C20]

**Analysis Method:**
- Identify agent dependency chains (supervisor → workers → specialists)
- Determine which agents must migrate first to maintain system stability
- Define rollback criteria if migration fails mid-sequence

**Migration Order Hypothesis:**
1. Supervisor agents first (my-supervisor-AGET)
2. Core infrastructure agents (routing, triage)
3. Specialized agents (research, analysis)
4. Experimental/bleeding-edge agents last

**Output:** Migration sequence DAG with validation checkpoints

---

### Step 5: Validation Gate Definition
**Objective:** Establish go/no-go criteria for v2.5 promotion

**Validation Gates:**

**Gate 1: Pre-Migration Health Check**
- All v2.4 agents pass current health check
- No critical routing issues in last 7 days
- All supervisor handoffs functioning

**Gate 2: Test Suite Green**
- All v2.5 contract tests pass in CI
- Identity tests pass on Linux (case-sensitive)
- Wake entrypoint tests validate script chaining
- No regressions in existing functionality

**Gate 3: Canary Deployment**
- Migrate 1 non-critical agent to v2.5
- Monitor for 24 hours
- Verify handoffs to/from v2.4 agents still work

**Gate 4: Staged Rollout**
- Migrate agents in dependency order
- Validate each stage before proceeding
- Maintain rollback capability at each stage

**Gate 5: Full System Validation**
- All agents on v2.5
- End-to-end tests pass
- No degradation in routing/collaboration metrics

**Output:** Validation gate checklist with pass/fail criteria

---

## Risks and Mitigations

### Risk 1: Case-Sensitivity Regression
**Severity:** HIGH
**Description:** Agent names or file paths behave differently on Linux vs macOS [C21]
**Mitigation:** Mandatory Linux CI tests for all migrations
**Validation:** Test failures block promotion to v2.5

### Risk 2: Wake Entrypoint Drift
**Severity:** CRITICAL
**Description:** Makefile wake stops calling shared script, breaking consistency [C22]
**Mitigation:** CI tests assert Makefile → script → output chain
**Validation:** Compare make wake vs python3 script output

### Risk 3: Version Metadata Desync
**Severity:** HIGH
**Description:** version.json and AGENTS.md declare different versions [C23]
**Mitigation:** Automated version alignment checks in CI
**Validation:** Fail if version.json.aget_version ≠ AGENTS.md @aget-version

### Risk 4: Breaking Collaboration Protocol
**Severity:** CRITICAL
**Description:** v2.5 changes break handoff compatibility with v2.4 agents [C24]
**Mitigation:** Schema versioning + backward compatibility tests
**Validation:** Mixed v2.4/v2.5 handoff tests pass

### Risk 5: Incomplete Migration
**Severity:** MEDIUM
**Description:** Some agents stuck on v2.4 indefinitely [C25]
**Mitigation:** Migration sequence DAG prevents partial rollout
**Validation:** All agents in dependency chain migrate together

---

## Validation Steps

### Pre-Research Validation
- ✅ Confirm v2.4 baseline health (see SESSION_2025-10-03_v24_health_check.md)
- ✅ Identify migration scope (v2.4→v2.5 minor version)
- ✅ Define research boundaries (no external APIs, local sources only)

### During Research Validation
- Review contract catalog against actual v2.4 implementations
- Validate risk matrix against historical migration issues
- Ensure test strategy covers all identified contracts
- Verify migration sequence respects actual dependencies

### Post-Research Validation
- Dry-run test suite against v2.4 agents (should all pass)
- Simulate migration sequence with dependency graph
- Review validation gates with supervisor agent
- Get approval for v2.5 migration plan

---

## Local-Only Citation Placeholders

[C1] AGET Framework Minor Version Contract Specification (local docs)
[C2] v2.3→v2.4 Migration Post-Mortem (git history)
[C3] CI/CD Best Practices for Agent Testing (local patterns)
[C4] Multi-Agent System Migration Patterns (coordination docs)
[C5] Release Gate Criteria for AGET Framework (version docs)
[C6] .aget/version.json schema and semantics
[C7] AGENTS.md specification and wake protocol
[C8] aget_wake_up.py implementation and output format
[C9] Makefile standard targets and conventions
[C10] .aget/schemas/ collaboration_context_v1.0.yaml, session_metadata_v1.0.yaml
[C11] Current v2.4 health check session notes
[C12] Git log --grep="v2.4" analysis
[C13] Migration history tracking files
[C14] Agent manifest, version files, configuration
[C15] Existing test suites in tests/ or .aget/tests/
[C16] GitHub Actions workflow configurations
[C17] Health check protocol as test template
[C18] Handoff request/response file patterns
[C19] Derived from managed_by fields and handoff logs
[C20] Version compatibility matrix (to be created)
[C21] Filesystem case-sensitivity differences
[C22] Wake entrypoint implementation coupling
[C23] Version declaration synchronization
[C24] Collaboration schema backward compatibility
[C25] Migration sequence enforcement mechanisms

---

## Expected Deliverables

1. **Contract Catalog** - Behavioral contracts for v2.4→v2.5 stability
2. **Risk Matrix** - Failure modes, severity, detection methods
3. **Test Specification** - CI test suite with assertions
4. **Migration DAG** - Dependency-ordered migration sequence
5. **Validation Checklist** - Go/no-go criteria for each gate
6. **Implementation Proposal** - GitHub issue for v2.5 contract tests

**Next Action:** File GitHub issue "[my-OpenAI-DeepResearch-aget] v2.5: add wake/identity contract tests" in gmelli/aget-aget

---

*Research plan generated by my-OpenAI-DeepResearch-aget (DeepThink)*
*Dry-run mode: No external API calls made*
*All citations reference local sources only*
