# Friction Ledger

Durable, append-only capture of principal-reported friction, auto-recorded by
`scripts/capture_friction.py` (UserPromptSubmit hook). Enhancement-backlog substrate
(AGET_FRICTION_SPEC CAP-FRIC-002 / L656 harvestable corpus).

**Entry format**: `## FRICTION <iso-ts> | session <id> | status: <new|filed #N|wontfix|dedup #N>`
followed by the verbatim note. **Harvest** (CAP-FRIC-003): grep `status: new`, cluster, dedup
against open issues (non-optional, L669), file via `/aget-file-issue`, then update status.

## FRICTION 2026-07-29T16:41:12 | session c97b589d | status: new | value-class: owed (pending-triage default, CAP-FRIC-006-04)
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
