# Session 2026-07-29 — v3.28 Health Check + Migration Review

**Agent**: public-OpenAI-DeepResearch-aget (DeepThink) v3.28.0
**Portfolio**: main | **Archetype**: analyst
**Entry state**: main, clean, HEAD `155e404`, 2 commits ahead of `origin/main`
**Trigger**: principal — "check your health, focus on your recent v3.28 migration"

---

## 1. Session Flow

1. Read `AGENTS.md` (12,436 B — under the 30k check, well under L146's 40k hard limit)
2. `/aget-wake-up` → v3.28.0, main clean, 38 skills, 5 L-docs, 0 PROJECT_PLANs
3. `/aget-study-topic` on health + v3.28 (dual query — the request spanned two topics)
4. Independent verification of the v3.28.0 migration (see §3 — re-run, not trusted from commit bodies)
5. Principal **GO** → remediation: L006 recorded, this session record, push
6. Friction captured (§5)

---

## 2. Health Result

`scripts/health_check.py` → **HEALTHY, 13/13**.

| Check | Value |
|---|---|
| `.aget/` structure | present |
| version.json | v3.28.0 |
| identity.json | north_star defined |
| governance/ | 3 files |
| evolution/ | 5 L-docs (now 6) |
| 5D structure | 5/5 dimensions |
| sessions/ | 5 session files (now 6) |
| planning/ | 0 PROJECT_PLANs |
| duplicate L-doc IDs | 5 unique, no collisions |
| config size | AGENTS.md 12,436 B (under 30k) |
| D71-STRUCTURAL frontmatter | 4/4 present, none carry `disable-model-invocation` |
| reliance manifest | absent — pre-adoption, advisory only |
| permission accumulation | within L500 thresholds |

---

## 3. v3.28.0 Migration Verification (independent re-run)

Migration was commits `6374cb4` (FLEET-SCRIPT payload) + `155e404` (specs pin). Everything
below was re-measured this session rather than read off the commit bodies.

| Check | Method | Result |
|---|---|---|
| Version triplet coherence | `jq .aget_version` vs `AGENTS.md:3` vs pin `AGENTS.md:4` | all 3.28.0 — **PASS** |
| Payload hash 4/4 | `shasum -a 256` vs `template-worker-aget` **and** `template-analyst-aget` | exact match both — **PASS** |
| pytest baseline | `pytest -q --deselect tests/test_init_with_patterns.py` | 7 passed, 0 failed, delta 0 — **PASS** |
| gh#1580 spec-tier fix | `study_topic.py --topic health` | Specs = 8 (structurally always 0 pre-v3.28) — **PASS** |
| R18 gate script | `scripts/migrations/pytest_two_clause_gate.py --help` | parses, present — **PASS** |
| Reachability of migration reasoning | `study_topic.py --topic v3.28` | **0 artifacts — FAIL** (remediated, §4) |

Payload hashes (first 16): `study_topic.py 2f3bd28ae29e4c0f` · `check_initiatives.py
f862edabc4180df5` · `close_gate_check.py 57c5fb09ca41fb89` · `wind_down.py cdceb2be526de6f4`.
Three of four were already at target — only `study_topic.py` changed.

---

## 4. Findings and Disposition

| # | Finding | Disposition |
|---|---|---|
| 1 | 2 commits unpushed; `origin/main` still at v3.27.0 (`474f5fd`). Deliberate per ruling R6, but v3.28 invisible to supervisor cohort tracking. | **Resolved** — principal GO, pushed this session |
| 2 | ENFORCEMENT payload deferred (gh#2009) with no searched-surface record; upstream-controlled unblock condition would never re-trigger locally. | **Resolved** — L006 §Integration Points tracks it, re-check at v3.29 |
| 3 | No session record for the 2026-07-29 migration (latest was 2026-07-11). | **Resolved** — this file |
| 4 | Commit body cites `--no-verify` against payload F541/F841, but no `.git/hooks/pre-commit` exists and only a `UserPromptSubmit` hook is configured — nothing was actually bypassed. Harmless, but a false signal in the audit trail. | **Noted** in L006 §Corollary. Payload lint state unverifiable locally (no flake8/pyflakes under Python 3.14) |
| 5 | Reliance manifest still absent (standing since v3.24 EC-5 derivation gate). Specs pin is the only reliance surface. | **Standing** — advisory, no action |

**L006 recorded**: `.aget/evolution/L006_migration_closure_leaves_no_kb_surface.md` —
framework-class. Core rule: *a migration is closed by verification **plus** a searched
surface*; commit bodies and `version.json` are provenance, not retrieval. Adds
`/aget-study-topic <version>` as a reachability V-test at migration close.

Post-remediation re-run: `study_topic.py --topic v3.28` → **1 artifact** (L006, 12 matches).
Reachability V-test now passes.

Note: `.aget/evolution/index.json` does not exist in this agent, so `/aget-record-lesson`
Step 5 (index update) was non-applicable. ID assigned max+1; duplicate-ID check clean.

---

## 5. Friction

One entry auto-captured to `sessions/FRICTION_LEDGER.md` (status: `new`, value-class: `owed`)
@ 16:41:12 — the `/aget-wake-up` skill permission prompt fires on every invocation of a
first-party AGET skill, and the "don't ask again" option is per-directory. Awaiting harvest
per CAP-FRIC-003 (cluster → dedup against open issues, L669 → `/aget-file-issue`).

---

## 6. NBA Batch — `/aget-propose-actions --budget=1h --count=auto --batch --go`

Principal-mode ACCEPT (REQ-PA-014, flags principal-typed) · batch GO via `--go` (Step 4.5) ·
focus: *remediations and enhancements* · count=auto → 5 · 56/60 min planned.
Pre-flight: D71 PASS (issue filing routed via `/aget-file-issue`) · HANDOFF-deferral PASS
(no `docs/HANDOFF_*.md`) · audit-pairing PASS (no same-artifact synthesis group).

| # | Action | Outcome |
|---|--------|---------|
| 1 | Measure gh#2009 + dedup surface | **Done, with a correction.** `gh#2009` does not resolve in `aget-framework/aget` (max #84) or the two other repos probed — it resolves in **`gmelli/aget-aget#2009`** (2072 issues, the private fleet tracker): *"[v3.29] release_gate_battery.sh is seat-coupled"*, OPEN, updated 18:26 today. Deferral is real and actively tracked. |
| 2 | Friction harvest → file via `/aget-file-issue` | **Done — deduped, NOT filed** (L669). Entry 16:41:12 → `dedup #1875` (+#1740); entry 16:53:35 → `dedup #1872` (identical prompt rendered 3-4x, N=2 → this session makes N=3). Ledger statuses updated with harvest rationale. Corroboration comment on #1872 held for approval (outward-facing). |
| 3 | Wire L006 into AGENTS.md (L467 Channel-1) | **Done.** New §Migration Close: three V-tests (reachability / trunk-parity / executed-not-just-delivered) + the `repo#number` citation rule. AGENTS.md 12,436 → 14,023 B (under 30k warn). |
| 4 | Record the surfaced observations | **Done, redirected.** Folded into L006 as two addenda rather than a separate observation file — Addendum 1 (`gh#` vs `repo#` unreachability) and Addendum 2 (six false-green class self-check). Keeps the finding on the same searched surface as its lesson. |
| 5 | Verification sweep + commit | **Done.** See §7. |

### The finding that reframed the batch: `gmelli/aget-aget#2072`

The v3.28 fleet XP report (31 seats) names **six false-green classes**, each of which passed
the check the fleet had at the time. Self-check of this seat found **two were live**:

| Class | This seat |
|---|---|
| 3 — delivered but not executed | **WAS FAILING.** `check_initiatives.py` / `close_gate_check.py` were hash-verified but never run here. Executed: check_initiatives → 0 initiatives, no anomalies; close_gate_check → arg-validated, no PROJECT_PLAN target. Now PASS |
| 5 — committed but OFF-TRUNK | **WAS FAILING.** v3.28 sat 2 commits ahead of `origin/main` for ~6h under ruling R6. All local axes green; the fleet could not see the release. Closed by `474f5fd..085af51` |
| 1, 2, 6 | PASS (hash 4/4 · tracked+committed · specs pin at v3.28.0) |
| 4 — `exit=0` without work | PASS, and **demonstrated live**: a `timeout python3 …` probe returned `exit=0` solely because macOS has no `timeout` binary. Zero work, green exit, this session |

Neither live failure was visible to `health_check.py` (13/13 throughout) or to the migration's
own V-test block. #2072's thesis — *a false-green class is an unasked question, not a missing
check* — is L006's thesis arriving from the fleet side.

### Second instrument disagreement (unprompted find)

`/aget-check-evolution` scored `.aget/evolution/` **CRITICAL** (index.json missing) while
`health_check.py` scored the same directory **HEALTHY** (it has no index check). The CRITICAL
was legitimate: `/aget-record-lesson` Steps 3+5 read and update `next_id`, so both were
unrunnable — L006 was filed with ID assigned by max+1 as a workaround hours earlier.

**Remediated**: created `.aget/evolution/index.json` (`next_id: 7`, 6 entries + 4
`legacy_entries` mapped to their superseding L-docs), shape mirrored from the fleet
supervisor's index. Every field derived by reading the source files' own headers — audit-class,
not composed from a prior index (there was none). Verified: `jq empty` valid · `next_id` 7 ·
all 10 `file`/`superseded_by` targets exist on disk · `stats.total_files` 11 = actual 11.

Evolution inventory: 11 files, 6 L-docs, 4 legacy, 88K, index valid → **OK** on every
`/aget-check-evolution` threshold.

## 7. Exit State

- **Version**: v3.28.0, coherent across all three surfaces
- **Health**: 13/13 HEALTHY · `/aget-check-evolution` OK (was CRITICAL, index created)
- **Tests**: 7 passed, baseline-delta 0
- **V-tests (the three from §Migration Close)**: reachability 1 artifact ✓ · trunk-parity `0 0` ✓ ·
  payload scripts executed ✓
- **Git**: main, level with `origin/main`
- **L-docs**: 6 (L006 + 2 addenda) · index.json now present, `next_id: 7`
- **Friction**: 0 entries at `status: new` (2 harvested → dedup #1875, #1872)
- **Open**: `gmelli/aget-aget#2009` ENFORCEMENT re-check at v3.29 · #1872 corroboration
  comment awaiting approval · reliance manifest pre-adoption (advisory, EC-5 gated upstream)

---

*Session record — public-OpenAI-DeepResearch-aget v3.28.0*
