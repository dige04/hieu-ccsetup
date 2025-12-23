# hieu-ccsetup

One-command setup for Claude Code with 20+ agents, 50+ skills, 25+ commands, and automation hooks.

## Quick Install

```bash
npx hieu-ccsetup
```

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Agents** | 20+ | code-reviewer, debugger, planner, researcher, tester, ui-ux-designer... |
| **Skills** | 50+ | ai-multimodal, devops, databases, frontend, backend, chrome-devtools... |
| **Commands** | 25+ | /cook, /scout, /plan, /fix, /design, /docs, /git, /test... |
| **Hooks** | 4 | Notifications, auto-compact, file-write triggers |

## Usage

### Options

```bash
# Standard install (merges with existing config)
npx hieu-ccsetup

# Force overwrite existing files
npx hieu-ccsetup --force

# Skip backups
npx hieu-ccsetup --no-backup
```

### Key Commands

After installation, use these in Claude Code:

```
/cook <task>      Full workflow: research → plan → implement → test → review
/scout            Find files across codebase
/plan <feature>   Create implementation plan
/fix <issue>      Debug and fix issues
/design <ui>      UI/UX design workflow
```

## Configuration

The installer **merges** with your existing config:

- **Permissions**: Union of existing + new allowed tools
- **Hooks**: Adds new hooks without removing existing
- **MCP Servers**: Adds new servers, doesn't overwrite existing
- **CLAUDE.md**: Appends to existing file

### Adding API Keys

Some MCP servers need API keys. Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Backup & Restore

Backups are created automatically with timestamp suffix:
- `~/.claude/settings.json.backup-1703123456789`

To restore:
```bash
cp ~/.claude/settings.json.backup-* ~/.claude/settings.json
```

## Uninstall

```bash
# Remove installed components
rm -rf ~/.claude/agents ~/.claude/skills ~/.claude/commands ~/.claude/hooks

# Restore from backup
cp ~/.claude/settings.json.backup-* ~/.claude/settings.json
```

## Development

```bash
# Clone and test locally
git clone https://github.com/hieudinh/hieu-ccsetup.git
cd hieu-ccsetup
node bin/setup.js --help
```

## License

MIT
