# SOP: Escalation Protocol

**Version**: 1.0
**Status**: ACTIVE
**Created**: 2026-01-18
**Agent**: private-supervisor-AGET

---

## Purpose

Define when and how to escalate decisions, blockers, or issues beyond this agent's authority.

## Scope

This SOP applies to all operational situations where:
- A decision exceeds the agent's authority level
- A blocker cannot be resolved within the agent's capabilities
- Principal input is required before proceeding

## Escalation Triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| Authority Exceeded | Decision requires approval beyond agent scope | Escalate to principal |
| Blocked | Cannot proceed without external input | Document blocker, notify principal |
| Uncertainty | Ambiguous requirements or conflicting guidance | Request clarification |
| Risk | Action could have irreversible consequences | Escalate before execution |
| Fleet Impact | Change affects multiple agents | Escalate to principal |

## Escalation Procedure

### Step 1: Document the Situation

Before escalating, document:
- [ ] What decision/blocker/issue requires escalation
- [ ] Why it exceeds current authority
- [ ] Options considered (if any)
- [ ] Recommended action (if any)
- [ ] Impact of delay

### Step 2: Identify Escalation Target

| Escalation Type | Target |
|-----------------|--------|
| Operational decision | Principal |
| Technical blocker | Principal or domain expert |
| Governance question | Framework owner (private-aget-framework-AGET) |
| Emergency | Principal (direct) |
| Fleet-wide impact | Principal with framework notification |

### Step 3: Escalate

1. Create escalation record in planning/ or sessions/
2. Clearly state the escalation reason
3. Provide sufficient context for decision-maker
4. Wait for response before proceeding

### Step 4: Document Resolution

After escalation is resolved:
- [ ] Document decision received
- [ ] Record any learnings for future reference
- [ ] Update relevant L-docs if pattern emerges

## Anti-Patterns

| Anti-Pattern | Description | Consequence |
|--------------|-------------|-------------|
| Silent Assumption | Proceeding without escalating ambiguity | Wrong direction, rework |
| Over-Escalation | Escalating routine decisions | Decision fatigue, bottleneck |
| Escalation without Context | Escalating without sufficient information | Delays, back-and-forth |
| Fleet Changes without Notice | Deploying to fleet without principal awareness | Governance violation |

## Related Documents

- governance/CHARTER.md — Agent authority boundaries
- governance/SCOPE_BOUNDARIES.md — Operational scope
- .aget/reasoning/decision_authority.yaml — Decision authority matrix

---

*SOP: Escalation Protocol v1.0*
*Agent: private-supervisor-AGET*
