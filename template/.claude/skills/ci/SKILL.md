---
name: ci
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Revue CI/CD - jobs obsolètes, actions non pinnées, secrets, cohérence CLAUDE.md
---

Revue des pipelines CI/CD via l'agent `ci`.

Utilise l'outil Agent avec `subagent_type: ci` pour :
- Vérifier la cohérence des commandes CI avec CLAUDE.md
- Détecter les actions non pinnées et les problèmes de sécurité pipeline
- Identifier les secrets référencés non documentés
- Signaler les jobs obsolètes ou redondants
