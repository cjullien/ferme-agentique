---
name: notebook
description: Audit et nettoyage des notebooks computationnels — outputs stale, ordre d'exécution incohérent, imports dupliqués, reproductibilité compromise. Applicable à Jupyter, Quarto, R Markdown, Observable, Pluto.jl…
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Audit Notebooks Computationnels

Détecte et corrige les problèmes courants dans les notebooks du projet.

## Processus

### 1. Lire CLAUDE.md
Identifier le format de notebook utilisé (`{{notebook_format}}` : `.ipynb`, `.qmd`, `.Rmd`, `.jl`…) et les conventions du projet.

### 2. Lister les notebooks
Glob sur `**/*.ipynb`, `**/*.qmd`, `**/*.Rmd` (adapter à `{{notebook_format}}`), en excluant les checkpoints (`.ipynb_checkpoints/`, `_freeze/`). Si aucun trouvé, le signaler et terminer.

### 3. Analyser chaque notebook

**Pour les `.ipynb` (Jupyter)** — lire le JSON et vérifier :

*Ordre d'exécution*
- Les `execution_count` sont-ils croissants et sans trou ?
- Y a-t-il des cellules jamais exécutées (`null`) hors cellules markdown ?

*Outputs*
- Outputs > 100 KB (images non compressées, DataFrames entiers affichés)
- `stderr` non nettoyés

*Imports*
- Imports dupliqués entre cellules
- Imports positionnés au milieu du notebook (doivent être en tête)
- `import *` non justifié

**Pour tous les formats** :

*Structure*
- Présence d'un titre et d'une description de l'objectif en première section
- Sections logiques (`## Étape`) pour structurer le flux
- Paramètres externalisés en cellule/section dédiée en haut (pattern Papermill / quarto params)

*Reproductibilité*
- Chemins absolus ou variables d'environnement non documentées
- Graines aléatoires non fixées (`random_state`, `set.seed`, `Random.seed!`)
- Dépendances non listées (`requirements.txt`, `renv.lock`, `Project.toml`)

### 4. Rapport

| Notebook | Cellule/Section | Problème | Sévérité |
|---|---|---|---|

Sévérités : `bloquant` (reproductibilité) · `avertissement` (qualité) · `style`

### 5. Nettoyage (si demandé)
- Jupyter : `jupyter nbconvert --clear-output --inplace {notebook}.ipynb`
- Regrouper les imports en première cellule/section code
- Ajouter titre si absent

## Règles

- Ne jamais supprimer des outputs contenant des résultats d'expériences non reproductibles
- Demander confirmation avant de modifier un notebook partagé ou en production
- Signaler (sans supprimer) les cellules de debug non retirées
