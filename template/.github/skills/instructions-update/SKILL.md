---
name: instructions-update
description: Maintient la cohérence entre CLAUDE.md, agents et commandes
---

Met à jour les instructions Claude, agents et commandes via l'agent `agent-maintainer`.

Utilise l'outil Agent avec `subagent_type: agent-maintainer` pour analyser la cohérence de la couche d'orchestration et corriger les incohérences détectées.

Si l'utilisateur demande un sous-ensemble (ex: uniquement les agents), transmets cette contrainte dans le prompt de l'agent.
