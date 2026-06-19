---
name: legal-check
allowed-tools: Agent, Read, Grep, Glob, Bash
description: ⚠️ Spécifique immobilier français. Vérifie la conformité légale - loi ALUR, DPE, encadrement des loyers, baux, relances
---

⚠️ Cet agent est spécifique au domaine immobilier français. Il n'est pas générique.

Vérifie la conformité légale du code métier (loi ALUR, DPE, encadrement des loyers, procédure d'impayé) via l'agent `legal-check`.

Utilise l'outil Agent avec `subagent_type: legal-check` pour auditer le code par rapport au droit locatif français.
