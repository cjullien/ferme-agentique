# Catalogue de la ferme agentic

Inventaire des agents et skills. Le **socle** (`template/.claude/`) est posé sur tout nouveau projet ;
les **modules** (`examples/`) sont ajoutés à la carte selon la stack et le domaine.

> Les descriptions proviennent des projets d'origine (POC-NB) et peuvent citer un domaine précis
> (sablier, immo, React…) à titre **illustratif**. Le concept reste réutilisable : adapter les chemins
> et commandes (voir `INSTALL.md`).

---

## Socle générique — `template/` (21 agents · 49 skills, en versions `.claude/` et `.github/`)

Le socle est organisé autour du cycle de vie d'une feature — trois phases — plus une couche
d'**audits globaux périodiques** qui balaient tout le code, sur le même principe que les audits
de connaissance de `km-toolkit` (`km-audit`, `doc-coverage`, `spec-drift`...) appliqué à la
qualité du code :

```
Backlog & specs  →  Implémentation TDD  →  Audit de la feature
      ↑                                          │
      └───────────── Audits globaux ─────────────┘   (périodique, tout le code)
```

Volontairement plus léger qu'un pipeline complet à la BMAD-METHOD : trois agents empruntent son
vocabulaire (`architect`, `story-writer`, `qa-gate`) mais restent optionnels dans le flux — un
item de backlog simple peut aller directement de `product-owner` à `tdd` sans passer par
`architect` ni `story-writer` si l'équipe n'en a pas besoin.

### Phase 1 — Backlog & specs

| Agent / Skill | Rôle |
|---|---|
| `backlog-manager` (agent) | Audit, priorisation et chiffrage de la backlog |
| `backlog-refinement` (skill) | Refinement backlog — mode simple (brainstorm) ou avancé (réévaluation par le code) |
| `product-owner` (agent) | Cohérence du plan, génère la spec Given/When/Then, maintient backlog + README |
| `product-spec` (skill) | `product-owner` enrichi d'une session de questionnement (grill) |
| `architect` (agent + skill) | Conçoit/documente `docs/ARCHITECTURE.md` — nouveau projet, extension, ou rétro-documentation d'un existant. *Optionnel* : seulement si une décision structurante est en jeu. |
| `story-writer` (agent + skill) | Découpe un item de backlog/spec en stories auto-suffisantes (contexte spec + architecture embarqué). *Optionnel* : `to-issues` suffit pour du travail simple. |
| `to-issues` (skill) | Publie rapidement des issues sur le tracker via vertical slices, sans contexte embarqué |
| `triage` (skill) | Triage des issues entrantes (bug/enhancement, prêt pour agent ou humain) |
| `grill-me` (skill) | Stress-test d'un plan par questionnement systématique |

### Phase 2 — Implémentation TDD

| Agent / Skill | Rôle |
|---|---|
| `tdd` (agent + skill) | Rétro-ingénierie des tests manquants, cycle red-green-refactor, correction des tests fragiles/redondants |
| `improve-architecture` (skill) | Opportunités d'approfondissement architectural (modules shallow, violations de couches) — trouve, discute, **applique** |
| `e2e` (agent + skill) | Génère/maintient les tests end-to-end des flux critiques |
| `diagnose` (skill) | Boucle de diagnostic disciplinée pour bugs et régressions |
| `schema`, `migrate`, `db-diagram` (skills) | Impact d'un changement de modèle, génération de migration, diagramme ER |
| `ui-component`, `api-client`, `typing` (skills) | Génération de composant UI, audit des appels réseau, audit de typage statique |

### Phase 3 — Audit de la feature

| Agent / Skill | Rôle |
|---|---|
| `audit` (agent + skill) | Pre-flight léger et systématique sur le diff courant, avant chaque commit |
| `review` (skill) | Revue avant merge — déclenche en plus les agents spécialisés pertinents selon les fichiers modifiés (a11y, sécurité, contrat API...) |
| `qa-gate` (agent + skill) | Gate formel — traçabilité critères d'acceptation ↔ tests, profil de risque, verdict PASS/CONCERNS/FAIL/WAIVED. *Optionnel* : à réserver aux zones à risque (auth, paiement, données) |

### Audits globaux (périodiques, tout le code)

| Agent / Skill | Rôle |
|---|---|
| `audit-360` (skill) | Lance tous les agents d'audit installés, note qualité /100, **plan de remédiation priorisé** |
| `owasp` | Sécurité OWASP Top 10 (2021) back + front |
| `accessibility` | Audit WCAG 2.2 AA approfondi du frontend |
| `performance` | N+1, index, pagination, re-renders, bundle |
| `dependencies` | Santé des dépendances — CVE, majeures, inutilisées |
| `test-quality` | Pyramide de tests, anti-patterns, couverture fonctionnelle (rapport seul, sur toute la suite) |
| `ci` | Revue CI/CD — jobs obsolètes, actions non pinnées, secrets |
| `dead-code` | Détecte/supprime code mort, imports, clés i18n orphelines |
| `externalize` | Config à externaliser — env vars, i18n, thèmes, persistance |
| `docs-update` | Synchronise README et docs avec le code |
| `design-system`, `ux-ui` | Design system et UX/UI frontend — **squelettes génériques à compléter avec l'IA pour ce projet** (exemple complété dans `examples/domain-immo/`) |
| `agent-maintainer` | Maintient la cohérence agents/skills de la ferme elle-même |

