#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const CLAUDE_DIR = path.join(os.homedir(), '.claude');
const CONFIG_DIR = path.join(__dirname, '..', 'config');
const BACKUP_SUFFIX = `.backup-${Date.now()}`;

const COLORS = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  dim: '\x1b[2m',
};

const log = {
  info: (msg) => console.log(`${COLORS.blue}[INFO]${COLORS.reset} ${msg}`),
  success: (msg) => console.log(`${COLORS.green}[OK]${COLORS.reset} ${msg}`),
  warn: (msg) => console.log(`${COLORS.yellow}[WARN]${COLORS.reset} ${msg}`),
  error: (msg) => console.log(`${COLORS.red}[ERROR]${COLORS.reset} ${msg}`),
  step: (msg) => console.log(`\n${COLORS.blue}==>${COLORS.reset} ${msg}`),
};

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    log.info(`Created directory: ${dir}`);
  }
}

function backupFile(filePath) {
  if (fs.existsSync(filePath)) {
    const backupPath = filePath + BACKUP_SUFFIX;
    fs.copyFileSync(filePath, backupPath);
    log.warn(`Backed up: ${filePath} -> ${backupPath}`);
    return true;
  }
  return false;
}

function copyRecursive(src, dest, overwrite = false) {
  const stats = fs.statSync(src);

  if (stats.isDirectory()) {
    ensureDir(dest);
    const entries = fs.readdirSync(src);
    for (const entry of entries) {
      copyRecursive(path.join(src, entry), path.join(dest, entry), overwrite);
    }
  } else {
    if (fs.existsSync(dest) && !overwrite) {
      log.dim?.(`Skipping (exists): ${dest}`);
      return;
    }
    fs.copyFileSync(src, dest);
    log.success(`Installed: ${dest.replace(os.homedir(), '~')}`);
  }
}

function mergeSettings(existingPath, newSettingsPath) {
  let existing = {};
  let newSettings = {};

  try {
    if (fs.existsSync(existingPath)) {
      existing = JSON.parse(fs.readFileSync(existingPath, 'utf8'));
    }
    newSettings = JSON.parse(fs.readFileSync(newSettingsPath, 'utf8'));
  } catch (e) {
    log.error(`Failed to parse settings: ${e.message}`);
    return false;
  }

  // Merge permissions (union of allow lists)
  if (newSettings.permissions?.allow) {
    existing.permissions = existing.permissions || {};
    existing.permissions.allow = [...new Set([
      ...(existing.permissions.allow || []),
      ...newSettings.permissions.allow
    ])];
  }

  // Merge hooks
  if (newSettings.hooks) {
    existing.hooks = existing.hooks || {};
    for (const [event, hooks] of Object.entries(newSettings.hooks)) {
      existing.hooks[event] = existing.hooks[event] || [];
      // Add hooks that don't already exist
      for (const hook of hooks) {
        const exists = existing.hooks[event].some(h =>
          JSON.stringify(h) === JSON.stringify(hook)
        );
        if (!exists) {
          existing.hooks[event].push(hook);
        }
      }
    }
  }

  // Merge MCP servers (add new ones, don't overwrite existing)
  if (newSettings.mcpServers) {
    existing.mcpServers = existing.mcpServers || {};
    for (const [name, config] of Object.entries(newSettings.mcpServers)) {
      if (!existing.mcpServers[name]) {
        existing.mcpServers[name] = config;
        log.info(`Added MCP server: ${name}`);
      }
    }
  }

  fs.writeFileSync(existingPath, JSON.stringify(existing, null, 2));
  return true;
}

