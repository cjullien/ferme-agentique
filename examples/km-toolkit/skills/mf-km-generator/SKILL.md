---
name: mf-km-generator
description: Orchestre la génération complète de la KB mainframe — inventaire, graphe d'appels, fiches programme, dictionnaire, règles métier — par vagues priorisées. ~90% de pages générées, ~10% rédigées.
allowed-tools: task
---

Lance la génération orchestrée de la KB mainframe via l'agent `mf-km-generator`.

Utilise l'outil `task` avec :
- `agent_type: "mf-km-generator"`
- un prompt demandant de générer la base de connaissances complète du patrimoine mainframe

L'agent orchestre les vagues dans l'ordre :
1. Inventaire (`mf-inventory`) — ce qui existe
2. Cartographie (`mf-callgraph`, `mf-batch-map`) — le graphe structure tout
3. Anomaly map (`mf-anomaly-map`) — pour prioriser les vagues suivantes
4. Référence (`mf-program-card`, `mf-data-dictionary`, `mf-crud-matrix`) — par lots priorisés par centralité
5. Règles métier (`mf-business-rules`) — sur les programmes à fort score de risque
6. Synthèses rédigées — onboarding, concepts par domaine, ADR

La KB produite dans `docs/kb/docs/mf/` est régénérable sans perdre les enrichissements manuels.

Affiche l'avancement par vague et le ratio pages générées / pages rédigées.
