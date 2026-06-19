---
name: scheduler-audit
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Audit tâches APScheduler - erreurs silencieuses, sessions BDD, jobs orphelins, retry, tests
---

Audit des tâches APScheduler - erreurs silencieuses, fuites de sessions BDD, jobs orphelins, observabilité via l'agent `scheduler-audit`.

Utilise l'outil Agent avec `subagent_type: scheduler-audit` pour auditer `scheduler_service.py` et sa couverture de tests.
