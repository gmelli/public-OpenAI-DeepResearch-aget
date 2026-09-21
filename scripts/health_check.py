#!/usr/bin/env python3
"""
AGET Housekeeping Protocol - Generic Template

Perform sanity checks and housekeeping for any AGET agent. Validates
structure, checks for issues, and reports agent health. Designed to
work across CLI agents (Claude Code, Codex CLI, Cursor, etc.).

Implements: CAP-SESSION-002 (Sanity Check Protocol)
Patterns: L038 (Agent-Agnostic), L021 (Verify-Before-Modify), L039 (Diagnostic Efficiency)

Usage:
    python3 health_check.py                    # Human-readable output
    python3 health_check.py --json             # JSON output
    python3 health_check.py --json --pretty    # Pretty-printed JSON
    python3 health_check.py --dir /path/agent  # Run on specific agent
    python3 health_check.py --fix              # Attempt auto-fixes

Exit codes:
    0: No detected errors or warnings (inspect skipped counts)
    1: Warnings found (non-blocking), or no check verified anything
    2: Errors found (blocking issues)
    3: Configuration/runtime error

L021 Verification Table:
    | Check | Resource | Before Action |
    |-------|----------|---------------|
    | 1 | .aget/ dir | Verify exists before reading |
    | 2 | version.json | Load before checking version |
    | 3 | identity.json | Load before checking identity |
    | 4 | governance/ | Check before verifying files |
    | 5 | evolution/ | Check before counting L-docs |

Author: aget-framework (canonical template)
Version: 1.0.0 (v3.1.0)
"""

import argparse
import importlib.util
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


# =============================================================================
# L039: Diagnostic Efficiency - Timing
# =============================================================================

_start_time = time.time()


def log_diagnostic(msg: str) -> None:
    """Log diagnostic message to stderr (L039: diagnostics to stderr)."""
    elapsed = (time.time() - _start_time) * 1000
    print(f"[{elapsed:.0f}ms] {msg}", file=sys.stderr)


# =============================================================================
# Check Result
# =============================================================================

class CheckResult:
    """Result of a single check."""

    def __init__(self, name: str, passed: bool, message: str = "",
                 severity: str = "info", fixable: bool = False,
                 skipped: bool = False):
        self.name = name
        # D-prime: `passed` stays a BOOLEAN and is False for every absent
        # subject. A skipped check verified nothing, so it cannot report a
        # pass; nulling the field instead (the rejected arm) broke every
        # bool-typed consumer for a distinction `skipped` already carries.
        self.passed = False if skipped else passed
        self.message = message
        self.severity = severity  # info, warning, error
        self.fixable = fixable
        # THE discriminator, not a convenience. Because a skip is `passed ==
        # False`, there is NO passed-only idiom that separates a failure from a
        # skip: `passed is False` now matches both. Every consumer asking for
        # failures MUST consult this key. It is therefore emitted on EVERY row
        # (see to_dict), never conditionally.
        self.skipped = skipped

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'passed': self.passed,
            'message': self.message,
            'severity': self.severity,
            'fixable': self.fixable,
            'skipped': self.skipped,
        }


# =============================================================================
# Checks
# =============================================================================

def check_aget_directory(agent_path: Path) -> CheckResult:
    """L021 Check 1: Verify .aget/ directory exists."""
    exists = (agent_path / '.aget').is_dir()
    return CheckResult(
        name=".aget_directory",
        passed=exists,
        message="" if exists else ".aget/ directory not found",
        severity="error" if not exists else "info"
    )


