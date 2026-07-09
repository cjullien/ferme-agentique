---
name: session-digest
description: Extrait le savoir opératoire d'une session de travail complexe — pièges découverts, procédures validées, comportements non documentés. À lancer en fin de session de diagnostic ou de refactoring.
allowed-tools: Agent
---

Lance l'extraction du savoir de session via l'agent `session-digest`.

Utilise l'outil Agent avec `subagent_type: session-digest`, en lui transmettant :
- un prompt résumant ce qui a été fait dans la session (ou demandant à l'agent de relire l'historique)

L'agent produit :
- Les pièges et comportements non documentés découverts
- Les procédures validées (étapes reproductibles)
- Les enrichissements à injecter dans les fiches programme ou pages concept concernées

Affiche le digest et les pages KB à mettre à jour.
