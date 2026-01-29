#!/bin/bash
# Install Excalidraw post-commit hook to a git repository
# Usage: install-excalidraw-hook.sh [repo-path]

REPO_PATH="${1:-.}"
HOOK_SOURCE="$HOME/.claude/hooks/excalidraw-post-commit.sh"
HOOK_DEST="$REPO_PATH/.git/hooks/post-commit"

# Verify it's a git repo
if [ ! -d "$REPO_PATH/.git" ]; then
    echo "❌ Not a git repository: $REPO_PATH"
    exit 1
fi

# Check if post-commit hook already exists
if [ -f "$HOOK_DEST" ]; then
    # Append to existing hook
    if grep -q "excalidraw-post-commit" "$HOOK_DEST"; then
        echo "✅ Excalidraw hook already installed in $REPO_PATH"
        exit 0
    fi
    echo "" >> "$HOOK_DEST"
    echo "# Excalidraw auto-update hook" >> "$HOOK_DEST"
    echo "source \"$HOOK_SOURCE\"" >> "$HOOK_DEST"
    echo "✅ Appended Excalidraw hook to existing post-commit"
else
    # Create new hook
    echo "#!/bin/bash" > "$HOOK_DEST"
    echo "# Excalidraw auto-update hook" >> "$HOOK_DEST"
    echo "source \"$HOOK_SOURCE\"" >> "$HOOK_DEST"
    chmod +x "$HOOK_DEST"
    echo "✅ Installed Excalidraw post-commit hook to $REPO_PATH"
fi
