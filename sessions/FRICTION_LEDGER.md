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

## FRICTION 2026-07-29T17:13:10 | session c97b589d | status: dedup #1846 (also #1872, #1875) | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     Class: PRIMARY match is #1846 (substitution-bearing commands re-trigger permission
     prompts every occurrence), not the two issues the earlier four entries deduped to.
     The diagnostic that makes it #1846:
       `Bash(git rev-list *)` has been in this seat's allowlist since 16:53 — granted by the
       principal precisely so this would stop asking. The 17:13 command was gated ANYWAY,
       because the gate evaluated the whole compound string, in which `git rev-list` appears
       only inside `$( ... )` command substitution nested in an `echo`. An existing grant for
       the substituted command does not satisfy the gate.
     Secondary matches:
       - #1872 duplicate render: 5x for one execution (running observed range 3-6x)
       - #1875 scope shaping: the offered grant was a FRAGMENT of a 6-line script —
         `echo "trunk-parity: $(git rev-list --left-right --count origin/main...main)"` —
         i.e. the incidental echo wrapper, not the gated verb. Won't generalize.
     NOT filed: instance of #1846.
     SELF-DIRECTED FINDING (the important half): this friction is substantially
     agent-manufactured. Compound one-liners with $(...) are MY habit, adopted for
     tool-call efficiency, and they defeat the very grants the principal keeps issuing.
     15 pattern grants were added at 17:0x and did not help, because the shape of my
     commands — not the absence of grants — is what trips the gate. Remediation is
     behavioral, not configurational: prefer separate simple commands, and prefer
     Read/Grep/Glob over Bash for diagnostics (which is exactly what R-CLOSE-040 in
     /aget-close-session already mandates, and which this session ignored for 5 hours).
     Session tally: 5 entries, 5 deduped, 0 filed. #1872 x2, #1875 x2, #1846 x1. -->

"Bash command

   cd /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   git push origin main 2>&1 | tail -2
   echo "--- V-tests ---"
   echo "trunk-parity: $(git rev-list --left-right --count
   origin/main...main)"
   python3 scripts/health_check.py 2>&1 | sed -n '3,4p'
   echo "reachability: $(python3 scripts/study_topic.py --topic 'v3.28' 2>&1
   | grep -o 'Found \*\*[0-9]*\*\*' )"
   echo "tree: $(git status --porcelain | wc -l | tr -d ' ') modified"
   Push and run wind-down readiness V-tests

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don’t ask again for: echo "trunk-parity: $(git rev-list
                                    --left-right --count origin/main...main)"
   3. No
", "Bash command

   cd /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   git push origin main 2>&1 | tail -2
   echo "--- V-tests ---"
   echo "trunk-parity: $(git rev-list --left-right --count
   origin/main...main)"
   python3 scripts/health_check.py 2>&1 | sed -n '3,4p'
   echo "reachability: $(python3 scripts/study_topic.py --topic 'v3.28' 2>&1
   | grep -o 'Found \*\*[0-9]*\*\*' )"
   echo "tree: $(git status --porcelain | wc -l | tr -d ' ') modified"
   Push and run wind-down readiness V-tests

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don’t ask again for: echo "trunk-parity: $(git rev-list
                                    --left-right --count origin/main...main)"
   3. No
", "Bash command

   cd /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   git push origin main 2>&1 | tail -2
   echo "--- V-tests ---"
   echo "trunk-parity: $(git rev-list --left-right --count
   origin/main...main)"
   python3 scripts/health_check.py 2>&1 | sed -n '3,4p'
   echo "reachability: $(python3 scripts/study_topic.py --topic 'v3.28' 2>&1
   | grep -o 'Found \*\*[0-9]*\*\*' )"
   echo "tree: $(git status --porcelain | wc -l | tr -d ' ') modified"
   Push and run wind-down readiness V-tests

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don’t ask again for: echo "trunk-parity: $(git rev-list
                                    --left-right --count origin/main...main)"
   3. No
