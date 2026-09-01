# Changelog

## [3.33.1] - 2026-08-30 - "Receiver-visible integrity"

### Changed
- Advanced the template's framework identity and migration history to v3.33.1.
- Preserved the v3.33.0 payload; this package carries release-coherence metadata only.

All notable changes to this template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



## [3.33.0] - 2026-08-30

### Changed
- Payload converged with canonical; version surfaces aligned. This bump crosses two releases: v3.32.0 never reached the template tier.

## [3.31.1] - 2026-08-18 - "Receiver-Safe Close Gates"

### Changed
- Version coherence bump to framework v3.31.1. The receiver-safe close-gate correction remains a
  core package and is not propagated into this template by this patch.

---

## [3.31.0] - 2026-08-15 - "Ship What Was Already Built"

### Changed
- Version coherence bump to framework v3.31.0. See the canonical
  [aget CHANGELOG](https://github.com/aget-framework/aget/blob/v3.31.0/CHANGELOG.md)
  for the release contents: five verification instruments promoted to canonical,
  routable skill descriptions, and the accumulated fixes.

---

## [3.30.0] - 2026-08-09 - "Portable Skills, Continuous Cadence"

### Added
- Added a bounded, digest-addressed Agent Skills package with a shipped conformance validator and documented manual cross-client use.

### Changed
- Changed Agent Skills frontmatter to the current specification shape for the packaged subset.

### Documentation
- Documented that hooks, permissions, release gates, and structural enforcement do not travel with the package.

## [3.29.0] - 2026-08-01 - "Repair release truth and reduce principal decision work"

### Added
- Added Codex-native discovery for wake-up, study-topic, and save-state with explicit recovery.
- Added exact Claude Code and Codex CLI control-conformance evidence plus a one-view release decision contract.

### Changed
- Changed study-topic ranking so purpose weighting is effective and recency, searched surfaces, and external omissions are disclosed.

### Fixed
- Fixed distribution evidence so producer, distribution point, received state, and downstream behavior remain independent predicates.

## [3.28.0] - 2026-07-26 - "Make the gates fire"

**Release class**: governance-hardening — inward-facing. Expect changed *gate behaviour*, not new features.

### Changed
- Theme: enforcement that fires without being invoked. The release-gate battery gains a forced firing point at the irreversible act (tag / `push --tags` / `push --follow-tags`), and the Phase 7.1.5 release-quality score must carry a resolvable **independent** verification leg — a producer-run score no longer settles its own gate. Triage freshness becomes a measured SLO whose rollup detects *rollup-without-triage*, so measuring the queue cannot substitute for working it.

### Fixed
- Release metadata dates were never bumped: `version_bump.py` moved version strings but left `codemeta.json:dateModified` and `CITATION.cff:date-released` stale (3.27.0 shipped 07-18 carrying 07-11 dates).
- `study_topic.py` advertised the specification tier in its printed search contract while never searching it — every study reported zero specs (*manufactured absence*, not omission).
- Release-metric issue counts saturated at a page cap and recorded `0` on API failure, making a failed count indistinguishable from zero.
- The contract suite could not pass its own 60s pre-release timeout (528s, with 81% of runtime in three tests that re-ran the whole battery).

### Governance
- Test-requirement traceability: the 80% figure was a never-met pilot aspiration; replaced by a ratified floor at the measured **39%**, rising +5pp per minor release — a bar that blocks regression rather than blocking everything.
- Release-gate scope made explicit: **release-integrity** failures block a tag absolutely; **codebase-quality** debt is reported with a named owner and does not block.

## [3.27.0] - 2026-07-18 - "Finish & Verify"

### Changed
- Theme: the portfolio learns to FINISH (EC tick-state maintained signal CIS-010; CIS-008 Achieve-only re-spec; NASCENT typing backfill; L-doc ID injectivity remediation L1200-L1209 + tombstone registry) and the release learns to VERIFY what it shipped runs (migration Rung-4 behavioral verification + mandatory Behavioral Smoke; 3-axis tag-payload coherence [14 origins x tagged-tree paths x executed-surface]; single Corrections-since-tag surface; DoD ID-axis row-completeness ratchet; public-graph coherence joins computed DoD; verify-before-claim coverage matrix). Also: Transactional Execution doctrine + workspace convention in all template AGENTS.md; universal-skill conformance 14/14 (core + document-processor backfilled); single-slash permission-rule detector; dual-status mask scanner; wind-down double-fire guard; delegated-prompt date contract; Filing_Candidate L-doc marker standard.

## [3.26.0] - 2026-07-11

**Theme**: Signals & Contracts

- `wake_up.py` release-currency signal — session start reports when the local framework version is behind the latest release; silent when current (fail-soft).
- `health_check_ext.py` + `study_topic_ext.py` extension hooks — instance customization without forking Framework_Artifacts.
- `study_topic.py` search contract: surface manifest in output, keyword hygiene, token-boundary matching, ranking floor, `inbox/` surface joined.
- `/aget-close-project`: C-CLOSE-007 (closer mutates scaffold in place) + C-CLOSE-008 (has-it-run gate — executable deliverables need execution evidence pre-COMPLETE).
- Three-state check contract (PASS / FAIL / UNREACHABLE) + terminal-state vocabulary + verify-before-claim coverage matrix (canonical `docs/CONVENTION_*.md`).
- Fixes: `wake_up.py` session-glob case-fold; `check_skill_reliance_manifest.py` archetype-index paths; `close_gate_check.py` independence-WARN restore.

## [3.25.0] - 2026-07-04

**Theme**: Grounded Entities & Trusted Releases

- aget-ask production v1.0.0 (SKILL-045 + spec) — entropy-reducing clarification/followup with altitude filter.
- `study_topic.py`: active-plan detection fixed (case-insensitive, Plan_Status-first — live plans no longer render inactive) + knowledge/+ontology/ search areas.
- `capture_friction.py`: ledger entries carry a value-class (`owed` pending-triage default, CAP-FRIC-006).
- `wake_up.py`/`health_check.py`: reliance self-attestation (R-BND-001-03) + permission-accumulation gate.
- `close_gate_check.py`: closure-substance detection + release-close DoD guard wiring.
- Conformance model: reliance-only (D-1) — canonical-specs reference line added to AGENTS.md; no spec copies shipped.

## [3.22.0] - 2026-06-13

**Theme**: Skill-Support Delivery + Verify-at-Point-of-Use + Hygiene

- Framework version sync to 3.22.0. `/aget-propose-actions` skill updated to **v1.8.0** (Step 3.5 Self-Critique 10-point checklist + Type column; also clears accumulated v1.7.x propagation lag). New framework gates (`deploy_skill.py`, `check_claim_freshness.py`, `check_skill_coherence.py`, `validate_spec_binding.py`) are available in canonical `aget/scripts/` — copy as needed. No breaking changes.

## [3.21.0] - 2026-06-06

**Theme**: Always-On Fleet Operations (governance-scoped)

- Framework version sync to 3.21.0. No template content change (governance scaffolding for unattended operation lands in the canonical framework; see aget/CHANGELOG.md).

## [3.20.3] - 2026-05-31

- C-P3 health-check correctness fix (`check_structural_skill_frontmatter`) propagated to template consumer surface.

## [3.20.2] - 2026-05-31

- Consumer-surface delivery: C-F1/C-P1/C-P3 health & config checks delivered to templates.

## [3.20.0] - 2026-05-30

- Framework version sync to 3.20.0.

## [3.19.0] - 2026-05-23

- Framework version sync to 3.19.0.

## [3.18.0] - 2026-05-16

**Theme**: Aligned with framework v3.18.0 (Substrate Hygiene + Memory-Layer Self-Application; Hybrid A primary + B-tagged streams)

### Changed

- Version bump: 3.17.0 → 3.18.0 (framework alignment)
- `.aget/version.json` `aget_version` updated to 3.18.0

### Framework v3.18.0 Highlights

- `AGET_MEMORY_SURFACE_SPEC v0.2.0` canonical promotion (T1.16 + T2.37) — harness-vs-KB taxonomy formalized
- Verb Registry Currency (T1.9 = PP-021) — 37 Active + 4 Reserved verbs + 11 §Hierarchy Decisions pairs
- `/aget-create-initiative` Strict promotion (T2.46) — D71 verb-pair gap closed
- Homepage Fork C Hybrid (T1.12) — L941-L944 cluster closed structurally
- L908 family memory-layer closure (L960 + L963 + L964 graduated)

See [framework v3.18.0 release notes](https://github.com/aget-framework/aget/releases/tag/v3.18.0) for full details + DEFECT-2/4 acknowledgment.

---

## [3.17.0] - 2026-05-09

**Theme**: Aligned with framework v3.17.0 (Theme C3 — Canonical Coherence + Structural Self-Conformance)

### Changed

- Version bump: 3.16.0 → 3.17.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.17.0
- Inherits framework v3.17.0 deliverables: framework-manager archetype formalization (Q4=A.2 disposition); T2.18 SOP_scope_lock_ceremony LANDED v1.0.0; T2.19 AGET_SKILL_LIFECYCLE_SPEC LANDED v1.0.0 with full V-test authoring; T2.20 AGET_FLEET_UPGRADE_SPEC v0.1 DRAFT; T2.23 AGET_TASK_ROUTING_SPEC v0.1 DRAFT.
- CAP-REL-030 + CAP-REL-031 (post-release CHANGELOG + tag validators) IMPLEMENTED (closes v3.16 sleeping CAPs); CAP-REL-032 + CAP-REL-033 grace-extended to v3.18.0 per Q1=B disposition.

### Compatibility

- **No breaking changes** in v3.17. Existing instances upgrade by version-bump only.
- Optional adoption: `framework-manager` archetype field in `.aget/identity.json`; existing `archetype` values continue to function.

---

## [3.16.0] - 2026-05-02

**Theme**: Aligned with framework v3.16.0 (Framework-Discipline Closure + Wave-1A Spec Contracts + /aget-go Production)

### Changed

- Version bump: 3.15.0 → 3.16.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.16.0
- **Universal-skills migration (#1120)**: 15 missing universal skills added from worker baseline (advisor/analyst/architect/consultant/developer/executive/operator/researcher/reviewer/spec-engineer pre-bump count 19 → post-migration 34, then post-archetype-fit-revert 31 = 29 universal + 2 archetype-specific).
- **Release-triad revert (CAP-TPL-016-07 NEW)**: 3 release-triad skills (`aget-release-build`, `aget-release-audit-specs`, `aget-release-critique`) removed from this template — moved to release-execution archetype catalog (worker, supervisor only). Closes the "presence-not-fit" misfit surfaced by Gate 1 defects audit.

### Compatibility

- **No breaking changes** in v3.16. Existing instances upgrade by version-bump only.
- Optional adoption: `**Plan_Status**:` / `**Gate_Status:**` schema in new PROJECT_PLAN files (CAP-PP-003 disambiguation; backward-compatible).

---

## [3.15.0] - 2026-04-25

**Theme**: Aligned with framework v3.15.0 (Two-Level Model Coherence + Security Hardening)

### Changed

- Version bump: 3.14.0 → 3.15.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.15.0

### Breaking

- **BC-001**: `.aget/version.json` old field names removed (e.g. `agent_name` → `aget_agent_name`). See `aget/docs/BREAKING_CHANGES_v3.15.md`.
- **BC-002**: `--fix` flag removed from `/aget-check-health` (SKILL-003). Use `/aget-enhance-health` instead.

---

## [3.14.0] - 2026-04-18

**Theme**: Aligned with framework v3.14.0 (v3.13 Loop Closure + Scope-Lock Discipline)

### Changed

- Version bump: 3.13.0 → 3.14.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.14.0

### Notes

Per-template CHANGELOG entries for 3.12.0 and 3.13.0 were not individually maintained; template work in those cycles is captured in `aget-framework/aget/CHANGELOG.md`. Gap flagged for v3.14.x / v3.15 retrospective.

---

## [3.11.1] - 2026-04-04

### Changed

- Renamed `aget_housekeeping_protocol.py` → `health_check.py`
- Renamed `study_up.py` → `study_topic.py`
- Config key `skip_sanity` → `skip_health_check`

---
## [3.11.0] - 2026-03-28 - "Skill Conformance, Requirements & Hooks"

### Added

- **requirements/** directory scaffolded (L742 two-level model, #725)
- **.claude/hooks/** directory with README (ADR-008 Generator, #505)
- **governance_intensity** field in AGENTS.md (#732)

### Changed

- 17 skill SKILL.md files updated for L736 conformance (SICR, #678)
- "sanity check" → "health check" terminology (#658)
- RUBRIC.template.md v2.0 deployed

---

## [3.10.0] - 2026-03-21 - "Structural Enforcement"

### Added
- MUST-invoke directives for /aget-create-project and /aget-file-issue (D71)
- Gate Boundary Protocol: plan update + commit as structural proof of gate completion
- Skill Completion Signal pattern in /aget-create-project and /aget-enhance-spec
- SOP Phase -0.5: Content Sync governance (D69/GOV-040)
- SKILL_SPEC_TEMPLATE.yaml (#439)

### Changed
- Skill renames: aget-capture-observation → aget-record-observation, aget-capture-nugget → aget-record-nugget, aget-study-up → aget-study-topic (#480)
- `capture` verb retired from Learning family
- Gate Execution Discipline strengthened with MUST update + MUST commit

### Fixed
- Template hygiene: VERSION, classifier, SECURITY.md corrections (#574)

## [3.9.0] - 2026-03-15 - "Governance Enforcement"

### Added
- Gate 0: Spec Verification (MP-1) in project plan template
- Phase -1: Release Readiness governance in SOP

### Changed
- Version bump to v3.9.0 (5/5 artifact types)
- version_bump.py: extended to cover AGENTS.md, codemeta.json, CITATION.cff
- TEMPLATE_PROJECT_PLAN.md: mandatory Gate 0 added

### Fixed
- aget-enhance-spec: Phase 6 consistency (#418), phantom spec reference (#419)

 - 2026-03-08 - "Governance Maturation"

### Added
- AGENTS.md governance patterns: capability declarations, CLI feature adoption guidance
- `.claude/` scaffolding: settings.json, skills directory structure
- Skill: `aget-expand-ontology` v1.0.0 (optional, acquirable)
- Skill: `aget-enhance-spec` v1.1.0 (specification enhancement lifecycle)

### Changed
- Version bump to v3.8.0
- identity.json: `type` field added
- SOP headers: CAP-SOP-001 compliance
- Migration history entry added

### Notes
- See aget/CHANGELOG.md [3.8.0] for framework changes
- Part of Governance Maturation release (principle codification, deliverable conformance)

---

## [3.7.0] - 2026-03-05 - "Quality Reconciliation"

### Added
- AGENTS.md governance patterns backported (TEMPLATE_AGENTS_MD_SPEC v1.0.0)
- `.claude/` directory scaffolding for CLI feature adoption

### Changed
- Skill renames: `aget-studyup` → `aget-study-up`, `aget-healthcheck-*` → `aget-check-*`
- README positioning: evidence-based reframe, removed undemonstrated claims
- Version bump to v3.7.0
- Migration history entry added

### Notes
- See aget/CHANGELOG.md [3.7.0] for framework changes
- Part of Quality Reconciliation release (content integrity, SOP lifecycle, positioning reframe)

---

## [3.6.0] - 2026-02-21 - "Infrastructure Maturation"

### Added
- Universal skill: `aget-studyup` (focused KB research before implementation)
- Canonical script: `scripts/study_up.py`

### Changed
- Platform claims: "Claude Code, Codex CLI, Gemini CLI" (was "Claude Code, Cursor, Aider, Windsurf")
- Version bump to v3.6.0
- Migration history entry added

### Notes
- See aget/CHANGELOG.md [3.6.0] for framework changes
- Part of Infrastructure Maturation release (observability, content integrity, ontology)

---

## [3.5.0] - 2026-02-14 - "Archetype Customization"

### Added
- Archetype-specific skills: `aget-analyze-data`, `aget-generate-report`
- Formal ontology: `ontology/ONTOLOGY_analyst.yaml` (7 concepts, 3 clusters)
- Universal skill: `aget-file-issue` (14th universal)
- Evaluator-focused README narrative

### Changed
- SKILL_VOCABULARY.md v1.2.0 with SKOS reference
- README structure: "Why Analyst?" value proposition

### Notes
- See aget/CHANGELOG.md [3.5.0] for framework changes
- Part of Archetype Customization release

---

## [3.4.0] - 2026-01-18 - "Session Skills Maturity"

### Added
- Session protocol enhancements (re-entrancy guard, calendar awareness)
- Template infrastructure: `sops/SOP_escalation.md`

### Changed
- Cross-CLI validation (Claude Code, Codex CLI, Gemini CLI)
- Governance formalization patterns

### Notes
- See aget/CHANGELOG.md [3.4.0] for framework changes

---

## [3.3.0] - 2026-01-11 - "Framework Alignment"

### Changed
- Updated to AGET framework v3.3.0
- Major upgrade from 3.0.0-beta.1 (skipping 3.0.x, 3.1.x, 3.2.x)

### Notes
- See aget/CHANGELOG.md for cumulative framework changes since 3.0.0
- L517 remediation: Template_Abandonment closure
- This template was in beta status; now aligned with stable release

---

## [3.0.0-beta.1] - 2025-12-27 - "Initial Beta"

### Added
- Initial template creation
- 5D Composition Architecture
- Basic analyst capabilities
