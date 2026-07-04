---
name: schema
description: Analyse l'impact d'une modification de modèle de données — liste tous les fichiers à mettre à jour pour éviter les oublis en cascade. Applicable à tout ORM ou schéma (SQLAlchemy, Prisma, TypeORM, Hibernate, ActiveRecord, GORM…).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Analyse d'impact — Modification de schéma

Avant de toucher au code, identifie tous les fichiers impactés par un changement de modèle de données.

## Processus

### 1. Lire CLAUDE.md
Identifier `{{orm_ou_schema_tool}}` (SQLAlchemy, Prisma, TypeORM, Hibernate, ActiveRecord, GORM, Mongoose…), les chemins des modèles, migrations, schémas de validation, tests et composants frontend.

### 2. Identifier le modèle concerné
Lire le modèle de données modifié dans le répertoire découvert via CLAUDE.md.

### 3. Lister les fichiers impactés

Pour chaque modification de champ (ajout, suppression, renommage, changement de type), lire le code et identifier :

**Couche persistance**
- Modèle de données lui-même
- Fichiers de migration (à créer ou mettre à jour)

**Couche validation / sérialisation**
- Schémas de validation I/O (DTOs, Pydantic models, Zod schemas, marshmallow, etc.)
- Schémas GraphQL / OpenAPI si existants

**Couche métier**
- Services / use cases qui accèdent aux champs modifiés
- Repositories / DAOs si la couche existe

**Couche API**
- Routers / controllers qui lisent/écrivent les champs
- Schémas de requête et réponse des endpoints

**Tests**
- Fixtures ORM / factories de test — désynchronisation silencieuse possible
- Mocks légers (SimpleNamespace, object literals) dans les tests unitaires
- Tests d'intégration avec données en dur

**Données**
- Scripts de seed / demo data si le champ doit être peuplé
- Fichiers de données de test (JSON, CSV, fixtures YAML)

**Internationalisation**
- Fichiers i18n backend (labels de champs, messages d'erreur)
- Fichiers i18n frontend (labels de formulaires, messages)

**Frontend**
- Formulaires (état initial, prefill, construction du payload, rendu)
- Composants qui affichent ou saisissent le champ

### 4. Avertir sur les risques BDD

- Ajout de colonne NOT NULL sans valeur par défaut → crash au démarrage si données existantes
- Renommage de colonne → perte de données silencieuse sans migration explicite
- Suppression de colonne → idem

### 5. Produire le plan de modification ordonné

```
1. Modèle de données
2. Migration BDD (→ utiliser /migrate pour générer)
3. Schémas de validation I/O
4. Services / use cases
5. Routers / controllers
6. Fixtures et mocks de test
7. Données de seed
8. i18n backend puis frontend
9. Formulaires et composants frontend
```

## Règles

- Ne rien modifier — analyse et plan uniquement, pour validation avant toute action
- Lire le code réel, ne pas supposer la structure à partir du nom des fichiers
- Signaler les dépendances transitives (service A → service B → modèle)
