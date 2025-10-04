#!/usr/bin/env python3
"""
Collaboration Context Handoff Tool - v2.3 Gate A6

Serialize, sanitize, and transfer work context between AGETs.
Core mechanism for multi-agent collaboration.
"""

import argparse
import json
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ContextHandoff:
    """Handle collaboration context handoffs between AGETs."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.schema_path = self.project_root / ".aget/schemas/collaboration_context_v1.0.yaml"
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict:
        """Load collaboration context schema."""
        if not self.schema_path.exists():
            print(f"ERROR: Schema not found: {self.schema_path}")
            sys.exit(1)

        with open(self.schema_path, 'r') as f:
            return yaml.safe_load(f)

    def generate_task_id(self) -> str:
        """Generate unique task ID."""
        now = datetime.now()
        return f"task-{now.strftime('%Y%m%d-%H%M%S')}"

    def create_context(
        self,
        initiator: str,
        target: str,
        task_type: str,
        description: str,
        parameters: Dict[str, Any],
        objectives: Optional[list] = None,
        completion_criteria: Optional[list] = None,
        priority: str = "medium"
    ) -> Dict:
        """Create collaboration context."""
        context = {
            'task_id': self.generate_task_id(),
            'initiator': initiator,
            'target': target,
            'task_type': task_type,
            'shared_state': {
                'description': description,
                'parameters': parameters,
                'current_status': 'pending'
            },
            'priority': priority,
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'schema_version': '1.0.0'
            }
        }

        if objectives:
            context['objectives'] = objectives

        if completion_criteria:
            context['completion_criteria'] = completion_criteria

        return context

    def sanitize_context(self, context: Dict) -> Dict:
        """Sanitize context to remove sensitive information."""
        sanitized = context.copy()

        # Patterns to redact
        api_key_pattern = r'(api[_-]?key|token|secret)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})'
        password_pattern = r'(password|passwd|pwd)["\']?\s*[:=]\s*["\']?([^\s"\']+)'

        def redact_recursive(obj):
            """Recursively redact sensitive data."""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        # Redact API keys
                        if re.search(api_key_pattern, value, re.IGNORECASE):
                            obj[key] = "[REDACTED-API-KEY]"
                        # Redact passwords
                        elif re.search(password_pattern, value, re.IGNORECASE):
                            obj[key] = "[REDACTED-PASSWORD]"
                        # Redact absolute paths (keep relative)
                        elif value.startswith('/') and len(value) > 10:
                            parts = value.split('/')
                            if len(parts) > 3:
                                obj[key] = '.../' + '/'.join(parts[-2:])
                    elif isinstance(value, (dict, list)):
                        redact_recursive(value)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, str):
                        if re.search(api_key_pattern, item, re.IGNORECASE):
                            obj[i] = "[REDACTED-API-KEY]"
                        elif re.search(password_pattern, item, re.IGNORECASE):
                            obj[i] = "[REDACTED-PASSWORD]"
                    elif isinstance(item, (dict, list)):
                        redact_recursive(item)

        redact_recursive(sanitized)
        return sanitized

    def serialize_context(self, context: Dict, format: str = "json") -> str:
        """Serialize context to string."""
        sanitized = self.sanitize_context(context)

        if format == "json":
            return json.dumps(sanitized, indent=2)
        elif format == "yaml":
            return yaml.dump(sanitized, default_flow_style=False, sort_keys=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def deserialize_context(self, serialized: str, format: str = "json") -> Dict:
        """Deserialize context from string."""
        if format == "json":
            return json.loads(serialized)
        elif format == "yaml":
            return yaml.safe_load(serialized)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def validate_context(self, context: Dict) -> list:
        """Validate context against schema."""
        errors = []

        # Check required fields
        required = self.schema.get('required_fields', [])
        for field in required:
            if field not in context:
                errors.append(f"Missing required field: {field}")

        # Validate task_id format
        if 'task_id' in context:
            if not re.match(r'^task-\d{8}-\d{6}$', context['task_id']):
                errors.append(f"Invalid task_id format: {context['task_id']}")

        # Validate task_type
        if 'task_type' in context:
            valid_types = ["file_issue", "review_pr", "analyze_code", "generate_docs", "research", "other"]
            if context['task_type'] not in valid_types:
                errors.append(f"Invalid task_type: {context['task_type']}")

        # Validate priority
        if 'priority' in context:
            valid_priorities = ["low", "medium", "high", "critical"]
            if context['priority'] not in valid_priorities:
                errors.append(f"Invalid priority: {context['priority']}")

        # Check shared_state exists and has content
        if 'shared_state' in context:
            if not context['shared_state']:
                errors.append("shared_state cannot be empty")
            elif not isinstance(context['shared_state'], dict):
                errors.append("shared_state must be object")

        return errors

    def save_context(self, context: Dict, filepath: Path):
        """Save context to file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(context, f, indent=2)

    def load_context(self, filepath: Path) -> Dict:
        """Load context from file."""
        if not filepath.exists():
            raise FileNotFoundError(f"Context file not found: {filepath}")

        with open(filepath, 'r') as f:
            return json.load(f)

    def handoff(
        self,
        context: Dict,
        output_file: Optional[Path] = None
    ) -> bool:
        """Perform handoff (serialize and optionally save)."""
        # Validate
        errors = self.validate_context(context)
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"  ❌ {error}")
            return False

        # Sanitize and serialize
        serialized = self.serialize_context(context, format="json")

        # Save if output file specified
        if output_file:
            self.save_context(context, output_file)
            print(f"✅ Context saved to {output_file}")

        # Print serialized context
        print("\nSerialized Context:")
        print("=" * 70)
        print(serialized)
        print("=" * 70)

        return True


