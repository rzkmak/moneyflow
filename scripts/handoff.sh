#!/bin/bash

# Handoff Script
# Usage: ./scripts/handoff.sh [direction]
# direction: "to-claude" or "to-gemini"

DIRECTION=$1

# 1. Find the latest spec directory
# Looks for directories starting with numbers in specs/ and takes the last one (highest number)
LATEST_SPEC_DIR=$(find specs -maxdepth 1 -type d -name '[0-9]*' | sort -V | tail -1)

if [ -z "$LATEST_SPEC_DIR" ]; then
    echo "❌ Error: No specification directories found in specs/"
    exit 1
fi

SPEC_ID=$(basename "$LATEST_SPEC_DIR")
PLAN_FILE="$LATEST_SPEC_DIR/plan.md"

echo "=========================================="
echo "🔄 Handoff Context Generator"
echo "📂 Feature: $SPEC_ID"
echo "=========================================="
echo ""

if [ "$DIRECTION" == "to-claude" ]; then
    if [ ! -f "$PLAN_FILE" ]; then
        echo "❌ Error: Plan file not found at $PLAN_FILE"
        exit 1
    fi

    echo "🤖 Handing off to Claude Code"
    echo "------------------------------------------------------"
    echo "📋 Copy and paste the following prompt into Claude Code:"
    echo "------------------------------------------------------"
    echo ""
    echo "Please implement the feature described in '$PLAN_FILE'."
    echo "Strictly follow the phases and steps outlined in the plan."
    echo "Refer to '$LATEST_SPEC_DIR/spec.md' for user requirements and '$LATEST_SPEC_DIR/data-model.md' for schema details."
    echo "Adhere to the project guidelines in 'CLAUDE.md'."
    echo ""
    echo "------------------------------------------------------"
    echo ""
    echo "Once Claude has finished, please run the verification tests listed in the plan."

elif [ "$DIRECTION" == "to-gemini" ]; then
    echo "🤖 Handing off back to Gemini"
    echo "------------------------------------------------------"
    echo "📋 Copy and paste the following prompt into your NEW Gemini session:"
    echo "------------------------------------------------------"
    echo ""
    echo "I have completed the implementation of feature '$SPEC_ID' using Claude."
    echo ""
    echo "Please perform the following sync tasks:"
    echo "1. Analyze the 'backend/src' and 'frontend/src' directories to understand the new structure."
    echo "2. Verify that the 'Transaction' model and any new entities (like 'CategoryRule') are correct."
    echo "3. Update 'GEMINI.md' to reflect that '$SPEC_ID' is now complete."
    echo "4. Update 'README.md' feature list if necessary."
    echo ""
    echo "The implementation was based on the plan in '$PLAN_FILE'."
    echo ""
    echo "------------------------------------------------------"

else
    echo "Usage: ./scripts/handoff.sh [to-claude|to-gemini]"
    exit 1
fi
