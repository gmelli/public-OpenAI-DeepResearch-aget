# Agent Configuration

@aget-version: 2.8.0

## Agent Compatibility
This configuration follows the AGENTS.md open-source standard for universal agent configuration.
Works with Claude Code, Cursor, Aider, Windsurf, and other CLI coding agents.
**Note**: CLAUDE.md is a symlink to this file for backward compatibility.

## Project Context

public-OpenAI-DeepResearch-aget (DeepThink) - Cognitive research agent - v2.8.0

Experimental agent with dual OpenAI implementation for advanced research capabilities.
Supports inter-agent collaboration via handoff protocol.

## Portfolio Configuration (v2.7.0)

**Portfolio Assignment**: `main` (Main Portfolio - private classification)

**Purpose**: Deep research and experimentation within the Main portfolio

**Portfolio Manifest**: `.aget/portfolios/MAIN_PORTFOLIO.yaml` (supervisor agent)

**Classification**: Private (research and experimentation, bleeding edge experimental)

**Portfolio Awareness**: Operates within Main portfolio boundaries, supports cross-agent research collaboration

## Session Management Protocols

### Wake Up Protocol
When user says "wake up" or "hey":
- Read AGENTS.md (this file)
- Show current directory and git status
- Report capabilities and readiness
- Note: Bleeding edge experimental structure, custom wake up behavior

**Output Format**:
```
public-OpenAI-DeepResearch-aget v{version} (DeepThink)
Type: Experimental cognitive research agent
Portfolio: Main

📍 Location: {pwd}
📊 Git: {status}

🎯 Key Capabilities:
• Deep research with dual OpenAI implementation
• Inter-agent collaboration via handoff protocol
• Advanced research capabilities
• Experimental bleeding-edge features

Ready for research tasks.
```

### Wind Down Protocol
When user says "wind down" or "save work":
- Commit changes with descriptive message
- Create session notes in `sessions/` (if directory exists)
- Report "Session preserved"
- Note: Custom experimental structure

## Housekeeping Commands

### Sanity Check
When user says "sanity check":
- Run: `python3 scripts/aget_housekeeping_protocol.py sanity-check`
- Verify critical components present and functional
- Report system status: OK/DEGRADED/CRITICAL

### Repository Best Practices

**Large Files & Git:**
- Never commit files >100MB (GitHub limit)
- Backup archives (*.tar, *.zip) should use Git LFS or be .gitignored
- Pattern for naming: `my-*` repos must be private
- Before first push: Use BFG Repo-Cleaner to remove large files from history if needed
  ```bash
  brew install bfg
  bfg --delete-files "*.tar" --no-blob-protection
  git reflog expire --expire=now --all && git gc --prune=now --aggressive
  ```

## Specification Creation (v2.2.0)

### When to Create Specs
User says: "create spec", "formal specification", "EARS spec", or "document capabilities formally"

### Specification Workflow

**Step 1: Read Format Documentation**
- File: `.aget/docs/SPEC_FORMAT_v1.1.md`
- Contains: EARS patterns, YAML structure, maturity levels, examples

**Step 2: Create Spec File**
- Location: `.aget/specs/{DOMAIN}_SPEC_v{VERSION}.yaml`
- Format: YAML with EARS temporal patterns
- Maturity levels:
  - **bootstrapping**: Simple capability list (no EARS)
  - **minimal**: EARS patterns with basic structure
  - **standard**: Full validation, test references
  - **exemplary**: Constitutional governance, comprehensive

**Step 3: Use Intelligence Tools**
- Run ambiguity detector on each capability
- During creation: Use detector logic to flag potential ambiguities
- Present flags to user for decision
- Add clarifications based on suggestions

### Intelligence Integration

**Ambiguity Detection (Automatic):**
- Proactively identify ambiguities during spec creation
- Use patterns from `.aget/intelligence/ambiguity_corpus.yaml`
- Present ambiguity flags with confidence scores
- User decides: accept flag, clarify, or reject
- Add clarifications to capability with `ambiguity_check` metadata

## Collaboration Protocol (v2.3)

### Receiving Handoff Requests
When another AGET needs research capabilities:

**Check for pending handoffs:**
```bash
python3 .aget/tools/handoff_receiver.py --list
```

**Process pending handoff:**
```bash
python3 .aget/tools/handoff_receiver.py --process-next
```

**Handoff structure:**
- Location: `.aget/coordination/handoff_*.json`
- Schema: `.aget/schemas/collaboration_context_v1.0.yaml`
- See: `.aget/coordination/README.md` for details

### Creating Handoff Requests
When delegating to other AGETs:

```bash
python3 .aget/tools/handoff_context.py \
  --initiator my-OpenAI-DeepResearch-aget \
  --target my-GITHUB-aget \
  --task-type file_issue \
  --description "Task description" \
  --params '{"param1": "value"}' \
  --objectives "Objective 1" \
  --completion "Completion criteria" \
  --priority medium \
  --output ~/github/my-GITHUB-aget/.aget/coordination/handoff_task.json
```

## Configuration Size Management (v2.6.0)

**Policy**: AGENTS.md must remain under 40,000 characters to ensure reliable Claude Code processing (L146).

**Current status**:
```bash
# Check this configuration's size
wc -c AGENTS.md
# Current: ~4k chars (well under 35k warning threshold)
# Target: <35,000 chars (warning threshold)
# Limit: 40,000 chars (hard limit)
```

### Why Size Matters

Large configuration files (>40k characters) cause performance degradation:
- Visible processing delays ("Synthesizing..." indicator)
- Increased latency on all commands (wake up, wind down, etc.)
- Degraded user experience

**Performance correlation** (per L146):
| Size | Wake Latency | User Experience |
|------|--------------|-----------------|
| <25k | <0.5s | Excellent (immediate) |
| 25-35k | <1s | Fast (minimal delay) |
| 35-40k | 1-2s | Borderline noticeable |
| >40k | 2-3s | Noticeable delay (⚠️) |

### Management Strategy

**This agent is well under the 35k warning threshold. Continue monitoring size when adding features.**

**What to extract** (if approaching 25k):
1. **Detailed protocols** → `.aget/docs/protocols/` (keep quick reference inline)
2. **Extended examples** → `.aget/docs/examples/` (verbose interaction examples)
3. **Helper tool documentation** → `.aget/docs/tools/` (tool usage with examples)
4. **Historical context** → `.aget/evolution/` (learnings and decisions)

**What to keep inline**:
- Agent identity and role
- Core protocols (wake/wind down)
- Frequently used commands
- Quick references (1-2 lines per concept)

**Before adding features**:
```bash
# Check current size
current=$(wc -c < AGENTS.md)

# If approaching or over 35k, extract content first
if [ $current -gt 35000 ]; then
  echo "⚠️ Over warning threshold: Extract content before adding"
fi
```

**Pattern**: L146 (Configuration Size Management)

## Capabilities
- Research and information synthesis (primary)
- Routing and delegation
- Citation management
- Learning and adaptation
- Memory and context retention
- Inter-agent collaboration (v2.3)

## Agent Type
Cognitive research agent (bleeding edge experimental)

---
*Generated by AGET v2.3 - DeepThink variant*