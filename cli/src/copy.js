'use strict';

const fs = require('node:fs');
const path = require('node:path');

// Copie récursive. overwrite:false reproduit le comportement `cp -n` de INSTALL.md
// (ne jamais écraser un settings.json / CLAUDE.md déjà présent sur le projet cible).
function copyDir(src, dest, { overwrite = true } = {}) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(s, d, { overwrite });
    } else if (overwrite || !fs.existsSync(d)) {
      fs.copyFileSync(s, d);
    }
  }
}

function copyFile(src, dest, { overwrite = true } = {}) {
  if (!fs.existsSync(src)) return false;
  if (!overwrite && fs.existsSync(dest)) return false;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  return true;
}

module.exports = { copyDir, copyFile };
