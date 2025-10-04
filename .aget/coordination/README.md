# Coordination Directory

**Purpose:** Inter-AGET collaboration handoff requests

This directory receives collaboration requests from other AGETs in the ecosystem. When another AGET needs Deep Research capabilities, they create a handoff JSON file here.

## Structure

```
.aget/coordination/
├── README.md                          # This file
├── handoff_<target>_<task>.json      # Active handoff requests
└── EXAMPLE_handoff.json               # Example handoff structure
```

## Handoff Protocol

### Receiving Handoffs

**1. Check for pending handoffs:**
```bash
python3 .aget/tools/handoff_receiver.py --list
```

**2. Process next pending handoff:**
```bash
python3 .aget/tools/handoff_receiver.py --process-next
```

**3. Process specific handoff:**
```bash
python3 .aget/tools/handoff_receiver.py --process .aget/coordination/handoff_deepresearch_task.json
```

### Creating Handoffs (to other AGETs)

```bash
python3 .aget/tools/handoff_context.py \
  --initiator my-OpenAI-DeepResearch-aget \
  --target my-GITHUB-aget \
  --task-type file_issue \
  --description "File issue about X" \
  --params '{"title": "Issue title", "body": "Issue body"}' \
  --objectives "Create issue" \
  --completion "Issue filed" \
  --priority high \
  --output ~/github/my-GITHUB-aget/.aget/coordination/handoff_issue_X.json
```

## Supported Task Types

### Research (Primary Capability)
DeepResearch AGET specializes in comprehensive research tasks.

**Parameters:**
- `urls`: List of URLs to analyze
- `questions`: Research questions to answer
- `topics`: Topics to investigate
- `depth`: Research depth (quick|standard|comprehensive)
- `output_file`: Where to write results

**Example:**
```json
{
  "task_type": "research",
  "shared_state": {
    "description": "Research agent communication protocols",
    "parameters": {
      "urls": ["https://example.com/doc"],
      "questions": ["What are best practices?"],
      "depth": "comprehensive",
      "output_file": "workspace/research_results.md"
    }
  }
}
```

### Analyze Code (Secondary Capability)
Code analysis and architecture review.

**Parameters:**
- `files`: Files to analyze
- `focus`: Analysis focus area
- `output_file`: Where to write analysis

### Generate Docs (Secondary Capability)
Documentation generation from research findings.

**Parameters:**
- `source_files`: Source material
- `doc_type`: Type of documentation
- `output_file`: Where to write docs

## Handoff Lifecycle

```
1. Initiator creates handoff JSON
2. Places in target's .aget/coordination/
3. Target lists pending handoffs
4. Target processes handoff (status: pending → in_progress)
5. Target completes work
6. Target updates handoff (status: in_progress → completed)
7. Target adds results to handoff JSON
```

## Status Values

- `pending`: Awaiting processing
- `in_progress`: Currently being worked on
- `blocked`: Waiting for dependencies
- `completed`: Successfully finished
- `failed`: Could not complete

## Security

Handoff contexts are automatically sanitized:
- API keys redacted
- Passwords redacted
- Absolute paths converted to relative
- Sensitive parameters removed

See: `.aget/schemas/collaboration_context_v1.0.yaml`

## Integration with AGENTS.md

Wake up protocol checks for pending handoffs:
```
wake up → check coordination/ → process pending → report ready
```

Wind down protocol updates handoff status:
```
wind down → complete handoff → update status → commit
```

## Troubleshooting

**No handoffs appearing:**
- Check directory exists: `ls -la .aget/coordination/`
- Check permissions: Should be readable/writable

**Validation errors:**
- Verify handoff has required fields (task_id, initiator, target, task_type, shared_state)
- Check task_type is supported (research, analyze_code, generate_docs)
- Validate target matches this AGET name

**Processing fails:**
- Check handoff_receiver.py is executable
- Verify collaboration schema exists: `.aget/schemas/collaboration_context_v1.0.yaml`
- Review error messages in handoff JSON result field

---

**Version:** 1.0.0 (v2.3)
**Created:** 2025-10-02
**Part of:** Wave 4 Collaboration Infrastructure
