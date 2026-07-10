---
name: ci
description: Revue CI/CD - actions non pinnées, secrets, cohérence CLAUDE.md, build natif en CI.
---

Lance l'agent `ci`.

Utilise l'outil Agent avec `subagent_type: ci` pour auditer les pipelines (`.github/workflows`, `.gitlab-ci.yml`…) : sécurité (actions pinnées, secrets, permissions), obsolescence, cohérence avec les commandes Maven du projet, et couverture (build JVM, build natif si le projet en a un — runner dimensionné selon le profil déclaré dans `CLAUDE.md`, tests).
