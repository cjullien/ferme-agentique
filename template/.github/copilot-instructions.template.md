# {{NOM_DU_PROJET}} — Instructions Copilot

> Squelette de `.github/copilot-instructions.md`. Miroir Copilot du `CLAUDE.md`.
> Remplacer les `{{placeholders}}`, supprimer les sections inutiles.
> Les instructions ici sont **prioritaires** et doivent rester courtes et actionnables.

## Comportement général

- Répondre en **français** (sauf code et commandes).
- Être concis et orienté action.
- Faire des **éditions chirurgicales** : ne pas réécrire un fichier complet pour un changement localisé.
- Vérifier d'abord le contexte projet (instructions `.github/`, `CLAUDE.md` s'il existe) avant de modifier du code.

## Stack

- **Langage / runtime** : {{ex: Node 20 / Python 3.12 / Java 21}}
- **Framework** : {{ex: Vite + React / FastAPI / Spring Boot}}
- **Tests** : {{ex: Vitest + Playwright / pytest / JUnit}}
- **Base de données** : {{ex: aucune / Supabase Postgres / —}}

## Commandes essentielles

| But | Commande |
|---|---|
| Dev | `{{npm run dev}}` |
| Build | `{{npm run build}}` |
| Lint | `{{npm run lint}}` |
| Tests | `{{npm test}}` |
| E2E | `{{npm run e2e}}` |

## Conventions

- {{Convention de nommage / structure de dossiers}}
- {{Règles de commit, branches}}
- {{Style : ne jamais …, toujours …}}

## Avant de committer

Lancer `/pre-commit` (ou la chaîne : lint + test + build).

## Agents & skills

Socle générique installé depuis la **ferme agentic** (`template/.github/`). Catalogue complet : voir
`catalog.md` à la racine de la ferme.

- Les **agents** vivent dans `.github/agents/*.agent.md` et sont chargés par
  `.github/extensions/agents-loader`.
- Les **skills** vivent dans `.github/skills/<nom>/SKILL.md`.
- `.github/lsp.json` configure les serveurs LSP (Python / TypeScript par défaut).

Modules optionnels ajoutés à ce projet :
- [ ] i18n (`examples/feature-i18n`)
- [ ] DB/migrations (`examples/stack-python-supabase`)
- [ ] KM / documentation pilotée par agents (`examples/km-toolkit`)
