---
name: perf
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Analyse performance — N+1, index manquants, pagination absente, re-renders, bundle frontend
---

Lance une analyse de performance via l'agent `performance`.

Utilise l'outil Agent avec `subagent_type: performance` pour analyser backend et frontend :
- Backend : requêtes N+1, index manquants, endpoints sans pagination, calculs répétés
- Frontend : re-renders inutiles, imports non optimisés, appels API redondants
