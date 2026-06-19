---
name: api-contract
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Vérifie l'alignement routes backend ↔ appels frontend - détecte routes orphelines et contrats rompus
---

Lance une vérification du contrat API via l'agent `api-contract`.

Utilise l'outil Agent avec `subagent_type: api-contract` pour croiser les routes backend avec les appels frontend et détecter :
- Routes frontend pointant vers des URLs inexistantes côté backend
- Méthodes HTTP divergentes
- Champs de payload incompatibles avec les schémas backend
- Routes backend sans aucun appel frontend (routes orphelines)

## Vérification d'isolation des données (si applicable)

Si le projet implémente un mécanisme d'isolation des données (multi-tenant, ownership, etc. - identifié via CLAUDE.md) :

1. **Toute route métier** (GET liste, GET détail, POST, PUT, DELETE) doit injecter l'identifiant utilisateur.
2. **Modèles racines** (avec identifiant d'appartenance direct) :
   - Liste → filtrage par utilisateur
   - Détail/mutation → vérification d'appartenance avant accès
   - Création → association à l'utilisateur courant
3. **Modèles enfants** (sans identifiant d'appartenance propre) :
   - Accès via le parent avec vérification d'appartenance
4. **Jamais** une query sans filtre d'appartenance sur une ressource métier (hors endpoints publics).

**Format de signalement** :
```
[ISOLATION MANQUANTE] METHOD /api/path - accès non filtré par utilisateur
```