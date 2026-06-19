---
name: backlog-feature
description: Ajoute une idée de fonctionnalité dans la backlog avec spec technique. À utiliser quand l'utilisateur veut ajouter une feature, une idée ou un item dans la backlog du projet.
allowed-tools: Read, Edit, Write, Glob, Bash
---

# Backlog Feature

Transforme une idée en item backlog structuré avec spec technique, sur le modèle des entrées existantes.

## Processus

### 1. Lire la backlog existante
Lire `docs/specs/backlog.md` pour :
- Connaître le prochain numéro d'item disponible (FEAT-N, A11Y-N, etc.)
- Comprendre le format des items "À implémenter"
- Identifier les dépendances avec d'autres items

### 2. Déterminer le préfixe et numéro
- `FEAT-N` : nouvelle fonctionnalité utilisateur
- `A11Y-N` : accessibilité
- `PERF-N` : performance
- `SEC-N` : sécurité
- `DX-N` : developer experience / tooling

### 3. Créer la spec technique
Créer `docs/specs/<slug>.md` avec la structure suivante :

```markdown
# Spec — <Titre>

**Statut** : À implémenter
**Priorité** : Haute / Moyenne / Faible
**Dépendances** : <items bloquants ou "Aucune">

## Problème
<Pourquoi cette feature est nécessaire>

## Solution cible
<Ce que ça fait, en une phrase>

## Architecture
<Schéma ou description du flux technique>

## Prérequis
<Infra, légal, autres features>

## Flux détaillé
<Pseudo-code ou étapes clés>

## Ce que ça ne change pas
<Effets de bord nuls — rassurer>

## Hors scope
<Ce qui est explicitement exclu>

## Estimation
| Tâche | Effort |
|---|---|
| ... | ~Xh |
| **Total** | **~Xh** |
```

### 4. Mettre à jour la backlog
Dans `docs/specs/backlog.md` :
1. Incrémenter `**Items pending**`
2. Ajouter l'item dans "À implémenter" **en tête de liste** :
```markdown
- **FEAT-N** — <Titre court>
  - Spec : `docs/specs/<slug>.md`
  - Prérequis : <résumé 1 ligne>
  - Effort estimé : ~Xh
  - Valeur : <bénéfice utilisateur en 1 phrase>
```

## Règles de qualité

- **Spec avant code** : la spec documente l'intention, pas l'implémentation finale
- **UX d'abord** : chaque spec commence par "Problème utilisateur", pas par la technique
- **Hors scope explicite** : évite la dérive de périmètre lors de l'implémentation
- **Estimation réaliste** : décomposer en tâches ≤ 2h, sommer honnêtement
- **Dépendances visibles** : tout prérequis bloquant doit être nommé
- **Accessibilité** : mentionner dans la spec si la feature a des impacts WCAG
- **i18n** : si la feature ajoute du texte visible → prévoir les clés i18n fr/en
- **Privacy** : si la feature collecte/envoie des données → mentionner RGPD

## Checklist avant de terminer

- [ ] `docs/specs/<slug>.md` créé et complet
- [ ] `docs/specs/backlog.md` mis à jour (compteur + item)
- [ ] Dépendances avec d'autres FEAT/A11Y identifiées
- [ ] Estimation en heures présente
- [ ] Valeur utilisateur formulée en 1 phrase
