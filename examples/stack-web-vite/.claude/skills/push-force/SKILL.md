---
name: push-force
description: Committe puis pousse immédiatement sans lancer les tests
disable-model-invocation: true
---

Committe les changements en cours puis pousse immédiatement, sans lancer les tests.

## Étapes

1. **Commit** — Exécute `/commit` pour stager et committer les fichiers modifiés.
   Si aucun changement à committer, passer directement à l'étape 2.

2. **Push** — Lance `git push` et affiche le résultat.

## Règles
- Ne jamais utiliser `--force`
- Ne jamais pousser sur `main` sans confirmation de l'utilisateur
- Si le push est rejeté (non fast-forward), proposer un `git pull --rebase` mais ne pas l'exécuter automatiquement
