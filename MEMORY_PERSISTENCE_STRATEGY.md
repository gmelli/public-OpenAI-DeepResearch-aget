# Memory Persistence Strategy for DeepThink

## Directory Structure Decision

### Chosen Approach: Hybrid Strategy
```
OpenAI-DeepResearch-aget/
├── .aget/
│   ├── memory/              # Framework metadata & patterns (backed up)
│   │   ├── patterns.json    # Learned routing patterns
│   │   ├── thresholds.json  # Dynamic threshold adjustments
│   │   └── registry.json    # Cross-AGET discovery data
│   └── checkpoints/         # Full state snapshots
│
└── workspace/
    └── memory/              # Working memory & cache (volatile)
        ├── cache/           # Query result cache (can be cleared)
        ├── sessions/        # Session-specific memory
        └── temp/            # Temporary processing

```

## Rationale

### .aget/memory/ - Persistent Framework Memory
**What Goes Here**: Critical learning that improves the agent
- Routing patterns that have proven successful
- Threshold adjustments from learning loops
- Cross-AGET integration configurations
- Quality baselines and benchmarks

**Backup Strategy**:
- Daily snapshots to .aget/checkpoints/
- Git commit after significant learning events
- Export to products/ as "memory-export-YYYY-MM-DD.json"

### workspace/memory/ - Volatile Working Memory
**What Goes Here**: Operational data that can be regenerated
- Result cache (expensive but reproducible)
- Session-specific working memory
- Temporary analysis results
- In-progress learning before validation

**Cleanup Strategy**:
- Cache entries expire after TTL (default 3600s)
- Session memory cleared after 24 hours
- Temp cleared on each wake-up

## Implementation

### Memory Manager
```python
# src/core/memory_manager.py
from pathlib import Path
import json
import shutil
from datetime import datetime

class MemoryManager:
    """Manages hybrid memory persistence"""

    def __init__(self):
        # Persistent memory (backed up)
        self.persistent_dir = Path(".aget/memory")
        self.persistent_dir.mkdir(parents=True, exist_ok=True)

        # Volatile memory (can be cleared)
        self.volatile_dir = Path("workspace/memory")
        self.volatile_dir.mkdir(parents=True, exist_ok=True)

        self.load_memories()

    def save_pattern(self, pattern):
        """Save learned pattern to persistent memory"""
        patterns_file = self.persistent_dir / "patterns.json"

        patterns = self.load_json(patterns_file, default=[])
        patterns.append(pattern)

        self.save_json(patterns_file, patterns)
        self.trigger_backup("pattern_learned")

    def cache_result(self, key, value):
        """Cache result in volatile memory"""
        cache_file = self.volatile_dir / "cache" / f"{key}.json"
        cache_file.parent.mkdir(exist_ok=True)

        self.save_json(cache_file, {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "hits": 0
        })

    def promote_to_persistent(self, data, reason):
        """Promote valuable volatile data to persistent"""
        if self.validate_for_promotion(data):
            persistent_file = self.persistent_dir / f"promoted_{datetime.now():%Y%m%d_%H%M%S}.json"
            self.save_json(persistent_file, {
                "data": data,
                "reason": reason,
                "promoted_at": datetime.now().isoformat()
            })
            self.trigger_backup(f"promotion: {reason}")

    def trigger_backup(self, reason):
        """Trigger checkpoint creation"""
        checkpoint_dir = Path(".aget/checkpoints")
        checkpoint_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_path = checkpoint_dir / f"memory_{timestamp}.tar.gz"

        # Create compressed backup
        shutil.make_archive(
            checkpoint_path.stem,
            'gztar',
            self.persistent_dir
        )

        # Log backup event
        self.log_backup(checkpoint_path, reason)

    def cleanup_volatile(self, max_age_hours=24):
        """Clean old volatile memory"""
        cleaned = 0
        for cache_file in (self.volatile_dir / "cache").glob("*.json"):
            data = self.load_json(cache_file)
            age = datetime.now() - datetime.fromisoformat(data["timestamp"])

            if age.total_seconds() > max_age_hours * 3600:
                cache_file.unlink()
                cleaned += 1

        return cleaned
```

### Backup Schedule
```python
# src/core/backup_scheduler.py

class BackupScheduler:
    """Automated backup scheduling"""

    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.schedule = {
            "hourly": self.incremental_backup,
            "daily": self.full_backup,
            "on_shutdown": self.emergency_backup
        }

    def incremental_backup(self):
        """Backup only changes since last backup"""
        changes = self.detect_changes()
        if changes:
            self.memory.trigger_backup("incremental")

    def full_backup(self):
        """Complete memory backup"""
        self.memory.trigger_backup("daily_full")
        self.prune_old_backups(keep_last=7)

    def emergency_backup(self):
        """Backup on unexpected shutdown"""
        self.memory.trigger_backup("emergency")
```

## Memory Lifecycle

### 1. Initial Learning (Volatile)
```
workspace/memory/sessions/current.json
→ Pattern emerges
→ Validation passes
```

### 2. Pattern Validation (Promotion)
```
→ Pattern proves valuable (3+ successes)
→ Promote to .aget/memory/patterns.json
→ Trigger backup
```

### 3. Long-term Storage (Persistent)
```
.aget/memory/patterns.json
→ Daily backup to checkpoints/
→ Git commit on significant changes
```

### 4. Recovery (Restore)
```
On startup:
1. Load .aget/memory/* (persistent)
2. Check workspace/memory/* (volatile)
3. Merge and deduplicate
4. Clean expired volatile entries
```

## Decision Tree for Memory Placement

```
Is this data critical for agent improvement?
├─ Yes → .aget/memory/ (persistent)
│   ├─ Routing patterns
│   ├─ Quality thresholds
│   └─ Integration configs
│
└─ No → workspace/memory/ (volatile)
    ├─ Result cache
    ├─ Session data
    └─ Temporary analysis
```

## Git Integration

### .gitignore Configuration
```gitignore
# Volatile memory (not tracked)
workspace/memory/cache/
workspace/memory/temp/
workspace/memory/sessions/

# Persistent memory (tracked)
# .aget/memory/ is tracked
# .aget/checkpoints/ is tracked (with LFS for large files)

# Large checkpoint files use Git LFS
*.tar.gz filter=lfs diff=lfs merge=lfs -text
```

### Commit Triggers
```python
def should_commit_memory():
    """Determine if memory changes warrant a git commit"""
    triggers = [
        patterns_changed > 5,
        new_integration_added,
        threshold_adjustment > 0.1,
        quality_baseline_updated
    ]
    return any(triggers)
```

## Benefits of This Approach

1. **Clear Boundaries**: Framework learning vs operational cache
2. **Backup Safety**: Critical memories are protected
3. **Performance**: Volatile cache can be aggressively optimized
4. **Git-Friendly**: Only important changes create commits
5. **Recovery**: Can restore from checkpoints after crashes
6. **Cleanup**: Volatile memory can be purged without data loss

---
*Memory Persistence Strategy v1.0*
*DeepThink AGET*