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

> Note : les modules `stack-java-spring` et `stack-python-supabase` embarquent chacun leur propre agent `backlog-refinement`, adapté à leur stack (chiffrage informé par les modèles/migrations). S'il est installé dans `.claude/agents/backlog-refinement.md`, l'utiliser à la place de `backlog-manager` — il est plus spécialisé pour ce projet.