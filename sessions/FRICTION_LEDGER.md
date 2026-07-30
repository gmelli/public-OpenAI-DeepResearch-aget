# Friction Ledger

Durable, append-only capture of principal-reported friction, auto-recorded by
`scripts/capture_friction.py` (UserPromptSubmit hook). Enhancement-backlog substrate
(AGET_FRICTION_SPEC CAP-FRIC-002 / L656 harvestable corpus).

**Entry format**: `## FRICTION <iso-ts> | session <id> | status: <new|filed #N|wontfix|dedup #N>`
followed by the verbatim note. **Harvest** (CAP-FRIC-003): grep `status: new`, cluster, dedup
against open issues (non-optional, L669), file via `/aget-file-issue`, then update status.

## FRICTION 2026-07-29T16:41:12 | session c97b589d | status: dedup #1875 (also #1740) | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     Class: first-party AGET skill invocation trips a permission prompt; the harness-offered
     "don't ask again" scope is per-directory, so every seat pays the grant separately.
     Deduped against gmelli/aget-aget open issues (200 scanned):
       - #1875 Permission-scope shaping: harness-offered "don't ask again" scopes are
         wrong-shaped (too broad or dead-narrow)  <- primary match
       - #1740 Recurring bash-gate friction (3 sub-classes) — adopt scoped allowlist
     NOT filed: filing would duplicate #1875. Local symptom already absorbed —
     settings.local.json carries Skill(aget-wake-up); 8 grants total, far under the
     SOP_permission_cleanup OK band (0–100 count / 0–30KB). -->

"
⏺ Skill(aget-wake-up)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-wake-up"?
 Claude may use instructions, code, or files from this Skill.

   Initialize AGET session with status briefing

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-wake-up in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", '

## FRICTION 2026-07-29T16:53:35 | session c97b589d | status: dedup #1872 | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     Class: one `git push` execution rendered the identical approval prompt 3x (the note
     below is the same block pasted three times — that repetition IS the report).
     Deduped against gmelli/aget-aget:
       - #1872 Duplicate permission-prompt render: identical Bash approval prompt rendered
         3-4x for one execution (N=2 sessions)  <- exact class match
     NOT filed: this session is corroborating evidence raising #1872 to N=3, not a new class.
     Corroboration comment on #1872 held for principal approval (outward-facing). -->

"
────────────────────────────────────────────────────────────────────────────────
 Bash command

   git push origin main 2>&1 | tail -5; echo "---"; git rev-list --left-right
   --count origin/main...main; git log --oneline -1 origin/main
   Push to origin main

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for git push and git rev-list commands in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
────────────────────────────────────────────────────────────────────────────────
 Bash command

   git push origin main 2>&1 | tail -5; echo "---"; git rev-list --left-right
   --count origin/main...main; git log --oneline -1 origin/main
   Push to origin main

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for git push and git rev-list commands in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
────────────────────────────────────────────────────────────────────────────────
 Bash command

   git push origin main 2>&1 | tail -5; echo "---"; git rev-list --left-right
   --count origin/main...main; git log --oneline -1 origin/main
   Push to origin main

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for git push and git rev-list commands in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
