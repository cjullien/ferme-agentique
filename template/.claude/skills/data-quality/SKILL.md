---
name: data-quality
description: Audit validation des données aux frontières du système — inputs non validés, schémas manquants, valeurs nullables non gérées, fuites de données. Applicable à tout framework de validation (Pydantic, Pandera, Zod, Bean Validation, Great Expectations…).
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Data Quality — Audit Validation

Vérifie que les données sont validées aux frontières du système avant tout traitement.

## Processus

### 1. Lire CLAUDE.md
Identifier l'outil de validation utilisé (`{{validation_framework}}` : Pydantic, Pandera, Great Expectations, Zod, Yup, Joi, Bean Validation, Cerberus…) et les chemins des couches d'entrée.

### 2. Cartographier les points d'entrée
Grep pour identifier toutes les sources de données :
- Lecture fichier : `read_csv(`, `read_parquet(`, `read_json(`, `readFile(`, `Files.readAllBytes`
- API entrante : endpoints qui reçoivent un body (POST/PUT/PATCH), uploads de fichiers
- Messages/events : consommateurs de queues (Kafka, RabbitMQ, SQS), webhooks entrants
- Base de données : requêtes qui retournent des collections non typées

### 3. Vérifier la présence de validation

Pour chaque point d'entrée :
- Existe-t-il un schéma de validation associé (`{{validation_framework}}`) ?
- La validation est-elle appliquée **avant** tout traitement des données ?
- Les erreurs de validation produisent-elles un message d'erreur exploitable ?

### 4. Détecter les risques

**Colonnes / champs manquants**
Code qui accède à un champ sans vérifier son existence (`.["col"]`, `.get("col")` sans défaut, accès direct en Java/TS)

**Types implicites**
Comparaisons ou calculs sur des colonnes sans vérification du type au préalable (risque de coercition silencieuse)

**Valeurs sentinelles**
`-1`, `""`, `"N/A"`, `"null"`, `0` utilisés comme marqueurs de null au lieu des valeurs nulles natives

**Cardinalité non bornée**
Colonnes catégorielles acceptant n'importe quelle valeur sans liste blanche (risque d'injection, erreurs silencieuses en aval)

**Données personnelles non filtrées**
Colonnes contenant potentiellement des données personnelles (noms, emails, téléphones, IP) transmises sans pseudonymisation (RGPD)

### 5. Rapport

| Fichier | Point d'entrée | Risque | Schéma existant | Action recommandée |
|---|---|---|---|---|

### 6. Génération de schémas (si demandée)
Proposer les schémas manquants adaptés à `{{validation_framework}}`. Exemple générique :

```
# Pydantic (Python)
class InputSchema(BaseModel):
    field: str
    value: float = Field(ge=0)

# Zod (TypeScript)
const schema = z.object({ field: z.string(), value: z.number().nonnegative() })

# Pandera (DataFrame Python)
schema = pa.DataFrameSchema({ "col": pa.Column(str, nullable=False) }, strict=True)
```

## Règles

- Valider à la **frontière** du système uniquement — pas dans les fonctions internes
- Un schéma par source de données (pas un schéma global qui masque les différences)
- Signaler explicitement toute donnée personnelle détectée (RGPD/HIPAA)
- Une validation qui passe silencieusement des données invalides est pire qu'une absence de validation
