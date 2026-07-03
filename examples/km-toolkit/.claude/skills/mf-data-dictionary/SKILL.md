---
name: mf-data-dictionary
description: Dictionnaire de données généré depuis les copybooks — structures, PIC, REDEFINES, OCCURS, valeurs 88. Croisé avec les DCLGEN DB2 et layouts VSAM. Chaque champ pointe vers ses programmes lecteurs/écrivains.
allowed-tools: task
---

Lance la génération du dictionnaire de données via l'agent `mf-data-dictionary`.

Utilise l'outil `task` avec :
- `agent_type: "mf-data-dictionary"`
- un prompt demandant de générer le dictionnaire de données depuis les copybooks et DCLGEN disponibles

L'agent produit :
- Extraction de toutes les structures de données (niveaux 01 à 88)
- Décodage des clauses PIC (type, longueur, décimales)
- Résolution des REDEFINES et OCCURS
- Valeurs et sens des niveaux 88 (flags, codes état)
- Croisement avec les DCLGEN DB2 et layouts VSAM
- Index des programmes qui lisent/écrivent chaque champ
- Dictionnaire dans `docs/kb/docs/mf/data-dictionary.md`

Affiche les structures les plus référencées et les champs sans documentation.
