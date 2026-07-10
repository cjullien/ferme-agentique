---
name: deps
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Audit dépendances — CVE (pip-audit/npm audit), versions obsolètes, packages inutilisés
---

Audit de santé des dépendances via l'agent `dependencies`.

Utilise l'outil Agent avec `subagent_type: dependencies` pour :
- Lancer l'outil d'audit CVE de chaque écosystème détecté (ex: pip-audit, npm audit, OWASP Dependency-Check, govulncheck, cargo audit — voir l'agent pour la liste complète)
- Signaler les CVE par sévérité avec version de fix disponible
- Identifier les versions majeures disponibles pour les dépendances critiques
- Détecter les dépendances potentiellement inutilisées
