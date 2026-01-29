#!/bin/bash
# Check for excalidraw update marker and notify user
# Called by Claude Code on session start

MARKER_FILE=".excalidraw-update-needed"

if [ -f "$MARKER_FILE" ]; then
    TIMESTAMP=$(cat "$MARKER_FILE")
    echo "📊 EXCALIDRAW UPDATE NEEDED"
    echo "Architecture files changed since: $TIMESTAMP"
    echo "Ask Claude: 'Update the excalidraw diagram with latest changes'"
    # Remove marker after notification
    rm -f "$MARKER_FILE"
fi
