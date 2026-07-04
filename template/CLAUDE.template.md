# {{NOM_DU_PROJET}}

> Squelette de `CLAUDE.md`. Remplacer les `{{placeholders}}`, supprimer les sections inutiles.
> Les instructions ici sont **prioritaires** et doivent rester courtes et actionnables.

## Stack

- **Langage / runtime** : {{ex: Node 20 / Python 3.12 / Java 21 / Go 1.22 / .NET 8 / Ruby 3.3}}
- **Framework** : {{ex: Vite + React / FastAPI / Spring Boot / Gin / Rails / aucun}}
- **Tests** : {{ex: Vitest / pytest / JUnit / go test / RSpec}}
- **Base de données** : {{ex: aucune / PostgreSQL / SQLite / MongoDB / Redis}}
- **Build / packaging** : {{ex: npm / Maven / Gradle / cargo / make / docker}}

## Commandes essentielles

| But | Commande |
|---|---|
| Dev / run | `{{commande pour lancer l'app localement}}` |
| Build | `{{commande de build}}` |
| Lint | `{{commande de lint}}` |
| Tests unitaires | `{{commande de test}}` |
| Tests E2E | `{{commande e2e — supprimer si absent}}` |

## Structure

```
{{décrire brièvement l'arborescence clé du projet}}
src/          ← sources principales
tests/        ← tests
docs/         ← documentation
```

> Adapter les chemins dans les agents/skills si l'arborescence diffère des conventions par défaut.

## Conventions

- {{Convention de nommage des fichiers / fonctions / classes}}
- {{Règles de commit et de branches}}
- {{Style : ne jamais …, toujours …}}
- {{Contraintes spécifiques au projet ou à la stack}}

## Avant de committer

Lancer `/pre-commit` (ou la chaîne : lint + test + build). Voir le hook `PreToolUse` dans `.claude/settings.json`.

## Agents & skills installés

Socle générique (`template/.claude/`) — tech-agnostique, couvre qualité, tests, sécurité, docs, git.

Modules optionnels ajoutés à ce projet :
- [ ] DB / migrations (`examples/stack-python-supabase` ou `examples/stack-java-spring`)
- [ ] Frontend React/Vite (`examples/stack-web-vite`)
- [ ] i18n (`examples/feature-i18n`)
- [ ] KM / documentation pilotée par agents (`examples/km-toolkit`)
- [ ] Métier : {{ex: `examples/domain-immo`}}
