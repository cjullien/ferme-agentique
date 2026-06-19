# {{NOM_DU_PROJET}}

> Squelette de `CLAUDE.md`. Remplacer les `{{placeholders}}`, supprimer les sections inutiles.
> Les instructions ici sont **prioritaires** et doivent rester courtes et actionnables.

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

- {{Convention de ncommage / structure de dossiers}}
- {{Règles de commit, branches}}
- {{Style : ne jamais …, toujours …}}

## Avant de committer

Lancer `/pre-commit` (ou la chaîne : lint + test + build). Voir le hook `PreToolUse` dans `.claude/settings.json`.

## Agents & skills

Socle générique installé depuis la **ferme agentic** (`template/.claude/`). Catalogue complet : voir `catalog.md` à la racine de la ferme.

Modules optionnels ajoutés à ce projet :
- [ ] i18n (`examples/feature-i18n`)
- [ ] DB/migrations (`examples/stack-python-supabase`)
- [ ] KM / documentation pilotée par agents (`examples/km-toolkit`)
