#!/usr/bin/env python3
"""
Handoff Receiver - Process incoming collaboration requests

Monitors .aget/coordination/ for handoff requests and processes them.
DeepResearch AGET implementation for v2.3 collaboration.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class HandoffReceiver:
    """Process incoming handoff requests for Deep Research tasks."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.coordination_dir = self.project_root / ".aget/coordination"
        self.coordination_dir.mkdir(parents=True, exist_ok=True)

    def list_pending_handoffs(self) -> list:
        """List all pending handoff requests."""
        if not self.coordination_dir.exists():
            return []

        handoff_files = list(self.coordination_dir.glob("*handoff*.json"))
        pending = []

        for file in handoff_files:
            try:
                with open(file, 'r') as f:
                    context = json.load(f)
                    if context.get('shared_state', {}).get('current_status') == 'pending':
                        pending.append({
                            'file': file,
                            'context': context
                        })
            except Exception as e:
                print(f"Warning: Could not read {file}: {e}")

        return pending

    def load_handoff(self, filepath: Path) -> Dict:
        """Load handoff context from file."""
        if not filepath.exists():
            raise FileNotFoundError(f"Handoff file not found: {filepath}")

        with open(filepath, 'r') as f:
            return json.load(f)

    def validate_handoff(self, context: Dict) -> tuple[bool, list]:
        """Validate handoff is intended for this AGET."""
        errors = []

        # Check target
        target = context.get('target')
        if target != 'my-OpenAI-DeepResearch-aget':
            errors.append(f"Handoff target mismatch: {target}")

        # Check task type
        task_type = context.get('task_type')
        valid_types = ['research', 'analyze_code', 'generate_docs']
        if task_type not in valid_types:
            errors.append(f"Unsupported task type: {task_type}")

        # Check required fields
        required = ['task_id', 'initiator', 'shared_state']
        for field in required:
            if field not in context:
                errors.append(f"Missing required field: {field}")

        return (len(errors) == 0, errors)

    def extract_research_params(self, context: Dict) -> Dict[str, Any]:
        """Extract research parameters from handoff context."""
        shared_state = context.get('shared_state', {})
        parameters = shared_state.get('parameters', {})

        return {
            'task_id': context.get('task_id'),
            'description': shared_state.get('description'),
            'urls': parameters.get('urls', []),
            'questions': parameters.get('questions', []),
            'topics': parameters.get('topics', []),
            'depth': parameters.get('depth', 'standard'),
            'output_file': parameters.get('output_file'),
            'objectives': context.get('objectives', []),
            'completion_criteria': context.get('completion_criteria', [])
        }

    def update_handoff_status(self, filepath: Path, status: str, result: Optional[Dict] = None):
        """Update handoff status."""
        context = self.load_handoff(filepath)
        context['shared_state']['current_status'] = status

        if result:
            context['shared_state']['result'] = result

        context['metadata'] = context.get('metadata', {})
        context['metadata']['updated_at'] = datetime.now().isoformat()

        with open(filepath, 'w') as f:
            json.dump(context, f, indent=2)

    def process_research_handoff(self, context: Dict, filepath: Path) -> bool:
        """Process a research handoff request."""
        print(f"Processing research handoff: {context.get('task_id')}")

        # Extract parameters
        params = self.extract_research_params(context)

        print("\nResearch Parameters:")
        print(f"  Description: {params['description']}")
        print(f"  URLs: {len(params['urls'])} provided")
        print(f"  Questions: {len(params['questions'])} questions")
        print(f"  Output file: {params['output_file']}")
        print(f"  Depth: {params['depth']}")

        # Update status to in_progress
        self.update_handoff_status(filepath, 'in_progress')

        print("\n" + "=" * 70)
        print("HANDOFF RECEIVED - Ready for manual processing")
        print("=" * 70)
        print("\nNext Steps:")
        print("1. Review the research parameters above")
        print("2. Execute the research task manually")
        print(f"3. Write results to: {params['output_file']}")
        print("4. Update handoff status to 'completed'")
        print(f"\nHandoff file: {filepath}")
        print("=" * 70)

        return True

    def process_handoff(self, filepath: Path) -> bool:
        """Process a handoff request."""
        try:
            # Load context
            context = self.load_handoff(filepath)

            # Validate
            valid, errors = self.validate_handoff(context)
            if not valid:
                print("❌ Handoff validation failed:")
                for error in errors:
                    print(f"  {error}")
                self.update_handoff_status(filepath, 'failed', {'errors': errors})
                return False

            # Process based on task type
            task_type = context.get('task_type')

            if task_type == 'research':
                return self.process_research_handoff(context, filepath)
            else:
                print(f"❌ Unsupported task type: {task_type}")
                return False

        except Exception as e:
            print(f"❌ Error processing handoff: {e}")
            return False


def main():
    """Run handoff receiver."""
    parser = argparse.ArgumentParser(
        description="Process incoming handoff requests"
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List pending handoffs'
    )
    parser.add_argument(
        '--process',
        type=Path,
        help='Process specific handoff file'
    )
    parser.add_argument(
        '--process-next',
        action='store_true',
        help='Process next pending handoff'
    )

    args = parser.parse_args()

    receiver = HandoffReceiver()

    if args.list:
        pending = receiver.list_pending_handoffs()
        if not pending:
            print("No pending handoffs")
        else:
            print(f"Pending handoffs: {len(pending)}\n")
            for item in pending:
                context = item['context']
                print(f"  Task ID: {context.get('task_id')}")
                print(f"  From: {context.get('initiator')}")
                print(f"  Type: {context.get('task_type')}")
                print(f"  File: {item['file']}")
                print()

    elif args.process:
        success = receiver.process_handoff(args.process)
        sys.exit(0 if success else 1)

    elif args.process_next:
        pending = receiver.list_pending_handoffs()
        if not pending:
            print("No pending handoffs")
            sys.exit(0)

        # Process first pending
        item = pending[0]
        success = receiver.process_handoff(item['file'])
        sys.exit(0 if success else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
