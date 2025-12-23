#!/bin/bash
# Claude Code Notification Sound Script
# Plays random macOS system sounds based on event type

# Get event type from argument or stdin
EVENT_TYPE="${1:-}"

# Read stdin if no argument provided (hooks pass JSON via stdin)
if [ -z "$EVENT_TYPE" ]; then
    INPUT=$(cat)
    EVENT_TYPE=$(echo "$INPUT" | grep -o '"hook_event_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
fi

# Define sound categories
# Pleasant sounds for task completion
COMPLETION_SOUNDS=(
    "Glass"
    "Hero"
    "Ping"
    "Pop"
    "Purr"
    "Submarine"
)

# Attention-grabbing sounds for approval/notification
APPROVAL_SOUNDS=(
    "Blow"
    "Bottle"
    "Funk"
    "Sosumi"
    "Tink"
)

# Warning sounds
WARNING_SOUNDS=(
    "Basso"
    "Frog"
    "Morse"
)

# Select sound based on event type
case "$EVENT_TYPE" in
    "Stop"|"SubagentStop"|"completion"|"done")
        SOUNDS=("${COMPLETION_SOUNDS[@]}")
        ;;
    "Notification"|"PermissionRequest"|"approval"|"question")
        SOUNDS=("${APPROVAL_SOUNDS[@]}")
        ;;
    "error"|"warning")
        SOUNDS=("${WARNING_SOUNDS[@]}")
        ;;
    *)
        # Default to completion sounds
        SOUNDS=("${COMPLETION_SOUNDS[@]}")
        ;;
esac

# Pick a random sound from the selected category
RANDOM_INDEX=$((RANDOM % ${#SOUNDS[@]}))
SELECTED_SOUND="${SOUNDS[$RANDOM_INDEX]}"

# Play the sound (non-blocking with & but we wait briefly)
SOUND_PATH="/System/Library/Sounds/${SELECTED_SOUND}.aiff"

if [ -f "$SOUND_PATH" ]; then
    # Play sound in background, low volume
    afplay -v 0.5 "$SOUND_PATH" &
fi

exit 0
