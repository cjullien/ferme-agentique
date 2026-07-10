---
name: story-writer
description: Transforme un item de backlog ou une spec en stories auto-suffisantes (contexte spec + architecture embarqué) via l'agent story-writer.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

Lance l'agent `story-writer`.

Cible (optionnel) : $ARGUMENTS — ex: `/story-writer A11Y-5`, `/story-writer P1` (toute la
priorité P1 du backlog), ou une description de feature directement.

Utilise l'outil Agent avec `subagent_type: story-writer` en transmettant la cible. Sans
argument, demander à l'utilisateur quel(s) item(s) traiter.
