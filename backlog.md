# Backlog — cohérence agents/skills de la ferme

Issu d'un audit de cohérence de `template/` (18 agents · 47 skills) mené le 2026-07-08.
Les bugs mécaniques (références `subagent_type` cassées, appels à des agents absents du
socle) ont été corrigés directement. Les items ci-dessous demandent un arbitrage de contenu
ou d'architecture — ils ne sont pas appliqués automatiquement.

## Table des items

| ID | Titre | Priorité | Effort | Fichiers concernés |
|----|-------|----------|--------|---------------------|
| FERME-1 | `design-system.md` / `ux-ui.md` non génériques (contenu Tailwind/shadcn d'une appli immo) | P1 | XL | `template/.claude/agents/design-system.md`, `template/.claude/agents/ux-ui.md`, `template/.claude/skills/design-system/SKILL.md`, `template/.claude/skills/ux-ui/SKILL.md` |
| FERME-2 | Section "Exigences IHM" de `product-owner.md` hardcodée au même produit immo | P2 | M | `template/.claude/agents/product-owner.md` |
| FERME-3 | Chevauchement `design-system` / `ux-ui` (~40% de contenu dupliqué) | P2 | M | dépend de FERME-1 |
| FERME-4 | Incohérence de nommage `backlog-manager` (socle) vs `backlog-refinement` (agents spécifiques aux modules stack-java-spring / stack-python-supabase) | P2 | S/M | `catalog.md`, `examples/stack-java-spring/.claude/agents/backlog-refinement.md`, `examples/stack-python-supabase/.claude/agents/backlog-refinement.md` |
| FERME-5 | Règle non documentée : quand créer un agent dédié vs un skill autonome | P3 | S | `README.md` ou `catalog.md` |
| FERME-6 | Hiérarchie non documentée entre `audit` / `tech-debt` / `audit-360` | P3 | S | `catalog.md` |
| FERME-7 | Alias `name:` de skill différents du répertoire/catalog (`a11y`, `deps`, `perf`, `stale`, `check`) | P3 | S | `catalog.md`, skills concernés |

---

## FERME-1 — `design-system.md` / `ux-ui.md` non génériques

**Constat.** Les deux agents (226 et 125 lignes) sont repris tels quels d'une application
immobilière React/Tailwind/shadcn précise : classes `bg-card border-border rounded-xl`,
composants `TipButton`/`StatusBadge`/`NavBadgesContext`, fichiers `pages/Tenants.jsx`,
`pages/Leases.jsx`, spec `docs/specs/details/TECHNIQUE/F-081-datatable-regles.md`. Aucune
découverte via `CLAUDE.md`, contrairement au reste du socle. Un projet qui n'est pas en
React+Tailwind+shadcn hérite d'un agent inutilisable ou trompeur (checklist qui n'a aucun
sens pour sa stack).

**Pourquoi ce n'est pas un fix mécanique.** Réécrire ces agents en version générique suppose
de trancher : quelle portion du contenu actuel est un vrai principe stack-agnostique (ex.
"pas de couleur en dur", "cohérence des tailles d'icônes", "touch target ≥ 44px") vs une
règle purement projet (ex. tailles Lucide exactes, tirets ASCII, `PAGE_SIZE`) ? Une réécriture
hâtive risque soit de perdre la valeur du contenu existant, soit de le diluer au point de le
rendre inutile.

**Options à trancher :**
1. Déplacer le contenu actuel tel quel vers `examples/domain-immo/` (ou un nouveau module
   `examples/stack-web-vite-shadcn/`), et écrire deux nouvelles versions génériques pour le
   socle (découverte des tokens/conventions via `CLAUDE.md` et lecture de composants
   existants, sans rien présupposer du framework CSS).
2. Fusionner `design-system` + `ux-ui` en un seul agent générique (voir FERME-3) plutôt que
   deux.

## FERME-2 — Section "Exigences IHM" de `product-owner.md`

