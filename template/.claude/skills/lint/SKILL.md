---
name: lint
description: Lance le linter backend (identifié via CLAUDE.md)
disable-model-invocation: true
---

Lance le linting du backend.

Cible (optionnelle) : $ARGUMENTS — ex: `/lint app/routers/`

Sans argument, analyse tout :
1. Identifier la commande de lint via CLAUDE.md (ex: `ruff check`, `eslint`, `golangci-lint`)
2. Si des erreurs auto-fixables : proposer la commande de fix automatique
3. Lancer le formatteur (ex: `ruff format --check`, `prettier --check`) — signaler les fichiers mal formatés

Affiche le résumé : nombre d'erreurs par catégorie, fichiers à corriger.
