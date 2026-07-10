---
name: mf-crud-matrix
description: Matrice CRUD programmes × tables/fichiers — qui crée, lit, met à jour, supprime quoi. Socle des analyses d'impact et de la documentation par domaine.
allowed-tools: Agent
---

Lance la génération de la matrice CRUD via l'agent `mf-crud-matrix`.

Utilise l'outil Agent avec `subagent_type: mf-crud-matrix`, en lui transmettant :
- un prompt demandant de construire la matrice CRUD entre programmes et ressources de données

L'agent produit :
- Détection des opérations par type : READ/WRITE/REWRITE/DELETE (fichiers VSAM), SELECT/INSERT/UPDATE/DELETE (SQL DB2), GET/PUT (files séquentielles)
- Matrice croisée programmes × tables/fichiers avec symboles C/R/U/D
- Identification des ressources accédées en écriture par plusieurs programmes (risques de contention)
- Export Markdown dans `docs/kb/docs/mf/crud-matrix.md`

Affiche les tables/fichiers les plus modifiés et les programmes avec le plus grand périmètre d'accès.
