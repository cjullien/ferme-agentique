---
name: mf-data-lineage
description: Suit un champ de données à travers les MOVE/COMPUTE entre programmes, fichiers et tables — "d'où vient cette valeur ?". Produit un diagramme de flux par champ critique.
allowed-tools: Agent
---

Lance le traçage du lignage de données via l'agent `mf-data-lineage`.

Utilise l'outil Agent avec `subagent_type: mf-data-lineage`, en lui transmettant :
- un prompt précisant le champ à tracer (ex: "trace CLI-MONTANT depuis sa source jusqu'à sa sortie")

L'agent produit :
- Séquence des MOVE/COMPUTE impliquant le champ à travers les programmes
- Diagramme de flux dans `docs/kb/docs/mf/lineage/<CHAMP>.md`
- Transformations appliquées à chaque étape

Affiche le lignage et le chemin du diagramme généré.
