# v3.35.0 Receiver Receipt — public-OpenAI-DeepResearch-aget

| Field | Value |
|---|---|
| Attempt | `v335-b1-OpenAI-DeepResearch-aget-20260927` |
| Member | `public-OpenAI-DeepResearch-aget` |
| Route | a1 + b1-with-sources, batch 1 |
| Date | 2026-09-27 |
| Operator | headless session launched by `private-supervisor-AGET` on the principal's authorization |
| Pre-migration HEAD (rollback reference) | `cd4ef837a1da04c0c5e5b9eb3afbe993d95d5412` |
| Version | 3.34.0 → 3.35.0 |

## Release pins

| Surface | Tag | Peeled commit |
|---|---|---|
| core `aget-framework/aget` | v3.35.0 | `1ffc358a9c97143532af6ad06740e60c16afa6f3` |
| `template-analyst-aget` | v3.35.0 | `889e39f46be51d93cc84b36b0f9d5d78086d6c33` |

This session did not verify the tags itself. Payload bytes were read from the supervisor's staging directory (`private-supervisor-AGET/workspace/.tmp/v335_batch1_stage/`), which the supervisor says holds the exact release bytes at these pins.

## Step-3 payload

sha256 column: **not computed.** The `shasum -a 256` call was refused by the session allowlist. Under the dispatch rules a refused call is final, so no other digest tool was tried. Instead, each installed file was compared byte-for-byte against its staged source with `git diff --no-index --stat`. Empty output means identical.

| Path | Action | Source | sha256 after | Byte comparison with source |
|---|---|---|---|---|
| `scripts/propose_actions_classify.py` | WRITE (new at this seat) | template-analyst-aget | not computed (refused) | identical |
| `scripts/propose_actions_handoff_scan.py` | WRITE (new) | template-analyst-aget | not computed (refused) | identical |
| `scripts/study_topic.py` | MERGE (no change to file) | template-analyst-aget | not computed (refused); file unchanged from `cd4ef83` | differs only by the kept receiver lines (see Preservation) |
| `specs/AGET_PROJECT_PLAN_SPEC.md` | WRITE (2 changelog lines differed; applied as edits) | template-analyst-aget | not computed (refused) | identical |
| `tests/test_close_authorization_guard.py` | WRITE (new) | core aget | not computed (refused) | identical |
| `tests/test_propose_actions_classify_hardening.py` | WRITE (new) | template-analyst-aget | not computed (refused) | **differs by 3 bytes**: line 46 is a blank docstring line that should hold 3 spaces; the Write/Edit tools strip trailing whitespace, and shell file writes are forbidden in this session. Whitespace-only, inside a docstring, no effect on any test |
| `tests/test_propose_actions_handoff_scan.py` | WRITE (new) | template-analyst-aget | not computed (refused) | identical |
| `tests/test_propose_actions_outcome_gating.py` | WRITE (new) | template-analyst-aget | not computed (refused) | identical |
| `tests/test_propose_actions_step_2_7.py` | WRITE (new) | template-analyst-aget | not computed (refused) | identical |

Step-4 carriers:
- `.aget/version.json`: `aget_version` changed 3.34.0 → 3.35.0, and one `migration_history` entry was appended (version 3.35.0, date 2026-09-27, route "batch 1, attempt v335-b1-OpenAI-DeepResearch-aget-20260927").
- `manifest.yaml`: line 3 changed from `version: 3.34.0` to `version: 3.35.0`. Nothing else in the file was touched.

## Protected files (written by the principal, not edited here)

These were already modified in the working tree when the session began. They are staged in this commit unedited.
- `.claude/skills/aget-check-evolution/SKILL.md`
- `.claude/skills/aget-propose-actions/SKILL.md`
- `.claude/skills/aget-record-lesson/SKILL.md`
- `.claude/skills/aget-record-observation/SKILL.md`
- `AGENTS.md` (reads `@aget-version: 3.35.0`)

