#!/bin/bash
# Excalidraw Auto-Update Post-Commit Hook
# Triggers diagram regeneration after git commits

# Get the repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi

# Check if excalidraw files exist in the repo
EXCALIDRAW_FILES=$(find "$REPO_ROOT" -name "*.excalidraw" -type f 2>/dev/null | head -1)

# Only proceed if excalidraw files exist
if [ -z "$EXCALIDRAW_FILES" ]; then
    exit 0
fi

# Get changed files in last commit
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null)

# Check if architecture-relevant files changed
RELEVANT_PATTERNS=(
    "package.json"
    "docker-compose"
    "Dockerfile"
    "*.tf"
    "*.yaml"
    "*.yml"
    "tsconfig"
    "schema.prisma"
    "requirements.txt"
    "go.mod"
    "Cargo.toml"
)

SHOULD_UPDATE=false
for pattern in "${RELEVANT_PATTERNS[@]}"; do
    if echo "$CHANGED_FILES" | grep -q "$pattern"; then
        SHOULD_UPDATE=true
        break
    fi
done

if [ "$SHOULD_UPDATE" = true ]; then
    # Create a marker file to signal Claude to update diagrams
    MARKER_FILE="$REPO_ROOT/.excalidraw-update-needed"
    echo "$(date -Iseconds)" > "$MARKER_FILE"
    echo "📊 Architecture files changed. Run 'claude' and ask to update excalidraw diagrams."
fi
