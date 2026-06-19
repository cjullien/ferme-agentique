---
name: mf-inventory
description: Inventaire exhaustif du patrimoine mainframe — programmes COBOL, copybooks, JCL, transactions CICS, tables DB2, fichiers VSAM. Détecte les sources manquantes. Préalable obligatoire à tout autre skill mf-*.
allowed-tools: task
---

Lance l'inventaire du patrimoine mainframe via l'agent `mf-inventory`.

Utilise l'outil `task` avec :
- `agent_type: "mf-inventory"`
- un prompt demandant d'inventorier tout le patrimoine mainframe disponible dans le répertoire courant

L'agent produit :
- Comptage et classification de chaque type de source (COBOL, copybook, JCL, CICS, DB2, VSAM)
- Détection des modules appelés sans source disponible
- Rapport d'inventaire structuré en `docs/kb/docs/mf/inventory.md`

Affiche le résumé de l'inventaire.
