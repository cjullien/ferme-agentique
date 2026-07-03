---
name: adr-capture
description: Transforme une décision technique prise en session ou en revue en ADR au format MADR, liée aux pages concept concernées de la KB.
allowed-tools: task
---

Lance la capture d'une décision via l'agent `adr-capture`.

Utilise l'outil `task` avec :
- `agent_type: "adr-capture"`
- un prompt décrivant la décision prise (contexte, options envisagées, choix retenu, raison)

L'agent produit une ADR au format MADR dans `docs/kb/docs/adr/` et met à jour l'index.

Affiche l'ADR générée.
