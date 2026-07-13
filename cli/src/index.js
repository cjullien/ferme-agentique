'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { createPrompter } = require('./prompt');
const { detectState } = require('./detect');
const { copyDir, copyFile } = require('./copy');
const { brainstormModules } = require('./modules');
const { fillClaudeMdFields, checkModuleBoxes } = require('./claude-md');
const { auditConfig, printAuditReport } = require('./audit');

// La ferme est bundlée avec ce CLI (cli/src -> racine du repo) : pas de clone
// séparé à localiser, npx récupère toujours la version publiée la plus récente.
const FARM_ROOT = path.join(__dirname, '..', '..');

function installSocle(cwd) {
  copyDir(path.join(FARM_ROOT, 'template', '.claude', 'agents'), path.join(cwd, '.claude', 'agents'));
  copyDir(path.join(FARM_ROOT, 'template', '.claude', 'skills'), path.join(cwd, '.claude', 'skills'));
  copyFile(
    path.join(FARM_ROOT, 'template', '.claude', 'settings.json'),
    path.join(cwd, '.claude', 'settings.json'),
    { overwrite: false },
  );

  copyDir(path.join(FARM_ROOT, 'template', '.github', 'agents'), path.join(cwd, '.github', 'agents'));
  copyDir(path.join(FARM_ROOT, 'template', '.github', 'skills'), path.join(cwd, '.github', 'skills'));
  copyDir(path.join(FARM_ROOT, 'template', '.github', 'extensions'), path.join(cwd, '.github', 'extensions'));
  copyFile(path.join(FARM_ROOT, 'template', '.github', 'lsp.json'), path.join(cwd, '.github', 'lsp.json'), {
    overwrite: false,
  });
  copyFile(
    path.join(FARM_ROOT, 'template', '.github', 'copilot-instructions.template.md'),
    path.join(cwd, '.github', 'copilot-instructions.md'),
    { overwrite: false },
  );

  copyFile(path.join(FARM_ROOT, 'template', 'CLAUDE.template.md'), path.join(cwd, 'CLAUDE.md'), {
    overwrite: false,
  });

  fs.mkdirSync(path.join(cwd, '.claude'), { recursive: true });
  const pkg = JSON.parse(fs.readFileSync(path.join(FARM_ROOT, 'package.json'), 'utf8'));
  fs.writeFileSync(path.join(cwd, '.claude', '.farm-source'), `npx ferme-agentic@${pkg.version}\n`);

  const agentCount = fs.readdirSync(path.join(cwd, '.claude', 'agents')).filter((f) => f.endsWith('.md')).length;
  const skillCount = fs.readdirSync(path.join(cwd, '.claude', 'skills')).length;
  console.log(`✅ Socle copié : ${agentCount} agents, ${skillCount} skills`);
}

async function main() {
  const cwd = process.cwd();
  console.log('Ferme agentique — installation\n');

  const state = detectState(cwd);
  const prompter = createPrompter();

  try {
    if (state.mode === 'A') {
      console.log('Aucun agent détecté sur ce projet — installation du socle générique.\n');
      installSocle(cwd);
    } else if (state.mode === 'B') {
      console.log('Socle déjà présent, CLAUDE.md incomplet — reprise de la configuration.\n');
    } else {
      console.log('Socle et CLAUDE.md déjà configurés — audit seul.\n');
    }

    let installedModules = [];
    if (state.mode === 'A' || state.mode === 'B') {
      console.log('\n== Configuration de CLAUDE.md ==\n');
      await fillClaudeMdFields(path.join(cwd, 'CLAUDE.md'), prompter);

      installedModules = await brainstormModules({ farmRoot: FARM_ROOT, cwd, prompter });
      checkModuleBoxes(path.join(cwd, 'CLAUDE.md'), installedModules);
    }

    const results = auditConfig(cwd);
    printAuditReport(results);
  } finally {
    prompter.close();
  }
}

module.exports = { main };