", "Bash command

   cd /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   git push origin main 2>&1 | tail -2
   echo "--- V-tests ---"
   echo "trunk-parity: $(git rev-list --left-right --count
   origin/main...main)"
   python3 scripts/health_check.py 2>&1 | sed -n '3,4p'
   echo "reachability: $(python3 scripts/study_topic.py --topic 'v3.28' 2>&1
   | grep -o 'Found \*\*[0-9]*\*\*' )"
   echo "tree: $(git status --porcelain | wc -l | tr -d ' ') modified"
   Push and run wind-down readiness V-tests

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don’t ask again for: echo "trunk-parity: $(git rev-list
                                    --left-right --count origin/main...main)"
   3. No
", "Bash command

   cd /Users/gabormelli/github/public-OpenAI-DeepResearch-aget
   git push origin main 2>&1 | tail -2
   echo "--- V-tests ---"
   echo "trunk-parity: $(git rev-list --left-right --count
   origin/main...main)"
   python3 scripts/health_check.py 2>&1 | sed -n '3,4p'
   echo "reachability: $(python3 scripts/study_topic.py --topic 'v3.28' 2>&1
   | grep -o 'Found \*\*[0-9]*\*\*' )"
   echo "tree: $(git status --porcelain | wc -l | tr -d ' ') modified"
   Push and run wind-down readiness V-tests

 This command requires approval

 Do you want to proceed?
   1. Yes
 ❯ 2. Yes, and don’t ask again for: echo "trunk-parity: $(git rev-list
                                    --left-right --count origin/main...main)"
   3. No
", "

## FRICTION 2026-07-29T17:21:51 | session c97b589d | status: dedup #1925 (capture artifact) + #1846 (underlying) | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     TWO distinct things in this entry, and separating them is the whole finding.

     (a) CAPTURE ARTIFACT — #1925. The friction described did not happen at this seat. The
     principal pasted a private-supervisor-AGET transcript for analysis; the UserPromptSubmit
     hook fired on the quoted prompt-render inside it and recorded another seat's friction as
     this seat's. That is exactly #1925 ("friction-capture hook fires on quoted/pasted trigger
     text; L255 false-positive; hit both fleets"). Consequence beyond noise: this ledger now
     contains an event this seat never experienced, so any per-seat friction rate computed
     from it is inflated. Cross-seat contamination is the sharper form of #1925 — not just a
     duplicate, but attribution to the wrong agent.

     (b) UNDERLYING EVENT (at the supervisor seat, not here) — #1846 family. A heredoc-bearing
     command was gated with "Contains shell syntax (file_redirect) that cannot be statically
     analyzed". Same root as this seat's 17:13 entry: the gate cannot decide a compound/
     redirect-bearing string, so no grant can pre-authorize it. Note the asymmetry worth
     reporting upstream — 17:13 was gated because substitution HID an allowed verb; this one
     was gated because the analyzer DECLINED to parse at all. Both defeat grants, by opposite
     mechanisms. [CORRECTED 17:27 — #1846 covers BOTH: its body enumerates three analyzer
     classes, class 2 being heredoc/"expansion obfuscation". The speculation that the
     declines-half "may warrant its own row" was made from the truncated title without
     reading the body. See the 17:26:44 harvest note.]

     NOT filed: (a) is #1925; (b) is another seat's event and not this seat's to file.
     Session tally: 6 entries, 6 deduped, 0 filed. #1872 x2, #1875 x2, #1846 x1, #1925 x1.
     Of the 6, ONE (this one) was never this seat's friction at all. -->

