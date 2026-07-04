# Ferme agentic — bootstrap

**Bootstrap tech-agnostique** pour initialiser ou compléter une ferme agentique Claude Code /
GitHub Copilot sur n'importe quel projet de développement, quelle que soit la stack.

Le socle générique (`template/`) couvre les invariants de tout projet : qualité, tests, sécurité,
documentation, git. Les modules `examples/` ajoutent des agents/skills spécifiques à une stack
ou un domaine métier, copiables à la carte.

## Principe

```
ferme_agentic/
├── template/          ← LE socle générique (stack-agnostique) à poser sur chaque projet
│   ├── .claude/                      version Claude Code
│   │   ├── settings.json     permissions + hooks neutres (à compléter par stack)
│   │   ├── agents/           18 agents génériques (.md)
│   │   └── skills/           36 skills génériques (SKILL.md)
│   ├── .github/                      version Copilot (miroir)
│   │   ├── agents/           18 agents génériques (.agent.md)
│   │   ├── skills/           36 skills génériques (SKILL.md)
│   │   ├── extensions/       agents-loader + accessibility
│   │   ├── lsp.json          serveurs LSP (Python / TypeScript)
│   │   └── copilot-instructions.template.md  squelette à remplir
│   └── CLAUDE.template.md    squelette de CLAUDE.md à remplir
├── examples/          ← modules optionnels, ajoutés à la carte (idées conservées, pas perdues)
│   ├── stack-web-vite/        frontend Vite/React (PWA)
│   ├── stack-python-supabase/ backend Python + Postgres/Supabase (DB, migrations…)
│   ├── stack-java-spring/     backend Java/Spring/Maven
│   ├── domain-immo/           métier gestion immobilière (juridique…)
│   ├── feature-i18n/          internationalisation
│   └── km-toolkit/            Knowledge Management piloté par agents (+ mainframe COBOL)
├── scripts/            ← outillage de maintenance de la ferme elle-même
│   ├── validate_farm.py         détecte les régressions (miroirs désynchronisés, outils Copilot/Claude mélangés, JSON invalide)
│   └── generate_github_mirror.py régénère `.github/` depuis `.claude/` (source de vérité) au lieu de dupliquer à la main
├── catalog.md         ← inventaire détaillé (rôle de chaque agent/skill)
├── CHANGELOG.md        ← historique des versions de la ferme
├── VERSION             ← version courante de la ferme
└── INSTALL.md         ← procédure d'installation sur un nouveau projet
```

## Pourquoi cette séparation `template` / `examples`

- **`template`** = ce qui est vrai partout (qualité, tests, sécurité, docs, git). On le copie tel quel.
- **`examples`** = ce qui dépend d'une stack ou d'un métier. Trop spécifique pour le socle, mais
  **l'idée du skill/agent est conservée** : on copie le module pertinent et on adapte, plutôt que
  de la réinventer.

Le socle a été dérivé du projet web le plus complet et le plus neutre (`petite-etoile`), puis les
éléments réellement spécifiques (DB, build Maven, i18n, métier immo, KM mainframe) ont été déplacés
dans `examples/`.

## Double version : Claude Code et Copilot

`template/` et chaque module `examples/` existent en **deux versions miroir**, à contenu
identique :

- **`.claude/`** — agents `*.md`, skills `*/SKILL.md`, `settings.json` (Claude Code).
- **`.github/`** — agents `*.agent.md` (chargés par `extensions/agents-loader`), skills `*/SKILL.md`,
  `lsp.json`, `copilot-instructions.template.md` (GitHub Copilot).

Installer la version correspondant à l'outil utilisé (ou les deux). Voir `INSTALL.md`.

**`.claude/` est la source de vérité.** `.github/` est dérivé automatiquement par
`scripts/generate_github_mirror.py` (corps identique, seul le frontmatter `tools:` est traduit
vers la syntaxe Copilot). Après toute modification d'un agent ou skill `.claude/`, lancer :

```bash
python3 scripts/generate_github_mirror.py --write   # régénère .github/
python3 scripts/validate_farm.py                    # vérifie l'ensemble (miroirs, outils, JSON)
```

## Démarrage rapide

Voir `INSTALL.md`. En résumé : copier `template/.claude/` dans le nouveau projet, renommer
`CLAUDE.template.md` → `CLAUDE.md` et le remplir, puis ajouter les modules `examples/` utiles.

## Note

Les fichiers du socle peuvent encore citer des détails du projet d'origine (sablier, React…)
en **exemple**. Ce sont des illustrations, pas de la logique figée : adapter les chemins/commandes
au projet cible (cf. la même convention que `examples/km-toolkit/INSTALL.md`).
