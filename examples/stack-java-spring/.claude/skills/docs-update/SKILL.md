---
name: docs-update
description: Met à jour la documentation en cohérence avec le code actuel.
---

Lance l'agent `docs-update`.

Utilise l'outil Agent avec `subagent_type: docs-update` pour aligner la doc (`README.md`, `CLAUDE.md`, `DOCKER.md`, `docs/specs/*`) avec le code réel : modules, endpoints, variables d'env, commandes Maven (profils déclarés dans `CLAUDE.md`), images Docker. Éditions ciblées.