def check_version_json(agent_path: Path) -> CheckResult:
    """L021 Check 2: Verify version.json exists and is valid."""
    version_file = agent_path / '.aget' / 'version.json'

    if not version_file.exists():
        return CheckResult(
            name="version_json",
            passed=False,
            message="version.json not found",
            severity="error"
        )

    try:
        with open(version_file) as f:
            data = json.load(f)

        if 'aget_version' not in data:
            return CheckResult(
                name="version_json",
                passed=False,
                message="version.json missing aget_version field",
                severity="warning",
                fixable=True
            )

        return CheckResult(
            name="version_json",
            passed=True,
            message=f"v{data.get('aget_version', 'unknown')}"
        )

    except json.JSONDecodeError as e:
        return CheckResult(
            name="version_json",
            passed=False,
            message=f"Invalid JSON: {e}",
            severity="error"
        )


def check_identity_json(agent_path: Path) -> CheckResult:
    """L021 Check 3: Verify identity.json exists and has north_star."""
    identity_file = agent_path / '.aget' / 'identity.json'

    if not identity_file.exists():
        return CheckResult(
            name="identity_json",
            passed=False,
            message="identity.json not found (recommended for v3.0)",
            severity="warning",
            fixable=True
        )

    try:
        with open(identity_file) as f:
            data = json.load(f)

        if 'north_star' not in data:
            return CheckResult(
                name="identity_json",
                passed=False,
                message="identity.json missing north_star field",
                severity="warning"
            )

        return CheckResult(
            name="identity_json",
            passed=True,
            message="north_star defined"
        )

    except json.JSONDecodeError:
        return CheckResult(
            name="identity_json",
            passed=False,
            message="identity.json invalid JSON",
            severity="error"
        )


def check_governance_directory(agent_path: Path) -> CheckResult:
    """L021 Check 4: Verify governance/ directory and required files."""
    gov_dir = agent_path / 'governance'

    if not gov_dir.is_dir():
        return CheckResult(
            name="governance_directory",
            passed=False,
            message="governance/ directory not found (recommended for v3.0)",
            severity="warning",
            fixable=True
        )

    required_files = ['CHARTER.md', 'MISSION.md', 'SCOPE_BOUNDARIES.md']
    missing = [f for f in required_files if not (gov_dir / f).exists()]

    if missing:
        return CheckResult(
            name="governance_directory",
            passed=False,
            message=f"Missing: {', '.join(missing)}",
            severity="warning",
            fixable=True
        )

    # C-34-30 D2: report what was MEASURED, not the length of the requirement list.
    # `len(required_files)` is a constant: it printed "3 files present" whether the
    # directory held 3 files or 300, so the number carried no observation at all.
    present = sorted(q.name for q in gov_dir.glob('*.md'))
    return CheckResult(
        name="governance_directory",
        passed=True,
        message=(f"{len(required_files)}/{len(required_files)} required present; "
                 f"{len(present)} governance .md file(s) enumerated")
    )


def check_evolution_directory(agent_path: Path) -> CheckResult:
    """L021 Check 5: Check evolution/ for L-doc count and index."""
    evolution_dir = agent_path / '.aget' / 'evolution'

    if not evolution_dir.is_dir():
        return CheckResult(
            name="evolution_directory",
            passed=False,
            # NOT APPLICABLE (info). This check's subject is the L-doc corpus and
            # its ">50 L-docs require index.json" rule. A new agent lawfully has
            # no corpus, so the rule has nothing to range over — nothing here is
            # expected-but-unseen. Contrast check_config_size, where the absent
            # file IS expected at every seat.
            message="No evolution/ directory — not applicable (OK for new agents)",
            severity="info",
            skipped=True,
        )

    l_docs = list(evolution_dir.glob('L*.md'))
    count = len(l_docs)

    # Check if index is needed (>50 L-docs)
    if count > 50:
        index_file = evolution_dir / 'index.json'
        if not index_file.exists():
            return CheckResult(
                name="evolution_directory",
                passed=False,
                message=f"{count} L-docs but no index.json (required >50)",
                severity="warning",
                fixable=True
            )

    return CheckResult(
        name="evolution_directory",
        passed=True,
        message=f"{count} L-docs"
    )


