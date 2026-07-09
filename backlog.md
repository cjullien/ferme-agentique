# Backlog — cohérence agents/skills de la ferme

Issu d'un audit de cohérence de `template/` mené le 2026-07-08, complété par un passage de
consolidation de la granularité (fusions/scissions FERME-8/9/10) et par l'ajout d'un pipeline
Backlog & specs → Implémentation TDD → Audit de la feature + audits globaux, inspiré de
BMAD-METHOD mais gardé plus léger (voir `catalog.md`). Les items restants demandent un
arbitrage plus léger, non appliqué automatiquement.

## Table des items

| ID | Titre | Priorité | Statut | Fichiers concernés |
|----|-------|----------|--------|---------------------|
| FERME-1 | `design-system.md` / `ux-ui.md` non génériques (contenu Tailwind/shadcn d'une appli immo) | P1 | ✅ Résolu | `template/.claude/agents/design-system.md`, `ux-ui.md`, `examples/domain-immo/.claude/agents/` |
| FERME-2 | Section "Exigences IHM" de `product-owner.md` hardcodée au même produit immo | P2 | ✅ Résolu | `template/.claude/agents/product-owner.md` |
| FERME-3 | Chevauchement `design-system` / `ux-ui` (~40% de contenu dupliqué) | P3 | 🟡 Partiel | `examples/domain-immo/.claude/agents/design-system.md`, `ux-ui.md` |
| FERME-4 | Incohérence de nommage `backlog-manager` (socle) vs `backlog-refinement` (agents spécifiques aux modules stack-java-spring / stack-python-supabase) | P2 | ✅ Résolu | `catalog.md`, `examples/stack-java-spring/.claude/agents/backlog-refinement.md`, `examples/stack-python-supabase/.claude/agents/backlog-refinement.md` |
| FERME-5 | Règle non documentée : quand créer un agent dédié vs un skill autonome | P3 | ✅ Résolu | `README.md` ou `catalog.md` |
| FERME-6 | Hiérarchie non documentée entre `audit` / `tech-debt` / `audit-360` | P3 | ✅ Résolu | `catalog.md` |
| FERME-7 | Alias `name:` de skill différents du répertoire/catalog (`a11y`, `deps`, `perf`, `check`) | P3 | ✅ Résolu | `catalog.md`, skills concernés |
| FERME-8 | `tech-debt` redondant avec `audit-360` (sous-ensemble strict) | P2 | ✅ Résolu | supprimé, plan de remédiation absorbé dans `audit-360/SKILL.md` |
| FERME-9 | `clean-tdd` mélangeait deux métiers (clean architecture + TDD) | P2 | ✅ Résolu | scindé en `tdd` (agent, Phase 2) + `improve-architecture` (audit de couches, applique désormais le refactoring) |
| FERME-10 | `push` / `push-force` : deux fichiers pour un flag, convention incohérente avec `backlog-refinement --avancé` | P3 | ✅ Résolu | fusionnés dans `push/SKILL.md` (`--skip-tests`) |
| FERME-11 | km-toolkit : `changelog`/`docs-update` collisionnent avec le socle, `changelog.md` est une fuite complète du domaine domain-immo | P1 | ✅ Résolu | `examples/km-toolkit/` |
| FERME-12 | km-toolkit : 25/26 skills + `mf-km-generator.md` utilisent la syntaxe Copilot (`task`/`agent_type`) au lieu de Claude Code (`Agent`/`subagent_type`) — cassé côté Claude Code partout | P1 | ✅ Résolu | `examples/km-toolkit/.claude/skills/*/SKILL.md`, `mf-km-generator.md` |
| FERME-13 | km-toolkit : `doc-coverage`/`spec-drift`/`glossary-sync` annoncés génériques dans `catalog.md` mais 100% câblés COBOL | P2 | ✅ Résolu | `examples/km-toolkit/.claude/agents/{doc-coverage,spec-drift,glossary-sync}.md` |
| FERME-14 | Fuite de noms d'outils Copilot dans le corps de texte (`run_in_terminal`, `create_file`, `replace_string_in_file`, `read_file`, `list_directory`, `grep_search`, `file_search`) — non détectée par `validate_farm.py` (ne vérifie que le frontmatter `tools:`) | P2 | ✅ Résolu | 3 agents du socle (`dead-code`, `accessibility`, `dependencies`, `e2e`) + 3 dans `examples/` (`domain-immo/design-system`, `stack-python-supabase/{migrate,km-generator}`) |
| FERME-15 | stack-python-supabase : `schema`/`schema-impact` et `db-diagram`/`mpd` — paires de fichiers strictement redondants | P2 | ✅ Résolu | doublons supprimés, références (`migrate.md`, `settings.json`) repointées vers les noms survivants |
| FERME-16 | stack-python-supabase : `db-reset` refuse d'agir si PostgreSQL détecté alors que c'est la stack déclarée du module | P1 | ✅ Résolu | `examples/stack-python-supabase/.claude/skills/db-reset/SKILL.md` |
| FERME-17 | feature-i18n : `translations-react-python.md` doublon byte-identique de `translations.md` avec collision de `name:` | P1 | ✅ Résolu | supprimé |
| FERME-18 | feature-i18n : règle anti-tiret-cadratin de `translations/SKILL.md` auto-contradictoire (caractère perdu) | P2 | ✅ Résolu | réécrit à l'identique de `traduction/SKILL.md` |
| FERME-19 | domain-immo : contradiction directe entre `ux-ui.md` (`rounded-lg` pour cartes) et `design-system.md` (`rounded-xl` obligatoire, `rounded-lg` listé comme anti-pattern) | P1 | ✅ Résolu | `examples/domain-immo/.claude/agents/ux-ui.md` |
| FERME-20 | stack-java-spring : plusieurs fichiers contiennent des détails d'un projet réel unique (Spring AI, Tika OCR, GraalVM, item `NATIVE-001`...) au-delà de "Java/Spring générique" | P2 | ✅ Résolu | `examples/stack-java-spring/.claude/agents/{ci,docs-update,product-owner,backlog-refinement}.md`, `.claude/skills/{coverage,improve-architecture}/SKILL.md` |
| FERME-21 | stack-python-supabase : `settings.json` mélange des hooks frontend (pnpm, `.jsx/.tsx`) dans un module documenté backend-only | P3 | ✅ Résolu | `examples/stack-python-supabase/.claude/settings.json` |
| FERME-22 | stack-java-spring : agent `backlog-refinement` spécialisé Maven sans skill dédié → `/backlog-refinement` invoque l'agent générique du socle à la place | P3 | ✅ Résolu | `examples/stack-java-spring/` |
| FERME-23 | Fuites domaine mineures : `fixture.md` (stack-python-supabase) utilise un modèle d'exemple `Lease` ; chevauchement partiel `postmortem`/`session-digest` (km-toolkit) | P3 | ✅ Résolu | `examples/stack-python-supabase/.claude/agents/fixture.md`, `examples/km-toolkit/` |

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

## FERME-4 — `backlog-manager` vs `backlog-refinement` — ✅ Résolu

Les agents `backlog-refinement` de `stack-java-spring` et `stack-python-supabase` ont été
renommés `backlog-manager` (même nom que l'agent générique du socle). Puisque l'installation
d'un module copie ses fichiers dans le même `.claude/agents/`, ils **surchargent
automatiquement** la version générique à l'installation — plus besoin de skill dédiée ni de
cas particulier documenté. Le skill socle `backlog-refinement` (qui invoque déjà
`subagent_type: backlog-manager`) fonctionne donc tel quel avec la version générique ou
spécialisée, selon ce qui est installé. Le skill `backlog-refinement` redondant de
`stack-python-supabase` a été supprimé (celui du socle suffit). `catalog.md` mis à jour.

## FERME-5 — Règle agent vs skill non documentée — ✅ Résolu

Ajouté dans `catalog.md` une section "Convention — agent dédié ou skill autonome ?" qui
explicite la règle de décision (agent dédié + skill fine si l'analyse est longue et produit un
rapport structuré ou des corrections étendues ; skill autonome si la procédure est courte et
déterministe), pour guider la création de futurs modules via `/farm-init`.

## FERME-6 — Hiérarchie `audit` / `tech-debt` / `audit-360` non documentée — ✅ Résolu

`catalog.md` documente désormais l'ensemble via la structure en 3 phases + audits globaux, et
explique explicitement pourquoi `tech-debt` a disparu (voir FERME-8).

## FERME-7 — Alias `name:` de skills divergents du répertoire — ✅ Résolu

`accessibility/` → `name: a11y`, `dependencies/` → `name: deps`, `performance/` → `name: perf`,
`pre-commit/` → `name: check`. Ce sont des alias de commande slash plus courts (`/a11y`,
`/deps`, `/perf`…), pas des bugs en soi. Documentés explicitement dans `catalog.md`
("Convention — alias de commandes courtes") avec un tableau répertoire ↔ commande, plutôt que
de les aligner (l'alias court reste utile au clavier).

## FERME-8 — `tech-debt` redondant avec `audit-360` — ✅ Résolu

`tech-debt` lançait 5 agents (`audit`, `clean-tdd`, `performance`, `dependencies`,
`externalize`) sur tout le code ; `audit-360` en lance jusqu'à 12 (socle) + les conditionnels,
avec en plus une note qualité /100. `tech-debt` était donc un sous-ensemble strict, sans
raison d'exister à côté. Sa seule valeur ajoutée réelle — le "plan de remédiation priorisé"
(semaine 1 bloquant / semaine 2-3 important / backlog technique) — a été portée dans
`audit-360/SKILL.md` (nouvelle Phase 5). `tech-debt/SKILL.md` supprimé (`.claude/` et
`.github/`).

## FERME-9 — `clean-tdd` mélangeait deux métiers — ✅ Résolu

`clean-tdd` faisait à la fois de l'audit de clean architecture (couches, sens des
dépendances, services fourre-tout) et de la rétro-ingénierie TDD (tests manquants, tests
fragiles, red-green-refactor) — deux compétences différentes dans un seul agent de 223
lignes, avec un recouvrement significatif avec `test-quality` sur les anti-patterns de test.

Scindé :
- **`tdd`** (nouvel agent + skill, remplace `clean-tdd`) : uniquement la partie TDD
  (rétro-ingénierie, red-green-refactor, correction de tests fragiles/redondants). Renvoie
  vers `/improve-architecture` pour toute violation de couche détectée au passage, et vers
  `/test-quality` pour l'audit exhaustif périodique de la pyramide de tests (lui ne corrige
  que ce qu'il touche).
- **`improve-architecture`** (skill existant, enrichi) : absorbe la détection des violations
  de couches/dépendances et des services fourre-tout, **et applique désormais le
  refactoring choisi** après validation utilisateur (il ne faisait auparavant que le
  proposer/discuter, sans étape d'application explicite).

Rangé en Phase 2 (Implémentation TDD) du nouveau pipeline. Toutes les références croisées
(`audit.md`, `audit-360/SKILL.md`, `examples/stack-python-supabase/.claude/agents/scheduler-audit.md`)
mises à jour vers `tdd`.

## FERME-10 — `push` / `push-force` — ✅ Résolu

Deux fichiers séparés pour une différence d'un seul flag (sauter les tests), alors que
`backlog-refinement` gérait une distinction comparable (mode simple/avancé) via un argument
(`--avancé`). Fusionnés dans `push/SKILL.md`, qui accepte maintenant `--skip-tests`.
`push-force/SKILL.md` supprimé du socle (`.claude/` et `.github/`) — au passage, son nom était
trompeur : il ne faisait jamais de `git push --force`, seulement un push sans tests au
préalable.

---

Items suivants issus d'un audit de cohérence et d'agnosticisme sur `template/` **et tous les
modules `examples/`** (2026-07-09), via 4 agents d'audit parallèles + vérification manuelle des
findings les plus surprenants avant correction.

## FERME-11 — km-toolkit : collision de noms avec le socle + fuite domain-immo — ✅ Résolu

`examples/km-toolkit/.claude/agents/changelog.md` et `docs-update.md` portaient les mêmes noms
que les agents du socle, avec un contenu différent. `INSTALL.md` faisait un `cp -R` récursif
sans détection de collision — installer km-toolkit sur un projet qui a déjà le socle écrasait
silencieusement 2 agents génériques. `changelog.md` était en plus entièrement rédigé pour
"l'application de gestion locative" (fuite du domaine `domain-immo`), sans rapport avec KM
générique ni COBOL.

**Résolu** : `docs-update.md`/skill supprimés de km-toolkit (celui du socle est utilisé tel
quel, même rôle, pas de duplication). `changelog.md` renommé `newsletter` (valeur réelle
différente : produit une newsletter HTML mensuelle, pas un `CHANGELOG.md`) et généricisé
(catégories neutres pilotées par `CLAUDE.md` au lieu de baux/locataires). `INSTALL.md` et
`catalog.md` mis à jour (24 agents / 25 skills), avec un avertissement explicite sur le risque
de collision pour les futurs ajouts au module.

## FERME-12 — km-toolkit : syntaxe Copilot dans les fichiers Claude Code — ✅ Résolu

25 des 26 skills `.claude/skills/*/SKILL.md` de km-toolkit utilisaient `allowed-tools: task` et
`` `agent_type: "X"` `` (syntaxe Copilot CLI) au lieu de `allowed-tools: Agent` et
`` `subagent_type: X` `` (Claude Code) — identique dans les deux miroirs, donc cassé côté
Claude Code sur la quasi-totalité du plus gros module de la ferme. Même bug dans l'agent
`mf-km-generator.md` pour son invocation de `mf-inventory`. `validate_farm.py` ne le détecte
pas : il ne vérifie que le frontmatter `tools:` des agents, pas ce genre de fuite dans le corps
des skills.

**Résolu** : script de correction ciblé sur les 25 skills (motif uniforme), correction manuelle
de `mf-km-generator.md`. Vérifié : plus aucune occurrence de `` `task` ``/`agent_type:` dans
tout le dépôt.

## FERME-13 — km-toolkit : agents "qualité KB générique" 100% COBOL — ✅ Résolu

`doc-coverage`, `spec-drift` et `glossary-sync` sont catégorisés dans `catalog.md` comme
"contrôle qualité KB" — une couche explicitement distincte du dispositif mainframe `mf-*` — mais
leurs commandes d'extraction étaient exclusivement câblées sur `.cob`/`.cpy`/`src/_copybooks/`
sans aucune découverte via `CLAUDE.md`, inutilisables tels quels sur un projet KM non-COBOL.

**Résolu** : ajout d'une Phase 0 "Identifier les sources du projet" (découverte du
langage/écosystème via `CLAUDE.md`) dans les trois agents, commandes COBOL conservées comme
exemple illustratif explicite plutôt que comme seul chemin possible.

## FERME-14 — Fuites de noms d'outils Copilot dans le corps de texte — ✅ Résolu

Au-delà de FERME-12 (km-toolkit), le même type de fuite existait ailleurs, non détecté par
`validate_farm.py` (qui ne vérifie que le frontmatter `tools:` des agents) : `run_in_terminal`,
`create_file`, `replace_string_in_file`, `read_file`, `list_directory`, `grep_search`,
`file_search` mentionnés en dur dans le corps de 3 agents du **socle** (`dead-code.md`,
`accessibility.md`, `dependencies.md`, `e2e.md`) et 2 modules `examples/`
(`domain-immo/design-system.md`, `stack-python-supabase/{migrate,km-generator}.md`).

**Résolu** : tous remplacés par les noms d'outils Claude Code (`Grep`, `Glob`, `Read`, `Bash`,
`Write`, `Edit`). Balayage final sur tout le dépôt confirmant qu'il n'en reste aucun.

## FERME-15 — stack-python-supabase : doublons `schema`/`schema-impact`, `db-diagram`/`mpd` — ✅ Résolu

Deux paires de skills strictement redondants (même agent, corps quasi identique, seul le
`name:` changeait) — `catalog.md` les présentait comme des alias alors que ce sont deux
fichiers séparés à maintenir en double. `/schema-impact` était en fait le nom activement
référencé ailleurs dans le module (`migrate.md`, hook `settings.json`), tandis que `/mpd`
n'était référencé nulle part comme commande (seul le fichier de sortie s'appelle `mpd.md`,
sans rapport).

