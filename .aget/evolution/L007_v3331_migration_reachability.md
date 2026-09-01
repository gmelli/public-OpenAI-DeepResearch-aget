# L007: v3.33.1 Migration Evidence Must Be Reachable

**Date**: 2026-08-31
**Type**: Lesson Learned
**Category**: Fleet Upgrade, Knowledge Reachability
**Status**: complete

---

## Summary

The public-OpenAI-DeepResearch Aget's v3.33.1 migration passed payload, closure-oracle,
focused-suite, full-suite, health, and persistence checks, yet migration close remained blocked
because `scripts/study_topic.py --topic "v3.33.1"` found zero searchable artifacts.

---

## Context

During the supervisor's four-pilot Gate 3R run, the receiver created migration commit
`08ae4a70d440b7e31af95cd3e60e61e05ae0b42f`. Its local Migration Close rule treats
verification, persistence, and reachability as independent V-tests. The first two passed; the
third returned zero. Because no lesson path was authorized in the exact migration batch, the
receiver created forward revert `faf8d74e0ce69217970ae1b7f61164087014ee63` and held.

---

## Key Finding

A version-carrying migration can be installed correctly and still be operationally unfindable.
Migration evidence must name the adopted version on a surface searched by `study_topic.py`; Git
history and `.aget/version.json` provide provenance but are not substitutes for retrieval.

---

## Implications

At migration close, run the receiver's reachability V-test after installation. If it returns zero,
record a Framework lesson through `/aget-record-lesson`, update the evolution index, rerun the
query, and retain the migration only when at least one artifact is returned. This repairs local
closure evidence; it does not waive other migration tests or authorize publication.

---

## Traceability

| Link | Reference |
|------|-----------|
| Project | `supervisor:PROJECT_PLAN_fleet_v3.33.1_migration_v1.0` Gate 3R |
| Trigger | Zero artifacts for `v3.33.1` after otherwise passing migration validation |
| Migration commit | `08ae4a70d440b7e31af95cd3e60e61e05ae0b42f` |
| Forward revert | `faf8d74e0ce69217970ae1b7f61164087014ee63` |

---

*L007: v3.33.1 Migration Evidence Must Be Reachable*
*Category: Fleet Upgrade, Knowledge Reachability*
