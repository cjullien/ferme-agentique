---
name: owasp
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Audit sécurité OWASP Top 10 (2021) sur backend et frontend
---

Lance un audit de sécurité complet via l'agent `owasp`.

Utilise l'outil Agent avec `subagent_type: owasp` en demandant explicitement :
- l'analyse complète du code source backend et frontend (chemins identifiés via CLAUDE.md),
- un rendu structuré par catégories OWASP Top 10 (2021),
- des findings localisés (`fichier:ligne`) avec sévérité et recommandation.
