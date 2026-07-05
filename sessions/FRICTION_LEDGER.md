# Friction Ledger

Durable, append-only capture of principal-reported friction, auto-recorded by
`scripts/capture_friction.py` (UserPromptSubmit hook). Enhancement-backlog substrate
(AGET_FRICTION_SPEC CAP-FRIC-002 / L656 harvestable corpus).

**Entry format**: `## FRICTION <iso-ts> | session <id> | status: <new|filed #N|wontfix|dedup #N>`
followed by the verbatim note. **Harvest** (CAP-FRIC-003): grep `status: new`, cluster, dedup
against open issues (non-optional, L669), file via `/aget-file-issue`, then update status.
