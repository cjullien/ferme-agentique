'use strict';

const fs = require('node:fs');

// Reproduit la Phase 2 de farm-init : remplace les {{placeholders}} de
// template/CLAUDE.template.md par les réponses de l'utilisateur.
// Couplé au contenu actuel de CLAUDE.template.md — si le squelette évolue,
// mettre à jour ces motifs en conséquence.
async function fillClaudeMdFields(claudeMdPath, prompter) {
  if (!fs.existsSync(claudeMdPath)) return;
  let content = fs.readFileSync(claudeMdPath, 'utf8');

  const projectName = await prompter.ask('Nom du projet');
  content = content.replaceAll('{{NOM_DU_PROJET}}', projectName || 'Projet');

  const singleLineFields = [
    { re: /\{\{ex: Node 20[^}]*\}\}/, question: 'Langage / runtime (ex: Node 20, Python 3.12, Java 21, Go 1.22)' },
    { re: /\{\{ex: Vite \+ React[^}]*\}\}/, question: 'Framework (ex: Vite + React, FastAPI, Spring Boot, Gin, aucun)' },
    { re: /\{\{ex: Vitest[^}]*\}\}/, question: 'Outil de tests (ex: Vitest, pytest, JUnit, go test)' },
    { re: /\{\{ex: aucune \/ PostgreSQL[^}]*\}\}/, question: 'Base de données (ex: aucune, PostgreSQL, SQLite, MongoDB)' },
    { re: /\{\{ex: npm \/ Maven[^}]*\}\}/, question: 'Build / packaging (ex: npm, Maven, Gradle, cargo, docker)' },
    { re: /\{\{commande pour lancer l'app localement\}\}/, question: 'Commande dev / run' },
    { re: /\{\{commande de build\}\}/, question: 'Commande de build' },
    { re: /\{\{commande de lint\}\}/, question: 'Commande de lint' },
    { re: /\{\{commande de test\}\}/, question: 'Commande de tests unitaires' },
    {
      re: /\{\{commande e2e — supprimer si absent\}\}/,
      question: 'Commande de tests e2e (laisser vide si absent)',
      removeLineIfEmpty: true,
    },
    {
      re: /\{\{décrire brièvement l'arborescence clé du projet\}\}/,
      question: "Arborescence clé du projet (une ligne)",
    },
  ];

  for (const field of singleLineFields) {
    if (!field.re.test(content)) continue;
    const answer = await prompter.ask(field.question);
    if (field.removeLineIfEmpty && !answer) {
      content = content.replace(new RegExp(`^.*${field.re.source}.*\\n`, 'm'), '');
    } else {
      content = content.replace(field.re, answer || '(non renseigné)');
    }
  }

  const conventionQuestions = [
    'Convention de nommage (fichiers / fonctions / classes) — vide pour ignorer',
    'Règles de commit et de branches — vide pour ignorer',
    'Style (ex: ne jamais ..., toujours ...) — vide pour ignorer',
    'Contraintes spécifiques au projet ou à la stack — vide pour ignorer',
  ];
  for (const question of conventionQuestions) {
    const bulletRe = /^- \{\{[^}]*\}\}\n/m;
    if (!bulletRe.test(content)) break;
    const answer = await prompter.ask(question);
    content = content.replace(bulletRe, answer ? `- ${answer}\n` : '');
  }

  fs.writeFileSync(claudeMdPath, content, 'utf8');
}

const MODULE_CHECKBOX_PATTERNS = {
  'stack-python-supabase': /^- \[ \] DB \/ migrations.*\n/m,
  'stack-java-spring': /^- \[ \] DB \/ migrations.*\n/m,
  'stack-web-vite': /^- \[ \] Frontend React\/Vite.*\n/m,
  'feature-i18n': /^- \[ \] i18n.*\n/m,
  'feature-decision-index': /^- \[ \] Mémoire décisionnelle.*\n/m,
  'km-toolkit': /^- \[ \] KM \/ documentation.*\n/m,
};

// Phase 3 (suite) : coche les modules effectivement installés dans le
// checklist "Agents & skills installés" de CLAUDE.md.
function checkModuleBoxes(claudeMdPath, installedModules) {
  if (!fs.existsSync(claudeMdPath)) return;
  let content = fs.readFileSync(claudeMdPath, 'utf8');

  for (const mod of installedModules) {
    const re = MODULE_CHECKBOX_PATTERNS[mod];
    if (!re) continue;
    content = content.replace(re, (line) => line.replace('[ ]', '[x]'));
  }

  fs.writeFileSync(claudeMdPath, content, 'utf8');
}

module.exports = { fillClaudeMdFields, checkModuleBoxes };
