#!/usr/bin/env node
/**
 * Reset Claude Session Stats
 *
 * Run this when starting a new task/session to reset the tool call counter.
 * Usage: node ~/.claude/hooks/reset-session.js
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const STATS_FILE = path.join(os.tmpdir(), 'claude-session-stats.json');

const freshStats = {
  toolCalls: 0,
  sessionStart: new Date().toISOString(),
  lastCompactReminder: 0,
  compactCount: 0
};

fs.writeFileSync(STATS_FILE, JSON.stringify(freshStats, null, 2));
console.log('✅ Session stats reset. Tool call counter: 0');