Même famille de problème que FERME-1 mais localisée : la section impose l'ordre des colonnes
de tableau, un badge `NavBadgesContext`, un fichier `api/client.js` — spécifique au même
produit. À déplacer vers `examples/domain-immo/` (ou le module produit concerné) et retirer
du socle, ou généraliser en "si votre projet a des tableaux avec statut, vérifier que la
convention de la codebase est respectée" sans imposer un design précis.

## FERME-3 — Chevauchement `design-system` / `ux-ui`

Une fois FERME-1 tranché, évaluer si les deux agents doivent rester séparés (ex. `design-system`
= conformité stricte aux tokens, `ux-ui` = audit ergonomique plus large) avec une frontière
documentée, ou fusionner en un seul agent pour éviter la double maintenance des checklists
(tailles d'icônes, `aria-hidden`, i18n obligatoire actuellement dupliquées dans les deux).

## FERME-4 — `backlog-manager` vs `backlog-refinement`

Le socle a un agent `backlog-manager` (audit + priorisation + chiffrage). Les modules
`stack-java-spring` et `stack-python-supabase` ont chacun un agent `backlog-refinement`
(probablement un vestige d'un renommage `backlog-refinement` → `backlog-manager` fait dans le
socle mais jamais répercuté dans les modules). Le skill socle `backlog-refinement` a été
repointé vers `backlog-manager` avec une note invitant à préférer l'agent du module s'il est
installé (fix immédiat appliqué), mais la duplication de nom et de mission entre les deux
agents mérite d'être nettoyée à la source :
- soit renommer les agents des deux modules en `backlog-manager` (variante stack-spécifique
  qui *surcharge* celui du socle),
- soit documenter explicitement dans `catalog.md` que ce sont deux mécanismes distincts et
  pourquoi.

## FERME-5 — Règle agent vs skill non documentée

Environ 12 skills du socle (`api-client`, `data-quality`, `db-diagram`, `eda`, `migrate`,
`notebook`, `schema`, `typing`, `ui-component`, `env-check`, `commit`, `test`…) embarquent
toute leur logique directement dans le `SKILL.md`, sans agent dédié — alors que la majorité
des autres skills ne sont qu'un déclencheur de 8-15 lignes pour un agent. Ce n'est pas un bug,
mais aucun document n'explicite la règle de décision ("skill autonome si l'exécution est
courte et déterministe ; agent dédié si l'analyse est longue et doit produire un rapport
formel"). À ajouter dans `README.md` ou `catalog.md` pour guider la création de futurs modules
(notamment via `/farm-init`, qui génère justement de nouveaux modules pour des stacks non
couvertes).

## FERME-6 — Hiérarchie `audit` / `tech-debt` / `audit-360` non documentée

Trois niveaux de synthèse qui se chevauchent partiellement :
- `audit` : revue du diff courant uniquement.
- `tech-debt` : 5 agents (audit, clean-tdd, performance, dependencies, externalize) sur tout
  le code, hors diff.
- `audit-360` : tous les agents d'audit installés (socle + conditionnels) + note qualité /100.

L'articulation est cohérente une fois qu'on lit les trois fichiers, mais rien ne l'explique à
l'utilisateur qui découvre la ferme. Ajouter un paragraphe dans `catalog.md` clarifiant quand
utiliser lequel.

## FERME-7 — Alias `name:` de skills divergents du répertoire

`accessibility/` → `name: a11y`, `dependencies/` → `name: deps`, `performance/` → `name: perf`,
`tech-debt/` → `name: stale`, `pre-commit/` → `name: check`. Ce sont des alias de commande
slash plus courts (`/a11y`, `/deps`, `/perf`…), pas des bugs en soi — mais `catalog.md` liste
ces skills par leur nom de répertoire, ce qui peut dérouter (l'utilisateur cherche `/tech-debt`
et doit deviner que la commande réelle est `/stale`). Décider : soit aligner les noms
(`name:` = nom du répertoire), soit documenter explicitement les alias dans `catalog.md`.
