---
name: commit
description: Prépare et crée un commit git en conventional commits format (type, scope, description en français)
disable-model-invocation: true
---

Prépare et crée un commit git avec message en conventional commits format.

Procédure :

1. Lancer `git --no-pager diff --staged` et `git --no-pager status` pour voir les changements
2. Si rien de stagé, lancer `git --no-pager diff HEAD` et demander confirmation pour stager les fichiers pertinents (exclure .env, secrets, fichiers générés)
3. Analyser les changements et déterminer :

   - **Type** : `feat` (nouvelle fonctionnalité) | `fix` (correction de bug) | `refactor` (refactoring sans changement fonctionnel) | `test` (ajout/modification de tests) | `docs` (documentation) | `chore` (maintenance, dépendances) | `perf` (performance) | `style` (formatage)
   - **Scope** : module ou domaine fonctionnel principal impacté (ex: `leases`, `auth`, `frontend`, `deps`)
   - **Breaking change** : y a-t-il un changement incompatible avec les versions précédentes ?
4. Proposer un message de commit au format :

   ```
   type(scope): description courte en impératif présent

   [Corps optionnel si changement complexe : expliquer le POURQUOI, pas le QUOI]

   [BREAKING CHANGE: description si applicable]
   ```
5. Demander confirmation avant de créer le commit
6. Créer le commit avec `git commit -m "message"`

Règles :

- Description en français, max 72 caractères
- Impératif présent : "ajoute" pas "ajouté" ni "ajout de"
- Ne jamais committer : .env, fichiers de credentials, fichiers générés (migrations auto, dist/)
