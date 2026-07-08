# Backlog — cohérence agents/skills de la ferme

Issu d'un audit de cohérence de `template/` (18 agents · 47 skills) mené le 2026-07-08.
Les bugs mécaniques (références `subagent_type` cassées, appels à des agents absents du
socle) ont été corrigés directement. FERME-1/2/3 ont ensuite été résolus en appliquant la
règle : tout ce qui n'est pas générique va dans `examples/`, et le socle ne garde qu'un
squelette générique explicite (voir détail sous chaque item). Les items restants demandent
un arbitrage plus léger, non appliqué automatiquement.

## Table des items

| ID | Titre | Priorité | Statut | Fichiers concernés |
|----|-------|----------|--------|---------------------|
| FERME-1 | `design-system.md` / `ux-ui.md` non génériques (contenu Tailwind/shadcn d'une appli immo) | P1 | ✅ Résolu | `template/.claude/agents/design-system.md`, `ux-ui.md`, `examples/domain-immo/.claude/agents/` |
| FERME-2 | Section "Exigences IHM" de `product-owner.md` hardcodée au même produit immo | P2 | ✅ Résolu | `template/.claude/agents/product-owner.md` |
| FERME-3 | Chevauchement `design-system` / `ux-ui` (~40% de contenu dupliqué) | P3 | 🟡 Partiel | `examples/domain-immo/.claude/agents/design-system.md`, `ux-ui.md` |
| FERME-4 | Incohérence de nommage `backlog-manager` (socle) vs `backlog-refinement` (agents spécifiques aux modules stack-java-spring / stack-python-supabase) | P2 | Ouvert | `catalog.md`, `examples/stack-java-spring/.claude/agents/backlog-refinement.md`, `examples/stack-python-supabase/.claude/agents/backlog-refinement.md` |
| FERME-5 | Règle non documentée : quand créer un agent dédié vs un skill autonome | P3 | Ouvert | `README.md` ou `catalog.md` |
| FERME-6 | Hiérarchie non documentée entre `audit` / `tech-debt` / `audit-360` | P3 | Ouvert | `catalog.md` |
| FERME-7 | Alias `name:` de skill différents du répertoire/catalog (`a11y`, `deps`, `perf`, `stale`, `check`) | P3 | Ouvert | `catalog.md`, skills concernés |

---

## FERME-1 — `design-system.md` / `ux-ui.md` non génériques — ✅ Résolu

**Ce qui a été fait :**
- Le contenu original (Tailwind/shadcn, `pages/Tenants.jsx`, `pages/Leases.jsx`, spec
  `F-081-datatable-regles.md`…) a été déplacé tel quel dans
  `examples/domain-immo/.claude/agents/{design-system,ux-ui}.md` (+ skills associés), comme
  illustration concrète et complète.
- Les versions du socle (`template/.claude/agents/{design-system,ux-ui}.md`) ont été
  remplacées par un **squelette générique** : rôle générique, section "Périmètre à
  instancier" volontairement vide, et une procédure explicite pour la compléter avec l'IA
  (lire `CLAUDE.md` + 3-5 composants représentatifs, en déduire les tokens/conventions
  réelles du projet) en s'appuyant sur l'exemple de `examples/domain-immo/`.
- Les skills `design-system`/`ux-ui` du socle renvoient vers cette procédure plutôt que
  d'imposer des règles Tailwind.
- `catalog.md` documente cette nature de squelette pour les deux agents.

## FERME-2 — Section "Exigences IHM" de `product-owner.md` — ✅ Résolu

La section a été retirée du socle et son contenu déplacé en annexe de
`examples/domain-immo/.claude/agents/design-system.md`. Le socle garde une section générique
courte : "vérifie les conventions IHM **si le projet en a documenté**, n'en invente aucune".

## FERME-3 — Chevauchement `design-system` / `ux-ui` — 🟡 Partiellement résolu

Résolu côté **socle** : les deux squelettes génériques sont courts et ne dupliquent plus
aucune checklist concrète. Reste présent côté **exemple** : les fichiers copiés dans
`examples/domain-immo/` gardent le chevauchement d'origine (tailles d'icônes, tokens,
`aria-hidden`, i18n mentionnés dans les deux). Acceptable en l'état — un seul module
d'illustration, pas le socle propagé partout — mais à nettoyer si `examples/domain-immo/`
est un jour utilisé comme référence à copier ailleurs.

## FERME-4 — `backlog-manager` vs `backlog-refinement`

Inchangé depuis le dernier audit. Le socle a un agent `backlog-manager` (audit + priorisation
+ chiffrage). Les modules `stack-java-spring` et `stack-python-supabase` ont chacun un agent
`backlog-refinement` (probablement un vestige d'un renommage `backlog-refinement` →
`backlog-manager` fait dans le socle mais jamais répercuté dans les modules). Le skill socle
`backlog-refinement` a été repointé vers `backlog-manager` avec une note invitant à préférer
l'agent du module s'il est installé, mais la duplication de nom et de mission entre les deux
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
