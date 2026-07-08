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

### Nouveau projet (aucun code, ou squelette vide)
1. `/farm-init` — installer/compléter la ferme et `CLAUDE.md`
2. `/architect` — mode nouveau projet (session de questions → `docs/ARCHITECTURE.md`)
3. `/product-spec` — spec détaillée de la première feature
4. `/story-writer` — découper en stories auto-suffisantes
5. Implémenter, puis `/review`

### Nouvelle feature sur projet existant
1. `/product-spec` — spec de la feature (crée/étend `docs/specs/details/<domaine>.spec.md`)
2. `/architect` — mode extension, **seulement si** la feature touche une décision structurante
   (nouveau composant, nouvelle intégration externe) ; sinon passer directement à l'étape 3
3. `/story-writer` — découper en stories
4. Implémenter, puis `/review`
5. `/qa-gate` si la feature touche une zone à risque (auth, paiement, données)

### Bugfix / régression
1. `/diagnose` — boucle de diagnostic disciplinée
2. Implémenter le fix + test de non-régression (fait par `/diagnose`)
3. `/review`

### Avant une release
1. `/audit-360` — bilan qualité complet
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
