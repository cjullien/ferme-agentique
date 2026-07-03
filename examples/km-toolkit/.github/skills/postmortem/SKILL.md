---
name: postmortem
description: Post-mortem structuré après un incident — produit la timeline, les causes, les actions correctives et directement la page runbook/troubleshooting correspondante dans la KB.
allowed-tools: task
---

Lance la rédaction du post-mortem via l'agent `postmortem`.

Utilise l'outil `task` avec :
- `agent_type: "postmortem"`
- un prompt décrivant l'incident (symptômes, date, impact, ce qui a été fait pour résoudre)

L'agent produit :
- Un post-mortem structuré (timeline, cause racine, actions correctives)
- Une page runbook/troubleshooting dans `docs/kb/docs/runbooks/`
- Les actions de suivi sous forme de tâches

Affiche le post-mortem et le chemin de la page runbook créée.