**Résolu** : gardé `schema` (cohérent avec le nom du skill générique du socle qu'il surcharge)
et `db-diagram`, supprimé `schema-impact` et `mpd`. Références mises à jour dans `migrate.md`
(agent + skill) et le hook de `settings.json`.

## FERME-16 — stack-python-supabase : `db-reset` contredit la stack déclarée — ✅ Résolu

Le module est "backend Python + ORM + Postgres/Supabase", mais `db-reset/SKILL.md` refusait
d'agir si PostgreSQL était détecté et imposait SQLite avec des chemins en dur — à l'inverse de
tous les autres skills du module qui découvrent tout via `CLAUDE.md`.

**Résolu** : réécrit pour gérer les deux cas (SQLite local en mode démo, ou reset via le
système de migration en place pour un Postgres/Supabase de dev), avec confirmation explicite
obligatoire avant toute action destructive et interdiction du `DROP DATABASE`.

## FERME-17 — feature-i18n : doublon `translations-react-python` — ✅ Résolu

`translations-react-python.md` avait `name: translations` (collision directe avec
`translations.md`) et était un doublon **byte-identique** de `translations.md` — aucun contenu
spécifique React ou Python malgré son nom. La "variante React/Python" annoncée dans
`catalog.md` était fictive.

**Résolu** : fichier supprimé (`.claude` et `.github`), `catalog.md` corrigé.

## FERME-18 — feature-i18n : règle auto-contradictoire — ✅ Résolu

La règle anti-tiret-cadratin de `translations/SKILL.md` affichait littéralement le même
caractère des deux côtés ("toujours `-`, jamais `-`") — le vrai tiret cadratin `—` avait été
perdu, rendant la règle inapplicable. Gouvernance (`allowed-tools`, `disable-model-invocation`)
également absente contrairement à l'alias `traduction/SKILL.md`.

**Résolu** : réécrit à l'identique de `traduction/SKILL.md` (caractère correct + gouvernance
alignée).

