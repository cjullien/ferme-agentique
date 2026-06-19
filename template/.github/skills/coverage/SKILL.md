---
name: coverage
description: Rapport de couverture de tests backend et frontend
disable-model-invocation: true
---

Génère un rapport de couverture de tests en local.

Cible (optionnelle) : $ARGUMENTS — ex: `/coverage backend`, `/coverage frontend`

Sans argument, lance en parallèle :
- Commande de couverture backend (identifiée via CLAUDE.md, ex: `pytest --cov`, `go test -cover`, etc.)
- Commande de couverture frontend (identifiée via CLAUDE.md, ex: `vitest --coverage`, `jest --coverage`, etc.)

Affiche un résumé :
- Couverture globale backend (%) + fichiers sous 80%
- Couverture globale frontend (%) + fichiers sous 80%
