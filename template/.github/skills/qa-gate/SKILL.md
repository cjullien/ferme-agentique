---
name: qa-gate
description: Gate qualité formel avant merge — traçabilité critères d'acceptation/tests, profil de risque, verdict PASS/CONCERNS/FAIL/WAIVED.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

Lance l'agent `qa-gate` sur la story ou feature ciblée : $ARGUMENTS (ex: ID de story, ou vide
pour le diff courant).

Utilise l'outil Agent avec `subagent_type: qa-gate`. À lancer typiquement après `/review`,
avant de considérer une story terminée — pas à chaque commit (voir `/review` pour une revue
plus légère et systématique).