def check_5d_structure(agent_path: Path) -> CheckResult:
    """Check 5D directory structure (v3.0 requirement)."""
    dimensions = ['persona', 'memory', 'reasoning', 'skills', 'context']
    aget_dir = agent_path / '.aget'

    present = [d for d in dimensions if (aget_dir / d).is_dir()]
    missing = [d for d in dimensions if d not in present]

    if not missing:
        return CheckResult(
            name="5d_structure",
            passed=True,
            message="5/5 dimensions present"
        )

    if len(present) == 0:
        return CheckResult(
            name="5d_structure",
            passed=False,
            message="No 5D directories (pre-v3.0 structure)",
            severity="warning"
        )

    return CheckResult(
        name="5d_structure",
        passed=False,
        message=f"Missing: {', '.join(missing)}",
        severity="warning",
        fixable=True
    )


def check_sessions_directory(agent_path: Path) -> CheckResult:
    """Check sessions/ directory exists."""
    sessions_dir = agent_path / 'sessions'

    if not sessions_dir.is_dir():
        return CheckResult(
            name="sessions_directory",
            passed=False,
            message="sessions/ directory not found",
            severity="warning",
            fixable=True
        )

    # SC-011: Use correct SESSION_*.md convention with legacy fallback
    session_files = list(sessions_dir.glob('SESSION_*.md'))
    if not session_files:
        session_files = list(sessions_dir.glob('session_*.md'))  # legacy fallback
    return CheckResult(
        name="sessions_directory",
        passed=True,
        message=f"{len(session_files)} session files"
    )


def check_planning_directory(agent_path: Path) -> CheckResult:
    """Check planning/ directory exists."""
    planning_dir = agent_path / 'planning'

    if not planning_dir.is_dir():
        return CheckResult(
            name="planning_directory",
            passed=False,
            message="planning/ directory not found",
            severity="warning",
            fixable=True
        )

    plans = list(planning_dir.glob('PROJECT_PLAN_*.md'))
    return CheckResult(
        name="planning_directory",
        passed=True,
        message=f"{len(plans)} PROJECT_PLANs"
    )


def check_duplicate_ldoc_ids(agent_path: Path) -> CheckResult:
    """L131: Detect duplicate L-doc IDs (two distinct lessons sharing one L###).

    Presence/count checks cannot catch ID collisions. This check CAN fail on a
    real, independently-detectable defect — the test L131/L671 demand of every
    health check ("what real failure turns this RED?").
    """
    evolution_dir = agent_path / '.aget' / 'evolution'
    if not evolution_dir.is_dir():
        # NOT APPLICABLE (info). An ID collision is undefined over zero IDs; the
        # absent corpus is the same lawful absence classified at
        # check_evolution_directory, and the two must agree or one seat reads as
        # half-unverified for a single missing directory.
        return CheckResult("duplicate_ldoc_ids", False,
                           "No evolution/ directory — not applicable",
                           "info", skipped=True)

    # C-34-30 D1: NORMALIZE the numeric part before counting. The prior key was the
    # literal matched text, so `L99_x.md` and `L099_y.md` were two different keys and
    # a real duplicate ID reported clean. Zero-padding is a filename convention, not
    # an identity: L99 and L099 are the same L-doc, and a duplicate-ID check that
    # cannot see that is blind to the exact collision it exists to find.
    seen: Dict[str, int] = {}
    variants: Dict[str, set] = {}
    for f in evolution_dir.glob('L*.md'):
        m = re.match(r'L(\d+)_', f.name)
        if m:
            key = f"L{int(m.group(1))}"          # L099 -> L99, L99 -> L99
            seen[key] = seen.get(key, 0) + 1
            variants.setdefault(key, set()).add(m.group(0).rstrip('_'))

    dups = sorted(k for k, v in seen.items() if v > 1)
    if dups:
        return CheckResult(
            name="duplicate_ldoc_ids",
            passed=False,
            message=(f"{len(dups)} duplicate L-doc ID(s): {', '.join(dups)} "
                     "(two lessons share one ID; renumber per L131)"),
            severity="warning"
        )
    return CheckResult(
        name="duplicate_ldoc_ids",
        passed=True,
        message=f"{len(seen)} unique L-doc IDs, no collisions"
    )


