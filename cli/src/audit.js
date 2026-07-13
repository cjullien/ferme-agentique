'use strict';

const fs = require('node:fs');
const path = require('node:path');

// Reproduit la Phase 4 de farm-init : audit de la configuration posée.
function auditConfig(cwd) {
  const results = [];

  const claudeMdPath = path.join(cwd, 'CLAUDE.md');
  const claudeMdExists = fs.existsSync(claudeMdPath);
  const claudeMdContent = claudeMdExists ? fs.readFileSync(claudeMdPath, 'utf8') : '';
  const placeholderCount = (claudeMdContent.match(/\{\{/g) || []).length;
  const lineCount = claudeMdContent ? claudeMdContent.split('\n').length : 0;

  results.push({
    section: 'CLAUDE.md',
    status: !claudeMdExists ? '❌' : placeholderCount > 0 || lineCount > 200 ? '⚠️' : '✅',
    notes: !claudeMdExists
      ? 'Absent'
      : `${placeholderCount} placeholder(s) restant(s), ${lineCount} lignes` +
        (lineCount > 200 ? ' — > 200 lignes : instructions ignorées silencieusement au-delà' : ''),
  });

  const agentsDir = path.join(cwd, '.claude', 'agents');
  const agentCount = fs.existsSync(agentsDir)
    ? fs.readdirSync(agentsDir).filter((f) => f.endsWith('.md')).length
    : 0;
  results.push({ section: 'Agents', status: agentCount > 0 ? '✅' : '❌', notes: `${agentCount} agents` });

  const skillsDir = path.join(cwd, '.claude', 'skills');
  const skillCount = fs.existsSync(skillsDir)
    ? fs.readdirSync(skillsDir).filter((d) => fs.existsSync(path.join(skillsDir, d, 'SKILL.md'))).length
    : 0;
  results.push({ section: 'Skills', status: skillCount > 0 ? '✅' : '❌', notes: `${skillCount} skills` });

  const settingsPath = path.join(cwd, '.claude', 'settings.json');
  let settingsStatus = '❌';
  let settingsNotes = 'Absent';
  let hooksPresent = false;
  if (fs.existsSync(settingsPath)) {
    try {
      const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
      const allow = settings.permissions?.allow || [];
      const stackCommands = allow.filter((a) =>
        /npm|pip|mvn|cargo|go |make|gradle|pytest|jest|dotnet|ruff|alembic/i.test(a),
      );
      hooksPresent = Boolean(settings.hooks);
      settingsStatus = stackCommands.length > 0 ? '✅' : '⚠️';
      settingsNotes =
        stackCommands.length > 0
          ? `${stackCommands.length} commande(s) de stack autorisée(s)`
          : 'JSON valide mais aucune commande de build/test/lint de stack détectée — compléter permissions.allow';
    } catch {
      settingsStatus = '❌';
      settingsNotes = 'JSON invalide';
    }
  }
  results.push({ section: 'settings.json', status: settingsStatus, notes: settingsNotes });
  results.push({
    section: 'Hooks',
    status: hooksPresent ? '✅' : '⚠️',
    notes: hooksPresent ? 'Présents' : 'Aucun hook configuré',
  });

  const gitignorePath = path.join(cwd, '.gitignore');
  const gitignoreExists = fs.existsSync(gitignorePath);
  const gitignoreContent = gitignoreExists ? fs.readFileSync(gitignorePath, 'utf8') : '';
  const commonPatterns = ['node_modules', '__pycache__', '\\.env', 'venv', '\\.venv', 'target/', 'dist/', 'build/'];
  const matched = commonPatterns.filter((p) => new RegExp(`^${p}$`, 'm').test(gitignoreContent));
  results.push({
    section: '.gitignore',
    status: !gitignoreExists ? '⚠️' : matched.length > 0 ? '✅' : '⚠️',
    notes: !gitignoreExists ? 'Absent' : `${matched.length} pattern(s) usuel(s) trouvé(s)`,
  });

  return results;
}

function printAuditReport(results) {
  console.log('\n## Farm Init — Configuration\n');
  const colWidths = [16, 8, 62];
  console.log(['Section', 'Statut', 'Notes'].map((h, i) => h.padEnd(colWidths[i])).join(' | '));
  console.log(colWidths.map((w) => '-'.repeat(w)).join('-|-'));
  for (const r of results) {
    console.log([r.section.padEnd(colWidths[0]), r.status.padEnd(colWidths[1]), r.notes].join(' | '));
  }

  const issues = results.filter((r) => r.status !== '✅');
  if (issues.length === 0) {
    console.log('\n✅ La ferme est correctement configurée. Lancez /audit dans Claude Code pour un premier pre-flight sur le code.');
  } else {
    console.log('\n### Actions recommandées');
    for (const r of issues) {
      console.log(`- [${r.status}] ${r.section} : ${r.notes}`);
    }
  }
}

module.exports = { auditConfig, printAuditReport };
