---
name: eda
description: Exploratory Data Analysis — profile un jeu de données (nulls, doublons, distributions, outliers, cardinalité) et génère un rapport markdown dans `docs/eda/`. Applicable à tout outil data (pandas, Polars, DuckDB, R, SQL, Julia…).
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Exploratory Data Analysis (EDA)

Profile les jeux de données du projet et documente leur structure pour guider le travail data.

## Processus

### 1. Lire CLAUDE.md
Identifier l'outil data utilisé (`{{data_tool}}` : pandas, Polars, DuckDB, R/dplyr, SQL, Julia DataFrames.jl…), les chemins des données (`data/`, `datasets/`, `inputs/`) et les conventions de documentation.

### 2. Identifier les sources de données
Glob et grep sur le projet :
- Fichiers de données : `*.csv`, `*.parquet`, `*.json`, `*.xlsx`, `*.feather`, `*.arrow`
- Chargements dans le code : `read_csv(`, `read_parquet(`, `read_json(`, `FROM '*.parquet'`, `load(`, `fread(`
- Tables en base référencées dans les modèles ou migrations

### 3. Profiler chaque dataset

Adapter la commande à `{{data_tool}}`. Exemple générique avec pandas :

```python
import pandas as pd
df = pd.read_csv("data/fichier.csv")          # ou read_parquet, read_json…
print(f"Shape: {df.shape}")
print(df.dtypes.to_string())
print(df.isnull().mean().mul(100).round(1).to_string())   # % nulls
print(df.describe(include='all').to_string())
print(f"Doublons: {df.duplicated().sum()}")
```

Pour chaque colonne :
- **Numériques** : min, max, moyenne, écart-type, % outliers (règle IQR × 1.5)
- **Catégorielles** : top-5 valeurs, cardinalité totale, % valeurs rares (< 1% des lignes)
- **Dates/timestamps** : plage temporelle, gaps détectés, granularité
- **Texte libre** : longueur min/max/médiane, % vides

### 4. Générer le rapport
Créer `docs/eda/{nom_dataset}.md` :

```markdown
# EDA — {nom_dataset}

**Source** : `{chemin}` | **Shape** : {N} lignes × {M} colonnes | **Généré le** : {date}

## Qualité des données

| Colonne | Type | % Nulls | Cardinalité | Remarque |
|---|---|---|---|---|

## Distributions clés
...

## Anomalies détectées
...

## Recommandations pour le pipeline
...
```

## Règles

- Ne jamais modifier les données sources — lecture seule
- Signaler tout dataset > 500 MB avant de le charger (proposer un échantillon d'abord)
- Créer `docs/eda/` s'il n'existe pas
- Signaler les colonnes contenant potentiellement des données personnelles (RGPD)