def check_config_size(agent_path: Path) -> CheckResult:
    """L146: AGENTS.md must stay under the 40k hard limit (30k recommended)."""
    agents_md = agent_path / 'AGENTS.md'
    if not agents_md.exists():
        # UNVERIFIED-BUT-EXPECTED (warning). Every AGET seat is defined by an
        # AGENTS.md; its absence is drift, not inapplicability, so this is the
        # one absent-subject site here that departs from the rejected arm's
        # `info`. Not a permanent warning floor: adding the file clears it.
        return CheckResult("config_size", False,
                           "No AGENTS.md — size not verified", "warning",
                           skipped=True)

    size = agents_md.stat().st_size
    if size > 40000:
        return CheckResult(
            name="config_size",
            passed=False,
            message=f"AGENTS.md {size} bytes exceeds 40k hard limit (L146)",
            severity="error"
        )
    if size > 30000:
        return CheckResult(
            name="config_size",
            passed=False,
            message=(f"AGENTS.md {size} bytes over 30k recommended (L146); "
                     "extract content to .aget/docs/"),
            severity="warning"
        )
    return CheckResult(
        name="config_size",
        passed=True,
        message=f"AGENTS.md {size} bytes (under 30k)"
    )


# =============================================================================
# Main Protocol
# =============================================================================

# Framework artifact-lifecycle routing skills checked for model invocability.
# This is not every locally Strict gate, engine-backed skill or provenance class.
# Local enforcement additions belong in the seat's extension and local routing
# register; their absence from this tuple does not invalidate the local policy.
D71_STRUCTURAL_SKILLS = (
    "aget-create-project", "aget-close-project",
    "aget-create-initiative", "aget-file-issue",
)


def check_structural_skill_frontmatter(agent_path: Path) -> CheckResult:
    """D71 invariant: no D71-STRUCTURAL skill may carry `disable-model-invocation`.

    The flag blocks model (agent) invocation, but D71 mandates the agent MUST
    invoke these skills; a drifted flag makes D71 unsatisfiable on this instance.
    Ref: gmelli/aget-aget#1489 (SGR remediation F2).
    """
    skills_dir = agent_path / ".claude" / "skills"
    if not skills_dir.is_dir():
        # NOT APPLICABLE (info). With no skills directory the seat declares no
        # D71 routes at all, so there is no frontmatter flag that could be wrong.
        # The sibling branch below is warning because there the seat DOES carry
        # skills and named routes are missing from them.
        return CheckResult("structural_skill_frontmatter", False,
                           "No .claude/skills/ — not applicable", "info", skipped=True)
    offenders = []
    absent = []
    unreadable = []
    for skill in D71_STRUCTURAL_SKILLS:
        sk = skills_dir / skill / "SKILL.md"
        if not sk.is_file():
            absent.append(skill)
            continue
        try:
            text = sk.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            unreadable.append(skill)
            continue
        # inspect only the frontmatter (between the first two '---' markers)
        parts = text.split("---", 2)
        front = parts[1] if text.startswith("---") and len(parts) >= 3 else text
        for line in front.splitlines():
            s = line.strip().replace(" ", "")
            if s.startswith("disable-model-invocation:true"):
                offenders.append(skill)
                break
    if offenders:
        return CheckResult(
            "structural_skill_frontmatter", False,
            "D71 violation: disable-model-invocation on STRUCTURAL skill(s): "
            f"{', '.join(offenders)} — agent cannot model-invoke; remove the flag (ref #1489)",
            severity="error", fixable=True)
    if absent or unreadable:
        present = len(D71_STRUCTURAL_SKILLS) - len(absent) - len(unreadable)
        # UNVERIFIED-BUT-EXPECTED (warning). D71_STRUCTURAL_SKILLS names routes
        # this framework expects to exist; an absent or unreadable one leaves a
        # named route unmeasured. Clearable by installing or repairing the skill.
        return CheckResult(
            "structural_skill_frontmatter", False,
            f"{present}/{len(D71_STRUCTURAL_SKILLS)} D71-STRUCTURAL skills present + clean; "
            f"ABSENT (not model-invocable; expected if unmigrated phantom, else drift): "
            f"{', '.join(absent) or 'none'}; UNREADABLE: "
            f"{', '.join(unreadable) or 'none'} (ref #1553); not verified",
            severity="warning", skipped=True)
    return CheckResult("structural_skill_frontmatter", True,
                       f"All {len(D71_STRUCTURAL_SKILLS)} framework artifact-lifecycle routes present + "
                       "carry no disable-model-invocation; local additions require checks "
                       "by the seat extension", "info")


