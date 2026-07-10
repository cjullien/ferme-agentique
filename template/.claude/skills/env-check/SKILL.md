---
name: env-check
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Vérifie que l'environnement local est correctement configuré (venv, .env, node_modules, ports)
---

Vérifie la santé de l'environnement de développement local.

## Processus

### 1. Lire CLAUDE.md
Identifier la stack (langages, gestionnaires de dépendances), les chemins backend/frontend s'ils existent, les fichiers d'environnement attendus (`.env`, `.env.example`, `app.env`…) et les ports de dev déclarés.

### 2. Contrôles par écosystème détecté

Adapter aux fichiers réellement présents (ne pas supposer une stack Python+Node par défaut) :

**Python** (si `requirements.txt` / `pyproject.toml` / `Pipfile` trouvé) :
- Environnement virtuel présent et fonctionnel (`.venv/`, `venv/`, ou géré par Poetry/uv)
- Fichier d'environnement local présent (comparer avec son `.example`/`.sample` si disponible)
- Dépendances installées à jour vs le fichier de dépendances (`pip freeze` / `poetry check` / équivalent)

**Node** (si `package.json` trouvé) :
- `node_modules/` existe
- Lockfile à jour vs `package.json` (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`)

**Autres écosystèmes** (Java/Maven, Go, Ruby, .NET…) : appliquer le même principe — dépendances installées, fichier d'environnement présent, lockfile à jour — avec les commandes identifiées via `CLAUDE.md`.

**Ports de dev** : pour chaque port déclaré dans `CLAUDE.md` (backend, frontend…), vérifier s'il est libre ou déjà occupé par un serveur de dev.

**Général :**
- Git propre ou fichiers non committés ?
- `.env` / secrets non trackés par git ?

### 3. Rapport
Affiche un tableau récapitulatif avec ✅/❌ par contrôle, uniquement pour les écosystèmes effectivement détectés.
