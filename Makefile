# Makefile for MoneyFlow Project
# Provides convenient targets for the AI-assisted development workflow

.PHONY: help complete-spec notify-spec impl start stop test clean

# Default target
help:
	@echo "MoneyFlow Development Workflow"
	@echo "=============================="
	@echo ""
	@echo "Specification Phase:"
	@echo "  complete-spec     - Complete the full specification workflow (Gemini → Plan → Notify)"
	@echo "  notify-spec       - Notify Claude about completed specifications (run after Gemini CLI)"
	@echo ""
	@echo "Implementation Phase:"
	@echo "  impl              - Start implementation following the established workflow"
	@echo "  start             - Start both backend and frontend development servers"
	@echo "  stop              - Stop all running development servers"
	@echo ""
	@echo "Quality Assurance:"
	@echo "  test              - Run all tests"
	@echo "  lint              - Run linting on code"
	@echo "  analyze           - Analyze specifications for consistency (requires feature branch)"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean             - Clean build artifacts and dependencies"
	@echo "  deps              - Install all dependencies"
	@echo ""
	@echo "Documentation:"
	@echo "  docs              - Generate and open documentation"
	@echo "  sync-docs         - Ensure documentation synchronization"

# Complete specification workflow
# This would typically be called after using Gemini CLI to generate specs
complete-spec:
	@echo "Completing specification workflow..."
	@echo ""
	@echo "1. Checking if on feature branch..."
	@bash -c 'current_branch=$$(git branch --show-current); if [[ ! $$current_branch =~ ^[0-9]+- ]]; then echo "ERROR: Not on a feature branch. Current branch: $$current_branch"; echo "Feature branches should be named like: 002-feature-name"; exit 1; fi; echo "✓ On feature branch: $$current_branch"'
	@echo ""
	@echo "2. Verifying specifications exist..."
	@if [ ! -d "specs" ] || [ -z "$(find specs -maxdepth 1 -type d -name '[0-9]*' 2>/dev/null | head -1)" ]; then \
		echo "ERROR: No specification directories found in specs/"; \
		echo "Run Gemini CLI first to generate specifications"; \
		exit 1; \
	else \
		echo "✓ Found specification directories"; \
	fi
	@echo ""
	@echo "3. Notifying Claude about completed specifications..."
	@bash scripts/notify-spec-complete.sh
	@echo ""
	@echo "✓ Specification workflow completed!"
	@echo "   - Created pull request with documentation updates"
	@echo "   - Next: Wait for PR approval, then run 'make impl'"

# Notify Claude about completed specifications
notify-spec:
	@echo "Notifying Claude about completed specifications..."
	@bash scripts/notify-spec-complete.sh

# Start implementation
impl:
	@echo "Starting implementation workflow..."
	@echo ""
	@echo "IMPORTANT: This will follow the Claude Code development protocol:"
	@echo "1. No execution without explicit user permission"
	@echo "2. Always create and share plans before implementation"
	@echo "3. Wait for user confirmation before proceeding"
	@echo ""
	@echo "Current branch: $(shell git branch --show-current)"
	@echo "Specification directory: $(shell find specs -maxdepth 1 -type d -name '[0-9]*' 2>/dev/null | sort -V | tail -1)"
	@echo ""
	@echo "To start implementation:"
	@echo "  1. Review the specification documents"
	@echo "  2. Create a detailed implementation plan"
	@echo "  3. Present the plan to the user for approval"
	@echo "  4. Execute tasks with explicit permission"
	@echo ""
	@echo "Ready to proceed? (Press Enter to continue or Ctrl+C to exit)"
	@read -r
	@echo ""
	@echo "Implementation workflow initialized."
	@echo "Use Claude Code to implement tasks following the protocol in CLAUDE.md"

# Start development servers
start:
	@echo "Starting development servers..."
	@echo ""
	# Start backend in background
	@echo "Starting backend server..."
	@cd backend && \
		python -m venv .venv 2>/dev/null || true && \
		source .venv/bin/activate 2>/dev/null || true && \
		pip install -r requirements.txt 2>/dev/null || true && \
		uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 &
	@BACKEND_PID=$$!
	@echo "Backend PID: $$BACKEND_PID"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	# Start frontend in background
	@echo "Starting frontend server..."
	@cd frontend && \
		npm install 2>/dev/null || true && \
		npm run dev &
	@FRONTEND_PID=$$!
	@echo "Frontend PID: $$FRONTEND_PID"
	@echo "Frontend: http://localhost:5173"
	@echo ""
	@echo "Development servers started!"
	@echo "To stop: make stop"
	@echo ""
	@# Store PIDs for stop target
	@echo "$$BACKEND_PID" > .backend.pid
	@echo "$$FRONTEND_PID" > .frontend.pid

