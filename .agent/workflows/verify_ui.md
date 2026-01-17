---
description: Verify UI changes using browser agent
---

# Verify UI Changes Workflow

This workflow uses Antigravity's browser capabilities to verify UI implementations visually and functionally.

## Purpose

After Claude implements UI changes, use this workflow to:
- Verify visual design and layout
- Test user interactions and flows
- Capture screenshots for documentation
- Identify UI/UX issues
- Create visual verification reports

## Steps

// turbo
1. **Start development servers**
   
   ```bash
   make start
   ```
   
   Wait for servers to be ready:
   - Backend: http://localhost:8000 (API)
   - Frontend: http://localhost:5173 (UI)

2. **Wait for servers to be ready**
   
   Give servers time to start (usually 5-10 seconds).
   Check backend health:
   ```bash
   curl http://localhost:8000/docs
   ```

3. **Open the application in browser**
   
   Navigate to: http://localhost:5173
   
   Take initial screenshot for reference.

4. **Test user flows according to specification**
   
   Navigate through key pages and test:
   
   - [ ] **Navigation**: All menu items and links work
   - [ ] **Interactive elements**: Buttons, dropdowns, modals
   - [ ] **Responsive design**: Mobile, tablet, desktop views
   - [ ] **Error states**: Invalid inputs, network errors
   - [ ] **Form submissions**: Data validation and submission
   - [ ] **Loading states**: Spinners, skeleton screens

5. **Verify visual design**
   
   Check design consistency:
   
   - [ ] **Color scheme**: Matches design system
   - [ ] **Typography**: Font sizes, weights, line heights
   - [ ] **Spacing**: Margins, padding, alignment
   - [ ] **Layout**: Grid, flexbox, responsive breakpoints
   - [ ] **Icons and images**: Proper sizing and alignment
   - [ ] **Animations**: Smooth transitions and effects

6. **Test MoneyFlow-specific functionality**
   
   **CSV Upload:**
   - [ ] Drag and drop file upload works
   - [ ] File validation (format, size)
   - [ ] Upload progress indicator
   - [ ] Success/error messages
   
   **Transaction Display:**
   - [ ] Transactions load and display correctly
   - [ ] Sorting works (by date, amount, merchant)
   - [ ] Filtering works (by source, category)
   - [ ] Pagination works
   
   **Dashboard Visualizations:**
   - [ ] Charts render correctly
   - [ ] Data is accurate
   - [ ] Interactive tooltips work
   - [ ] Responsive on different screen sizes
   
   **Categorization UI:**
   - [ ] Category selection works
   - [ ] Auto-categorization applies
   - [ ] Manual categorization works
   - [ ] Category rules display

7. **Test with sample data**
   
   Use sanitized sample files:
   ```bash
   # Upload PayPay sample
   # Upload SMBC sample
   # Verify data displays correctly
   ```
   
   Files available:
   - `sanitized-samples/paypay-sample.csv`
   - `sanitized-samples/smbc-sample.csv`

8. **Document findings**
   
   Create a verification report with:
   
   - **Screenshots**: Capture key states and flows
   - **UI/UX issues**: Note any problems found
   - **Acceptance criteria**: Verify against spec
   - **Browser console**: Check for errors or warnings
   - **Performance**: Note any slow loading or lag

9. **Create verification report**
   
   Generate a walkthrough document with:
   - Screenshots of key flows
   - List of verified features
   - Any deviations or issues found
   - Recommendations for improvements
   - Browser compatibility notes

## Screenshot Checklist

Capture screenshots of:
- [ ] Landing page / Dashboard
- [ ] CSV upload interface
- [ ] Transaction list view
- [ ] Filtering and sorting in action
- [ ] Category management
- [ ] Visualization charts
- [ ] Mobile responsive views
- [ ] Error states
- [ ] Loading states

## Browser Testing

Test on multiple browsers if possible:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (macOS)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

## Notes

- Use browser DevTools to check console for errors
- Test with realistic data volumes (100+ transactions)
- Verify accessibility (keyboard navigation, screen readers)
- Check performance (page load times, interaction responsiveness)
- Test offline behavior if applicable
- Verify that all images and assets load correctly
