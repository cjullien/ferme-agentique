---
name: test
description: Lance tests backend et frontend en parallèle avec résumé
disable-model-invocation: true
---

Lance les tests backend et frontend en parallèle (commandes identifiées via CLAUDE.md), puis affiche un résumé des résultats.

Si un argument est fourni, cibler uniquement ce fichier ou module : $ARGUMENTS

Exemples : `/test tests/test_users.py`, `/test backend`, `/test frontend`

Sans argument, lance simultanément :
- Commande de test backend (identifiée via CLAUDE.md)
- Commande de test frontend (identifiée via CLAUDE.md)

Affiche le nombre de tests passés / échoués pour chaque suite.
