---
name: ux-ui
description: Audit et amélioration UX/UI du frontend — cohérence visuelle, ergonomie, micro-interactions, par rapport aux conventions établies de ce projet.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

Lance un audit UX/UI complet via l'agent `ux-ui`.

L'agent `ux-ui` du socle (`template/.claude/agents/ux-ui.md`) est un squelette générique : sa
section "Périmètre à instancier" doit être complétée une fois, avec l'IA, à partir des
conventions réelles de ce projet (voir la procédure décrite dans l'agent). Un exemple
entièrement complété est disponible dans `examples/domain-immo/.claude/agents/ux-ui.md`.

Une fois complété, ce skill déclenche l'agent avec le périmètre demandé (composant, page, ou
tout le frontend par défaut) et restitue les findings classés par sévérité (🔴/🟠/🟡) ainsi
que le résultat des corrections appliquées.
