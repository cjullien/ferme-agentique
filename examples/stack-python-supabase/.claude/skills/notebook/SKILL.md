---
name: notebook
description: Audit et nettoyage des notebooks Jupyter — outputs stale, cellules désordonnées, imports dupliqués, variables non définies. À utiliser avant un commit ou une revue de notebook.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Audit Notebooks Jupyter

Détecte et corrige les problèmes courants dans les notebooks du projet.

## Processus

### 1. Lister les notebooks
Glob `**/*.ipynb` en excluant `.ipynb_checkpoints/`. Si aucun notebook trouvé, le signaler et terminer.

### 2. Analyser chaque notebook
Lire le JSON du `.ipynb` et vérifier :

**Ordre d'exécution**
- Les `execution_count` sont-ils croissants et sans trou ?
- Y a-t-il des cellules jamais exécutées (`execution_count: null`) en dehors des cellules markdown ?

**Outputs volumineux**
- Outputs > 100 KB (images non compressées, DataFrames entiers affichés)
- Cellules avec `stream` de type `stderr` non nettoyées

**Imports**
- Imports dupliqués entre cellules
- Imports au milieu du notebook (doivent être regroupés en cellule 1 ou 2)
- `import *` non justifié

**Structure**
- Première cellule : titre markdown `# Titre` + description de l'objectif
- Sections `## Étape` pour structurer le flux
- Paramètres externalisés dans une cellule dédiée en haut (pattern Papermill)

**Reproductibilité**
- Appels à des chemins absolus ou des variables d'environnement non documentées
- `random_state` non fixé dans les modèles ML

### 3. Rapport

| Notebook | Cellule | Problème | Sévérité |
|---|---|---|---|

Sévérités : `bloquant` (reproductibilité) · `avertissement` (qualité) · `style`

### 4. Nettoyage (si demandé)
- Strip les outputs : `jupyter nbconvert --clear-output --inplace {notebook}.ipynb`
- Regrouper les imports en première cellule code
- Ajouter une cellule titre si absente

## Règles

- Ne jamais supprimer des outputs contenant des résultats d'expériences non reproductibles
- Demander confirmation avant de modifier un notebook partagé ou en production
- Signaler (sans supprimer) les cellules de debug `print()` / `display()` non retirées
