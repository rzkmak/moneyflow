---
description: Verify Claude's implementation
---

# Verify Implementation Workflow

This workflow guides you through verifying Claude Code's implementation against the specification.

## Steps

1. **Review implemented code**
   
   Check the changes made by Claude:
   
   **Backend changes:**
   ```bash
   git diff master -- backend/
   ```
   
   **Frontend changes:**
   ```bash
   git diff master -- frontend/
   ```
   
   Verify against specification:
   - [ ] All required features implemented
   - [ ] Code follows project structure
   - [ ] Error handling included
   - [ ] Edge cases covered

2. **Run tests**
   
   Execute the test suite:
   ```bash
   make test
   ```
   
   Check for:
   - [ ] All tests passing
   - [ ] New tests added for new features
   - [ ] Test coverage adequate
   - [ ] No regressions in existing functionality

3. **Start development servers**
   
   Launch both backend and frontend:
   ```bash
   make start
   ```
   
   Wait for servers to be ready:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

4. **Manual verification**
   
   Test all user flows:
   - [ ] Navigate through key pages
   - [ ] Test new features
   - [ ] Verify existing features still work
   - [ ] Check error handling
   - [ ] Test edge cases
   - [ ] Verify data persistence

5. **Check against acceptance criteria**
   
   Review the specification's acceptance criteria:
   ```bash
   cat specs/00X-feature-name/spec.md | grep -A 20 "Acceptance Criteria"
   ```
   
   Verify each criterion is met.

6. **Update documentation**
   
   Update project documentation:
   
   - **ANTIGRAVITY.md**: Update feature status to complete
   - **README.md**: Update if new features affect user-facing documentation
   - **Specification**: Document any deviations from original plan

7. **Create pull request for review**
   
   If verification passes:
   ```bash
   git add .
   git commit -m "feat: implement [feature-name]"
   git push origin [branch-name]
   ```
   
   Create PR with:
   - Description of changes
   - Link to specification
   - Verification results
   - Screenshots (if UI changes)

## Verification Checklist

- [ ] Code review completed
- [ ] All tests passing
- [ ] Manual testing completed
- [ ] Acceptance criteria met
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] Ready for PR

## Notes

- Don't skip manual testing even if automated tests pass
- Test on different browsers if UI changes were made
- Verify database migrations if schema changed
- Check for console errors in browser
- Test with realistic data volumes
