---
name: eda
description: Exploratory Data Analysis — profile un DataFrame (nulls, doublons, distributions, outliers) et génère un rapport markdown dans `docs/eda/`. À utiliser en début de sprint data ou à réception d'un nouveau dataset.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Exploratory Data Analysis (EDA)

Profile les jeux de données du projet et documente leur structure pour guider le travail data.

## Processus

### 1. Identifier les sources de données
Glob sur le projet :
- Fichiers `*.csv`, `*.parquet`, `*.json` dans `data/` ou `datasets/`
- DataFrames créés par `pd.read_*`, `pl.read_*`, `pd.DataFrame(`
- Tables Supabase/Postgres référencées dans les modèles SQLAlchemy

### 2. Profiler chaque dataset

Pour les fichiers locaux, lancer via Bash :

```python
import pandas as pd, sys
df = pd.read_csv("data/fichier.csv")
print(f"Shape: {df.shape}")
print(df.dtypes.to_string())
print(df.isnull().sum().to_string())
print(df.describe(include='all').to_string())
print(f"Doublons: {df.duplicated().sum()}")
```

Pour chaque colonne :
- **Numériques** : min, max, moyenne, écart-type, % outliers (règle IQR × 1.5)
- **Catégorielles** : top-5 valeurs, cardinalité, % valeurs rares (< 1% des lignes)
- **Dates** : plage temporelle, gaps, granularité détectée

### 3. Générer le rapport
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
- Signaler tout dataset > 500 MB avant de le charger (proposer un échantillon avec `nrows=10000`)
- Si Polars est installé, le préférer à pandas pour les fichiers > 100 MB
- Créer `docs/eda/` s'il n'existe pas
