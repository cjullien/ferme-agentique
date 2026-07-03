# Changelog

Historique des versions de la ferme agentic. Un projet qui a installé une version donnée peut
comparer son `.claude/`/`.github/` local à celui du dépôt pour savoir s'il a pris les correctifs
d'une version plus récente.

## [1.1.0] — 2026-07-03

### Corrigé
- 13 agents `.claude/agents/*.md` du socle utilisaient des noms d'outils Copilot
  (`read_file`, `run_in_terminal`...) au lieu des noms Claude Code (`Read`, `Bash`...) —
  copie non traduite depuis `.agent.md`. Même bug trouvé et corrigé dans `examples/stack-web-vite`
  (`externalize`, `agent-maintainer`) et, en sens inverse (noms Claude Code dans des `.agent.md`
  Copilot), dans 19 fichiers du socle et de 4 modules `examples/`.
- Les hooks `PreToolUse`/`PostToolUse` de `settings.json` (socle + `stack-web-vite` +
  `stack-python-supabase`) lisaient `$CLAUDE_TOOL_INPUT`, une variable d'environnement qui
  n'existe pas côté Claude Code — le payload est transmis en JSON sur stdin. Les hooks ne se
  déclenchaient donc jamais.
- `settings.json` (socle + 2 modules) : la deny-list bloquait `git push --force` et
  `git reset --hard`/`git clean -f` uniquement quand un argument suivait, laissant passer
  `--force-with-lease` et les invocations sans argument. Ajout d'un blocage de `curl`/`wget`
  en entier (plus robuste qu'essayer de bloquer `curl ... | bash` par pattern, cf. doc
  officielle des règles de permission Bash) et de deux règles ciblant `git checkout -- *`
  / `git checkout .` (peuvent écraser des modifications non commitées).
- `clean-tdd.md` (socle) : l'introduction se présentait comme un agent React/Vitest alors
  que le corps du fichier décrivait une architecture backend (routers/services/domain,
  FastAPI-style) — rendu stack-agnostique comme les autres agents du socle.
- 7 emplacements du socle traitaient la mise à jour de `docs/specs/backlog.md` comme
  "OBLIGATOIRE" sans vérifier son existence : comportement non défini sur un projet sans ce
  fichier. Ajout d'un garde-fou (ignorer si absent) sur les agents où c'est un effet de bord
  (`accessibility`, `owasp`, `performance`, `audit-360`, `review`) ; le chemin est documenté
  comme adaptable via `CLAUDE.md` sur les agents où le backlog est le sujet central
  (`backlog-manager`, `product-owner`).
- `catalog.md`/`INSTALL.md` : suppression de la mention d'alias (`a11y`, `deps`, `perf`,
  `quick-push`) inexistants dans le socle actuel ; ajout des agents manquants dans l'entrée
  `stack-web-vite` du catalogue ; correction d'une référence à un `settings.json` Java/Spring
  qui n'existe pas ; remplacement du chemin personnel en dur par un placeholder.
- `audit-360/SKILL.md` : le texte annonçait "16 agents" (compte figé) au lieu de renvoyer aux
  tableaux socle + conditionnels.

### Ajouté
- `scripts/validate_farm.py` : détecte les régressions rencontrées ci-dessus (miroirs
  `.claude`/`.github` désynchronisés, outils Copilot/Claude Code mélangés, JSON invalide).
- `scripts/generate_github_mirror.py` : génère `.github/` depuis `.claude/` (source de
  vérité) au lieu de maintenir les deux à la main — élimine la classe de bug ci-dessus à la
  racine plutôt que de compter sur une revue manuelle.
- `CHANGELOG.md` et `VERSION` : suivi de version de la ferme elle-même.

## [1.0.0] — commit initial

Extraction du socle `template/` et des modules `examples/` depuis les projets POC-NB
(`boulier-app`, `gestion-immo`, `ocr-spring-ai`, `petite-etoile`, `sablier_app_web`) et du
`km-toolkit`.