## FERME-19 — domain-immo : contradiction `design-system` / `ux-ui` — ✅ Résolu

Pas un simple chevauchement mais une vraie contradiction : `ux-ui.md` prescrivait `rounded-lg`
pour les cartes/boutons, alors que `design-system.md` impose `rounded-xl` pour tous les types de
card (section, table, toolbar, modale, empty state) et liste explicitement `rounded-lg`/
`rounded-md` comme anti-pattern interdit sur un conteneur. Les boutons sont en réalité en
`rounded-md` dans `design-system.md`, pas `rounded-lg` non plus.

**Résolu** : `ux-ui.md` corrigé pour renvoyer vers `design-system.md` comme source de vérité
sur les tokens de conteneurs plutôt que de dupliquer (et contredire) la règle.

## FERME-20 — stack-java-spring : fuite d'un projet réel unique — ✅ Résolu

Plusieurs fichiers (`ci`, `docs-update`, `product-owner`, `backlog-manager`, `coverage`,
`improve-architecture`) contenaient des détails d'un projet précis (Spring AI, Tika OCR, classe
`OcrSpringAiApplicationTest`, modules `service-llm`/`service-tika`, bean `LlmConfiguration`,
item backlog `NATIVE-001`, contrainte "runner ≥ 24 Go", Tesseract) qui dépassaient largement
"Java/Spring Boot/Maven générique".

