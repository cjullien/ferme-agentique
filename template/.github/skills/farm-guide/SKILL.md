---
name: farm-guide
description: Recommande la séquence d'agents/skills à utiliser selon l'étape du projet (nouveau projet, nouvelle feature, bugfix, avant release). Point de repère dans une ferme à 20+ agents et 50+ skills.
allowed-tools: Read, Glob, Grep, Bash
---

# Farm Guide — quel agent/skill pour quelle étape ?

Indique la séquence recommandée selon la situation. Ne lance rien automatiquement — restitue la
liste des commandes à lancer, dans l'ordre, à l'utilisateur.

## Détection du contexte

```bash
ls docs/ARCHITECTURE.md 2>/dev/null && echo "architecture: présente" || echo "architecture: absente"
ls docs/specs/backlog.md 2>/dev/null && echo "backlog: présent" || echo "backlog: absent"
ls docs/specs/stories/ 2>/dev/null | wc -l
git log -5 --oneline 2>/dev/null
```

Si un argument est fourni ($ARGUMENTS), l'utiliser directement comme situation. Sinon, demander :
"Nouveau projet, nouvelle feature, bugfix, ou préparation de release ?"

## Séquences recommandées

Trois phases (backlog & specs → implémentation TDD → audit de la feature), plus les audits
globaux périodiques — voir `catalog.md` pour le détail complet.

### Nouveau projet (aucun code, ou squelette vide)
1. `/farm-init` — installer/compléter la ferme et `CLAUDE.md`
2. **Phase 1** — `/architect` (mode nouveau projet, session de questions → `docs/ARCHITECTURE.md`), puis `/product-spec` (spec détaillée de la première feature), puis `/story-writer` (stories auto-suffisantes)
3. **Phase 2** — `/tdd` pour chaque story (red-green-refactor)
4. **Phase 3** — `/review`, puis `/qa-gate` si la feature touche une zone à risque

### Nouvelle feature sur projet existant
1. **Phase 1** — `/product-spec` (crée/étend `docs/specs/details/<domaine>.spec.md`) ; `/architect` **seulement si** la feature touche une décision structurante (nouveau composant, nouvelle intégration externe) ; `/story-writer` pour découper en stories — ou `/to-issues` si le travail est simple et ne demande pas de contexte embarqué
2. **Phase 2** — `/tdd` (+ `/e2e` si un flux critique est concerné, `/improve-architecture` si une friction architecturale apparaît en cours de route)
3. **Phase 3** — `/review`, puis `/qa-gate` si la feature touche une zone à risque (auth, paiement, données)

### Bugfix / régression
1. `/diagnose` — boucle de diagnostic disciplinée (inclut l'écriture du test de non-régression)
2. `/review`

### Avant une release
1. `/audit-360` — bilan qualité complet (audits globaux, tout le code) + plan de remédiation priorisé
2. `/changelog` — notes de release non-techniques
3. `/docs-update` — synchroniser la doc avec le code livré

### Je ne sais pas / projet repris sans contexte
1. `/farm-init` — audite la configuration de la ferme
2. `/zoom-out` — vue macro du code si la zone est inconnue
3. `/architect --existant` — si `docs/ARCHITECTURE.md` est absent, le reconstituer depuis le code

## Restitution

```
## Situation détectée
[nouveau projet / feature / bugfix / release / inconnue]

## Séquence recommandée
1. /commande — pourquoi
2. /commande — pourquoi
...
```
