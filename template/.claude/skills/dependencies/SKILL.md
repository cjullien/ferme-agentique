---
name: deps
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Audit dépendances — CVE (pip-audit/npm audit), versions obsolètes, packages inutilisés
---

Audit de santé des dépendances via l'agent `dependencies`.

Utilise l'outil Agent avec `subagent_type: dependencies` pour :
- Lancer pip-audit (backend) et npm audit (frontend)
- Signaler les CVE par sévérité avec version de fix disponible
- Identifier les versions majeures disponibles pour les dépendances critiques
- Détecter les dépendances potentiellement inutilisées
