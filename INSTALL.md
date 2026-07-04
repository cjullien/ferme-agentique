# Installer la ferme agentic sur un nouveau projet

> Deux versions miroir sont disponibles : **Claude Code** (`.claude/`) et **Copilot** (`.github/`).
> Installer celle de l'outil utilisé — ou les deux (contenus identiques).

## 1. Poser le socle générique

### Version Claude Code (`.claude/`)

Depuis la racine du projet cible :

```bash
FERME=/chemin/vers/votre/clone/de/ferme-agentique   # adapter à votre environnement

mkdir -p .claude
cp -R "$FERME/template/.claude/agents"   .claude/
cp -R "$FERME/template/.claude/skills"   .claude/
cp -n  "$FERME/template/.claude/settings.json" .claude/settings.json   # ne pas écraser un existant
```

### Version Copilot (`.github/`)

```bash
mkdir -p .github
cp -R "$FERME/template/.github/agents"     .github/
cp -R "$FERME/template/.github/skills"     .github/
cp -R "$FERME/template/.github/extensions" .github/
cp -n  "$FERME/template/.github/lsp.json"  .github/lsp.json
cp -n  "$FERME/template/.github/copilot-instructions.template.md" .github/copilot-instructions.md
```

Les agents `*.agent.md` sont chargés automatiquement par `extensions/agents-loader` au démarrage
de session. Remplir ensuite `copilot-instructions.md` (placeholders) comme un `CLAUDE.md`.

## 2. Créer le CLAUDE.md

```bash
cp "$FERME/template/CLAUDE.template.md" CLAUDE.md
```

Remplir les `{{placeholders}}` (stack, commandes dev/build/lint/test) et supprimer les sections inutiles.

## 3. Adapter `settings.json` à la stack

Le `settings.json` du socle n'autorise que des commandes neutres (lecture, git read, `jq`, `rtk`…).
Ajouter les commandes de build/test de la stack en s'inspirant des exemples :

| Stack | Fichier de référence |
|---|---|
| Web Vite/React | `examples/stack-web-vite/.claude/settings.json` |
| Python/Supabase | `examples/stack-python-supabase/.claude/settings.json` |
| Java/Spring/Maven | `examples/stack-java-spring/.claude/settings.json` |
| Autre stack | Ajouter manuellement : commandes de build/test/lint de la stack, git read, gh, rtk |

**Principe pour toute stack non listée** : identifier les commandes courantes du cycle dev
(`build`, `test`, `lint`, `run`) et les ajouter à `permissions.allow`. Le socle couvre déjà
git, gh, lecture (`ls`, `find`, `grep`, `rg`, `cat`, `head`, `tail`, `jq`), et `rtk`.

Compléter aussi les hooks `PostToolUse` (rappels migrations / lint / tests…) selon le besoin.

## 4. Ajouter les modules optionnels

Les modules `examples/` couvrent les stacks les plus courantes. Pour une stack absente des
exemples, le socle seul suffit : ses 18 agents et 36 skills sont tech-agnostiques et couvrent
qualité, tests, sécurité, documentation et git sur n'importe quelle techno. Les exemples sont
des **points de départ**, pas des prérequis.

Copier uniquement les dossiers `agents/` et `skills/` du module voulu :

```bash
# Exemple : projet Python avec base de données
cp -R "$FERME/examples/stack-python-supabase/.claude/agents/." .claude/agents/
cp -R "$FERME/examples/stack-python-supabase/.claude/skills/." .claude/skills/

# Exemple : internationalisation
cp -R "$FERME/examples/feature-i18n/.claude/agents/." .claude/agents/
cp -R "$FERME/examples/feature-i18n/.claude/skills/." .claude/skills/
```

Pour la **version Copilot**, copier la variante `.github/` du même module :

```bash
cp -R "$FERME/examples/stack-python-supabase/.github/agents/." .github/agents/
cp -R "$FERME/examples/stack-python-supabase/.github/skills/." .github/skills/
```

Pour le **km-toolkit** (KB pilotée par agents / mainframe), suivre sa propre procédure :
`examples/km-toolkit/INSTALL.md`.

### FinOps — contrôle des coûts token (recommandé sur tout projet)

```bash
cp -R "$FERME/examples/finops/.claude/skills/." .claude/skills/
```

Merger ensuite l'entrée `PostToolUse` de `examples/finops/settings.finops.json` dans le tableau
`hooks.PostToolUse` de votre `settings.json` (ne pas remplacer les entrées existantes).

Coller le contenu de `examples/finops/CLAUDE.finops.md` à la fin du `CLAUDE.md` du projet.

Ajouter `.claude/finops.log` au `.gitignore` du projet.

## 5. Nettoyer le hors-stack

- Supprimer les agents/skills sans objet sur le projet (ex : `design-system`, `ux-ui`,
  `accessibility` sur un projet purement backend).

## 6. Vérifier

```bash
ls .claude/agents .claude/skills        # version Claude
ls .github/agents .github/skills        # version Copilot
```

Dans Claude Code, taper `/` : les skills installées doivent apparaître. Lancer `/audit` ou
`/instructions-update` pour valider la cohérence agents ↔ CLAUDE.md.
Dans Copilot, les agents `.github/agents/*.agent.md` sont annoncés au démarrage de session par
`extensions/agents-loader`.

## Convention de chemins

Les agents/skills supposent par défaut : sources sous `src/` (et `backend/`, `frontend/` pour
les projets séparés), tests sous `tests/` ou `__tests__/`, docs sous `docs/`. Si l'arborescence
du projet diffère, ajuster les chemins **dans les fichiers concernés** — ce sont des conventions,
pas du code en dur.

## Ajouter un nouveau module à la ferme

Quand un projet introduit des agents/skills non couverts par le socle (ex : nouvelle stack, nouveau
domaine métier), les reverser dans la ferme plutôt que de les laisser dans le projet :

1. Créer `examples/<nom-du-module>/.claude/` (agents + skills) et générer le miroir `.github/` :
   ```bash
   python3 scripts/generate_github_mirror.py --write
   ```
2. Valider :
   ```bash
   python3 scripts/validate_farm.py
   ```
3. Documenter le module dans `catalog.md` et committer.

La ferme grandit ainsi avec chaque projet sans jamais perdre la connaissance accumulée.
