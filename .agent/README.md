# Agent Configuration

This directory contains configuration and workflows for AI agents working on the MoneyFlow project.

## Overview

MoneyFlow uses a collaborative AI-assisted development workflow with three main tools:

1. **Antigravity** - Planning, specification review, UI verification, and project coordination
2. **Spec-kit** - Structured specification documentation and project constitution
3. **Claude Code** - Implementation following established specifications and protocols

## Files

- **ANTIGRAVITY.md**: Primary context file for the Antigravity agent
- **workflows/**: Workflow definitions for common development tasks

## Workflows

The workflows directory contains step-by-step guides for common tasks:

- `start_feature.md` - Start a new feature with spec-kit
- `sync_with_specs.md` - Catch up with current project specifications
- `review_spec.md` - Review spec-kit generated specifications
- `handoff_to_claude.md` - Hand off implementation to Claude Code
- `verify_implementation.md` - Verify Claude's implementation
- `verify_ui.md` - Verify UI changes using browser agent

## Usage

Workflows can be invoked using slash commands (e.g., `/sync-with-specs`) or by referencing the workflow files directly.

## Development Protocol

All agents follow strict development protocols:
- **No execution without explicit user permission**
- **Always create and share plans before implementation**
- **Wait for user confirmation before proceeding**

See `ANTIGRAVITY.md` for detailed guidelines.
