---
name: migrate
description: Génère et vérifie une migration de base de données — classifie les risques, produit le contenu de la migration et les scripts de backfill si nécessaire. Applicable à tout outil (Alembic, Flyway, Liquibase, Prisma, Django, Rails, Knex…).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Génération et Vérification de Migration BDD

Produit le contenu d'une migration, évalue les risques sur les données existantes et propose les backfills nécessaires.

## Processus

### 1. Lire CLAUDE.md
Identifier l'outil de migration (`{{migration_tool}}` : Alembic, Flyway, Liquibase, Prisma Migrate, Django migrations, ActiveRecord, Knex, TypeORM…), les chemins des modèles et des migrations, et la base de données cible.

### 2. Identifier la modification
Lire le diff courant (`git diff HEAD`) pour identifier les modèles modifiés.

Pour chaque modification, classifier :
- **Ajout de colonne** : nullable ou NOT NULL ? Valeur par défaut présente ?
- **Suppression de colonne** : données perdues ?
- **Renommage** : données à préserver → nécessite stratégie explicite
- **Modification de type** : compatibilité des données existantes
- **Nouvelle table** : simple
- **Suppression de table** : données perdues
- **Modification de contrainte** (FK, unique, index) : impact sur données existantes

### 3. Évaluer les risques

**🔴 Destructif — validation obligatoire avant application**
- Suppression de colonne ou table avec données existantes
- Ajout de colonne NOT NULL sans valeur par défaut (crash au démarrage si données)
- Modification de type incompatible
- Renommage de colonne (= DROP + ADD en SQL sans stratégie → perte de données)

**🟡 À surveiller**
- Ajout de colonne NOT NULL avec valeur par défaut (backfill potentiel)
- Ajout de contrainte unique sur colonne existante (peut échouer si doublons présents)
- Ajout d'index sur table volumineuse (lent en production, lock potentiel)

### 4. Générer la migration

Adapter à `{{migration_tool}}`. Structure générique :

```
# upgrade / up / change
# Étape 1 — Backfill si nécessaire (avant la contrainte DDL)
# Étape 2 — DDL (ALTER TABLE, CREATE TABLE, DROP TABLE…)

# downgrade / down
# Rollback complet ou déclaré irréversible avec justification
```

Vérifier avant génération : chaîne de migrations cohérente (une seule tête/branche active).

### 5. Proposer le backfill si nécessaire
Si des données existantes doivent être mises à jour :
- Fournir le script SQL ou code équivalent
- Préciser l'ordre d'exécution (avant ou après le DDL)
- Estimer l'impact en volume si possible

### 6. Checklist de validation

```
- [ ] upgrade/up complet et correct
- [ ] downgrade/down correct (ou déclaré irréversible avec justification)
- [ ] Backfill prévu si colonne NOT NULL sans défaut
- [ ] Chaîne de migrations vérifiée avant génération
- [ ] Migration vérifiée après génération (dry-run si disponible)
- [ ] Fixtures de test mises à jour
- [ ] Données de seed mises à jour si applicable
```

## Règles

- Ne jamais appliquer une migration destructive sans confirmation explicite
- Toute modification de modèle doit être accompagnée d'une migration — jamais de `create_all()` / `sync()` en production
- Préférer des migrations additives (ajout nullable puis backfill puis contrainte) aux modifications directes
