---
name: push
description: Committe puis pousse la branche courante, après tests réussis par défaut (--skip-tests pour pousser immédiatement)
disable-model-invocation: true
---

Committe les changements en cours puis pousse la branche courante vers le dépôt distant.

Argument (optionnel) : $ARGUMENTS — `--skip-tests` pour committer et pousser immédiatement
sans lancer les tests (à réserver aux changements déjà validés autrement, ex: doc seule).

## Étapes

1. **Commit** — Exécute `/commit` pour stager et committer les fichiers modifiés. Si aucun
   changement à committer, passer directement à l'étape suivante.

2. **Tests** (sautée si `--skip-tests`) — Lance les tests backend et frontend en parallèle
   (commandes identifiées via CLAUDE.md).

   Si des tests échouent → **arrêter ici**, afficher les erreurs et indiquer `❌ Push annulé — tests en échec`.

3. **État git** — Vérifie l'état du working tree (`git status`).
   - S'il y a des fichiers modifiés non committés → **signaler en avertissement** mais continuer.
   - S'il n'y a aucun commit à pousser (`nothing to push`) → l'indiquer et s'arrêter.

4. **Push** — Lance `git push` et affiche le résultat.

## Règles
- `--skip-tests` ne saute que l'étape 2 (tests) — il ne concerne pas `git push --force`
- Ne jamais utiliser `git push --force` sauf si explicitement demandé par l'utilisateur
- Ne jamais pousser directement sur `main` sans confirmation de l'utilisateur
- Si le push est rejeté (non fast-forward), proposer un `git pull --rebase` mais ne pas l'exécuter automatiquement
