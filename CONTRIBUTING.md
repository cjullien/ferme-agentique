# Contribuer à la ferme agentic

Merci de vouloir enrichir la ferme ! Voici les conventions à respecter pour que chaque contribution
s'intègre proprement.

## Règle d'or : `.claude/` est la source de vérité

Ne jamais modifier `.github/` à la main. Toujours travailler dans `.claude/`, puis générer le miroir :

```bash
python3 scripts/generate_github_mirror.py --write
python3 scripts/validate_farm.py
```

## Ajouter un agent au socle

1. Créer `template/.claude/agents/<nom>.md` avec le frontmatter `tools:` en noms Claude Code
   (`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`).
2. Générer le miroir (commandes ci-dessus).
3. Documenter l'agent dans `catalog.md` (section « Socle générique — Agents »).
4. Mettre à jour le comptage dans `README.md` et `catalog.md` si nécessaire.

## Ajouter un skill au socle

1. Créer `template/.claude/skills/<nom>/SKILL.md`.
2. Générer le miroir.
3. Ajouter le skill dans la liste thématique du `catalog.md`.

## Ajouter un module `examples/`

1. Créer `examples/<nom>/.claude/agents/` et/ou `examples/<nom>/.claude/skills/`.
2. Générer le miroir (`--write` parcourt aussi `examples/`).
3. Valider (`validate_farm.py`).
4. Documenter dans `catalog.md` (section « Modules optionnels ») et `README.md` (arborescence).
5. Ajouter un `INSTALL.md` dans le module si la procédure d'installation est non triviale.

## Règles de nommage

| Fichier | Convention |
|---|---|
| Agent Claude Code | `template/.claude/agents/<nom>.md` |
| Agent Copilot (généré) | `template/.github/agents/<nom>.agent.md` |
| Skill | `template/.claude/skills/<nom>/SKILL.md` |
| Module example | `examples/<stack-ou-feature>/` |

## Workflow PR

1. Créer une branche : `git checkout -b feat/<nom-court>`
2. Apporter les modifications dans `.claude/`
3. Générer + valider : `python3 scripts/generate_github_mirror.py --write && python3 scripts/validate_farm.py`
4. Committer les deux versions (`.claude/` **et** `.github/` générée)
5. Ouvrir une Pull Request — la CI relancera la validation

## CI

Le workflow `.github/workflows/ci.yml` vérifie à chaque push/PR :
- que `.github/` est synchronisé avec `.claude/`
- qu'aucun fichier ne mélange les noms d'outils des deux plateformes
- que tous les `settings.json` sont du JSON valide

## Release

Le workflow `.github/workflows/release.yml` est déclenché manuellement et :
- relance les validations du dépôt
- crée le tag `vX.Y.Z` à partir de `VERSION`
- publie la GitHub Release
- incrémente `VERSION` selon `patch/minor/major`
