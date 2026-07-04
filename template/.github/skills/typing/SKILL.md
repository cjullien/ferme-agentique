---
name: typing
description: Audit typage statique — détecte les suppressions de typage, les types génériques non contraints, les valeurs potentiellement nulles non gérées. Applicable à tout langage typé (TypeScript, Python, Java, Go, Kotlin, Rust…).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Audit Typage Statique

Détecte les affaiblissements du système de types et propose ou applique les corrections.

## Processus

### 1. Lire CLAUDE.md
Identifier le langage, le vérificateur de types utilisé (`{{linter_typage}}` : `tsc`, `mypy`, `pyright`, `javac -Xlint`, `go vet`, `ktlint`, etc.) et la configuration associée (`tsconfig.json`, `mypy.ini`, `pyrightconfig.json`, etc.).

### 2. Vérifier la configuration du vérificateur de types
- Le mode strict est-il activé ? (`strict: true`, `--strict`, `disallow_untyped_defs = true`, etc.)
- Des règles ont-elles été désactivées explicitement ? Sont-elles justifiées ?

### 3. Détecter les anti-patterns par langage

**TypeScript**
- `: any` — type générique non contraint
- `as X` — assertions de type qui court-circuitent le compilateur
- `@ts-ignore` / `@ts-expect-error` sans commentaire explicatif
- `!` postfix (non-null assertion) sans vérification préalable

**Python**
- Fonctions sans annotations de type sur les paramètres ou le retour
- `# type: ignore` sans commentaire
- `Any` importé de `typing` et utilisé sans justification
- `cast()` abusif

**Java / Kotlin**
- Raw types (`List` au lieu de `List<T>`)
- `@SuppressWarnings("unchecked")` sans justification
- `!!` en Kotlin (non-null assertion)

**Go**
- `interface{}` / `any` là où un type concret est possible
- Absence de vérification d'erreur (`_ = err`)

### 4. Rapport

| Fichier | Ligne | Anti-pattern | Correction suggérée |
|---|---|---|---|

Classer par sévérité : `P1` (masque un bug potentiel) · `P2` (fragilise le typage) · `P3` (style)

### 5. Correction (si explicitement demandée)
- Remplacer les types génériques par des types inférés ou contraints
- Retirer les suppressions après correction de la cause racine
- Ajouter les annotations manquantes

## Règles

- Lancer `{{linter_typage}}` avant et après pour confirmer que les corrections ne régressent pas
- Ne jamais remplacer un type générique par `unknown`/`Object` sans vérifier les usages
- Prioriser la couche d'entrée du système (API, lecture fichier) — les erreurs y sont les plus coûteuses
- Conserver les suppressions légitimes avec un commentaire `// justification`
