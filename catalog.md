# Catalogue de la ferme agentic

Inventaire des agents et skills. Le **socle** (`template/.claude/`) est posé sur tout nouveau projet ;
les **modules** (`examples/`) sont ajoutés à la carte selon la stack et le domaine.

> Les descriptions proviennent des projets d'origine (POC-NB) et peuvent citer un domaine précis
> (sablier, immo, React…) à titre **illustratif**. Le concept reste réutilisable : adapter les chemins
> et commandes (voir `INSTALL.md`).

---

## Socle générique — `template/` (18 agents · 47 skills, en versions `.claude/` et `.github/`)

### Agents

| Agent | Rôle |
|---|---|
| `accessibility` | Audit WCAG 2.2 AA approfondi du frontend |
| `agent-maintainer` | Maintient la cohérence agents/skills pendant les releases |
| `audit` | Pre-flight : revue qualité, conventions et cohérence du diff |
| `backlog-manager` | Gère/priorise/chiffre la backlog |
| `changelog` | Release notes non-techniques pour utilisateurs |
| `ci` | Revue CI/CD — jobs obsolètes, actions non pinnées, secrets |
| `clean-tdd` | Revue **et correction** clean architecture + TDD |
| `dead-code` | Détecte/supprime code mort, imports, clés i18n orphelines |
| `dependencies` | Santé des dépendances — CVE, majeures, inutilisées |
| `design-system` | Garant du design system frontend — **squelette générique à compléter avec l'IA pour ce projet** (voir l'exemple complété dans `examples/domain-immo/`) |
| `docs-update` | Synchronise README et docs avec le code |
| `e2e` | Génère/maintient les tests end-to-end des flux critiques |
| `externalize` | Audit config — env vars, i18n, thèmes, persistance |
| `owasp` | Audit sécurité OWASP Top 10 (2021) back + front |
| `performance` | N+1, index, pagination, re-renders, bundle |
| `product-owner` | Cohérence plan/spec, maintient README + backlog |
| `test-quality` | Audit qualité des tests (rapport seul) |
| `ux-ui` | Audit/amélioration UX/UI frontend — **squelette générique à compléter avec l'IA pour ce projet** (voir l'exemple complété dans `examples/domain-immo/`) |

### Skills

**Qualité & audit** : `audit`, `audit-360`, `tech-debt`, `review`, `clean-tdd`, `test-quality`,
`improve-architecture`, `owasp`, `accessibility`, `performance`, `design-system`, `dead-code`,
`externalize`, `dependencies`, `ci`.

**Tests** : `test`, `coverage`, `e2e`, `env-check`.

**Git & flux** : `commit`, `pre-commit`, `push`, `push-force`, `lint`.

**Produit & backlog** : `product-spec`, `backlog-refinement`, `to-issues`, `triage`, `changelog`.

**Docs & exploration** : `docs-update`, `instructions-update`, `zoom-out`, `diagnose`.

**Méta / interaction** : `caveman` (mode concis), `grill-me` (stress-test d'un plan).

**Onboarding** : `farm-init` — point d'entrée universel : détecte si la ferme est installée, guide l'installation (chemin local ou URL GitHub + clone auto), brainstorme les modules optionnels (dialogue interactif), audite la configuration finale. `farm-update` — synchronise les agents/skills du projet avec la ferme source après une mise à jour.

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
