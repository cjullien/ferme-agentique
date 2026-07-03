---
name: docs-update
description: Met à jour la documentation du projet pour rester cohérente avec l'application, via l'agent `docs-update`.
allowed-tools: task
---

Lance une mise à jour documentaire via l'agent `docs-update`.

Utilise l'outil `task` avec :
- `agent_type: "docs-update"`
- `name: "docs-update-run"`
- un prompt demandant d'analyser les changements en cours et de corriger les sections documentaires devenues inexactes

Si l'utilisateur précise un périmètre (ex: README uniquement), transmets cette contrainte dans le prompt de l'agent.
