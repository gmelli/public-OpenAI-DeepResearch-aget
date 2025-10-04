#!/usr/bin/env python3
"""Housekeeping Protocol for DeepResearch AGET"""
import sys, subprocess
from pathlib import Path

def sanity_check():
    print("🚨 Sanity Check - Emergency Diagnostic")
    print("=" * 50)
    checks_passed = 0
    checks_total = 4

    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        print(f"  ✓ {result.stdout.strip()}")
        checks_passed += 1
    except: print("  ✗ Python check failed")

    try:
        if subprocess.run(["git", "status"], capture_output=True).returncode == 0:
            print("  ✓ Git repository operational")
            checks_passed += 1
    except: print("  ✗ Git check failed")

    if Path("AGENTS.md").exists():
        print("  ✓ AGENTS.md present")
        checks_passed += 1
    else: print("  ✗ AGENTS.md missing")

    if Path(".aget").is_dir():
        print("  ✓ .aget/ directory present")
        checks_passed += 1
    else: print("  ✗ .aget/ missing")

    print()
    if checks_passed == checks_total:
        print("✅ System Status: OK")
        return 0
    elif checks_passed >= 3:
        print("⚠️  System Status: DEGRADED")
        return 1
    else:
        print("❌ System Status: CRITICAL")
        return 2

if __name__ == "__main__":
    sys.exit(sanity_check() if len(sys.argv) < 2 or sys.argv[1] == "sanity-check" else 1)