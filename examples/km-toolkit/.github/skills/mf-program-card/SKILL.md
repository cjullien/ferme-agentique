---
name: mf-program-card
description: Génère les fiches d'identité de programmes COBOL — rôle déduit, entrées/sorties, appelants/appelés, tables accédées, volumétrie. Unité atomique de la KB mainframe, générée par lots.
allowed-tools: Agent
---

Lance la génération des fiches programme via l'agent `mf-program-card`.

Utilise l'outil Agent avec `subagent_type: mf-program-card`, en lui transmettant :
- un prompt demandant de générer les fiches d'identité pour tous les programmes COBOL (ou un sous-ensemble si précisé)

L'agent produit pour chaque programme :
- Rôle déduit depuis les commentaires d'en-tête et la structure du code
- Entrées/sorties (fichiers, tables DB2, paramètres LINKAGE)
- Appelants et appelés (depuis le graphe mf-callgraph si disponible)
- Dernière modification (depuis les cartouches d'en-tête ou l'historique SCM)
- Fiches générées dans `docs/kb/docs/mf/programs/<NOM>.md`

Affiche le nombre de fiches générées et les programmes sans commentaires d'en-tête.
