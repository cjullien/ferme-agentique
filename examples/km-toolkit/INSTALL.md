# KM Toolkit — installation sur un nouveau projet

Chaîne complète d'agents de **Knowledge Management piloté par agents** : génération de KB
depuis le code, audit de fraîcheur/complétude, et dispositif mainframe COBOL à grande échelle.
Réutilisable sur n'importe quel projet (le socle KM est agnostique ; les agents `mf-*` ciblent
les patrimoines COBOL/mainframe).

## Contenu

```
km-toolkit/
├── agents/        25 agents (.agent.md)  — la logique (procédure, format de sortie)
├── skills/        26 skills (SKILL.md)   — les déclencheurs invocables
├── hooks.py       hook MkDocs            — moteur d'override universel
├── test_hooks.py  garde-fou du hook      — `python3 km-toolkit/test_hooks.py`
└── INSTALL.md     ce fichier
```

`zoom-out` est une skill autonome (sans agent dédié) → 26 skills pour 25 agents.

## Installation (3 étapes)

### 1. Copier agents et skills

```bash
cp -r km-toolkit/agents/*   .github/agents/
cp -r km-toolkit/skills/*   .github/skills/
```

(Adapter le chemin si votre orchestrateur d'agents utilise un autre répertoire.)

> **Dépendance d'environnement.** Le front-matter `tools:` des agents emploie les
> noms d'outils de GitHub Copilot dans VS Code (`read_file`, `create_file`,
> `replace_string_in_file`, `run_in_terminal`…). Si votre orchestrateur utilise
> d'autres identifiants d'outils, adaptez ces listes — sinon le champ est ignoré.

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

**Socle KM générique (8)** : `km-generator`, `docs-update`, `changelog`,
`adr-capture`, `session-digest`, `postmortem`, `faq-harvest`, `glossary-sync`.
*(+ `zoom-out` : skill autonome sans agent dédié.)*

**Contrôle qualité KB (5)** : `doc-coverage`, `spec-drift`, `km-audit`, `runbook-verify`,
`onboarding-test`.

## Principe d'override (rappel)

> L'humain n'écrit que des `*.override.*`. Les agents n'écrivent que le `.md` généré.
> Le hook fond les deux au build. Ils ne se croisent jamais, rien n'est jamais perdu.

## Note sur les exemples

4 agents (`mf-data-lineage`, `mf-modernization-bridge`, `km-audit`, `onboarding-test`)
contiennent des exemples illustratifs issus du projet d'origine (noms de champs, de fichiers).
Ce sont des exemples, pas de la logique — ils n'empêchent pas l'usage sur un autre patrimoine.