def main():
    """Run context handoff tool."""
    parser = argparse.ArgumentParser(
        description="Create and handoff collaboration context"
    )
    parser.add_argument(
        '--initiator',
        required=True,
        help='Initiating AGET'
    )
    parser.add_argument(
        '--target',
        required=True,
        help='Target AGET'
    )
    parser.add_argument(
        '--task-type',
        required=True,
        choices=['file_issue', 'review_pr', 'analyze_code', 'generate_docs', 'research', 'other'],
        help='Type of task'
    )
    parser.add_argument(
        '--description',
        required=True,
        help='Task description'
    )
    parser.add_argument(
        '--params',
        type=str,
        help='Task parameters (JSON string)'
    )
    parser.add_argument(
        '--objectives',
        nargs='+',
        help='Task objectives'
    )
    parser.add_argument(
        '--completion',
        nargs='+',
        help='Completion criteria'
    )
    parser.add_argument(
        '--priority',
        choices=['low', 'medium', 'high', 'critical'],
        default='medium',
        help='Task priority'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Save context to file'
    )
    parser.add_argument(
        '--validate-only',
        type=Path,
        help='Validate existing context file'
    )

    args = parser.parse_args()

    handoff = ContextHandoff()

    if args.validate_only:
        # Validate existing file
        try:
            context = handoff.load_context(args.validate_only)
            errors = handoff.validate_context(context)

            if errors:
                print("❌ Validation failed:")
                for error in errors:
                    print(f"  {error}")
                sys.exit(1)
            else:
                print("✅ Context is valid")
                sys.exit(0)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    # Create context
    parameters = {}
    if args.params:
        try:
            parameters = json.loads(args.params)
        except json.JSONDecodeError:
            print("ERROR: Invalid JSON in --params")
            sys.exit(1)

    context = handoff.create_context(
        initiator=args.initiator,
        target=args.target,
        task_type=args.task_type,
        description=args.description,
        parameters=parameters,
        objectives=args.objectives,
        completion_criteria=args.completion,
        priority=args.priority
    )

    # Perform handoff
    success = handoff.handoff(context, output_file=args.output)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
