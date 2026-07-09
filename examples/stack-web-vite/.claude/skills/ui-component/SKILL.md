---
name: ui-component
description: Génère un composant React TypeScript depuis une spec naturelle — produit le `.tsx`, les tests Vitest et met à jour l'index d'exports. Variante Vite/React du skill générique `ui-component` du socle (surcharge automatiquement à l'installation, même nom).
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Génération de composant React

Crée un composant React TypeScript complet, testé et intégré aux conventions du projet.

## Processus

### 1. Analyser les conventions existantes
Lire 2-3 composants existants dans `src/components/` pour identifier :
- Convention de nommage des fichiers (`PascalCase.tsx` ou `kebab-case/index.tsx`)
- Pattern d'export (named ou default)
- Librairie de styles (Tailwind, CSS modules, styled-components)
- Pattern de test utilisé (describe/it, render + userEvent)

### 2. Créer le composant
Générer `src/components/{NomComposant}/{NomComposant}.tsx` :
- Interface `{NomComposant}Props` explicite (jamais `any`)
- Type de retour `JSX.Element`
- Props avec valeurs par défaut si applicable
- Accessibilité : `aria-label`, rôles ARIA, focus visible si interactif

### 3. Créer les tests
Générer `src/components/{NomComposant}/{NomComposant}.test.tsx` :
- Import `@testing-library/react` + `userEvent`
- Test du rendu nominal
- Test des états limite (props optionnelles absentes, liste vide, état d'erreur)
- Test des interactions utilisateur si le composant est interactif
- Pas de snapshot test — préférer les assertions sémantiques (`getByRole`, `getByText`)

### 4. Mettre à jour l'index
Ajouter l'export dans `src/components/index.ts` (ou créer le fichier s'il n'existe pas).

## Règles

- Un composant = un seul rôle (SRP)
- Aucun appel API dans le composant — passer les données via props ou hooks dédiés
- Accessibilité non optionnelle : vérifier le contraste et les rôles ARIA
- Nommer les handlers `onXxx` (props exposées) et `handleXxx` (implémentation locale)
- Si le composant gère un état complexe, proposer un hook `use{NomComposant}` séparé
