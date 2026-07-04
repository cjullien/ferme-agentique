---
name: record
description: Capture une décision architecturale ou technique et l'écrit dans .decisions/ au format Markdown. Utiliser après avoir pris une décision importante (choix de stack, pattern architectural, contrainte transverse).
allowed-tools: Agent
---

Lance la capture de décision via l'agent `decision-record`.

Utilise l'outil Agent avec `subagent_type: decision-record` en passant la description de la décision : contexte, options envisagées, choix retenu, raison.
