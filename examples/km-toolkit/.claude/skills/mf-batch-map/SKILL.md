---
name: mf-batch-map
description: Cartographie des chaînes batch — jobs, steps, dépendances par datasets, fenêtres batch, points de reprise. Un diagramme par chaîne critique.
allowed-tools: task
---

Lance la cartographie des chaînes batch via l'agent `mf-batch-map`.

Utilise l'outil `task` avec :
- `agent_type: "mf-batch-map"`
- un prompt demandant de cartographier toutes les chaînes batch depuis les JCL disponibles

L'agent produit :
- Identification des jobs et steps
- Dépendances entre jobs via datasets partagés (GDG, fichiers séquentiels)
- Fenêtres batch et contraintes d'ordonnancement (Control-M/TWS si présent)
- Points de reprise (RESTART, CHECKPOINT)
- Un diagramme Mermaid par chaîne critique dans `docs/kb/docs/mf/batch/`

Affiche la liste des chaînes détectées et les dépendances critiques.
