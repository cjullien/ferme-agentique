---
name: to-issues
description: Découpe un plan, spec ou PRD en issues indépendantes sur le tracker du projet en utilisant des vertical slices (tracer bullets). À utiliser quand l'utilisateur veut convertir un plan en issues ou découper du travail.
allowed-tools: Agent, Read, Grep, Glob, Bash
---

# To Issues

Découpe un plan en issues indépendantes via vertical slices (tracer bullets).

## Processus

### 1. Contexte
Travailler à partir du contexte en conversation. Consulter `CONTEXT.md` si existant.

### 2. Découper en vertical slices
Chaque issue = tranche verticale fine traversant TOUTES les couches end-to-end.

Règles :
- Chemin complet mais étroit (modèle, API, UI, tests)
- Démontrable ou vérifiable seul
- HITL (nécessite humain) ou AFK (autonome)

### 3. Valider avec l'utilisateur
Liste numérotée : Titre · Type HITL/AFK · Bloqué par · Stories couvertes.

### 4. Publier
Créer une issue par slice avec : description, critères d'acceptation, blockers.

> Ce skill publie rapidement des issues courtes sur le tracker. Si l'implémentation doit
> pouvoir se faire sans redérivation de contexte (relecture de spec, d'architecture...), utiliser
> `/story-writer` à la place : il produit des fichiers locaux auto-suffisants (spec + architecture
> embarquées) plutôt que de courtes descriptions d'issue.
