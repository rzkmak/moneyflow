---
description: Start a new feature with spec-kit
---

# Start New Feature Workflow

This workflow guides you through starting a new feature using spec-kit for structured specification documentation.

## Steps

1. **Create a new feature branch**
   
   Follow the naming convention: `00X-feature-name`
   
   ```bash
   git checkout -b 004-feature-name
   ```

2. **Use spec-kit to generate specifications**
   
   Run spec-kit commands to create structured specification documents:
   - `spec.md` - Feature requirements and user stories
   - `plan.md` - Implementation plan and phases
   - `tasks.md` - Detailed task breakdown
   - `data-model.md` - Database schema and models
   - `completion-checklist.md` - Verification criteria

3. **Review generated specifications**
   
   Verify completeness and quality:
   - [ ] User requirements clearly defined
   - [ ] Technical approach documented
   - [ ] Data models specified
   - [ ] Testing strategy outlined
   - [ ] Acceptance criteria listed

4. **Check against project constitution**
   
   Ensure compliance with project principles:
   ```bash
   cat .specify/memory/constitution.md
   ```

5. **Update documentation**
   
   Run the notification script to update project documentation:
   ```bash
   make notify-spec
   ```
   
   This will update:
   - `README.md` with new feature reference
   - `ANTIGRAVITY.md` with specification details
   - `CLAUDE.md` with implementation guidance

6. **Hand off to Claude for implementation**
   
   Generate the handoff prompt:
   ```bash
   make handoff-to-claude
   ```
   
   Copy the generated prompt and paste it into Claude Code to begin implementation.

## Notes

- Always work on a feature branch, never directly on `master`
- Ensure spec-kit generates all required documentation files
- Review specifications thoroughly before handing off to Claude
- Keep the constitution principles in mind throughout planning
