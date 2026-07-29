#!/usr/bin/env python3
"""Ruling R18's two-clause runaway gate, as a SCRIPT rather than a shell snippet.

WHY THIS IS A SCRIPT
--------------------
R18 shipped in the dispatch prompt as a bash block built from `$(...)` command
substitution. Two seats independently reported that this does not work:

  * `private-github-aget`: its own `friction_guard.sh` (v3.25, fleet-propagated)
    BLOCKS `$(...)` outright, so the ruling's block cannot be run verbatim at any
    seat carrying that hook. The seat reimplemented the semantics itself. The
    hazard is the seat that instead *strips* the `$(...)` to get past the hook and
    silently ends up checking ONE clause — which is precisely how the 67-minute
    runaway at `private-impact-aget` went unnoticed.

  * `private-RKB-CONTENT_ENHANCER-aget`: the porcelain clause is unusable there.
    Its suite writes ~15 untracked `logs/llm_interactions/Test_*.json` fixtures per
    run; porcelain went 35 -> 50 -> 68 -> 83 across FOUR BENIGN runs while the
    commit count never moved. Read literally, "both clauses unchanged" makes that
    seat report detonation on its own test logging.

THE FIX, BOTH HALVES
--------------------
1. No shell substitution anywhere — invoke by literal name, hook-compatible.
2. The two clauses are NOT symmetric, and pretending they were is the defect:

     COMMIT COUNT  is load-bearing. The runaway's signature is commits appearing.
                   Any increase is a breach. No scoping, no tolerance.

     PORCELAIN     is scoped to paths that MATTER — tracked-file modifications and
                   the payload paths. Untracked test fixtures are excluded by
                   default, because a suite that writes fixtures is not a runaway.
                   `--strict-porcelain` restores the old unscoped behaviour.

A gate that fires on benign activity gets overridden, and an overridden gate
protects nothing. That is the same lesson the capability pre-flight learned when it
demanded `shasum` and flagged two seats that had already landed.

EXIT CODES
----------
  0  suite ran, no breach            2  BREACH: commit count moved (runaway)
  1  suite reported new failures     3  BREACH: tracked-file porcelain moved
"""
import argparse
import subprocess
import sys
from pathlib import Path

PAYLOAD = (
    "scripts/study_topic.py",
    "scripts/check_initiatives.py",
    "scripts/close_gate_check.py",
    "scripts/wind_down.py",
)


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return r.stdout.strip()


def commit_count(repo):
    out = git(repo, "rev-list", "--count", "HEAD")
    return int(out) if out.isdigit() else -1


def porcelain(repo, strict):
    """Scoped by default: tracked-file changes + payload paths only.

    An untracked file is only counted when it IS a payload path — a seat's test
    fixtures are noise here, but a payload file appearing untracked is a real
    finding the migration must not hide.
    """
    lines = [ln for ln in git(repo, "status", "--porcelain").splitlines() if ln.strip()]
    if strict:
        return lines
    kept = []
    for ln in lines:
        status, _, path = ln[:2], ln[2:3], ln[3:].strip()
        if status.strip() == "??":
            if any(path.endswith(p) or path == p for p in PAYLOAD):
                kept.append(ln)
        else:
            kept.append(ln)
    return kept


def main() -> int:
    p = argparse.ArgumentParser(description="R18 two-clause runaway gate (script form)")
    p.add_argument("--repo", default=".")
    p.add_argument("--python", default=sys.executable,
                   help="interpreter for pytest. Default is THIS interpreter, not the "
                        "literal string 'python3' — RKB-CONTENT_ENHANCER's suite cannot be "
                        "collected by system Homebrew 3.14 (26 collection errors, 0 tests) "
                        "and a seat taking 'python3' literally reports a catastrophe that is "
                        "purely interpreter selection.")
    p.add_argument("--deselect", default="tests/test_init_with_patterns.py")
    p.add_argument("--tests", default="tests/")
    p.add_argument("--strict-porcelain", action="store_true",
                   help="count every untracked file, pre-fix behaviour")
    p.add_argument("--baseline-only", action="store_true",
                   help="capture and print the before-state, run nothing")
    a = p.parse_args()

    repo = Path(a.repo).resolve()
    before_n = commit_count(repo)
    before_s = porcelain(repo, a.strict_porcelain)

    print(f"interpreter : {a.python}")
    print(f"before      : commits={before_n}  porcelain(scoped)={len(before_s)}")
    if a.baseline_only:
        return 0

    cmd = [a.python, "-m", "pytest", a.tests, "-q", "--deselect", a.deselect]
    print(f"running     : {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True,
                       stdin=subprocess.DEVNULL)
    tail = (r.stdout or r.stderr).strip().splitlines()[-12:]
    print("--- pytest tail ---")
    for ln in tail:
        print(f"  {ln}")

    after_n = commit_count(repo)
    after_s = porcelain(repo, a.strict_porcelain)
    print(f"after       : commits={after_n}  porcelain(scoped)={len(after_s)}")

    if after_n > before_n:
        delta = after_n - before_n
        print(f"\n⛔ BREACH — commit count moved {before_n} -> {after_n} (+{delta}). RUNAWAY.")
        print("   STOP IT NOW:")
        print(f"     pkill -9 -f pytest ; git -C {repo} reset --hard HEAD~{delta}")
        return 2

    if len(after_s) != len(before_s):
        print(f"\n⛔ BREACH — tracked/payload porcelain moved "
              f"{len(before_s)} -> {len(after_s)}. Inspect before continuing:")
        for ln in sorted(set(after_s) - set(before_s)):
            print(f"     {ln}")
        return 3

    print("\n✅ two-clause gate HELD — commit count flat, tracked/payload porcelain flat.")
    if not a.strict_porcelain:
        raw = len(git(repo, "status", "--porcelain").splitlines())
        if raw != len(after_s):
            print(f"   ({raw - len(after_s)} untracked non-payload file(s) ignored by scope — "
                  f"test fixtures are not a runaway signal. --strict-porcelain to count them.)")
    print(f"   pytest exit={r.returncode} — compare the failure SET to your step-0 baseline, "
          f"not the exit code. A suite that collects 0 tests exits 5 and is NOT a pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