## Tests (`python3 -m pytest -q`)

| | Passed | Failed | Errors | Skipped | Subtests passed |
|---|---|---|---|---|---|
| Before (step 2) | 569 | 0 | 0 | 2 | 2 |
| After (step 5) | 628 | 2 | 4 | 2 | 2 |

- **Failing test ids before:** none.
- **Failing or erroring test ids after.** All six are in test files installed by this migration. None of the 569 baseline tests regressed.
  - FAILED `tests/test_close_authorization_guard.py::test_principal_go_close_is_attributed_with_pointer`
  - FAILED `tests/test_close_authorization_guard.py::test_principal_go_without_pointer_fails_check_a`
  - ERROR `tests/test_propose_actions_step_2_7.py::test_fixture_loads_three_actions`
  - ERROR `tests/test_propose_actions_step_2_7.py::test_per_action_classification_matches_expected`
  - ERROR `tests/test_propose_actions_step_2_7.py::test_positive_pairing_satisfied`
  - ERROR `tests/test_propose_actions_step_2_7.py::test_negative_unmet_surfaces_friction`

**Causes.** Both are delivery defects, not receiver drift.
1. **Missing companion fixture.** `test_propose_actions_step_2_7.py` reads `tests/fixtures/l980_session_2026_05_21_action_batch.json`. That file is absent at this seat, is not in the step-3 list, and is not in the staging directory. The fixture-backed tests error with `FileNotFoundError`.
2. **Test and script version skew.** `tests/test_close_authorization_guard.py` comes from core. Its two 2026-09-19 regression tests expect a principal-GO branch in `scripts/close_authorization_guard.py`. This seat's guard is byte-identical to the staged `template-analyst-aget` copy (`git diff --no-index`: empty), and that copy lacks the branch. The observed result was `['agent-autonomous close, no irreversible consequence — allowed']` and PASS where FAIL was expected. The step-3 note "paths not listed are already current" therefore does not hold for the guard against the core test.

## Behaviour evidence (step 5)

Targeted run: `python3 -m pytest -q -rA` over the five installed test files gave **59 passed, 2 failed, 4 errors**.

**Credited capability (M-3.35-1: deferral scan plus outcome gating).** All 17 tests in `test_propose_actions_handoff_scan.py` and all 11 in `test_propose_actions_outcome_gating.py` pass.
- **Capability shown:** `tests/test_propose_actions_handoff_scan.py::test_untracked_handoff_is_a_candidate_and_matches` and `::test_recent_committed_handoff_matches`. The scan finds untracked handoffs and handoffs committed inside the window, and reports MATCHED. The outcome-gating capability is shown by `tests/test_propose_actions_outcome_gating.py::test_gated_outcome_step_listed_passes`.
- **Rejection path shown:** `tests/test_propose_actions_handoff_scan.py::test_not_a_git_repository_is_unavailable_not_clean` returns UNAVAILABLE, not a clean scan. `::test_git_that_cannot_run_is_unavailable_exit_2` exits 2, not 1. `tests/test_propose_actions_outcome_gating.py::test_gated_outcome_step_must_be_listed_as_a_decision` returns UNMET, and `::test_malformed_batch_is_refused_not_passed` returns UNAVAILABLE.
- **Classifier hardening:** all 16 tests in `test_propose_actions_classify_hardening.py` pass. These include the rejection-path test `test_two_writes_on_one_artifact_do_not_pass_the_gate` (UNMET) and `test_malformed_batch_does_not_report_pass` (exit 3).

**Close-authorization guard.** 8 of 10 pass. The rejection path works for the pre-existing checks: `tests/test_close_authorization_guard.py::test_v323_voided_close_fails` and `::test_check_a_fires_when_pointer_removed` both return FAIL. The principal-GO branch is **not** present (cause 2 above).

