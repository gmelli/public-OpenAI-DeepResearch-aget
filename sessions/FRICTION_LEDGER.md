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

## FRICTION 2026-07-29T17:04:43 | session c97b589d | status: dedup #1872 (extends class) | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     Class: same duplicate-render class as the 16:53:35 entry (#1872), but with TWO
     properties #1872 does not currently cover:
       1. Render count = 6 (counted: 6x "Use skill \"aget-file-issue\"?"). #1872's title
          documents 3-4x for one execution — this is 1.5-2x the documented band.
       2. Surface = Skill() approval prompt, not Bash. #1872 is titled "identical Bash
          approval prompt". Same defect shape, different permission surface.
     Third instance this session: 3x (Bash git push, 16:53) -> 6x (Skill, 17:04), both
     single executions. Within-session escalation is itself a data point.
     NOT filed: still #1872's class, not a new one — but the corroboration comment now
     carries a scope-extension ask (widen title/body from "Bash" to any approval prompt;
     widen "3-4x" to an observed range of 3-6x, N=3 sessions).
     Held for principal approval (outward-facing). -->

"
⏺ Skill(aget-file-issue)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-file-issue"?
 Claude may use instructions, code, or files from this Skill.

   File issues with L520 governance compliance

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-file-issue in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
⏺ Skill(aget-file-issue)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-file-issue"?
 Claude may use instructions, code, or files from this Skill.

   File issues with L520 governance compliance

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-file-issue in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
⏺ Skill(aget-file-issue)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-file-issue"?
 Claude may use instructions, code, or files from this Skill.

   File issues with L520 governance compliance

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-file-issue in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
⏺ Skill(aget-file-issue)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-file-issue"?
 Claude may use instructions, code, or files from this Skill.

   File issues with L520 governance compliance

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-file-issue in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
⏺ Skill(aget-file-issue)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-file-issue"?
 Claude may use instructions, code, or files from this Skill.

   File issues with L520 governance compliance

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-file-issue in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
", "
⏺ Skill(aget-file-issue)

────────────────────────────────────────────────────────────────────────────────
 Use skill "aget-file-issue"?
 Claude may use instructions, code, or files from this Skill.

   File issues with L520 governance compliance

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don't ask again for aget-file-issue in
      /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   3. No
"

## FRICTION 2026-07-29T17:07:42 | session c97b589d | status: dedup #1875 (dead-narrow half, materialized) | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     Class: #1875's "dead-narrow" half, and this is the strongest form of it yet — the
     harness-offered scope was
       Bash(awk '/17:04:43/,0' sessions/FRICTION_LEDGER.md)
     which embeds a literal wall-clock timestamp from the command being approved. The grant
     is dead by construction: it can never match a future command. The principal selected it
     (option 2), so it is now grant #13 in this seat's .claude/settings.local.json — a
     permanent no-op occupying a slot in the accumulation budget SOP_permission_cleanup
     measures. #1875 describes the shape; this entry is a reproducible instance of it
     landing in a real settings file.
     Deduped against gmelli/aget-aget:
       - #1875 Permission-scope shaping: harness-offered "don't ask again" scopes are
         wrong-shaped (too broad or dead-narrow)  <- exact match, dead-narrow half
       - #1740 Recurring bash-gate friction — adopt scoped allowlist (the remediation path)
     NOT filed: instance of #1875, not a new class.
     Remediated locally same session: dead grant pruned, replaced with pattern-shaped grants
     for the first-party AGET operations that actually recur (see commit).
     Session tally: 4 entries, 4 deduped, 0 filed — 2 to #1872 (duplicate render), 2 to
     #1875 (scope shaping). Both halves of the permission surface, one session. -->

"───────────────────────────────────────────────────────────────────────────────
 Bash command

   cd /Users/gabormelli/github/public-OpenAI-DeepResearch-aget; grep -n "^##
   FRICTION" sessions/FRICTION_LEDGER.md; echo "--- render count in newest
   entry ---"; awk '/17:04:43/,0' sessions/FRICTION_LEDGER.md | grep -c "Use
   skill \"aget-file-issue\"?"
   Locate and measure new friction entry

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don’t ask again for: awk '/17:04:43/,0'
                                    sessions/FRICTION_LEDGER.md
   3. No
"
