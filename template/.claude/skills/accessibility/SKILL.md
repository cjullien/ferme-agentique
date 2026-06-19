---
name: a11y
description: Audit accessibilité WCAG 2.2 AA sur les composants frontend
---

Lance un audit d'accessibilité complet via l'agent `accessibility`.

Utilise l'outil Agent avec `subagent_type: a11y` en demandant explicitement :
- d'appeler **en premier** l'outil `a11y_audit` (fourni par l'extension) pour collecter le code source frontend,
- l'analyse complète du code collecté (pages, composants, composants UI, i18n),
- un rendu structuré par catégories WCAG 2.2 Level AA,
- des findings localisés (`fichier:ligne`) avec sévérité, critère WCAG et recommandation concrète.
