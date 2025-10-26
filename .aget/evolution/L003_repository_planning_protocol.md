# L003: Repository Planning Protocol

**Original**: 2025-09-25-LESSON-REPOSITORY-PLANNING.md
**Date**: 2025-09-25
**Context**: First awakening session - discovered gap in AGET creation workflow
**Category**: Development Workflow, Repository Management

---

## Problem

**Repository Planning Gap Waste**: Creating agents without repository strategy causes:
- 6+ tool calls at "sign off" discovering no remote exists
- Forced decision-making at worst time (after full development)
- Push failures requiring retroactive planning

**Example Waste Pattern**:
1. Create agent locally (5-8 hours development)
2. Build entire structure, memory, personality
3. Commit everything locally
4. Attempt "sign off" (tries to push)
5. **FAILURE**: No remote repository exists
6. Scramble to decide: Public? Private? Which account?

**Optimal Approach**: 5 questions BEFORE creation (2 minutes) prevents 6+ error cycles.

**Quantification**:
- Time waste: 10-15 minutes resolving at sign-off vs. 2 minutes planning upfront
- Error cycles: 6+ tool calls (status → error → decision → retry → push)
- Mental overhead: Decision-making under pressure vs. strategic planning

---

## Learning

### Repository Planning Protocol (CHECK FIRST)

**Before creating ANY new agent, establish:**

1. **Location**: Local only | GitHub | GitLab | Other
2. **Visibility**: Private | Public
3. **Account**: Personal | Organization
4. **Name**: Exact repository name
5. **Timing**: Create remote now or after local development?

### Standard Questions Template

```yaml
Repository Planning:
  - Location: [Local only | GitHub | GitLab | Other]
  - Visibility: [Private | Public]
  - Account: [Personal | Organization]
  - Name: [Exact repository name]
  - URL: [Where it will live]
  - Create Now: [Y/N]
```

### Integration Planning Questions

- How does this relate to other repositories?
- Is it standalone or part of a monorepo?
- Will it be a submodule of something else?

---

## Protocol

```bash
# 1. Answer planning questions FIRST (before mkdir)
# Use template above - takes 2 minutes

# 2. Create remote repository if needed
gh repo create <name> --<public|private>

# 3. Clone or init with remote configured
git clone <url>
# OR
git init && git remote add origin <url>

# 4. Develop agent (now sign-off will work)
# All commits can be pushed when ready

# 5. Verify remote configured
git remote -v
```

---

## Anti-Patterns

❌ **Don't create agents without repository strategy**
- Creates sign-off failures and forced decision-making
- Wastes time with error cycles

❌ **Don't delay remote creation until sign-off**
- Wrong time to make strategic decisions
- Under pressure, suboptimal choices made

❌ **Don't assume "we'll figure it out later"**
- "Later" = worst time (after full development)
- 2 minutes now saves 15+ minutes later

✅ **Do answer 5 questions BEFORE mkdir**
- Strategic planning upfront
- Clear repository strategy from start

✅ **Do create remote early (or explicitly defer)**
- If deferring, document decision
- Know WHY you're waiting

✅ **Do document strategy in creation session**
- Capture decisions for future reference
- Clear audit trail

---

## Impact

**Before**:
- Sign-off waste: 6+ tool calls (error cycles)
- Decision-making: Under pressure after 5-8 hours work
- Error rate: 100% (if remote not created)
- Time cost: 10-15 minutes resolving

**After**:
- Planning overhead: 2 minutes (5 questions upfront)
- Sign-off: Smooth (remote already configured)
- Error rate: 0% (when protocol followed)
- Time cost: 2 minutes vs. 15 minutes (87% reduction)

**Metrics**:
- Planning overhead: 2 minutes (5 questions)
- Sign-off waste prevented: 6+ tool calls (error → decision → retry cycles)
- Error rate: 100% → 0% (when protocol followed)
- Time savings: 13 minutes per agent creation (87% reduction)

---

## Integration Points

**Where this applies**:
- Agent creation workflows (all AGETs)
- AGET template initialization
- Sign-off protocols (git push operations)
- Repository setup scripts

**Proposed enhancement to AGET template**:
```python
class AGETCreation:
    def plan_repository(self):
        """MUST happen before creating agent"""
        return {
            "strategy": input("New repo or existing? "),
            "platform": input("GitHub/GitLab/Local? "),
            "visibility": input("Public/Private? "),
            "account": input("Which account? "),
            "name": input("Repository name? "),
            "create_now": input("Create remote first? Y/N ")
        }
```

---

## Related Learnings

- L001: Agent Identity Awakening (identity established, needs repository home)
- [Future: L0XX on AGET creation workflow]
- [Future: L0XX on repository naming conventions]

---

**Generated**: 2025-10-26
**Session**: Learning Standardization Engagement - Checkpoint 2
**Migration**: 2025-09-25-LESSON-REPOSITORY-PLANNING.md → L003
