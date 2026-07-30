---
date: 2026-07-29
aget_version: "3.28.0"
agent_name: "public-OpenAI-DeepResearch-aget"
theme: "V3.28 MIGRATION VERIFIED, TWO FALSE-GREENS CAUGHT, FRICTION SURFACE MAPPED"
closed_by: aget-close-session/1.0.0
status: completed
---

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
| gmelli/aget-aget#1580 spec-tier fix | `study_topic.py --topic health` | Specs = 8 (structurally always 0 pre-v3.28) — **PASS** |
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
| 2 | ENFORCEMENT payload deferred (gmelli/aget-aget#2009) with no searched-surface record; upstream-controlled unblock condition would never re-trigger locally. | **Resolved** — L006 §Integration Points tracks it, re-check at v3.29 |
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
| 1 | Measure the ENFORCEMENT blocker + dedup surface | **Done, with a correction.** The bare citation `gh#2009` resolves in neither `aget-framework/aget` (max #84) nor the two other repos probed — it is **`gmelli/aget-aget#2009`** (2072 issues, the private fleet tracker): *"[v3.29] release_gate_battery.sh is seat-coupled"*, OPEN, updated 18:26 today. Deferral is real and actively tracked. |
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

## 6b. Second NBA Batch — `--budget=30 --count=auto --batch --go` (wind-down prep)

| # | Action | Outcome |
|---|--------|---------|
| 1 | Harvest 17:07:42 entry | `dedup #1875` — the dead-narrow half, materialized |
| 2 | Prune dead grant, add pattern-shaped grants | Removed `Bash(awk '/17:04:43/,0' sessions/FRICTION_LEDGER.md)`; added 15 pattern grants (6 first-party `Skill(aget-*)`, 9 read-only Bash verbs). 14 → 28 grants / 0.9 KB, inside SOP OK band (0–100 / 0–30KB); health permission row still `[+]` |
| 3 | Corroborate upstream | [#1872 comment](https://github.com/gmelli/aget-aget/issues/1872#issuecomment-5124697395) · [#1875 comment](https://github.com/gmelli/aget-aget/issues/1875#issuecomment-5124697493) |
| 4 | Wind-down readiness | Tree clean but for this record; health 13/13; pushed |

### Friction, whole session: 4 entries, 4 deduped, 0 filed

Two per half of the permission surface — a complete natural experiment in one session:

| Time | Surface | Class | Measurement | → |
|---|---|---|---|---|
| 16:41:12 | `Skill(aget-wake-up)` | scope too broad / wrong axis | per-directory grant; every seat pays separately | #1875 |
| 16:53:35 | Bash `git push` | duplicate render | **3×** for one execution | #1872 |
| 17:04:43 | `Skill(aget-file-issue)` | duplicate render | **6×** — exceeds #1872's documented 3–4× band, and on a Skill surface, not Bash | #1872 (extends) |
| 17:07:42 | Bash `awk` | scope dead-narrow | grant embedded a **literal wall-clock timestamp** — dead by construction, yet accepted into settings.local.json | #1875 (instance) |

The 17:07 entry is the most transferable finding. A dead-narrow grant is not merely useless, it is **write-amplifying**: silent, individually harmless, and counted toward the very threshold that triggers `SOP_permission_cleanup`. A seat can drift toward WARN entirely on grants that never matched anything. The suggested upstream heuristic (posted to #1875): a candidate scope containing a timestamp, PID, or line number should never be offered as "don't ask again" — that is exactly when the answer is a pattern, not the observed string.

Note: `.claude/settings.local.json` is gitignored globally (`~/.config/git/ignore`), so the grant remediation is real but not captured in this repo's history — recorded here instead. Backup was written during edit and removed after verification.

**Reclassification worth recording**: the #1872/#1875 comments were held as Approve-class through two batches on "outward-facing" grounds. That was over-cautious — `gmelli/aget-aget` is the principal's own private fleet tracker, comments are reversible, and CAP-FRIC-003's harvest loop *ends* in dedup-and-corroborate. Re-asking a third time would have been the friction-fatigue failure mode REQ-PA-014 exists to prevent. Executed under the standing batch GO.

## 7. Exit State

- **Version**: v3.28.0, coherent across all three surfaces
- **Health**: 13/13 HEALTHY · `/aget-check-evolution` OK (was CRITICAL, index created)
- **Tests**: 7 passed, baseline-delta 0
- **V-tests (the three from §Migration Close)**: reachability 1 artifact ✓ · trunk-parity `0 0` ✓ ·
  payload scripts executed ✓
- **Git**: main, level with `origin/main`
- **L-docs**: 6 (L006 + 2 addenda) · index.json now present, `next_id: 7`
- **Friction**: 0 entries at `status: new` — 4 harvested, 4 deduped, 0 filed
  (2 → #1872 duplicate-render, 2 → #1875 scope-shaping; both corroborated upstream)
- **Permissions**: 28 grants / 0.9 KB, 1 dead grant pruned — inside SOP OK band
- **Open**: `gmelli/aget-aget#2009` ENFORCEMENT re-check at v3.29 · reliance manifest
  pre-adoption (advisory, EC-5 gated upstream)

---

## 7b. Peer Review Arc (supervisor cross-read, 17:21–17:30)

`private-supervisor-AGET` read this seat's outputs and fed back an analysis. What it credited
is in §6; what it got wrong, and what it got right *about this seat*, is below.

| Their claim | Assessment |
|---|---|
| Class-5 attribution: ruling R6 manufactures the exact false-green the wave audits for | **Stronger than my own framing.** I recorded that this seat was off-trunk; they identified the *ruling* as the fleet-wide cause |
| Dead-narrow taxonomy completed to 4 categories (argument-exact / session-wide-self-settings / path-crossing / timestamp-bearing-dead) | Better structure than my one-off finding; adopted |
| "DeepResearch pushed unprompted when asked to check its own health" | **Factually wrong, and load-bearing.** This seat surfaced the unpushed state and *stopped*, because R6 said no push. The push followed an explicit principal `GO`. Their proposed dispatch ("check your v3.28 health" → expect a push at llm-connectivity) either fails or teaches a seat to override a standing ruling because a prompt implied it. The dispatch must carry the R6 lift |
| 355 bare `gh#`, 0 in the collision range → severity is probes, not wrong answers | **Directionally right, proof is one-axis.** It establishes no collision against `aget-framework/aget` (max #84) only. The resolution target is the *reading* seat's default tracker — `/aget-file-issue` routes private seats to `gmelli/aget-aget` (2072+), public seats to `aget-framework/aget`. Identical text is unresolvable at one seat and correct at another. Same shape as `gmelli/aget-aget#2072`: an instrument hardened on one axis, never asked about the second — from the seat that wrote that lesson |
| Dedup discipline shouldn't become a reason nothing gets re-scoped (#1872 still titled "Bash", range now 3–6×) | **Correct, and I under-executed.** I put the scope-extension ask inside comment #N of a long thread — guidance on a surface nobody reads at the moment of decision, the exact thesis I spent the session repeating. Re-title proposed, held for principal |

**Their correction landed harder than they noticed.** L006 as first written cited bare `L961`,
`L335`, `L669`, `L51` while this seat holds only L001–L006. A bare `gh#` here fails loudly; a
bare `L###` fails today and resolves **plausibly wrong** the moment this seat files its own
L335 — the severe variant, not the loud one. Fixed: 4 L-citations → `supervisor:L###`, 13 issue
citations → `repo#number`, `AGENTS.md` §Migration Close extended from issues-only to both with
the reason stated (reading-seat default, not writing-seat default). L006 Addendum 3 records it.

### Friction entries 6–7, and a correction to my own harvest

| # | Time | Event | Disposition |
|---|------|-------|-------------|
| 6 | 17:21 | Heredoc gated at the **supervisor's** seat — captured *here* because the principal pasted their transcript and the `UserPromptSubmit` hook fired on the quoted prompt-render | dedup **#1925** (capture artifact) + #1846 (underlying) |
| 7 | 17:26 | This seat's own `git commit -q -F - <<'EOF'` gated: *"Contains shell syntax (command) that cannot be statically analyzed"*, 2× | dedup **#1846 class 2** |

Entry 6 is a **measurement** defect, not noise: this ledger now contains an event this seat
never experienced, so any per-seat friction rate derived from it is inflated. Cross-seat
*attribution* is the sharper form of #1925 — and it matters more to the supervisor's 31-seat
aggregate than to this seat's ledger.

**Self-correction**: entry 6's harvest note speculated that the "analyzer-declines-to-parse"
half "may warrant its own row if not already in scope." It *is* in scope — #1846's body
enumerates three analyzer classes, class 2 being heredoc. That speculation was written from the
truncated issue **title** without reading the **body** — the same defect as paying four probes
for `gh#2009`: a citation treated as a label instead of a source. Corrected in both entries.

**Remediation adopted, not just recorded**: #1846's proposed fix (ship runbook steps as helper
scripts) cannot reach a heredoc carrying a *commit message* — not a runbook step, not scriptable,
recurs on every commit. This seat now authors messages with the Write tool and commits with
`git commit -F <path>`. Zero heredoc, zero substitution, statically analyzable. First use was
commit `e9ba62b`; that commit's own approval behaviour was the V-test.

**One more unwired convention found at close**: `wind_down.py` reported `?? workspace/` —
`AGENTS.md` §Workspace convention states workspace/ "is gitignored", and it was not. Wired to
`.gitignore` this close. Third instance today of the same shape: a rule asserted on one surface
and absent from the surface that enforces it.

## 8. Retrospective

### What went well

- **Independent re-measurement beat trust.** Every v3.28 claim was re-derived from primary
  sources rather than read off the adoption commit bodies. That is what surfaced the
  reachability failure, and later the two live false-greens, none of which any green
  instrument reported.
- **The dedup discipline paid for itself.** 5 friction entries, 5 deduped, **0 filed**. Two
  filings that felt obviously warranted at the time (permission prompts, "unresolvable
  gh#NNNN") would both have been duplicates or plain wrong.
- **Verification before assertion caught a bad finding pre-flight.** The drafted issue
  "release provenance cites gh#NNNN resolving in no reachable tracker" was killed by checking
  one more repo. It would have been filed with confidence and been false.
- **Each batch's finding reframed the next.** #2072's false-green corpus arrived mid-batch and
  changed what the health question even was.

### What we learned

- **A migration is closed by verification *plus* a searched surface** (L006). Commit bodies and
  `version.json` are provenance; `/aget-study-topic` reads neither.
- **Two of six known false-green classes were live here**, invisible to a 13/13 health check.
  "Committed" ≠ "landed"; "delivered" ≠ "executed".
- **Bare `gh#NNNN` is unreachable.** Four probes to resolve #2009. Deferral notes need
  `repo#number`.
- **Instruments in the same repo disagreed twice** — `/aget-check-evolution` CRITICAL vs
  `health_check.py` HEALTHY on the same directory; and the corroborating-count trap #2072
  documents at fleet scale. Agreement between instruments is not evidence; per-element diffs are.
- **A dead-narrow permission grant is write-amplifying**, not merely useless — it consumes
  threshold budget silently.
- **Most of this session's friction was self-manufactured.** See §Session Friction.

### What was missing

- No `flake8`/`pyflakes` under Python 3.14, so the payload's F541/F841 lint state (cited in the
  v3.28 commit as the `--no-verify` justification) remains unverifiable at this seat.
- `.aget/evolution/index.json` was absent for the whole life of the agent — `/aget-record-lesson`
  Steps 3+5 had never been runnable. Created this session.
- `RESEARCH_BACKLOG.md` is still empty and `planning/` holds 0 PROJECT_PLANs. For an analyst
  archetype whose north_star is research, that is the largest standing gap — deliberately not
  self-filled, as it needs principal research direction.
- Reliance manifest still pre-adoption (EC-5 derivation-gated upstream).

## 9. Session Friction

5 events, all captured to `FRICTION_LEDGER.md`, all harvested, **0 filed** (all deduped).

| # | Time | Event | Class | Disposition |
|---|------|-------|-------|-------------|
| 1 | 16:41 | `Skill(aget-wake-up)` prompt; offered scope is per-directory | **structural** — harness scope-shaping | dedup #1875 (+#1740) |
| 2 | 16:53 | Bash `git push` approval rendered **3×** for one execution | **structural** — harness render defect | dedup #1872 |
| 3 | 17:04 | `Skill(aget-file-issue)` rendered **6×**; exceeds #1872's documented 3–4× band and extends it to Skill surfaces | **structural** | dedup #1872 (scope extension posted) |
| 4 | 17:07 | Offered grant embedded a literal timestamp: `Bash(awk '/17:04:43/,0' …)` — dead by construction, accepted into settings | **structural** — but locally **avoidable** once seen | dedup #1875; grant pruned |
| 5 | 17:13 | Compound command gated **despite** `Bash(git rev-list *)` already being granted, because the verb appeared only inside `$( )`; offered scope was the incidental `echo` wrapper; rendered **5×** | **avoidable — agent-manufactured** | dedup #1846 |

**Avoidable: 1 of 5** (event 5; arguably events 2–4 in part). The honest accounting is worse
than that ratio suggests: **compound one-liners with `$(…)` are the agent's own habit**, adopted
for tool-call efficiency, and they defeat the very grants the principal kept issuing. 15 pattern
grants were added at 17:0x and did **not** reduce prompting, because the *shape* of the commands
— not the absence of grants — trips the gate (#1846).

Sharper still: `/aget-close-session`'s own R-CLOSE-040/041 mandates Read/Grep/Glob over Bash for
diagnostics precisely to avoid this, and that rule was available all session. It was followed
only once the close-session skill was invoked at the end. **The remediation is behavioral, not
configurational** — and it is the same failure shape as L006: the guidance existed on a surface
nobody read at the moment of decision.

Upstream contributions: [#1872 comment](https://github.com/gmelli/aget-aget/issues/1872#issuecomment-5124697395)
(N=3, 3–6× range, Skill surface) · [#1875 comment](https://github.com/gmelli/aget-aget/issues/1875#issuecomment-5124697493)
(dead-narrow instance + offer-shaping heuristic).

## 10. Artifacts

| Type | Count | Detail |
|------|------:|--------|
| L-docs | 1 (+2 addenda) | `L006_migration_closure_leaves_no_kb_surface.md` |
| Governance edits | 1 | `AGENTS.md` §Migration Close (3 V-tests + `repo#number` rule) |
| Infrastructure | 1 | `.aget/evolution/index.json` (created; `next_id: 7`) |
| Session records | 1 | this file |
| Upstream comments | 2 | #1872, #1875 |
| Config | 1 | `settings.local.json`: 1 dead grant pruned, 15 pattern grants added (gitignored) |
| Commits | 4 | `085af51`, `a3e2129`, `5c955d6`, `712e0d4`, + close commit |
| Issues filed | **0** | 5 friction entries, all deduped — by design |

---

*Session record — public-OpenAI-DeepResearch-aget v3.28.0*