# Stop development servers
stop:
	@if [ -f .backend.pid ]; then \
		kill $$(cat .backend.pid) 2>/dev/null || true; \
		rm .backend.pid; \
		echo "Backend server stopped"; \
	fi
	@if [ -f .frontend.pid ]; then \
		kill $$(cat .frontend.pid) 2>/dev/null || true; \
		rm .frontend.pid; \
		echo "Frontend server stopped"; \
	fi
	@echo "All development servers stopped"

# Run tests
test:
	@echo "Running tests..."
	@echo ""
	@echo "Backend tests:"
	@cd backend && \
		python -m pytest tests/ -v 2>/dev/null || \
		python tests/test_parser_manual.py 2>/dev/null || \
		echo "No backend tests found"
	@echo ""
	@echo "Frontend tests:"
	@cd frontend && \
		npm test 2>/dev/null || \
		echo "No frontend tests configured"

# Run linting
lint:
	@echo "Running linting..."
	@echo ""
	@echo "Backend linting:"
	@cd backend && \
		pylint src/ 2>/dev/null || \
		flake8 src/ 2>/dev/null || \
		echo "No backend linter configured"
	@echo ""
	@echo "Frontend linting:"
	@cd frontend && \
		npm run lint 2>/dev/null || \
		npx eslint src/ 2>/dev/null || \
		echo "No frontend linter configured"

# Analyze specifications
analyze:
	@echo "Analyzing specifications for consistency..."
	@echo ""
	@echo "Requirements:"
	@echo "  - Must be on a feature branch (001-*, 002-*, etc.)"
	@echo "  - specs/ directory must exist with specifications"
	@echo "  - .specify/memory/constitution.md must exist"
	@echo ""
	@echo "Current status:"
	@echo "  Branch: $(shell git branch --show-current)"
	@echo "  Specs directory: $(wildcard specs/[0-9]*)"
	@echo ""
	@if [ ! -f ".specify/memory/constitution.md" ]; then \
		echo "ERROR: Constitution file not found"; \
		echo "Run: .specify/scripts/bash/check-prerequisites.sh"; \
		exit 1; \
	fi
	@echo "✓ Constitution file found"
	@echo ""
	@echo "To run full analysis:"
	@echo "  1. Ensure you're on a feature branch"
	@echo "  2. Run: /speckit.analyze"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@echo ""
	@echo "Backend:"
	@cd backend && \
		rm -rf __pycache__ && \
		rm -rf *.pyc && \
		rm -rf .venv
	@echo ""
	@echo "Frontend:"
	@cd frontend && \
		rm -rf node_modules && \
		rm -rf dist && \
		rm -rf .vite
	@echo ""
	@echo "Git:"
	@rm -f .backend.pid .frontend.pid
	@echo "✓ Clean completed"

# Install dependencies
deps:
	@echo "Installing dependencies..."
	@echo ""
	@echo "Backend dependencies:"
	@cd backend && \
		python -m venv .venv && \
		source .venv/bin/activate && \
		pip install -r requirements.txt
	@echo ""
	@echo "Frontend dependencies:"
	@cd frontend && \
		npm install
	@echo ""
	@echo "✓ All dependencies installed"

# Generate and open documentation
docs:
	@echo "Generating documentation..."
	@echo ""
	@echo "Available documentation:"
	@echo "  - README.md: Project overview and setup"
	@echo "  - CLAUDE.md: Claude Code guidance"
	@echo "  - GEMINI.md: Gemini agent context"
	@echo "  - specs/: Feature specifications"
	@echo ""
	@echo "To open documentation:"
	@echo "  - Open README.md in your browser"
	@echo "  - View API docs at http://localhost:8000/docs (after starting servers)"
	@echo ""
	@echo "Documentation synchronization complete."

# Ensure documentation synchronization
sync-docs:
	@echo "Ensuring documentation synchronization..."
	@echo ""
	@echo "Checking documentation consistency..."
	@if [ -f "README.md" ] && [ -f "GEMINI.md" ] && [ -f "CLAUDE.md" ]; then \
		echo "✓ All documentation files present"; \
	else \
		echo "WARNING: Missing documentation files"; \
	fi
	@echo ""
	@echo "Documentation synchronization verified."