---
name: farm-init
description: Point d'entrée universel de la ferme — détecte si le socle est installé, guide l'installation si nécessaire, brainstorme les modules à ajouter selon le projet, puis audite la configuration. À lancer en tout premier sur un projet vierge ou repris.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Farm Init — Installation, brainstorm et audit

Point d'entrée universel. Adapte son comportement selon l'état détecté.

---

## Phase 0 — Détecter l'état

```bash
ls .claude/agents/ 2>/dev/null | wc -l
ls .claude/skills/ 2>/dev/null | wc -l
ls CLAUDE.md 2>/dev/null && echo "present" || echo "absent"
```

- **0 agents** → Mode A : installation guidée
- **Agents présents + CLAUDE.md avec `{{`** → Mode B : configuration incomplète, reprendre à Phase 2
- **Agents présents + CLAUDE.md propre** → Mode C : audit seul (Phase 4)

---

## Mode A — Installation guidée (ferme absente)

### A1. Localiser la ferme

Demander :
> "La ferme agentique n'est pas encore installée sur ce projet. Quel est le chemin absolu vers votre clone de la ferme ? (ex: /Users/moi/ferme_agentic)"

Vérifier que le chemin existe et contient `template/.claude/agents/`.

### A2. Copier le socle

```bash
mkdir -p .claude .github
cp -R "<FERME>/template/.claude/agents"   .claude/
cp -R "<FERME>/template/.claude/skills"   .claude/
cp -n  "<FERME>/template/.claude/settings.json" .claude/settings.json
cp -R "<FERME>/template/.github/agents"     .github/
cp -R "<FERME>/template/.github/skills"     .github/
cp -R "<FERME>/template/.github/extensions" .github/
cp -n  "<FERME>/template/.github/lsp.json"  .github/lsp.json
cp -n  "<FERME>/template/.github/copilot-instructions.template.md" .github/copilot-instructions.md
cp -n  "<FERME>/template/CLAUDE.template.md" CLAUDE.md
```

Confirmer le résultat :
```bash
echo "Agents : $(ls .claude/agents/*.md 2>/dev/null | wc -l)"
echo "Skills : $(ls .claude/skills/*/SKILL.md 2>/dev/null | wc -l)"
```

Enchaîner sur Phase 2.

---

## Phase 2 — Compléter CLAUDE.md

Lire `CLAUDE.md` et identifier les placeholders `{{...}}` non remplacés.

Pour chaque placeholder manquant, poser la question directement :

- `{{NOM_DU_PROJET}}` → "Quel est le nom du projet ?"
- Stack (langage, framework, tests, base de données, build) → "Quelle est votre stack ? (ex: Node 20 + Express, Python 3.12 + FastAPI, Java 21 + Spring Boot, Go 1.22 + Gin…)"
- Commandes (`dev`, `build`, `lint`, `test`) → "Quelles sont les commandes de votre cycle de dev ?"
- Conventions → "Y a-t-il des conventions particulières à retenir ? (nommage, branches, règles de commit…)"

Remplir les placeholders dans `CLAUDE.md` au fur et à mesure des réponses.

---

## Phase 3 — Brainstorm modules

> "Maintenant explorons les modules optionnels à ajouter. Je vais vous poser quelques questions sur votre projet pour vous recommander les plus utiles."

### Questions de brainstorm

Poser ces questions une par une, en attendant la réponse :

1. **Base de données** : "Avez-vous une base de données ? Si oui, laquelle et quel ORM ?"
   - PostgreSQL/Supabase + Python → suggérer `stack-python-supabase`
   - PostgreSQL/MySQL + Java → suggérer `stack-java-spring`
   - Prisma/TypeORM + Node → suggérer les skills `schema`, `migrate`, `db-diagram` du socle

2. **Frontend** : "Y a-t-il un frontend ? Quel framework ?"
   - React/Vite → suggérer `stack-web-vite`
   - Autre → les skills `accessibility`, `design-system`, `ux-ui` du socle suffisent

3. **Internationalisation** : "L'application est-elle multilingue ?"
   - Oui → suggérer `feature-i18n`

4. **Mémoire décisionnelle** : "Avez-vous des décisions architecturales importantes à capturer et à retrouver facilement ?"
   - Oui → suggérer `feature-decision-index`
   - Si km-toolkit déjà envisagé → proposer à la place

5. **Documentation structurée / Knowledge Base** : "Avez-vous besoin d'une documentation pilotée par agents (wiki, ADR, runbooks) ?"
   - Oui → suggérer `km-toolkit` avec lien vers son INSTALL.md

6. **Coûts token** : "Travaillez-vous avec plusieurs agents en parallèle ou sur des tâches longues ?"
   - Oui → suggérer `finops`

### Pour chaque module recommandé

Présenter un résumé en 2 lignes :
> "`feature-decision-index` — capture vos décisions architecturales dans `.decisions/` et les injecte automatiquement en contexte. 3 skills : `/record`, `/recall`, `/harvest`. Voulez-vous l'ajouter ? (oui/non)"

Si oui : copier agents + skills depuis `<FERME>/examples/<module>/` vers `.claude/` (et `.github/` si présent).

### Récapitulatif des modules ajoutés

Après le brainstorm, afficher la liste des modules installés.

---

## Phase 4 — Audit de configuration

### Checks

```bash
# CLAUDE.md
ls CLAUDE.md 2>/dev/null && echo "present" || echo "absent"
grep -c '{{' CLAUDE.md 2>/dev/null
wc -l < CLAUDE.md 2>/dev/null

# Agents / skills
ls .claude/agents/*.md 2>/dev/null | wc -l
ls .claude/skills/*/SKILL.md 2>/dev/null | wc -l

# settings.json
jq . .claude/settings.json 2>/dev/null && echo "JSON valide" || echo "invalide ou absent"
jq -r '.permissions.allow[]' .claude/settings.json 2>/dev/null | grep -iE "(npm|pip|mvn|cargo|go |make|gradle|pytest|jest|dotnet|ruff|alembic)" | head -5
jq 'has("hooks")' .claude/settings.json 2>/dev/null

# .gitignore
grep -cE "^(node_modules|__pycache__|\.env|venv|\.venv|target/|dist/|build/)$" .gitignore 2>/dev/null
```

### Rapport final

```
## Farm Init — Configuration

| Section        | Statut | Notes                                          |
|----------------|--------|------------------------------------------------|
| CLAUDE.md      | ✅/⚠️/❌ | ⚠️ si > 200 lignes (instructions ignorées silencieusement au-delà) |
| Agents         | ✅/⚠️/❌ | X agents                                      |
| Skills         | ✅/⚠️/❌ | X skills                                      |
| settings.json  | ✅/⚠️/❌ |                                               |
| Hooks          | ✅/⚠️/❌ |                                               |
| .gitignore     | ✅/⚠️/❌ |                                               |

### Actions recommandées
[uniquement les points ⚠️ et ❌, avec la correction concrète]
```

> Si tout est ✅ : "La ferme est correctement configurée. Lancez `/audit` pour un premier pre-flight sur le code."
