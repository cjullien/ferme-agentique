---
name: backlog-refinement
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
description: Refinement du backlog - mode simple (brainstorming + repriorisation) ou avancé (réévaluation par le code)
---

Lance un refinement du backlog via l'agent `backlog-refinement`.

**Mode simple** (défaut) - brainstorming et repriorisation :
```
/backlog-refinement
```

**Mode avancé** - réévaluation des chiffrages et détection de nouveaux items par analyse du code :
```
/backlog-refinement --avancé
```

Utilise l'outil Agent avec `subagent_type: backlog-refinement` en transmettant les arguments fournis par l'utilisateur.