"
  ⏺ Bash(python3 -c "
        import subprocess,sys…)
    ⎿  Waiting…

  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ───
   Bash command

     python3 -c "
     import subprocess,sys
     sys.path.insert(0,'scripts')
     import measure_published_pin_axis as m
     for name,repo in m.main.__globals__ and []: pass
     " 2>/dev/null; python3 - scripts/measure_published_pin_axis.py <<'EOF' 2>/dev/null || python3
     scripts/measure_published_pin_axis.py 2>&1 | grep -iE "public-|stale  " | head -6
     EOF
     Check the public-* blocking subset

   Contains shell syntax (file_redirect) that cannot be statically analyzed

   Do you want to proceed?
   ❯ 1. Yes
     2. No")

· Topsy-turvying… (14s · thinking with high effort)
  ⎿  Tip: Running multiple Claude sessions? Use /color and /rename to tell them apart at a glance.

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
❯
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  supervisor v3.28.0"

## FRICTION 2026-07-29T17:26:44 | session c97b589d | status: dedup #1846 (class 2, heredoc) | value-class: owed (pending-triage default, CAP-FRIC-006-04)

<!-- HARVEST 2026-07-29 (CAP-FRIC-003, L669 dedup non-optional):
     First-party this time (unlike the 17:21:51 entry, which was another seat's event
     captured here by the #1925 paste artifact). The gated command was this seat's own
     `git commit -q -F - <<'EOF'` — "Contains shell syntax (command) that cannot be
     statically analyzed", rendered 2x.

     Read #1846's body before deciding: it already enumerates THREE analyzer classes, and
     class 2 is "`Contains brace with quote character (expansion obfuscation)` — python3
     heredoc". Heredocs are in scope. Deduped, not filed.

     CORRECTION to the 17:21:51 harvest note, which speculated that the
     "analyzer-declines-to-parse" half "may warrant its own row if it is not already in
     scope." It IS in scope — #1846 class 2. That speculation was written without reading
     #1846's body, only its truncated title. Same defect as the four probes for gh#2009:
     a citation treated as a label instead of a source. Corrected in place.

     WHAT IS GENUINELY OUTSIDE #1846's REMEDIATION LANE (comment-worthy, not issue-worthy):
     #1846 frames the cluster as *migration-runbook* commands and proposes shipping the
     deterministic steps as tracked helper scripts invoked by plain path. That fix cannot
     reach this instance — the heredoc here carries a COMMIT MESSAGE, which is not a runbook
     step and not scriptable as a helper. It recurs on every commit, unconditionally, and it
     accounted for a prompt on all 6 commits of this session.
     Generalizable remediation for this sub-case: author the message with the Write tool to
     a file, then `git commit -F <path>` — no heredoc, statically analyzable, no grant needed.
     ADOPTED at this seat from this commit forward (this very commit uses it).

     Session tally: 7 entries, 7 deduped, 0 filed. #1872 x2, #1875 x2, #1846 x2, #1925 x1.
     Two were caused by the agent's own command shape; one was never this seat's at all. -->

"       worth reporting: 17:13 was gated because substitution HID an allowed
         verb; this one because the analyzer DECLINED to parse a heredoc at
   all.
         Both defeat existing grants, by opposite mechanisms.

   Session tally: 6 entries, 6 deduped, 0 filed. One was never this seat's.

   Health 13/13. AGENTS.md under 30k.

   Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
   EOF
   Commit peer-review corrections and push

 Contains shell syntax (command) that cannot be statically analyzed

 Do you want to proceed?
 ❯ 1. Yes
   2. No
", "       worth reporting: 17:13 was gated because substitution HID an allowed
         verb; this one because the analyzer DECLINED to parse a heredoc at
   all.
         Both defeat existing grants, by opposite mechanisms.

   Session tally: 6 entries, 6 deduped, 0 filed. One was never this seat's.

   Health 13/13. AGENTS.md under 30k.

   Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
   EOF
   Commit peer-review corrections and push

 Contains shell syntax (command) that cannot be statically analyzed

 Do you want to proceed?
 ❯ 1. Yes
   2. No
", "
