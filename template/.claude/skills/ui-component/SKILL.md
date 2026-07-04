---
name: ui-component
description: Génère un composant UI depuis une spec naturelle — analyse les conventions du projet, produit le composant, les tests et l'export. Applicable à tout framework UI (React, Vue, Angular, Svelte, Web Components…).
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Génération de composant UI

Crée un composant UI complet, testé et intégré aux conventions du projet, peu importe le framework.

## Processus

### 1. Lire CLAUDE.md
Identifier le framework UI (`{{ui_framework}}` : React, Vue 3, Angular, Svelte, etc.), le runner de tests (`{{test_runner}}` : Vitest, Jest, Testing Library, Karma, Jasmine…), la librairie de styles (Tailwind, CSS Modules, SCSS, styled-components), et les conventions de nommage.

### 2. Analyser les conventions du projet
Lire 2-3 composants existants pour identifier :
- Convention de nommage des fichiers (`PascalCase.vue`, `kebab-case/index.ts`, `ComponentName.component.ts`)
- Pattern d'export (named, default, barrel `index.ts`)
- Structure des props/inputs (interface TypeScript, `defineProps`, `@Input()`, props Svelte)
- Pattern de test utilisé (`describe/it`, `render + userEvent`, `mount`, `TestBed`)
- Localisation des composants dans le projet (`src/components/`, `src/app/`, `lib/`)

### 3. Créer le composant
Générer le fichier composant aux conventions détectées :
- Types des props/inputs explicites (jamais `any`)
- Valeurs par défaut pour les props optionnelles
- Accessibilité : rôles ARIA appropriés, labels, focus visible sur les éléments interactifs
- Nommage des handlers : `onXxx` (props exposées) / `handleXxx` (implémentation locale)
- Logique complexe extraite dans un composable/hook/service dédié

### 4. Créer les tests
Générer le fichier de tests aux conventions du projet :
- Rendu nominal avec les props requises
- États limites : props optionnelles absentes, listes vides, état d'erreur
- Interactions utilisateur si le composant est interactif (clic, saisie, focus)
- Préférer les assertions sémantiques (`getByRole`, `getByText`, `getByLabelText`) aux sélecteurs CSS ou snapshots

### 5. Mettre à jour l'index d'exports
Ajouter l'export dans le barrel `index.ts` (ou équivalent) si le projet en utilise un.

## Règles

- Un composant = un seul rôle (responsabilité unique)
- Aucun appel réseau dans le composant — les données arrivent via props, slots ou un hook dédié
- Accessibilité non optionnelle : vérifier les rôles ARIA et le contraste
- Si le composant gère un état complexe, proposer un hook/composable `use{Nom}` ou service séparé
- Pas de snapshot tests — ils cassent pour des raisons cosmétiques et masquent les régressions réelles
