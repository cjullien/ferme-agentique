---
name: recall
description: Recherche dans les décisions capturées (.decisions/) par mot-clé ou domaine. Utile pour retrouver pourquoi un choix a été fait avant de le remettre en question.
allowed-tools: Bash, Read, Glob
---

# Recall — Recherche de décisions

Recherche dans les décisions capturées du projet.

## Processus

### 1. Vérifier l'existence du dossier

```bash
ls .decisions/ 2>/dev/null || echo "Aucune décision capturée (dossier .decisions/ absent)"
```

Si absent, informer l'utilisateur et suggérer `/harvest` pour détecter les décisions implicites.

### 2. Recherche par mot-clé

Grep dans tous les fichiers `.decisions/` :

```bash
grep -rli "<mot-clé>" .decisions/ 2>/dev/null
```

Puis lire les fichiers correspondants et afficher titre + décision (sections `# Titre` et `## Décision`).

### 3. Recherche par domaine

Si l'utilisateur demande un domaine (auth, db, api…) :

```bash
ls .decisions/<domaine>/ 2>/dev/null
```

Lister les fichiers avec leur titre (première ligne `# ...`).

### 4. Vue d'ensemble (sans mot-clé)

Si invoqué sans argument, afficher la liste complète des décisions par domaine :

```bash
find .decisions/ -name "*.md" ! -name "CONSTITUTION.md" | sort
```

Pour chaque fichier : domaine / date / titre / statut (depuis le frontmatter).

### 5. Afficher la constitution

Si `.decisions/CONSTITUTION.md` existe, l'afficher en tête de résultats comme rappel des décisions fondamentales.