def check_permission_accumulation(agent_path: Path) -> CheckResult:
    """L500/L027 (#1516, v3.25 C-25-06): permission-file accumulation gate.

    WARN over 100 permissions or 30KB; ERROR over 200 or 50KB. Previously a
    documented threshold with no failing check — HEALTHY-through (L671).
    """
    worst = None
    inspected = []
    for name in ('settings.local.json', 'settings.json'):
        f = agent_path / '.claude' / name
        if not f.exists():
            continue
        inspected.append(name)
        size = f.stat().st_size
        try:
            allow = json.loads(f.read_text()).get('permissions', {}).get('allow', [])
        except Exception:
            allow = []
        n = len(allow)
        if n > 200 or size > 50_000:
            return CheckResult('permission_accumulation', False,
                               f'{name}: {n} permissions / {size} bytes exceeds CRITICAL '
                               f'(200 / 50KB) — run SOP_permission_cleanup', severity='error')
        if n > 100 or size > 30_000:
            worst = f'{name}: {n} permissions / {size} bytes over WARN (100 / 30KB)'
    if worst:
        return CheckResult('permission_accumulation', False, worst, severity='warning')
    # NOT A SKIP, deliberately — the one absent-subject site here where absence is
    # DISPOSITIVE. No permission file means zero accumulated permissions and zero
    # bytes, which cannot exceed a threshold: absence proves the very property this
    # check asserts. Calling it "not verified" would be false about the only thing
    # the absence does establish. The message must say what was read, so a genuine
    # pass over a live file is never confused with a pass over nothing.
    if not inspected:
        return CheckResult('permission_accumulation', True,
                           'no .claude/settings*.json present — 0 permissions '
                           'accumulated, within L500 thresholds')
    return CheckResult('permission_accumulation', True,
                       f"{', '.join(inspected)} within L500 thresholds")


