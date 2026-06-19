---
name: schema-impact
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Analyse l'impact d'une modification de modèle de données - liste les fichiers à mettre à jour
---

Lance une analyse d'impact via l'agent `schema`.

Utilise l'outil Agent avec `subagent_type: schema` pour analyser l'impact d'une modification de modèle de données avant de toucher au code.
