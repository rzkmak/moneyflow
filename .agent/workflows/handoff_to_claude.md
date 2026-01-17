---
description: Hand off implementation to Claude Code
---

# Handoff to Claude Code Workflow

This workflow generates a handoff prompt for Claude Code to begin implementation based on approved specifications.

## Steps

// turbo
1. **Generate handoff prompt**
   
   ```bash
   make handoff-to-claude
   ```
   
   This script will:
   - Find the latest specification directory
   - Generate a structured prompt for Claude
   - Include references to all relevant specification files

2. **Copy the generated prompt**
   
   The script outputs a prompt that includes:
   - Path to the implementation plan (`plan.md`)
   - Reference to feature specification (`spec.md`)
   - Reference to data model (`data-model.md`)
   - Reference to project guidelines (`CLAUDE.md`)

3. **Open Claude Code**
   
   Navigate to Claude Code interface (claude.ai/code)

4. **Paste the prompt**
   
   Paste the generated prompt into Claude Code to start the implementation session.

5. **Claude will follow its protocol**
   
   Claude Code will:
   - Review the specification documents
   - Create a detailed implementation plan
   - Request your approval before proceeding
   - Implement with explicit permission for each step
   - Follow the development protocol in `CLAUDE.md`

6. **Monitor implementation progress**
   
   Stay engaged during implementation:
   - Review Claude's implementation plan
   - Approve or request changes
   - Monitor code changes
   - Test incrementally if possible

7. **When complete, verify implementation**
   
   Use Antigravity to verify:
   - Run `/verify-implementation` workflow
   - Run `/verify-ui` workflow for UI changes

## Example Handoff Prompt

```
Please implement the feature described in 'specs/003-feature-name/plan.md'.

Strictly follow the phases and steps outlined in the plan.

Refer to:
- 'specs/003-feature-name/spec.md' for user requirements
- 'specs/003-feature-name/data-model.md' for schema details
- 'CLAUDE.md' for project guidelines and development protocol

Adhere to the project guidelines and request approval before executing any commands or making changes.
```

## Notes

- Always review the generated prompt before sending to Claude
- Ensure all specification files are complete before handoff
- Claude follows a strict protocol: plan → approval → implementation
- Stay engaged during implementation for best results
- Use Antigravity for verification after Claude completes work