def check_reliance_manifest(agent_path: Path) -> CheckResult:
    """R-BND-001-03 (v3.25, gh#1787): self-attest reliance-manifest conformance.

    Graceful: agents without a manifest (pre-adoption) PASS with an advisory
    message — absence is expected lag, not an error (L601). When both the
    manifest and its validator are present, the validator's verdict is the check.
    """
    manifest = agent_path / '.aget' / 'skill_reliance_manifest.yaml'
    validator = agent_path / 'scripts' / 'check_skill_reliance_manifest.py'
    if not manifest.exists():
        # NOT APPLICABLE (info). R-BND-001-03 is opt-in and pre-adoption lag is
        # expected (L601). With no manifest the seat asserts no reliance claim,
        # so there is no claim left unverified.
        return CheckResult('reliance_manifest', False,
                           'no manifest (pre-adoption — not applicable, not required)',
                           severity='info', skipped=True)
    if not validator.exists():
        # UNVERIFIED-BUT-EXPECTED (warning) — wiring gap. The manifest EXISTS, so
        # a conformance claim is being made, and the declared instrument for it is
        # missing. The rejected arm marked this `failed`, while the identical
        # instrument-absent case in check_spec_enforcement_truthfulness was marked
        # skipped; one wiring gap cannot be a verified failure and its twin a skip.
        return CheckResult('reliance_manifest', False,
                           'manifest present but validator missing — not verified '
                           '(R-BND-001-03 wiring gap)',
                           severity='warning', skipped=True)
    import subprocess
    try:
        r = subprocess.run([sys.executable, str(validator)], capture_output=True,
                           text=True, timeout=15, cwd=str(agent_path))
        ok = r.returncode == 0
        tail = (r.stdout or r.stderr).strip().splitlines()
        msg = tail[-1] if tail else f'exit {r.returncode}'
        return CheckResult('reliance_manifest', ok, msg,
                           severity='info' if ok else 'warning')
    except Exception as e:
        # UNVERIFIED-BUT-EXPECTED (warning) — same wiring-gap class as the branch
        # above, one step later: the instrument is present but did not run, so its
        # verdict is absent rather than negative. A validator that crashed has not
        # found the manifest non-conformant.
        return CheckResult('reliance_manifest', False,
                           f'validator error — not verified: {e}',
                           severity='warning', skipped=True)


