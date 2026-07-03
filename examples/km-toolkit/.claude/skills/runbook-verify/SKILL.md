---
name: runbook-verify
description: Rejoue chaque runbook en dry-run — vérifie que les commandes, chemins et services nommés existent et sont cohérents. Marque les étapes cassées.
allowed-tools: task
---

Lance la vérification des runbooks via l'agent `runbook-verify`.

Utilise l'outil `task` avec :
- `agent_type: "runbook-verify"`
- un prompt demandant de vérifier tous les runbooks de `docs/kb/docs/runbooks/`

L'agent produit :
- Pour chaque runbook : statut (✅ valide / ⚠️ à vérifier / ❌ cassé)
- Étapes dont les commandes ou chemins sont invalides
- Rapport dans `docs/kb/docs/runbooks/verification-report.md`

Affiche le résumé de vérification.
