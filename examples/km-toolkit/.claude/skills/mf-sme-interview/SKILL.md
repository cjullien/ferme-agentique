---
name: mf-sme-interview
description: Prépare et conduit l'interview d'un expert métier avant son départ — questions générées depuis la cartographie (zones denses, code sans doc, anomalies), réponses rangées dans les fiches.
allowed-tools: Agent
---

Lance la préparation d'interview expert via l'agent `mf-sme-interview`.

Utilise l'outil Agent avec `subagent_type: mf-sme-interview`, en lui transmettant :
- un prompt précisant le domaine ou les programmes à couvrir (ou "tous les programmes à risque")

L'agent produit :
- Guide d'interview structuré depuis l'anomaly-map et les fiches programme
- Questions ciblées sur les zones sans documentation ou à fort risque
- Template de capture des réponses dans les fiches programme correspondantes

Affiche le guide d'interview prêt à utiliser.
