---
name: audit-360
description: Audit 360° — lance tous les agents d'audit installés en parallèle, consolide les résultats et produit une note qualité /100.
---

# Skill : Audit 360°

Lance un audit complet du projet en invoquant **tous les agents d'audit installés** en parallèle, puis consolide les résultats.

## Agents du socle (toujours lancés)

| Agent | Périmètre |
|-------|-----------|
| `audit` | Qualité, sécurité, conventions (diff courant) |
| `owasp` | Sécurité OWASP Top 10 (code complet) |
| `accessibility` | Accessibilité WCAG 2.2 AA (frontend complet) |
| `performance` | N+1, index, pagination, re-renders, bundle |
| `dependencies` | CVE, versions obsolètes, deps inutilisées |
| `test-quality` | Pyramide, anti-patterns, couverture |
| `clean-tdd` | Clean architecture + TDD |
| `dead-code` | Code mort, imports inutilisés, docs obsolètes |
| `ci` | Pipelines CI/CD |
| `externalize` | Valeurs hardcodées à externaliser |
| `docs-update` | Documentation désynchronisée |
| `ux-ui` | UX/UI, responsivité, design system |

## Agents conditionnels (si le module est installé)

Lancer uniquement ceux présents dans `.claude/agents/` (ou `.github/agents/`) :

| Agent | Module | Périmètre |
|-------|--------|-----------|
| `api-contract` | stack-python-supabase | Alignement routes backend ↔ appels frontend |
| `scheduler-audit` | stack-python-supabase | Tâches planifiées |
| `legal-check` | domain-immo | Conformité légale métier |
| `translations` | feature-i18n | Clés i18n manquantes ou incohérentes |

## Processus

### Phase 1 — Lancement parallèle

Lancer les 16 agents en mode background simultanément :

**Copilot CLI :**
```
task agent_type="audit" mode="background"
task agent_type="owasp" mode="background"
... (les 16)
```

**Claude :**
```
Agent subagent_type="audit"
Agent subagent_type="owasp"
... (les 16)
```

### Phase 2 — Collecte

Attendre la complétion de tous les agents. Lire chaque résultat.

### Phase 3 — Consolidation

Produire un tableau de synthèse :

```markdown
| Agent | 🔴 | 🟡 | 🔵 | Score | Top finding |
|-------|-----|-----|-----|-------|-------------|
```

### Phase 4 — Note qualité /100

Calculer selon la grille :

| Axe | Points max |
|-----|------------|
| Fonctionnalités métier | 25 |
| Sécurité | 25 |
| Qualité / Maintenabilité | 20 |
| Accessibilité | 15 |
| Performance | 15 |

### Phase 5 — Mise à jour backlog

1. Ajouter chaque finding 🔴/🟡 non déjà présent dans `docs/specs/backlog.md`
2. Préfixer les IDs : `SEC-`, `BUG-`, `A11Y-`, `PERF-`, `QUAL-`, `CI-`, `UX-`, `I18N-`, `LEGAL-`, `DEPS-`, `DEAD-`, `EXT-`, `SCHED-`, `DOC-`, `TEST-`
3. Nettoyer les items livrés (barrer avec ~~)
4. Mettre à jour la note /100 avec la date

## ⚠️ Règle anti-faux-positifs (OBLIGATOIRE pour tous les agents)

Les agents doivent **vérifier factuellement** avant de signaler un problème 🔴 :

- **CI** : ne pas déclarer une version d'action invalide sans vérifier que le CI échoue réellement (`gh run list --limit 3`). Si le CI passe, la version est valide.
- **Externalize** : ne pas déclarer des secrets committés sans vérifier `git ls-files <fichier>`. Un fichier sur disque mais absent de git n'est pas un secret commité.
- **Dead-code** : ne pas déclarer du code mort si le code est utilisé dynamiquement (ex: `__all__`, re-exports, plugins).
- **Général** : tout finding 🔴 doit être **prouvé**, pas supposé. En cas de doute → 🔵 "à vérifier".
