---
name: stale
description: Rapport de dette technique consolidé — lance audit, clean-tdd, perf, deps, externalize
disable-model-invocation: true
context: fork
---

Rapport de dette technique consolidé — lance plusieurs agents en parallèle pour un bilan global.

Lance en séquence les agents suivants et synthétise les résultats :

1. Utilise l'outil Agent avec `subagent_type: audit` — revue du diff courant
2. Utilise l'outil Agent avec `subagent_type: clean-tdd` — violations architecture et tests manquants (phase analyse uniquement, sans corrections automatiques pour ce rapport)
3. Utilise l'outil Agent avec `subagent_type: performance` — problèmes de performance
4. Utilise l'outil Agent avec `subagent_type: dependencies` — vulnérabilités et dépendances obsolètes
5. Utilise l'outil Agent avec `subagent_type: externalize` — valeurs en dur

Après avoir collecté tous les résultats, produis un rapport consolidé :

## Rapport de dette — [date]

### Score global par axe
| Axe | Statut | Findings critiques |
|-----|--------|-------------------|
| Code quality (audit) | 🔴/🟡/✅ | X |
| Architecture (clean-tdd) | 🔴/🟡/✅ | X |
| Performance | 🔴/🟡/✅ | X |
| Dépendances | 🔴/🟡/✅ | X |
| Config externalisée | 🔴/🟡/✅ | X |

### Plan de remédiation priorisé
**Semaine 1 — Bloquant**
1. [Finding critique le plus urgent + agent qui le corrige]

**Semaine 2-3 — Important**
...

**Backlog technique**
...
