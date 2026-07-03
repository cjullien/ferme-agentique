---
name: doc-coverage
description: Mesure la couverture documentaire comme une couverture de tests — composants sans page concept, how-to ni runbook, trous priorisés par criticité (fan-in).
allowed-tools: task
---

Lance l'audit de couverture documentaire via l'agent `doc-coverage`.

Utilise l'outil `task` avec :
- `agent_type: "doc-coverage"`
- un prompt demandant de mesurer la couverture documentaire du projet

L'agent produit :
- Score de couverture global (% de composants documentés)
- Liste des composants sans documentation, triés par criticité
- Recommandations priorisées

Affiche le rapport de couverture.
