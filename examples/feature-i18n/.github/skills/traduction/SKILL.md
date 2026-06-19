---
name: traduction
description: Synchronise les fichiers de traduction i18n - détecte et ajoute les clés manquantes entre fr.js et en.js
allowed-tools: Agent, Read, Grep, Glob, Bash, Write
disable-model-invocation: true
---

Lance la synchronisation des traductions via l'agent `translations`.

Utilise l'outil Agent avec `subagent_type: translations` pour détecter et ajouter les clés manquantes entre `fr.js` et `en.js`.

## Règles de contenu i18n (obligatoires)
- **Séparateur** : toujours ` - ` (trait d'union ASCII U+002D), jamais ` — ` (tiret cadratin U+2014)
- **Valeur vide** : toujours `'-'`, jamais `'—'`
- Vérifier la présence de `—` dans les valeurs existantes lors de chaque sync et les remplacer par `-`