function main() {
  console.log(`
${COLORS.blue}╔═══════════════════════════════════════════════════════╗
║     Claude Code Power User Setup                        ║
║     Agents • Skills • Commands • Hooks                  ║
╚═══════════════════════════════════════════════════════╝${COLORS.reset}
`);

  const args = process.argv.slice(2);
  const forceOverwrite = args.includes('--force') || args.includes('-f');
  const skipBackup = args.includes('--no-backup');

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: npx hieu-ccsetup [options]

Options:
  --force, -f      Overwrite existing files
  --no-backup      Skip creating backups
  --help, -h       Show this help message

What gets installed:
  ~/.claude/agents/       Custom subagents (35+)
  ~/.claude/skills/       Skills & workflows (70+)
  ~/.claude/commands/     Slash commands (30+)
  ~/.claude/hooks/        Automation hooks
  ~/.claude/principles/   Core principles & guidelines
  ~/.claude/CLAUDE.md     Global instructions (merged)
  ~/.claude/settings.json Settings (merged, not overwritten)
`);
    process.exit(0);
  }

  // Ensure base directory exists
  log.step('Checking Claude Code installation...');
  ensureDir(CLAUDE_DIR);

  // Backup existing settings if present
  if (!skipBackup) {
    log.step('Creating backups...');
    backupFile(path.join(CLAUDE_DIR, 'settings.json'));
    backupFile(path.join(CLAUDE_DIR, 'CLAUDE.md'));
  }

  // Install agents
  log.step('Installing agents...');
  const agentsSrc = path.join(CONFIG_DIR, 'agents');
  if (fs.existsSync(agentsSrc)) {
    copyRecursive(agentsSrc, path.join(CLAUDE_DIR, 'agents'), forceOverwrite);
  }

  // Install skills
  log.step('Installing skills...');
  const skillsSrc = path.join(CONFIG_DIR, 'skills');
  if (fs.existsSync(skillsSrc)) {
    copyRecursive(skillsSrc, path.join(CLAUDE_DIR, 'skills'), forceOverwrite);
  }

  // Install commands
  log.step('Installing commands...');
  const commandsSrc = path.join(CONFIG_DIR, 'commands');
  if (fs.existsSync(commandsSrc)) {
    copyRecursive(commandsSrc, path.join(CLAUDE_DIR, 'commands'), forceOverwrite);
  }

  // Install hooks
  log.step('Installing hooks...');
  const hooksSrc = path.join(CONFIG_DIR, 'hooks');
  if (fs.existsSync(hooksSrc)) {
    copyRecursive(hooksSrc, path.join(CLAUDE_DIR, 'hooks'), forceOverwrite);
    // Make hooks executable
    try {
      execSync(`chmod +x "${path.join(CLAUDE_DIR, 'hooks')}"/*.sh 2>/dev/null || true`);
      execSync(`chmod +x "${path.join(CLAUDE_DIR, 'hooks')}"/*.js 2>/dev/null || true`);
    } catch (e) {}
  }

  // Install principles
  log.step('Installing principles...');
  const principlesSrc = path.join(CONFIG_DIR, 'principles');
  if (fs.existsSync(principlesSrc)) {
    copyRecursive(principlesSrc, path.join(CLAUDE_DIR, 'principles'), forceOverwrite);
  }

  // Merge settings
  log.step('Merging settings...');
  const settingsTemplatePath = path.join(CONFIG_DIR, 'settings.template.json');
  if (fs.existsSync(settingsTemplatePath)) {
    if (mergeSettings(path.join(CLAUDE_DIR, 'settings.json'), settingsTemplatePath)) {
      log.success('Settings merged successfully');
    }
  }

  // Install/merge CLAUDE.md
  log.step('Installing CLAUDE.md...');
  const claudeMdSrc = path.join(CONFIG_DIR, 'CLAUDE.md');
  const claudeMdDest = path.join(CLAUDE_DIR, 'CLAUDE.md');
  if (fs.existsSync(claudeMdSrc)) {
    if (fs.existsSync(claudeMdDest) && !forceOverwrite) {
      // Append to existing
      const existing = fs.readFileSync(claudeMdDest, 'utf8');
      const newContent = fs.readFileSync(claudeMdSrc, 'utf8');
      if (!existing.includes('## Power User Extensions')) {
        fs.appendFileSync(claudeMdDest, '\n\n' + newContent);
        log.success('Appended to existing CLAUDE.md');
      } else {
        log.info('CLAUDE.md already contains power user config');
      }
    } else {
      fs.copyFileSync(claudeMdSrc, claudeMdDest);
      log.success('Installed CLAUDE.md');
    }
  }

  console.log(`
${COLORS.green}════════════════════════════════════════════════════════
  Installation complete!
════════════════════════════════════════════════════════${COLORS.reset}

${COLORS.blue}Next steps:${COLORS.reset}
  1. Restart Claude Code: ${COLORS.dim}claude${COLORS.reset}
  2. Try a command: ${COLORS.dim}/cook your task${COLORS.reset}
  3. List skills: ${COLORS.dim}/skill list${COLORS.reset}

${COLORS.yellow}Note:${COLORS.reset} Some MCP servers may require API keys.
      Check ~/.claude/settings.json to configure.

${COLORS.dim}Backups saved with suffix: ${BACKUP_SUFFIX}${COLORS.reset}
`);
}

main();
