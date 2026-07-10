---
name: design-system
description: Audit et application du design system frontend — cohérence visuelle et patterns d'interface par rapport aux conventions établies de ce projet.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

Lance un audit design system via l'agent `design-system`.

L'agent `design-system` du socle (`template/.claude/agents/design-system.md`) est un
squelette générique : sa section "Périmètre à instancier" doit être complétée une fois, avec
l'IA, à partir des conventions réelles de ce projet (voir la procédure décrite dans l'agent).
Un exemple entièrement complété est disponible dans
`examples/domain-immo/.claude/agents/design-system.md`.

Une fois complété, ce skill déclenche l'agent avec le périmètre demandé (fichier/dossier
ciblé, ou tout le frontend par défaut) et restitue les findings classés par sévérité
(🔴/🟠/🟡) ainsi que le résultat des corrections appliquées.
