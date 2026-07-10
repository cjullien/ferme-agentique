---
name: backlog-refinement
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
description: Refinement du backlog - mode simple (brainstorming + repriorisation) ou avancé (réévaluation par le code)
---

Lance un refinement du backlog via l'agent `backlog-manager` (agent de gestion de backlog du socle).

**Mode simple** (défaut) - brainstorming et repriorisation, sans relire le code :
```
/backlog-refinement
```
Demander à l'agent `backlog-manager` de faire uniquement les Phases 1 (audit du fichier backlog) et 2 (priorisation) de son workflow standard, sans grep du code source.

**Mode avancé** - réévaluation des chiffrages et détection de nouveaux items par analyse du code :
```
/backlog-refinement --avancé
```
Demander à l'agent `backlog-manager` de dérouler l'intégralité de son workflow standard (Phases 1 à 3), y compris le grep du code source (TODO/FIXME) et la mise à jour de `docs/specs/backlog.md`.

Utilise l'outil Agent avec `subagent_type: backlog-manager` en transmettant le mode et les arguments fournis par l'utilisateur.

> Les modules `stack-java-spring` et `stack-python-supabase` embarquent chacun une variante de
> `backlog-manager` adaptée à leur stack (chiffrage informé par les modèles/migrations/build).
> Comme ils portent le même nom, ils **surchargent automatiquement** la version générique du
> socle à l'installation — aucune action supplémentaire n'est nécessaire.