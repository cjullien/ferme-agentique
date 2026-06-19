---
name: push
description: Pousse la branche courante après tests réussis
disable-model-invocation: true
---

Pousse la branche courante vers le dépôt distant après vérification complète.

## Étapes

1. **Tests** — Lance les tests backend et frontend en parallèle (commandes identifiées via CLAUDE.md) :
   - Commande de test backend (identifiée via CLAUDE.md)
   - Commande de test frontend (identifiée via CLAUDE.md)

   Si des tests échouent → **arrêter ici**, afficher les erreurs et indiquer `❌ Push annulé — tests en échec`.

2. **État git** — Vérifie l'état du working tree (`git status`).
   - S'il y a des fichiers modifiés non committés → **signaler en avertissement** mais continuer.
   - S'il n'y a aucun commit à pousser (`nothing to push`) → l'indiquer et s'arrêter.

3. **Push** — Lance `git push` et affiche le résultat.

## Règles
- Ne jamais utiliser `--force` sauf si explicitement demandé
- Ne jamais pousser directement sur `main` sans confirmation de l'utilisateur
- Si le push est rejeté (non fast-forward), proposer un `git pull --rebase` mais ne pas l'exécuter automatiquement
