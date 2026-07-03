---
name: data-quality
description: Audit validation des données — détecte les DataFrames sans schéma Pydantic/Pandera, les colonnes nullables non gérées, les inputs non validés aux frontières du système.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Data Quality — Audit Validation

Vérifie que les données entrantes sont validées avant d'être traitées, aux frontières du système.

## Processus

### 1. Cartographier les points d'entrée
Grep sur le projet pour identifier les sources de données :
- `pd.read_csv(`, `pd.read_parquet(`, `pd.read_sql(`, `pd.read_excel(`
- `pl.read_csv(`, `pl.read_parquet(`
- Endpoints FastAPI/Flask recevant des données tabulaires (`UploadFile`, `Form`)
- Requêtes Supabase/SQLAlchemy retournant des DataFrames

### 2. Vérifier la présence de schémas
Pour chaque point d'entrée :
- Existe-t-il un schéma **Pydantic** ou **Pandera** associé ?
- Le schéma est-il appliqué (`.validate()`, `model_validate()`) avant tout traitement ?
- Les colonnes `nullable=True` ont-elles un traitement explicite (`.dropna()`, `.fillna()`, ou imputation documentée) ?

### 3. Détecter les risques

**Colonnes manquantes**
Code qui suppose des colonnes présentes sans vérifier (`df["col"]` sans try/except ni `.get`)

**Types implicites**
Comparaisons `df["col"] > 0` sans vérification préalable du dtype — risque si la source change

**Valeurs sentinelles**
`-1`, `""`, `"N/A"`, `0` utilisés comme marqueurs de null au lieu de `None`/`NaN`

**Cardinalité non bornée**
Colonnes catégorielles sans liste de valeurs attendues (risque injection, erreurs silencieuses)

**Fuite de données**
Colonnes qui ne devraient pas être présentes en production (identifiants personnels, colonnes de debug)

### 4. Rapport

| Fichier | Point d'entrée | Risque | Schéma existant | Action recommandée |
|---|---|---|---|---|

### 5. Génération de schémas (si demandée)
Proposer les schémas Pandera manquants sur le modèle :

```python
import pandera as pa

schema = pa.DataFrameSchema(
    {
        "colonne_texte": pa.Column(str, nullable=False),
        "colonne_num": pa.Column(float, pa.Check.ge(0), nullable=True),
        "colonne_cat": pa.Column(str, pa.Check.isin(["val1", "val2"])),
    },
    strict=True,  # rejette les colonnes inattendues
)
```

## Règles

- Valider à la frontière du système (lecture fichier, réponse API) — pas dans les fonctions internes
- Un schéma par source de données, pas un schéma global qui masque les différences
- Préférer Pandera pour les DataFrames, Pydantic pour les objets métier structurés
- Signaler les données personnelles (RGPD) détectées dans les colonnes (noms, emails, téléphones)
