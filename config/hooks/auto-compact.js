#!/usr/bin/env node
/**
 * Auto-Compact Hook for Claude Code
 *
 * Monitors tool call count and recommends /compact when approaching
 * 60% context usage (estimated via ~40 tool calls threshold).
 *
 * This hook runs on PostToolUse and tracks session statistics.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const TOOL_CALL_THRESHOLD = 40; // ~60% context estimate
const STATS_FILE = path.join(os.tmpdir(), 'claude-session-stats.json');
const COMPACT_REMINDER_INTERVAL = 10; // Remind every 10 calls after threshold

// Initialize or load stats
let stats = {
  toolCalls: 0,
  sessionStart: new Date().toISOString(),
  lastCompactReminder: 0,
  compactCount: 0
};

try {
  const existing = fs.readFileSync(STATS_FILE, 'utf8');
  stats = JSON.parse(existing);
} catch {
  // File doesn't exist, use defaults
}

// Increment tool call count
stats.toolCalls++;

// Check if we should remind about compaction
if (stats.toolCalls >= TOOL_CALL_THRESHOLD) {
  const callsSinceReminder = stats.toolCalls - stats.lastCompactReminder;

  if (callsSinceReminder >= COMPACT_REMINDER_INTERVAL || stats.lastCompactReminder === 0) {
    const usage = Math.min(Math.round((stats.toolCalls / 70) * 100), 100);
    console.log(`\n🔄 Context Monitor: ${stats.toolCalls} tool calls (~${usage}% estimated usage)`);
    console.log(`   Consider running /compact to refresh context and prevent hallucination.`);
    stats.lastCompactReminder = stats.toolCalls;
  }
}

// Save stats
fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));

// Exit cleanly (don't block the tool)
process.exit(0);
