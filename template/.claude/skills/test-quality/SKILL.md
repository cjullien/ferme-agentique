---
name: test-quality
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Audit qualité des tests — pertinence, pyramide, couverture, anti-patterns
---

Lance un audit complet de la qualité des tests via l'agent `test-quality`.

Utilise l'outil Agent avec `subagent_type: test-quality` pour analyser la suite de tests du projet.
