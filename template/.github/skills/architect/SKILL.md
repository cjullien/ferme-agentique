---
name: architect
description: Conçoit ou documente l'architecture technique du projet (docs/ARCHITECTURE.md) — nouveau projet, nouvelle feature, ou rétro-documentation d'un existant.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

Lance l'agent `architect`.

Utilise l'outil Agent avec `subagent_type: architect` en précisant le mode :
- `/architect` sans `docs/ARCHITECTURE.md` existant → mode nouveau projet (session de questions
  puis rédaction complète)
- `/architect <description de la feature>` avec `docs/ARCHITECTURE.md` existant → mode
  extension ciblée
- `/architect --existant` sur un projet sans `docs/ARCHITECTURE.md` mais avec du code déjà
  écrit → mode rétro-documentation

Argument (optionnel) : $ARGUMENTS
