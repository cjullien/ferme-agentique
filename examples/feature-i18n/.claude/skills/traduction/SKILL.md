---
name: traduction
description: Synchronise les fichiers de traduction i18n - détecte et ajoute les clés manquantes entre fr.js et en.js
allowed-tools: Agent, Read, Grep, Glob, Bash, Write
disable-model-invocation: true
---

Lance la synchronisation des traductions via l'agent `translations`.

Utilise l'outil Agent avec `subagent_type: translations` pour détecter et ajouter les clés manquantes entre `fr.js` et `en.js`.

> ⚠️ Alias de `translations` (commande EN) — même contenu, deux fichiers car le frontmatter
> `name:` ne peut porter qu'une seule commande. Toute modification des règles ci-dessous doit
> être répercutée à l'identique dans `../translations/SKILL.md`, sinon les deux commandes
> divergent silencieusement (cf. historique : c'est exactement le bug qui a affecté ce module).

## Règles de contenu i18n (obligatoires)
- **Séparateur** : toujours ` - ` (trait d'union ASCII U+002D), jamais ` — ` (tiret cadratin U+2014)
- **Valeur vide** : toujours `'-'`, jamais `'—'`
- Vérifier la présence de `—` dans les valeurs existantes lors de chaque sync et les remplacer par `-`
