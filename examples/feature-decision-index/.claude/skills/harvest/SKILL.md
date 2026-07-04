---
name: harvest
description: Scanne le codebase pour détecter les décisions architecturales implicites (commentaires, commits, config) et propose de les formaliser dans .decisions/. À lancer en début de projet ou après reprise d'un existant.
allowed-tools: Agent
---

Lance la récolte de décisions implicites via l'agent `decision-harvest`.

Utilise l'outil Agent avec `subagent_type: decision-harvest` pour scanner le codebase (commentaires, git log, fichiers de config) et proposer les décisions non encore capturées.
