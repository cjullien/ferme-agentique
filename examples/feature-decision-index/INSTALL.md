# Installer feature-decision-index

Module léger de capture de décisions architecturales. Zéro infrastructure — juste des fichiers Markdown committés dans `.decisions/`.

> Alternative légère à `km-toolkit/adr-capture` pour les projets sans besoin de KB complète.

## 1. Copier les agents et skills

```bash
FERME=/chemin/vers/ferme_agentic

# Version Claude Code
cp "$FERME/examples/feature-decision-index/.claude/agents/decision-record.md"  .claude/agents/
cp "$FERME/examples/feature-decision-index/.claude/agents/decision-harvest.md" .claude/agents/
cp -R "$FERME/examples/feature-decision-index/.claude/skills/record"   .claude/skills/
cp -R "$FERME/examples/feature-decision-index/.claude/skills/recall"   .claude/skills/
cp -R "$FERME/examples/feature-decision-index/.claude/skills/harvest"  .claude/skills/

# Version Copilot (optionnel)
cp "$FERME/examples/feature-decision-index/.github/agents/decision-record.agent.md"  .github/agents/
cp "$FERME/examples/feature-decision-index/.github/agents/decision-harvest.agent.md" .github/agents/
cp -R "$FERME/examples/feature-decision-index/.github/skills/record"   .github/skills/
cp -R "$FERME/examples/feature-decision-index/.github/skills/recall"   .github/skills/
cp -R "$FERME/examples/feature-decision-index/.github/skills/harvest"  .github/skills/
```

## 2. Créer le dossier .decisions/

```bash
mkdir -p .decisions
```

Ajouter à `.gitignore` si les décisions ne doivent pas être versionnées (déconseillé — versionner les décisions est la valeur principale du module).

## 3. Activer la constitution dans CLAUDE.md

Ajouter cette ligne dans `CLAUDE.md` (après la section Stack ou Conventions) :

```markdown
@.decisions/CONSTITUTION.md
```

Claude Code injectera automatiquement le contenu de ce fichier à chaque session. La constitution est créée automatiquement par `/record` ou `/harvest` lors de la première décision fondamentale capturée.

## 4. Utilisation

| Skill | Quand l'utiliser |
|---|---|
| `/record` | Après une décision importante — "on utilise JWT", "on passe à Postgres" |
| `/recall <mot-clé>` | Avant de remettre en question un choix — retrouver pourquoi il a été fait |
| `/harvest` | En début de projet ou reprise d'existant — détecter les décisions implicites |

## Format des décisions

Les décisions sont stockées dans `.decisions/<domaine>/<YYYY-MM-DD>-<slug>.md` :

```markdown
---
date: 2026-07-04
domain: auth
status: active
---
# JWT stateless tokens

## Contexte
...

## Décision
...

## Conséquences
...
```

Statuts possibles : `active` · `superseded` · `deprecated`
