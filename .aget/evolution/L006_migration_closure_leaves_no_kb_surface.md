# L006: Migration Closure Leaves No KB Surface

**Date**: 2026-07-29
**Context**: v3.28.0 FLEET-SCRIPT adoption (commits 6374cb4, 155e404), verified during a same-day health check
**Category**: Fleet Upgrade, Deferral Discipline, Knowledge Retention
**Classification**: Framework (reusable across AGETs)
**Pattern**: complements L961 (HANDOFF-Deferral Discipline), L335 (Memory Architecture)

---

## Problem

**A hash-clean migration can be simultaneously well-executed and unfindable.**

The v3.28.0 adoption was rigorous: 4/4 payload hash-match, version triplet coherent, pytest
baseline-delta 0, and one payload item (the ENFORCEMENT release-gate guard + battery)
*deliberately* not installed because it fail-closes on a framework-release-only companion
(gh#2009). Every one of those judgements was recorded — in `.aget/version.json`
`migration_history` and in two commit message bodies.

Then, hours later, `/aget-study-topic v3.28` returned **0 artifacts across every searched
surface**: 0 L-docs, 0 patterns, 0 PROJECT_PLANs, 0 SOPs, 0 governance, 0 specs, 0 knowledge,
0 inbox. The skill's own recommendation was "this appears to be a **novel topic**."

**Quantified gap**:

| Decision made during migration | Recorded where | Visible to `/aget-study-topic` |
|---|---|---|
| ENFORCEMENT payload deferred (gh#2009) | commit body + version.json | No |
| Behavioral Smoke probes 1–5 N/A (payload absent) | commit body | No |
| `verify_deployment.py` skipped as vacuous (no M-rows) | commit body | No |
| `--no-verify` per gh#2041 hash-BLOCKER precedence | commit body | No |
| Hash-match as sole closure test (R20/R25) | commit body | No |

Five reasoned judgements, zero study-time reachability. The canonical repo holds
`RELEASE_HANDOFF_v3.28.0.md`, `CORRECTIONS_v3.28.0.md`, `DELIVERED_FILES_v3.28.0.yaml`,
`DEPLOYMENT_SPEC_v3.28.0.yaml` — none copied locally, and `docs/release-notes/` +
`handoffs/` are outside the study scope anyway (per the skill's own NOT-searched list).

**Cost**: a deferral with an upstream unblock condition (gh#2009 gets fixed) has nothing
locally that will ever prompt re-adoption. The next agent — or the next context window of
the same agent — studies the topic, is told it is novel, and re-derives or silently drops it.

**Why this is not merely "should have written notes"**: git *is* durable and *is* the audit
trail. The failure is a **surface mismatch** — the retrieval tool the fleet actually uses at
decision time does not read the surface the migration wrote to. Discipline was present;
reachability was not.

---

## Learning

### A migration is not closed by verification alone; it is closed by verification + a searched surface

**Core principle**: for any migration judgement that a *future* decision depends on, write it
to a surface `/aget-study-topic` searches. Commit messages and `version.json` are provenance,
not retrieval.

**Surfaces that are searched** (per `study_topic.py` as of v3.28.0):
`.aget/evolution/**/L*.md` (recursive) · `docs/patterns/**` + `patterns/**` ·
`planning/PROJECT_PLAN*.md` · `sops/SOP_*.md` · `governance/*.md` ·
`knowledge/**` + `ontology/**` · `specs/**` + `.aget/specs/**` · `../aget/specs/**` +
`../aget/sops/**` · `inbox/` ≤14d.

**Surfaces that are NOT searched**: `sessions/`, `workspace/`, `data/`, and `docs/` outside
`patterns/`. Also: git history, commit bodies, and `.aget/version.json`.

### The deferral test

A deferral needs a durable local surface when it has an **unblock condition someone else
controls**. Classify at deferral time:

| Deferral shape | Needs searched surface? |
|---|---|
| Blocked on upstream fix (gh#N) | **Yes** — nothing local will re-trigger it |
| Out of scope for this seat, permanently | No — version.json note suffices |
| Optional / opt-in per-agent policy | Yes if revisitable at next release |
| Superseded by a later payload row | No — the supersession is the record |

The v3.28 ENFORCEMENT deferral is row 1: gh#2009 is a framework-repo problem, its fix will
not announce itself here, and only a searched-surface note closes the loop.

### Corollary: `--no-verify` claims should be checked against installed hooks

The v3.28 commit cites `--no-verify` against payload F541/F841 lint. This repo has **no**
`.git/hooks/pre-commit` and only a `UserPromptSubmit` hook in `.claude/settings.json` —
nothing was actually bypassed. Harmless here, but a migration note that describes a bypass
that could not have occurred is a small false signal in the audit trail. Verify the guard
exists before recording that you routed around it.

---

## Protocol

### At migration close (add to the V-test block)

```bash
# 1. Verify the migration (existing practice)
python3 scripts/health_check.py
python3 -m pytest -q --deselect tests/test_init_with_patterns.py
grep -n "aget-version" AGENTS.md && jq -r .aget_version .aget/version.json

# 2. NEW — reachability test. Study the version you just adopted.
python3 scripts/study_topic.py --topic "v3.28"
#    0 artifacts => the migration is verified but unfindable. Not closed.

# 3. If 0: record the reasoned judgements to a searched surface
#    /aget-record-lesson  (framework-class -> .aget/evolution/L###)
#    and re-run step 2 to confirm the surface now answers.
```

### Deferral note minimum content

```markdown
- **Deferred**: <payload row / capability>
- **Reason**: <why it fail-closes / why out of scope>
- **Unblock condition**: <gh#N fixed | policy change | next release>
- **Who controls it**: <framework seat | supervisor | this agent>
- **Re-check at**: <next fleet upgrade | specific version>
```

---

## Anti-Patterns

❌ **Don't treat the commit message as the record of a revisitable decision**
- Git is provenance. Nobody greps `git log` at study time; they run `/aget-study-topic`.

❌ **Don't put migration reasoning only in `sessions/`**
- `sessions/` is deliberately NOT searched (2026-07-04 scope decision — noise at study time).
  A session record is the narrative; the L-doc is the retrievable finding. Write both.

❌ **Don't conclude "novel topic" from a 0-result study without reading the NOT-searched list**
- The skill prints it for a reason. 0 results can mean "unrecorded" *or* "recorded off-surface."

❌ **Don't record a bypass you did not need**
- Check `.git/hooks/` and `.claude/settings*.json` before claiming `--no-verify` was required.

✅ **Do run the version you just adopted through `/aget-study-topic` as the last V-test**
- Cheapest possible reachability check; catches the whole class.

✅ **Do classify each deferral by who controls the unblock condition**
- Upstream-controlled deferrals are the ones that silently die.

✅ **Do note which payload rows were *already at target***
- 3 of 4 v3.28 scripts needed no change. Recording that prevents a future seat from
  "re-adopting" and manufacturing a divergence.

---

## Impact

**v3.28.0 migration, as verified 2026-07-29 (independent re-run, not trusted from commit)**:

| Check | Result |
|---|---|
| Version triplet coherence | `version.json` == `AGENTS.md:3` == specs pin `AGENTS.md:4` == 3.28.0 — PASS |
| Payload hash 4/4 | exact match vs `template-worker-aget` **and** `template-analyst-aget` (own archetype) — PASS |
| pytest baseline | 7 passed / 0 failed, baseline-delta 0 — PASS |
| `health_check.py` | 13/13 HEALTHY |
| gh#1580 spec-tier fix | live-confirmed: `--topic health` returns Specs = 8 (was structurally always 0) — PASS |
| Reachability of migration reasoning | **0 artifacts** — FAIL, remediated by this L-doc |

**The gh#1580 fix is itself an instance of this lesson's shape**: `study_topic.py` advertised a
`specs` tier in its SURFACES_SEARCHED banner while no finder ever populated the key. Every
study silently reported zero specs — *manufactured absence*, indistinguishable from a genuine
gap. A tool that claims a surface it does not read produces exactly the same failure as a
migration that writes to a surface nothing reads. Same defect, opposite direction.

**Before this L-doc**: `/aget-study-topic v3.28` → 0 artifacts, "novel topic."
**After**: the ENFORCEMENT deferral, its gh#2009 unblock condition, and the hash-match
closure rule are all reachable from the fleet's standard retrieval path.

---

## Integration Points

- **Applies to**: every fleet upgrade / self-upgrade close (SOP_fleet_upgrade Gate-1)
- **Interacts with**: L961 (HANDOFF-Deferral Discipline — this is the retrieval half of it),
  L335 (Memory Architecture — harness vs KB taxonomy), L669 (dedup before filing)
- **Skill surface**: `/aget-record-lesson` at migration close; `/aget-study-topic <version>`
  as the reachability V-test
- **Open deferral tracked by this L-doc**: v3.28 ENFORCEMENT payload (release-gate firing
  guard + battery), blocked on **gh#2009**, controlled by the framework seat, re-check at
  the v3.29 fleet upgrade.

---

## Related Learnings

- L003: Repository Planning Protocol (planning artifacts as durable surface)
- L005: File-Based Coordination Protocol (files as ground truth over conversation — same
  principle, applied to coordination rather than retention)
- L001: Agent Identity Awakening (version coherence as identity)

---

## Validation

**L51 Compliance Check**:
- ✅ Problem with quantified waste (5 judgements, 0 study-time reachability)
- ✅ Learning with protocol-first framing (searched-surface rule + deferral test)
- ✅ Protocol with copy-paste commands (reachability V-test, deferral note template)
- ✅ Anti-patterns in ❌/✅ format (4 don'ts, 3 dos)
- ✅ Impact with before/after (0 artifacts → reachable) and independent verification table
- ✅ Integration points (SOP_fleet_upgrade Gate-1, L961/L335 linkage, open deferral)
- ✅ Related learnings

**Note**: `.aget/evolution/index.json` does not exist in this agent; Step 5 of
`/aget-record-lesson` (index update) was skipped as non-applicable. ID assigned by
max-existing + 1 (L005 → L006); `health_check.py` duplicate-ID check confirms no collision.

---

**Generated**: 2026-07-29
**Session**: v3.28 health check + migration review (post-adoption, same day)
**Significance**: First L-doc to treat *retrievability* as a migration exit criterion rather
than a documentation nicety