**Résolu** : contenu géré différemment de FERME-1 (pas d'extraction vers un module dédié, la
matière ne le justifiait pas) — chaque mention spécifique remplacée par une découverte via
`CLAUDE.md` (dépendances, profils Maven, prérequis système déclarés plutôt que supposés). Le
concept générique et légitime de build natif GraalVM (réel dans l'écosystème Spring Boot,
pas propre à un seul projet) est conservé comme exemple explicitement conditionnel ("si le
projet en a un"). `coverage/SKILL.md` : le nom de classe de test spécifique remplacé par un
motif d'exclusion générique à adapter. `improve-architecture/SKILL.md` : noms de modules Maven
en dur remplacés par une découverte via `CLAUDE.md`.

## FERME-21 — stack-python-supabase : `settings.json` mélange frontend/backend — ✅ Résolu

Le hook `.jsx`/`.tsx` → `/translations` (frontend + module optionnel `feature-i18n` non
déclaré) a été retiré de `settings.json`. Le hook `[DEPS]` générique (`requirements.txt`/
`pyproject.toml`) est conservé sans le marqueur `package.json`, pour rester strictement
backend.

## FERME-22 — stack-java-spring : `backlog-refinement` sans skill dédié — ✅ Résolu

Résolu par le même changement que FERME-4 : l'agent a été renommé `backlog-manager`, il
surcharge automatiquement la version générique du socle à l'installation — aucun skill dédié
n'est nécessaire.

## FERME-23 — Fuites domaine mineures restantes — ✅ Résolu

`examples/stack-python-supabase/.claude/agents/fixture.md` : l'exemple `Lease` remplacé par un
exemple neutre (`User`). `examples/km-toolkit/` : note de distinction ajoutée dans
`postmortem.md` et `session-digest.md` (incident avec impact identifiable → `postmortem` ;
session complexe sans incident → `session-digest`).
