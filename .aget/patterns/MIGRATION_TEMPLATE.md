# Pattern Migration Guide Template

**Pattern:** {PATTERN_NAME}
**From Version:** {OLD_VERSION}
**To Version:** {NEW_VERSION}
**Migration Date:** {DATE}
**Breaking Changes:** {YES/NO}

---

## Summary

Brief description of what changed and why migration is needed.

## Breaking Changes

List all breaking changes in this version:

1. **Change 1**: Description
   - **Impact**: What breaks
   - **Migration**: How to fix

2. **Change 2**: Description
   - **Impact**: What breaks
   - **Migration**: How to fix

## New Features (Backward Compatible)

List new features that don't require migration:

- Feature 1
- Feature 2

## Deprecations

List deprecated features (to be removed in future versions):

- Deprecated 1: Use alternative X instead
- Deprecated 2: Use alternative Y instead

## Migration Steps

### Step 1: Pre-migration Check

```bash
# Check current pattern version
python3 .aget/tools/bump_pattern.py {PATTERN_NAME} --show

# Check compatibility
python3 .aget/tools/check_pattern_compatibility.py
```

### Step 2: Backup Current State

```bash
# Backup pattern files
cp .aget/patterns/{PATTERN_FILE} .aget/patterns/{PATTERN_FILE}.backup

# Commit current state
git add .
git commit -m "backup: Pre-migration state for {PATTERN_NAME}"
```

### Step 3: Update Pattern Code

Detailed code changes required:

**File:** .aget/patterns/{PATTERN_FILE}

**Old code:**
```python
# Old implementation
```

**New code:**
```python
# New implementation
```

### Step 4: Update Pattern Version

```bash
# Bump pattern version
python3 .aget/tools/bump_pattern.py {PATTERN_NAME} --{major/minor/patch}
```

### Step 5: Test Migration

```bash
# Run pattern tests
# Add specific test commands here

# Verify compatibility
python3 .aget/tools/check_pattern_compatibility.py
```

### Step 6: Deploy to AGETs

```bash
# Deploy to specific AGET
# Add deployment commands here

# Or broadcast to all AGETs
python3 .aget/patterns/routing/broadcast_upgrade.py {PATTERN_NAME}
```

## Rollback Procedure

If migration fails:

```bash
# Restore backup
cp .aget/patterns/{PATTERN_FILE}.backup .aget/patterns/{PATTERN_FILE}

# Revert version
git checkout HEAD~1 .aget/patterns/versions.yaml

# Verify rollback
python3 .aget/tools/check_pattern_compatibility.py
```

## Testing Checklist

- [ ] Pattern loads without errors
- [ ] All existing functionality works
- [ ] New features work as documented
- [ ] Backward compatibility preserved (if minor/patch)
- [ ] No dependency conflicts
- [ ] Documentation updated
- [ ] Tests pass

## Timeline

- **Preparation:** X days
- **Migration:** Y days
- **Testing:** Z days
- **Rollout:** W days

**Total:** N days

## Support

Questions or issues with this migration?

- File issue: [Link to GitHub issues]
- Check documentation: [Link to docs]
- Review pattern: .aget/patterns/{PATTERN_FILE}

---

*Generated from MIGRATION_TEMPLATE.md*
*Last updated: 2025-10-02*
