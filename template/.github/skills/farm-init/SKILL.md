---
name: farm-init
description: Point d'entrée universel de la ferme — détecte si le socle est installé, guide l'installation si nécessaire, brainstorme les modules à ajouter selon le projet, puis audite la configuration. À lancer en tout premier sur un projet vierge ou repris.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
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
> "La ferme agentique n'est pas encore installée sur ce projet. Fournissez :
> - un chemin local : `/Users/moi/ferme_agentic`
> - ou une URL GitHub : `https://github.com/org/ferme_agentic`"

**Si chemin local** : vérifier qu'il existe et contient `template/.claude/agents/`.

**Si URL GitHub** : cloner dans `~/.claude/ferme_agentic` (ou demander le répertoire cible) :
```bash
git clone "<URL>" ~/.claude/ferme_agentic 2>/dev/null \
  || git -C ~/.claude/ferme_agentic pull 2>/dev/null
```
Utiliser `~/.claude/ferme_agentic` comme `<FERME>`.

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

Sauvegarder le chemin pour `/farm-update` :
```bash
echo "<FERME>" > .claude/.farm-source
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

**Obligatoire : poser chacune des 6 questions ci-dessous via l'outil `AskUserQuestion` (une question à la fois, attendre la réponse avant de passer à la suivante). Ne jamais supposer une réponse par défaut (ex: "pas de DB", "pas multilingue") ni sauter cette phase — c'est ce qui garantit que `feature-i18n`, `stack-web-vite`, etc. sont réellement proposés plutôt qu'omis silencieusement.**

### Questions de brainstorm

Poser ces questions une par une, en attendant la réponse :

1. **Base de données** : "Avez-vous une base de données ? Si oui, laquelle et quel ORM ?"
   - PostgreSQL/Supabase + Python → suggérer `stack-python-supabase`
   - PostgreSQL/MySQL + Java → suggérer `stack-java-spring`
   - Prisma/TypeORM + Node → suggérer les skills `schema`, `migrate`, `db-diagram` du socle

2. **Frontend** : "Y a-t-il un frontend ? Quel framework ?"
   - React/Vite → suggérer `stack-web-vite`
   - Autre → les skills `accessibility`, `design-system`, `ux-ui` du socle suffisent
   - Si oui (quel que soit le framework) : l'agent `design-system` du socle est livré vide
     (section "Périmètre à instancier" à remplir — voir `template/.claude/agents/design-system.md`).
     Demander : "Voulez-vous instancier l'agent `design-system` maintenant à partir de 3-5
     composants représentatifs du projet (tokens, composants de référence, anti-patterns) ?
     Sans cette étape l'agent reste un squelette générique et ne sera jamais réellement appliqué."
     Si oui, suivre la procédure décrite dans l'agent avant de poursuivre le brainstorm.

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

### Question finale — stack non couverte

Après les 6 questions, vérifier si la stack du projet correspond à un module existant de la ferme.

**Stacks couvertes** : Python/FastAPI/Django, Java/Spring, Node/Vite/React, domaine immo.
**Stacks non couvertes** : Go, .NET, Ruby/Rails, PHP, mobile (React Native, Flutter), Rust, Scala, Elixir, etc.

Si la stack du projet n'est pas couverte par un module existant :

> "Votre stack ({{stack}}) n'a pas encore de module dédié dans la ferme. Voulez-vous en créer un ? Cela prend ~10 minutes et permettra aux prochains projets sur cette stack de bénéficier de vos agents/skills dès le départ."

**Si oui** — lancer `/farm-new-module` (scaffolding complet du module, puis commit optionnel dans `<FERME>`).
**Si non** — passer au récapitulatif. Le socle générique est suffisant pour démarrer.

### Récapitulatif des modules ajoutés

Après le brainstorm, afficher :
- Modules installés sur ce projet
- Si un nouveau module a été créé via `/farm-new-module` : "✅ Module `stack-<nom>` ajouté à la ferme — les prochains projets sur cette stack en bénéficieront directement."

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
