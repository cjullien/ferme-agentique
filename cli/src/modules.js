'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { copyDir } = require('./copy');

// Copie agents + skills d'un module examples/<nom> par-dessus .claude/ et .github/
// du projet cible. Écrase volontairement les fichiers de même nom (cf. catalog.md :
// les variantes stack-spécifiques comme backlog-manager sont conçues pour surcharger
// la version générique du socle).
function installModule(farmRoot, cwd, moduleName) {
  const claudeSrc = path.join(farmRoot, 'examples', moduleName, '.claude');
  copyDir(path.join(claudeSrc, 'agents'), path.join(cwd, '.claude', 'agents'), { overwrite: true });
  copyDir(path.join(claudeSrc, 'skills'), path.join(cwd, '.claude', 'skills'), { overwrite: true });

  const githubSrc = path.join(farmRoot, 'examples', moduleName, '.github');
  if (fs.existsSync(githubSrc)) {
    copyDir(path.join(githubSrc, 'agents'), path.join(cwd, '.github', 'agents'), { overwrite: true });
    copyDir(path.join(githubSrc, 'skills'), path.join(cwd, '.github', 'skills'), { overwrite: true });
  }
}

// Reproduit la Phase 3 de farm-init : brainstorm interactif des modules optionnels.
async function brainstormModules({ farmRoot, cwd, prompter }) {
  const installed = [];
  console.log('\n== Modules optionnels ==\n');

  const hasDb = await prompter.confirm(
    'Avez-vous une base de données (PostgreSQL/MySQL) avec un backend Python ou Java ?',
    false,
  );
  if (hasDb) {
    const dbModule = await prompter.select('Quel langage backend ?', [
      { label: 'Python (FastAPI/Django + Supabase/Postgres) → stack-python-supabase', value: 'stack-python-supabase' },
      { label: 'Java (Spring Boot + Maven) → stack-java-spring', value: 'stack-java-spring' },
      { label: 'Autre / Node+Prisma (déjà couvert par les skills schema/migrate du socle)', value: null },
    ]);
    if (dbModule) installed.push(dbModule);
  }

  const hasFrontend = await prompter.confirm('Le projet a-t-il un frontend React/Vite ?', false);
  if (hasFrontend) installed.push('stack-web-vite');

  const isI18n = await prompter.confirm("L'application est-elle multilingue ?", false);
  if (isI18n) installed.push('feature-i18n');

  const wantsDecisions = await prompter.confirm(
    'Voulez-vous capturer les décisions architecturales importantes (ADR légers, sans infra) ?',
    false,
  );
  if (wantsDecisions) installed.push('feature-decision-index');

  const wantsKm = await prompter.confirm(
    "Avez-vous besoin d'une documentation structurée pilotée par agents (KM/wiki/ADR complets) ?",
    false,
  );
  if (wantsKm) installed.push('km-toolkit');

  const wantsFinops = await prompter.confirm(
    'Travaillez-vous avec plusieurs agents en parallèle ou des tâches longues (contrôle des coûts token) ?',
    true,
  );
  if (wantsFinops) installed.push('finops');

  for (const mod of installed) {
    installModule(farmRoot, cwd, mod);
    console.log(`  ✅ Module installé : ${mod}`);
    if (mod === 'km-toolkit') {
      console.log(
        '     ⚠️  Agents/skills copiés. Le branchement MkDocs (hooks.py) n\'est pas automatisé —' +
          ' voir examples/km-toolkit/INSTALL.md étape 2.',
      );
    }
  }

  if (installed.length === 0) {
    console.log('  (aucun module optionnel — le socle générique suffit pour démarrer)');
  }

  return installed;
}

module.exports = { brainstormModules, installModule };
