# Ferme agentic — template

Socle réutilisable d'**agents** et de **skills** Claude Code, extrait des projets POC-NB
(`boulier-app`, `gestion-immo`, `ocr-spring-ai`, `petite-etoile`, `sablier_app_web`) et du
`km-toolkit`. Objectif : démarrer tout nouveau projet avec la même boîte à outils agentique,
sans repartir de zéro.

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
├── catalog.md         ← inventaire détaillé (rôle de chaque agent/skill)
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

Chaque socle/module existe en **deux versions miroir**, à contenu identique :

- **`.claude/`** — agents `*.md`, skills `*/SKILL.md`, `settings.json` (Claude Code).
- **`.github/`** — agents `*.agent.md` (chargés par `extensions/agents-loader`), skills `*/SKILL.md`,
  `lsp.json`, `copilot-instructions.template.md` (GitHub Copilot).

Installer la version correspondant à l'outil utilisé (ou les deux). Voir `INSTALL.md`.

## Démarrage rapide

Voir `INSTALL.md`. En résumé : copier `template/.claude/` dans le nouveau projet, renommer
`CLAUDE.template.md` → `CLAUDE.md` et le remplir, puis ajouter les modules `examples/` utiles.

## Note

Les fichiers du socle peuvent encore citer des détails du projet d'origine (sablier, React…)
en **exemple**. Ce sont des illustrations, pas de la logique figée : adapter les chemins/commandes
au projet cible (cf. la même convention que `examples/km-toolkit/INSTALL.md`).
