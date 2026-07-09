---
name: mf-anomaly-map
description: Carte des zones à risque documentaire — programmes très appelés jamais modifiés, GO TO denses, code mort probable, sections démesurées. Priorise où l'effort de documentation est vital.
allowed-tools: Agent
---

Lance la détection des anomalies via l'agent `mf-anomaly-map`.

Utilise l'outil Agent avec `subagent_type: mf-anomaly-map`, en lui transmettant :
- un prompt demandant de cartographier les zones à risque du patrimoine COBOL

L'agent détecte et signale :
- Programmes très appelés (centralité élevée dans le graphe) sans modification récente
- Densité de GO TO (spaghetti code) par programme
- Code mort probable : sections jamais référencées en JCL ni en CICS
- Sections démesurées (nombre de lignes hors normes)
- Programmes sans commentaires d'en-tête ni documentation
- Score de risque documentaire par programme (0-100)
- Carte dans `docs/kb/docs/mf/anomaly-map.md` triée par criticité

Affiche le top 10 des programmes à documenter en priorité.