`architect`, `story-writer` et `qa-gate` s'inspirent du pipeline planning → stories → gate
qualité de BMAD-METHOD, adaptés au principe stack-agnostique de la ferme (tout est découvert
via `CLAUDE.md`/`docs/ARCHITECTURE.md`, rien n'est codé en dur pour une stack donnée) et gardés
optionnels pour rester plus léger que BMAD.

### Git & flux
`commit`, `pre-commit`, `push` (inclut `--skip-tests` pour committer/pousser sans lancer les
tests), `lint`, `test`, `coverage`, `env-check`.

### Docs & exploration
`docs-update`, `instructions-update`, `zoom-out`.

### Release
`changelog` (agent) — résumé non-technique des nouveautés pour utilisateurs, à lancer avant
publication (voir séquence "Avant une release" ci-dessus : `audit-360` → `changelog` →
`docs-update`).

### Méta / interaction
`caveman` (mode concis), `farm-guide` (recommande la séquence d'agents/skills selon l'étape du
projet — nouveau projet, feature, bugfix, release).

### Onboarding
`farm-init` — point d'entrée universel : détecte si la ferme est installée, guide
l'installation (chemin local ou URL GitHub + clone auto), brainstorme les modules optionnels
(dialogue interactif), audite la configuration finale. `farm-update` — synchronise les
agents/skills du projet avec la ferme source après une mise à jour.

### Pourquoi `tech-debt` et `push-force` n'existent plus

`tech-debt` était un sous-ensemble strict d'`audit-360` (5 agents contre tout le socle + note
/100) ; son unique valeur ajoutée — le plan de remédiation priorisé — a été absorbée dans
`audit-360` (Phase 5). `push-force` ne différait de `push` que par un flag (sauter les tests) ;
`push` accepte maintenant `--skip-tests`, cohérent avec la convention déjà utilisée par
`backlog-refinement --avancé`. `clean-tdd` a été scindé : sa partie TDD devient l'agent `tdd`
(Phase 2), sa partie audit de couches est absorbée par `improve-architecture`, qui applique
désormais aussi le refactoring choisi (il ne faisait auparavant que le proposer).

---

## Modules optionnels — `examples/`

### `stack-python-supabase/` — backend Python + ORM + Postgres/Supabase
Agents : `schema`, `migrate`, `db-diagram`, `fixture`, `seed`, `api-contract`, `scheduler-audit`,
`km-generator`, `backlog-refinement`.
Skills : `schema`/`schema-impact`, `migrate`, `db-diagram`/`mpd`, `db-reset`, `fixture`, `seed`,
`api-contract`, `scheduler-audit`, `neon-postgres`, `km-generator`,
`eda` (profil dataset : nulls, distributions, outliers → rapport markdown),
`notebook` (audit notebooks Jupyter : ordre cellules, outputs stale, imports),
`data-quality` (validation schémas Pydantic/Pandera, colonnes nullables, frontières système).
+ `settings.json` (hooks py/ruff/alembic).

### `finops/` — contrôle des coûts token (cross-stack)

Skills : `token-budget` (burn rate + recommandation modèle), `cost-check` (verdict continuer/résumer),
`model-pick` (sélecteur interactif coût/qualité).
Hook `PostToolUse` : log léger des appels Agent/Task dans `.claude/finops.log` (aucune dépendance externe).
Snippet `CLAUDE.finops.md` : routage modèle par défaut, hygiène prompt, grille fork-vs-inline, checklist pré-sous-agent.

### `stack-java-spring/` — backend Java / Spring Boot / Maven
Variantes adaptées au build Maven & natif : agents `ci`, `docs-update`, `product-owner`,
`backlog-refinement` ; skills `ci`, `coverage` (JaCoCo), `docs-update`, `improve-architecture`.
+ `settings.json` (permissions mvn/java/git/gh).

### `stack-web-vite/` — frontend Vite + React (PWA)
Agents : `agent-maintainer`, `externalize`.
`settings.json` (permissions npm/git/gh + hooks i18n/PWA/a11y) et skills `backlog-feature`, `push-force`,
`typescript` (audit strictness, `any`, assertions), `component` (génération composant + tests Vitest),
`api-client` (audit appels réseau, React Query/SWR, typage réponses).

### `domain-immo/` — métier gestion immobilière
Agent `legal-check` ; skills `legal-check`, `product-spec` (glossaire métier).

Contient aussi l'**exemple concret et complet** des agents `design-system` et `ux-ui` du
socle (React + Tailwind + shadcn/ui, conventions IHM de tableaux/statuts incluses) : à
consulter comme modèle pour compléter, avec l'IA, les squelettes génériques du socle sur
n'importe quelle stack.

### `feature-decision-index/` — mémoire décisionnelle légère (opt-in)
Alternative légère à `km-toolkit/adr-capture` pour les projets sans besoin de KB complète.
Agents : `decision-record` (capture une décision), `decision-harvest` (détecte les décisions implicites dans le codebase).
Skills : `record`, `recall` (recherche par mot-clé), `harvest`.
Constitution : `.decisions/CONSTITUTION.md` injectée via `@` dans `CLAUDE.md` à chaque session.
Voir `examples/feature-decision-index/INSTALL.md`.

### `feature-i18n/` — internationalisation (opt-in)
Agent `translations` (+ variante React/Python) ; skills `traduction`, `translations`.

### `km-toolkit/` — Knowledge Management piloté par agents
Chaîne complète (25 agents / 26 skills) : socle KM générique (`km-generator`, `adr-capture`,
`session-digest`, `postmortem`, `faq-harvest`, `glossary-sync`…), contrôle qualité KB
(`doc-coverage`, `spec-drift`, `km-audit`, `runbook-verify`, `onboarding-test`) et dispositif
**mainframe COBOL** (`mf-*`). Moteur d'override MkDocs (`hooks.py`, testé par `test_hooks.py`).
Voir `examples/km-toolkit/INSTALL.md`.