def check_spec_enforcement_truthfulness(agent_path: Path) -> CheckResult:
    """Check canonical spec-enforcement declarations when the corpus is present.

    Most downstream agents do not ship the public specification corpus or this
    validator, so absence of either surface is an explicit not-applicable pass.
    Repositories that carry both surfaces receive a warning-only truthfulness
    result; the existing baseline is non-conformant and must remain remediable.
    """
    specs = agent_path / 'specs'
    checker = agent_path / 'scripts' / 'check_enforcement_claims.py'
    if not specs.is_dir() or not checker.is_file():
        missing = []
        if not specs.is_dir():
            missing.append('spec corpus')
        if not checker.is_file():
            missing.append(f'checker ({checker.name})')
        count = sum(p.is_file() for p in specs.glob('*.md')) if specs.is_dir() else 0
        detail = f'; {count} spec document(s) present and UNVERIFIED' if count else ''
        # SPLIT DECISION on one branch, deliberately. No spec corpus at all =>
        # NOT APPLICABLE (info): nothing claims an enforcement level here. Spec
        # documents present but the checker absent => UNVERIFIED-BUT-EXPECTED
        # (warning): claims exist and are unmeasured. `count` is the evidence,
        # and it is counted from actual files, not from the directory existing.
        return CheckResult(
            'spec_enforcement_truthfulness',
            False,
            f"not verified -- {' and '.join(missing)} absent{detail}",
            severity='warning' if count else 'info',
            skipped=True,
        )

    scripts_dir = str(checker.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        from check_enforcement_claims import scan

        result = scan(agent_path, r'specs/.*\.md$')
    except Exception as exc:
        # UNVERIFIED-BUT-EXPECTED (warning) — wiring gap. Both surfaces are
        # present and the import/scan failed, so no truthfulness verdict exists.
        # Unchanged from the reviewed arm; the reliance_manifest branches above
        # were brought into line with THIS one, not the reverse.
        return CheckResult(
            'spec_enforcement_truthfulness',
            False,
            f'checker unavailable — not verified: {type(exc).__name__}',
            severity='warning',
            skipped=True,
        )

    passed = result['status'] == 'PASS'
    message = (
        f"{result['status']}: {len(result['findings'])} finding(s) across "
        f"{result['claims_checked']} named claim(s) in "
        f"{result['specs_scanned']} spec(s); scope=this repository"
    )
    return CheckResult(
        'spec_enforcement_truthfulness',
        passed,
        message,
        severity='info' if passed else 'warning',
    )


def run_housekeeping(agent_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """
    Run all housekeeping checks.

    Returns structured dict suitable for JSON or human output.
    """
    data = {
        'timestamp': datetime.now().isoformat(),
        'agent_path': str(agent_path),
        'checks': [],
        'summary': {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'warnings': 0,
            'errors': 0,
            'fixable': 0,
        },
        'status': 'unknown',
    }

    # Run all checks
    checks = [
        check_aget_directory,
        check_version_json,
        check_identity_json,
        check_governance_directory,
        check_evolution_directory,
        check_5d_structure,
        check_sessions_directory,
        check_planning_directory,
        check_duplicate_ldoc_ids,
        check_config_size,
        check_structural_skill_frontmatter,
        check_reliance_manifest,
        check_spec_enforcement_truthfulness,
        check_permission_accumulation,
    ]

    for check_fn in checks:
        if verbose:
            log_diagnostic(f"Running {check_fn.__name__}")

        result = check_fn(agent_path)
        data['checks'].append(result.to_dict())

        data['summary']['total'] += 1
        # Verdict partition: passed + failed + skipped == total, mutually
        # exclusive. `skipped` is tested FIRST because a skip is passed=False.
        if result.skipped:
            data['summary']['skipped'] += 1
        elif result.passed:
            data['summary']['passed'] += 1
        else:
            data['summary']['failed'] += 1
        # Severity counters OVERLAP the partition and stay gated on `not passed`.
        # Ungating them (the rejected arm) makes an advisory pass — passed=True
        # with severity='warning', which several checks return by design —
        # increment `warnings` forever, so status never leaves 'warning' and exit
        # 1 becomes a floor no repair can clear. Skips reach these counters
        # because a skip is passed=False: that is the intent, and it is what
        # keeps a warning-severity skip visible as a warning.
        if not result.passed:
            if result.severity == 'warning':
                data['summary']['warnings'] += 1
            elif result.severity == 'error':
                data['summary']['errors'] += 1

        if result.fixable:
            data['summary']['fixable'] += 1

    # Determine status
    if data['summary']['errors'] > 0:
        data['status'] = 'error'
    elif data['summary']['warnings'] > 0:
        data['status'] = 'warning'
    elif data['summary']['passed'] == 0 and data['summary']['skipped']:
        # Zero-verified guard. A run that verified nothing must not report
        # 'healthy' — 0/0 is not a clean bill. It lands on WARNING/exit 1 rather
        # than minting a fourth status and a fourth exit code: no exit code is
        # added and none is remapped, so every consumer of (0, 1, 2) keeps
        # working and the distinction is read off summary['skipped'].
        data['status'] = 'warning'
    else:
        data['status'] = 'healthy'

    return data


def format_human_output(data: Dict[str, Any]) -> str:
    """Format data for human-readable output."""
    lines = []

    lines.append("\n=== AGET Housekeeping Report ===\n")

    # Summary
    summary = data['summary']
    status = data['status']

    status_symbol = {'healthy': '+', 'warning': '!', 'error': 'x'}.get(status, '?')
    lines.append(f"Status: [{status_symbol}] {status.upper()}")
    skipped = summary.get('skipped', 0)
    lines.append(f"Checks: {summary['passed']}/{summary['total'] - skipped} passed")
    if skipped:
        lines.append(f"Skipped: {skipped} (not verified)")

    if summary['warnings']:
        lines.append(f"Warnings: {summary['warnings']}")
    if summary['errors']:
        lines.append(f"Errors: {summary['errors']}")
    if summary['fixable']:
        # C-34-30 D3: the previous advice told the operator to re-run with the repair
        # flag, which was parsed and never read. Report the count; do not advertise a
        # capability that does not exist.
        lines.append(f"Fixable: {summary['fixable']} (no automatic fixer — use /aget-enhance-health or repair manually)")

    lines.append("")
    lines.append("Checks:")

    # Individual checks
    for check in data['checks']:
        # `skipped` is read FIRST: a skip is passed=False, so a passed-only
        # ladder would render every skip as a failure marker.
        symbol = ('SKIP' if check.get('skipped', False) else
                  '+' if check['passed'] else ('!' if check['severity'] == 'warning' else 'x'))
        name = check['name'].replace('_', ' ').title()
        lines.append(f"  [{symbol}] {name}: {check['message']}")

    lines.append("")
    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def call_extension_hook(agent_path, data, verbose=False):
    """HC extension hook (v3.26 C-26-05, gh#1836/#1848): call
    scripts/health_check_ext.py:post_health(data) if present.

    Same contract as wake_up.py WU-008: hook receives the housekeeping data
    dict, returns an augmented dict (additive-only per L464); absence = no-op;
    failure = warning + continue (ADR-004). Root cause this closes: instances
    needing agent-specific checks had no hook point and patched the
    Framework_Artifact itself, which the next upgrade clobbered (a downstream fleet
    GATE-0 halt class).
    """
    ext_path = agent_path / 'scripts' / 'health_check_ext.py'
    if not ext_path.exists():
        return data
    try:
        spec = importlib.util.spec_from_file_location('health_check_ext', str(ext_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'post_health'):
            result = module.post_health(data)
            if isinstance(result, dict):
                return result
            if verbose:
                log_diagnostic("health_check_ext returned non-dict, ignoring")
    except Exception as e:
        print(f"Warning: health_check extension hook failed: {e}", file=sys.stderr)
    return data


def main():
    parser = argparse.ArgumentParser(
        description='AGET Housekeeping Protocol (v3.1 template)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
L021 Verification Table:
  1. .aget/ dir - Verify exists before reading
  2. version.json - Load before checking version
  3. identity.json - Load before checking identity
  4. governance/ - Check before verifying files
  5. evolution/ - Check before counting L-docs

Exit codes:
  0 - All checks passed
  1 - Warnings found
  2 - Errors found
  3 - Runtime error
        """
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        help='Agent directory (default: current directory)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='REFUSED — no automatic fixer exists; the flag is rejected, not ignored'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable diagnostic output to stderr'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='health_check.py 1.0.0 (AGET v3.1.0)'
    )

    args = parser.parse_args()

    # C-34-30 D3: REFUSE rather than ignore. `--fix` was accepted and never read, so
    # an operator running it got a clean report and believed something was repaired.
    # A silently-ignored flag is worse than an absent one: it manufactures confidence.
    if getattr(args, 'fix', False):
        print("health_check: --fix is REFUSED — no automatic fixer is implemented.\n"
              "               Findings are reported for manual repair. Re-run without --fix.",
              file=sys.stderr)
        return 2

    # L039: Diagnostic timing
    if args.verbose:
        log_diagnostic("Starting housekeeping protocol")

    # Find agent root
    if args.dir:
        agent_path = Path(args.dir).resolve()
    else:
        agent_path = Path.cwd()

    # Check .aget/ exists
    if not (agent_path / '.aget').is_dir():
        if args.json:
            error = {
                'status': 'error',
                'errors': ['Could not find .aget/ directory'],
            }
            print(json.dumps(error, indent=2 if args.pretty else None))
        else:
            print("Error: Could not find .aget/ directory", file=sys.stderr)
        return 3

    if args.verbose:
        log_diagnostic(f"Found agent at: {agent_path}")

    # Run housekeeping
    data = run_housekeeping(agent_path, verbose=args.verbose)

    # Extension hook (v3.26 C-26-05) — instance-specific checks join here
    data = call_extension_hook(agent_path, data, verbose=args.verbose)

    if args.verbose:
        log_diagnostic(f"Housekeeping complete, status={data['status']}")

    # Output
    if args.json:
        print(json.dumps(data, indent=2 if args.pretty else None))
    else:
        print(format_human_output(data))

    if args.verbose:
        elapsed = (time.time() - _start_time) * 1000
        log_diagnostic(f"Complete in {elapsed:.0f}ms")

    # Exit code based on status
    if data['status'] == 'error':
        return 2
    elif data['status'] == 'warning':
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
