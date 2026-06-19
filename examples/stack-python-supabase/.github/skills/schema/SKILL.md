---
name: schema
description: Analyse l'impact d'une modification de modèle de données - liste les fichiers à mettre à jour
allowed-tools: Agent, Read, Grep, Glob, Bash
disable-model-invocation: true
---

Lance une analyse d'impact de schéma via l'agent `schema`.

Utilise l'outil Agent avec `subagent_type: schema` pour analyser l'impact d'une modification de modèle de données avant de toucher au code. L'agent liste tous les fichiers à mettre à jour (migrations, schémas de validation, services, frontend, fixtures, seeds, i18n).
