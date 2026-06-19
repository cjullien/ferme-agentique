---
name: mf-callgraph
description: Graphe d'appels complet du patrimoine COBOL — CALL statiques et dynamiques, COPY/INCLUDE, liens JCL→programme. Produit une vue agrégée par domaine et une page interactive filtrable.
allowed-tools: task
---

Lance la génération du graphe d'appels via l'agent `mf-callgraph`.

Utilise l'outil `task` avec :
- `agent_type: "mf-callgraph"`
- un prompt demandant de construire le graphe d'appels complet du patrimoine COBOL

L'agent produit :
- Résolution des CALL statiques et dynamiques (noms de programme variables)
- Liens COPY/INCLUDE entre programmes et copybooks
- Liens JCL→programme via EXEC PGM=
- Vue agrégée par domaine fonctionnel
- Fichier Mermaid/DOT exporté dans `docs/kb/docs/mf/callgraph.md`

Affiche le résumé du graphe (noeuds, arcs, domaines détectés).