**Not run.** The release smoke probes are not recorded: the `--self-test` runs, `close_gate_check.py --help`, the fixture-plan gate probe, and `wake_up.py`. The dispatch forbids running scripts, and the fixture-plan probe needs a temp-file redirect, which is also forbidden. The M-3.35-3 close-gate fixture probe is unverified at this seat.

## Preservation

- `scripts/study_topic.py` (MERGE): the release copy differs from ours only inside `_resolve_canonical_spec_roots`. Every differing line on our side is receiver-owned: 32 lines by `git diff` count, against the supervisor's figure of 25. They cover:
  - the early return once an explicit declaration resolves;
  - `study_topic.canonical_root` config support, with a legacy top-level key and relative-path resolution against the agent root;
  - the bounded `aget-framework/aget` portfolio layout, which replaces enumeration of the grandparent directory.
  The release has no changes outside that region, so there was nothing to take. All receiver lines are kept and the file is unchanged from `cd4ef83`.
- `specs/AGET_PROJECT_PLAN_SPEC.md`: the only difference from the release was two changelog lines (`gmelli/aget-aget#1180` → `internal tracker #1180`, the release's hygiene commit 4b93592). The release text was taken. There were no receiver extensions to keep.
- No other path was touched.

## Limitations

- sha256 digests are not recorded (shasum refused). Identity was established by byte comparison instead.
- `tests/test_propose_actions_classify_hardening.py` is 3 whitespace bytes off the release (tool limitation, see table).
- Two delivery defects produce 6 new non-passing tests (missing fixture; test and guard version skew).
- Smoke probes were not run (scripts forbidden in this session). Tag objects were not verified by this seat.
- `@aget-canonical-specs` in AGENTS.md still reads `v3.33.1`. AGENTS.md is protected and was not edited here.
- Trunk parity: this is a local commit only and has not been pushed. That is the authorized divergence, lifted by the supervisor's separate push step.
- The L006 reachability V-test (`scripts/study_topic.py --topic "v3.35.0"`) was not run, because scripts are forbidden.

## Rollback

`git revert <migration commit>`. The pre-migration reference is `cd4ef837a1da04c0c5e5b9eb3afbe993d95d5412`. Do not reset shared history.

## Terminal

**REJECTED**

Reason: the credited capability (M-3.35-1) and its rejection paths pass. However, the release's own acceptance bar ("no new receiver test failures against the baseline") fails. The delivered test set adds 2 failures and 4 errors, caused by two blocking delivery defects: a missing `tests/fixtures/l980_session_2026_05_21_action_batch.json`, and a core `test_close_authorization_guard.py` shipped against a template guard without the principal-GO branch. The install is committed locally for the supervisor's check. Re-evaluate once the release supplies the fixture and a guard that matches the test.

---

## Attempt v335-b1-OpenAI-DeepResearch-aget-20260927-repair (repair)

| Field | Value |
|---|---|
| Attempt | `v335-b1-OpenAI-DeepResearch-aget-20260927-repair` |
| Route | a1 + b1 route-b-restricted-hooks (detective), batch 1 |
| Date | 2026-09-28 |
| Operator | headless session launched by `private-supervisor-AGET` on the principal's authorization |
| Rollback reference (previous attempt) | `a9e801d8053b91d9f332be3a7ec01f2346c7cb4e` |
| Release pins | core `aget-framework/aget` v3.35.0 = `1ffc358a9c97143532af6ad06740e60c16afa6f3`; `template-analyst-aget` v3.35.0 = `889e39f46be51d93cc84b36b0f9d5d78086d6c33` (not re-verified by this seat) |

### Repaired files (placed by the principal's apply script; not edited in this session)

| Path | Source | Git blob after (`git hash-object`) | Expected release sha256 (prefix) |
|---|---|---|---|
| `scripts/close_authorization_guard.py` | core `aget` | `546547ea0912276af502ae93be96a597f5971046` | `8bc4f5f9d1b5` |
| `tests/test_propose_actions_classify_hardening.py` | template-analyst-aget | `032564e67ceeb5e6b73aa6ba65a6082d361d28e2` | `132e931f25ea` |
| `tests/fixtures/l980_session_2026_05_21_action_batch.json` | template-analyst-aget | `753334ee2d3497e8d4962aa9fb7b5d899b874cdc` | `f325660825f5` |

- `git diff` of `tests/test_propose_actions_classify_hardening.py` against `a9e801d` shows only line 46: the blank docstring line now holds the 3 spaces. This fixes the 3-byte defect recorded above.
- `scripts/close_authorization_guard.py` against `a9e801d`: 38 insertions and 3 deletions (the core principal-GO branch).
- The fixture is new at this seat.
- No other path was touched. Protected files, version carriers and `scripts/study_topic.py` were not edited.

### Tests (`python3 -m pytest -q`)

| | Passed | Failed | Errors | Skipped | Subtests passed |
|---|---|---|---|---|---|
| Baseline (previous attempt, step 2, pre-migration) | 569 | 0 | 0 | 2 | 2 |
| Now (after repair) | 634 | 0 | 0 | 2 | 2 |

- **Failing test ids in the baseline:** none.
- **New failures against the baseline:** none. The previous attempt's 2 failures (`test_close_authorization_guard.py::test_principal_go_*`) and 4 errors (`test_propose_actions_step_2_7.py::*`) now pass. 634 = 628 + 2 + 4.

### Behaviour evidence

- `python3 scripts/propose_actions_handoff_scan.py --self-test` prints `PASS`. This shows the **credited capability** (M-3.35-1 deferral and handoff scan).
- `python3 scripts/propose_actions_classify.py --self-test` prints `PASS`. This covers the classifier and pairing gate that the capability relies on.
- `python3 scripts/close_gate_check.py --help` shows the **rejection path** interface. `--mode closure` (the default, CAP-PP-013-05/06) "blocks any live non-terminal gate or contradictory state". `--phase` and `--disposition` are required, and "no phase is inferred". This is usage text only: it documents the refusal path but does not exercise it. The rejection paths themselves are exercised by the passing suite, including:
  - `test_close_authorization_guard.py::test_principal_go_without_pointer_fails_check_a` (FAIL);
  - `::test_v323_voided_close_fails`;
  - `test_propose_actions_step_2_7.py::test_negative_unmet_surfaces_friction`;
  - `test_propose_actions_handoff_scan.py::test_not_a_git_repository_is_unavailable_not_clean`.

### Limitations

- **sha256 not verified here.** This seat recorded git blob ids only; it did not compute sha256 (the prompt's command set has no digest tool). The expected release sha256 prefixes above are the supervisor's figures and are not matched by this seat.
- **Staging cross-check refused.** A `git hash-object` cross-check against the supervisor's staging copies was refused by the session allowlist. Per the dispatch rules it was not retried.
- **Probes not run.** The fixture-plan close-gate probe (M-3.35-3), `wake_up.py`, and the L006 `study_topic.py` reachability check were not run. They are outside the allowed command set.
- **Stale spec pin.** `@aget-canonical-specs` in AGENTS.md still reads `v3.33.1`. AGENTS.md is protected and was not edited.
- **Not pushed.** This is a local commit only; the supervisor handles the push.

### Rollback

`git revert <this repair commit>` restores the state of `a9e801d8053b91d9f332be3a7ec01f2346c7cb4e`. The full pre-migration reference remains `cd4ef837a1da04c0c5e5b9eb3afbe993d95d5412`. Do not reset shared history.

### Terminal

**BEHAVIOUR_VERIFIED**

Reason: there are no new failures against the baseline (634 passed, 0 failed, 0 errors), and both self-tests pass. The three delivery defects from the previous attempt are resolved. The terminal is not ACCEPTED because this seat did not independently confirm the release sha256 digests.
