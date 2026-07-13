'use strict';

const fs = require('node:fs');
const path = require('node:path');

// Reproduit la Phase 0 de template/.claude/skills/farm-init/SKILL.md
function detectState(cwd) {
  const agentsDir = path.join(cwd, '.claude', 'agents');
  const skillsDir = path.join(cwd, '.claude', 'skills');
  const claudeMdPath = path.join(cwd, 'CLAUDE.md');

  const agentCount = fs.existsSync(agentsDir)
    ? fs.readdirSync(agentsDir).filter((f) => f.endsWith('.md')).length
    : 0;

  const skillCount = fs.existsSync(skillsDir)
    ? fs.readdirSync(skillsDir).filter((d) => fs.existsSync(path.join(skillsDir, d, 'SKILL.md'))).length
    : 0;

  const claudeMdExists = fs.existsSync(claudeMdPath);
  const claudeMdContent = claudeMdExists ? fs.readFileSync(claudeMdPath, 'utf8') : '';
  const hasPlaceholders = /\{\{/.test(claudeMdContent);

  let mode;
  if (agentCount === 0) {
    mode = 'A'; // installation guidée
  } else if (claudeMdExists && hasPlaceholders) {
    mode = 'B'; // configuration incomplète
  } else {
    mode = 'C'; // audit seul
  }

  return { mode, agentCount, skillCount, claudeMdExists, claudeMdPath };
}

module.exports = { detectState };
