---
name: typing
description: Audit TypeScript strictness — détecte `any`, assertions de type, `ts-ignore`, types manquants sur les props et return values React. Variante Vite/React du skill générique `typing` du socle (surcharge automatiquement à l'installation, même nom).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# TypeScript Strictness Audit

Détecte les affaiblissements du typage et propose ou applique les corrections.

## Processus

### 1. Vérifier la configuration
Lire `tsconfig.json` et vérifier que `strict: true` est activé. Signaler si `noImplicitAny`, `strictNullChecks` ou `strictFunctionTypes` sont désactivés explicitement.

### 2. Détecter les anti-patterns
Grep sur `src/` :
- `: any` — type générique non justifié
- `as ` — assertions de type qui contournent le compilateur
- `@ts-ignore` / `@ts-expect-error` — suppressions silencieuses
- `!` postfix (non-null assertion) sans commentaire explicatif

### 3. Analyser les composants React
Pour chaque composant `.tsx` :
- Vérifier que les props ont une interface ou un type explicite
- Vérifier que le type de retour est annoté (`JSX.Element`, `ReactNode`, etc.)
- Signaler les `useState<any>`, `useRef<any>`

### 4. Rapport

| Fichier | Ligne | Anti-pattern | Correction suggérée |
|---|---|---|---|

### 5. Correction (si `--fix` ou explicitement demandé)
Appliquer les corrections automatisables :
- Remplacer `any` par le type inféré ou un type générique approprié
- Retirer les `@ts-ignore` après correction de la cause racine
- Ajouter les interfaces de props manquantes

## Règles

- Ne jamais remplacer `any` par `unknown` sans vérifier que le code utilise le type correctement
- Conserver les `@ts-expect-error` légitimes avec un commentaire explicatif
- Prioriser les fichiers de la couche API/service (les erreurs y sont les plus coûteuses)
- Lancer `tsc --noEmit` avant et après pour confirmer que les corrections ne cassent rien
