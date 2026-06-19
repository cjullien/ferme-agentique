---
name: env-check
allowed-tools: Agent, Read, Grep, Glob, Bash
description: Vérifie que l'environnement local est correctement configuré (venv, .env, node_modules, ports)
---

Vérifie la santé de l'environnement de développement local.

Contrôles à effectuer :

**Backend :**
- `backend/.venv/` existe et Python y est fonctionnel
- `backend/conf/app.env` existe (comparer avec `app.env.demo.example` si disponible)
- `pip freeze` vs `requirements.lock` — packages manquants ?
- Port 8000 libre ou serveur déjà lancé

**Frontend :**
- `frontend/node_modules/` existe
- Lockfile à jour vs fichier de dépendances (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`)
- Port 5173 libre ou serveur déjà lancé

**Général :**
- Git propre ou fichiers non committés ?
- `.env` / secrets non trackés par git ?

Affiche un tableau récapitulatif avec ✅/❌ par contrôle.
