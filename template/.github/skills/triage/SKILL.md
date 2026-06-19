---
name: triage
description: Triage des issues via une state machine de rôles. Évalue, catégorise et prépare les issues pour un agent AFK ou un humain. À utiliser quand l'utilisateur veut trier des issues, reviewer des bugs ou préparer du travail.
allowed-tools: Agent, Read, Grep, Glob, Bash
---

# Triage

Triage des issues via une state machine de rôles.

## Rôles de catégorie
- `bug` — quelque chose est cassé
- `enhancement` — nouvelle fonctionnalité ou amélioration

## Rôles d'état
- `needs-triage` → `needs-info` | `ready-for-agent` | `ready-for-human` | `wontfix`
- `needs-info` → `needs-triage` (quand le reporter répond)

## Processus

1. **Contexte** — Lire l'issue. Consulter `CLAUDE.md` et `CONTEXT.md` si existants.
2. **Recommandation** — Catégorie + état + justification. Attendre validation.
3. **Reproduction (bugs)** — Tenter de reproduire avant questionnement.
4. **Questionnement** — Utiliser le pattern grill-me si nécessaire.
5. **Appliquer** le résultat : brief agent, questions needs-info, ou wontfix.
