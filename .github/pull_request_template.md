## Objectif

Décrire en 1-2 phrases ce que cette PR apporte.

## Type de changement

- [ ] Correction
- [ ] Nouvelle feature
- [ ] Documentation
- [ ] Refactor / maintenance

## Portée

- [ ] `template/.claude`
- [ ] `template/.github`
- [ ] `examples/`
- [ ] `scripts/`
- [ ] `docs` (`README`, `INSTALL`, `catalog`, `CHANGELOG`)

## Checklist

- [ ] Les changements sont faits côté `.claude` (source de vérité)
- [ ] Le miroir `.github` a été régénéré (`python3 scripts/generate_github_mirror.py --write`)
- [ ] La validation passe (`python3 scripts/validate_farm.py`)
- [ ] La documentation liée a été mise à jour
- [ ] Les comptes (agents/skills) sont cohérents si impactés

## Notes de validation

Coller ici la sortie utile des commandes exécutées.

