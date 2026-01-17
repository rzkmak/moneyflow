---
description: Review spec-kit generated specifications
---

# Review Specification Workflow

This workflow guides you through reviewing spec-kit generated specifications for completeness and quality.

## Steps

1. **Locate the latest spec directory**
   
   ```bash
   ls -la specs/
   ```
   
   Or find the most recent:
   ```bash
   find specs -maxdepth 1 -type d -name '[0-9]*' | sort -V | tail -1
   ```

2. **Review key specification files**
   
   Read each file in order:
   
   - **spec.md** - Feature requirements and user stories
   - **plan.md** - Implementation plan with phases
   - **tasks.md** - Detailed task breakdown
   - **data-model.md** - Database schema and entity relationships

3. **Verify against constitution**
   
   Check project principles:
   ```bash
   cat .specify/memory/constitution.md
   ```
   
   Ensure the specification complies with:
   - Architectural principles
   - Technology constraints
   - Development standards
   - Quality requirements

4. **Validate completeness**
   
   Use this checklist:
   
   - [ ] **User requirements** clearly defined with acceptance criteria
   - [ ] **Technical approach** documented with rationale
   - [ ] **Data models** specified with relationships and constraints
   - [ ] **Testing strategy** outlined with test cases
   - [ ] **Acceptance criteria** listed and measurable
   - [ ] **Dependencies** identified (libraries, APIs, services)
   - [ ] **Migration plan** included if database changes required
   - [ ] **Rollback strategy** defined for risky changes

5. **Check for potential issues**
   
   Look for:
   - Ambiguous requirements
   - Missing edge cases
   - Unclear acceptance criteria
   - Incomplete data models
   - Missing error handling scenarios
   - Performance considerations
   - Security implications

6. **Provide feedback or approval**
   
   If issues found:
   - Document specific concerns
   - Suggest improvements
   - Request clarification
   
   If approved:
   - Proceed to implementation handoff
   - Run `make handoff-to-claude`

## Quality Criteria

A good specification should:
- Be **clear** and unambiguous
- Be **complete** with all necessary details
- Be **consistent** with project principles
- Be **testable** with measurable criteria
- Be **implementable** by Claude Code

## Notes

- Take time to review thoroughly - good specs lead to good implementations
- Don't hesitate to ask for clarification or improvements
- Consider edge cases and error scenarios
- Think about testing and verification upfront
