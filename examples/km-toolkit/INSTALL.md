# KM Toolkit — installation sur un nouveau projet

Chaîne complète d'agents de **Knowledge Management piloté par agents** : génération de KB
depuis le code, audit de fraîcheur/complétude, et dispositif mainframe COBOL à grande échelle.
Réutilisable sur n'importe quel projet (le socle KM est agnostique ; les agents `mf-*` ciblent
les patrimoines COBOL/mainframe).

## Contenu

Comme les autres modules `examples/`, deux versions miroir à contenu identique :

```
km-toolkit/
├── .claude/
│   ├── agents/    24 agents (.md)         — noms d'outils Claude Code (Read, Write, Edit, Bash, Grep, Glob)
│   └── skills/    24 skills (SKILL.md)    — les déclencheurs invocables
├── .github/
│   ├── agents/    24 agents (.agent.md)   — noms d'outils Copilot (read_file, create_file...)
│   └── skills/    24 skills (SKILL.md)    — identiques à .claude/skills/
├── hooks.py       hook MkDocs             — moteur d'override universel
├── test_hooks.py  garde-fou du hook       — `python3 km-toolkit/test_hooks.py`
└── INSTALL.md     ce fichier
```

Chaque agent a exactement une skill fine qui l'invoque (`/zoom-out` du socle couvre déjà le
besoin de recadrage générique — km-toolkit ne le redéfinit pas).

## Installation (3 étapes)

### 1. Copier agents et skills

⚠️ **Collision de noms avec le socle** : km-toolkit ne fournit **pas** son propre
`docs-update` (il utilise celui du socle `template/` — même rôle, pas de duplication) et son
agent de résumé mensuel s'appelle `newsletter` (pas `changelog`, pour ne pas entrer en
collision avec l'agent `changelog` du socle qui produit un `CHANGELOG.md` plutôt qu'une
newsletter HTML). Si votre projet a modifié ces noms localement, vérifiez qu'aucun autre nom
de km-toolkit ne collisionne avant le `cp -R` — il n'y a pas de détection automatique.

```bash
# Version Claude Code
cp -R km-toolkit/.claude/agents/.   .claude/agents/
cp -R km-toolkit/.claude/skills/.   .claude/skills/

# Version Copilot
cp -R km-toolkit/.github/agents/.   .github/agents/
cp -R km-toolkit/.github/skills/.   .github/skills/
```

(Adapter le chemin si votre orchestrateur d'agents utilise un autre répertoire.)

### 2. Brancher le moteur d'override dans MkDocs

Si le projet a une KB MkDocs :

```bash
cp km-toolkit/hooks.py docs/kb/hooks.py    # ou fusionner avec un hooks.py existant
```

Dans `mkdocs.yml`, ajouter :

```yaml
hooks:
  - hooks.py

exclude_docs: |
  *.override.md
```

Le hook applique automatiquement, au build, tout `X.override.yml` (corrige titre, sections,
valeurs) et `X.override.md` (note libre) à **toute** page. Dépend de PyYAML — déjà fourni par
MkDocs, aucune dépendance à ajouter.

La réécriture des liens `specs/` vers GitHub déduit la base depuis `repo_url` de votre
`mkdocs.yml` (aucune édition requise). À défaut de `repo_url`, définissez la variable
d'environnement `KB_GITHUB_BASE` (ex. `https://github.com/OWNER/REPO/blob/main`).

### 3. Lancer la génération

```
/mf-km-generator        # orchestre toute la KB mainframe (inventaire → cartographie → fiches → règles)
/km-generator           # ou : KB générique multi-audiences (projet non-COBOL)
```

## Conventions attendues par les agents

| Convention | Valeur par défaut | Rôle |
|---|---|---|
| Sources | `src/` (COBOL : `.cob`, copybooks : `.cpy` sous `src/_copybooks/`) | Ce que les agents analysent |
| Sortie KB | `docs/kb/docs/mf/` (mainframe), `docs/kb/docs/` (générique) | Où les pages sont écrites |
| Override | `<page>.override.yml` / `<page>.override.md` à côté du `.md` | Surcharge humaine, jamais écrasée |

Ces chemins sont des conventions, pas du code en dur — adaptez-les dans les agents si votre
arborescence diffère.

## Catalogue des agents

**Mainframe COBOL (12)** : `mf-inventory`, `mf-callgraph`, `mf-program-card`,
`mf-data-dictionary`, `mf-crud-matrix`, `mf-anomaly-map`, `mf-business-rules`,
`mf-data-lineage`, `mf-batch-map`, `mf-sme-interview`, `mf-modernization-bridge`,
`mf-km-generator`.

**Socle KM générique (7)** : `km-generator`, `newsletter`, `adr-capture`, `session-digest`,
`postmortem`, `faq-harvest`, `glossary-sync`. *(`docs-update` n'est pas dupliqué ici — celui du
socle `template/` est utilisé tel quel.)*

**Contrôle qualité KB (5)** : `doc-coverage`, `spec-drift`, `km-audit`, `runbook-verify`,
`onboarding-test`. Génériques par construction (langage/écosystème découvert via `CLAUDE.md`),
avec des exemples illustrés pour COBOL quand le dispositif mainframe est installé.

## Principe d'override (rappel)

> L'humain n'écrit que des `*.override.*`. Les agents n'écrivent que le `.md` généré.
> Le hook fond les deux au build. Ils ne se croisent jamais, rien n'est jamais perdu.

## Note sur les exemples

7 agents (`mf-data-lineage`, `mf-modernization-bridge`, `km-audit`, `onboarding-test`,
`doc-coverage`, `faq-harvest`, `postmortem`) contiennent des exemples illustratifs issus du
projet d'origine (noms de champs, de fichiers, cas d'usage). Ce sont des exemples, pas de la
logique — ils n'empêchent pas l'usage sur un autre patrimoine.
