'use strict';

const readline = require('node:readline');
const { stdin: input, stdout: output } = require('node:process');

// readline/promises .question() se bloque sur les appels successifs quand
// stdin n'est pas un TTY (pipe/heredoc, notamment en test) : le premier
// appel résout, les suivants restent en attente indéfiniment. On lit donc
// les lignes via l'itérateur async de l'interface, qui fonctionne de façon
// identique en TTY et en pipe.
function createPrompter() {
  const rl = readline.createInterface({ input, output, terminal: false });
  const lines = rl[Symbol.asyncIterator]();

  async function nextLine() {
    const { value, done } = await lines.next();
    return done ? '' : value;
  }

  async function ask(question, defaultValue = '') {
    const suffix = defaultValue ? ` (${defaultValue})` : '';
    output.write(`${question}${suffix} : `);
    const answer = (await nextLine()).trim();
    return answer || defaultValue;
  }

  async function confirm(question, defaultYes = true) {
    const suffix = defaultYes ? '(O/n)' : '(o/N)';
    output.write(`${question} ${suffix} : `);
    const answer = (await nextLine()).trim().toLowerCase();
    if (!answer) return defaultYes;
    return answer === 'o' || answer === 'oui' || answer === 'y' || answer === 'yes';
  }

  async function select(question, choices) {
    console.log(question);
    choices.forEach((c, i) => console.log(`  ${i + 1}. ${c.label}`));
    output.write(`Choix (1-${choices.length}, vide = aucun) : `);
    const answer = (await nextLine()).trim();
    if (!answer) return null;
    const idx = Number.parseInt(answer, 10) - 1;
    if (Number.isInteger(idx) && idx >= 0 && idx < choices.length) return choices[idx].value;
    return null;
  }

  function close() {
    rl.close();
  }

  return { ask, confirm, select, close };
}

module.exports = { createPrompter };
