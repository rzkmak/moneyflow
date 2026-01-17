---
description: Catch up with current project specifications
---

# Sync with Specifications Workflow

This workflow helps Antigravity catch up with the current state of specifications when starting a new session or reviewing existing work.

## Purpose

When you start a new Antigravity session, use this workflow to:
- Understand the current project state
- Review what's been implemented vs. what's pending
- Identify any deviations from specifications
- Get context for providing assistance

## Steps

// turbo
1. **List all specification directories**
   
   ```bash
   find specs -maxdepth 1 -type d -name '[0-9]*' | sort -V
   ```

2. **Identify the latest or target specification**
   
   For the latest spec:
   ```bash
   find specs -maxdepth 1 -type d -name '[0-9]*' | sort -V | tail -1
   ```
   
   Or specify manually, e.g., `specs/002-visualization-and-categorization`

3. **Review specification files in order**
   
   For each spec directory, review these files:
   - `README.md` - Overview and context
   - `spec.md` - Detailed requirements and user stories
   - `data-model.md` - Database schema and models
   - `plan.md` - Implementation plan and phases
   - `tasks.md` - Task breakdown and checklist
   - `completion-checklist.md` - Verification status

4. **Check implementation status**
   
   - Review `ANTIGRAVITY.md` for feature status updates
   - Check current git branch:
     ```bash
     git branch --show-current
     ```
   - Review recent commits related to the spec:
     ```bash
     git log --oneline --grep="002" -10
     ```

5. **Verify against constitution**
   
   Read the project constitution to understand core principles:
   ```bash
   cat .specify/memory/constitution.md
   ```
   
   Ensure specifications comply with project principles.

6. **Summarize findings**
   
   Create a summary including:
   - **Implemented**: What features have been completed
   - **Pending**: What tasks remain
   - **Deviations**: Any changes from the original plan
   - **Next steps**: Recommended actions

7. **Update context as needed**
   
   If necessary, update `ANTIGRAVITY.md` with current status information.

## Example Usage

```bash
# Quick sync with latest spec
LATEST_SPEC=$(find specs -maxdepth 1 -type d -name '[0-9]*' | sort -V | tail -1)
echo "Syncing with: $LATEST_SPEC"
cat "$LATEST_SPEC/README.md"
cat "$LATEST_SPEC/spec.md"
```

## Notes

- Run this workflow at the start of each Antigravity session
- Use it when switching between different features
- Helpful for understanding project history and decisions
