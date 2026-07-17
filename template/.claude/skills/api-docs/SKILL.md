---
name: api-docs
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
description: Audit et maintien de la documentation API (Swagger/OpenAPI) — endpoints non documentés, schémas manquants, dérive spec/code.
---

Lance un audit de la documentation API via l'agent `api-docs`.

Utilise l'outil Agent avec `subagent_type: api-docs` pour vérifier que chaque endpoint HTTP est
documenté (résumé, paramètres, schémas de requête/réponse) et que la spec OpenAPI, générée
automatiquement (FastAPI, springdoc, NestJS Swagger…) ou maintenue à la main (`openapi.yaml`),
reflète réellement le code.

Périmètre ciblé (optionnel) : $ARGUMENTS

Si aucun argument, auditer tous les endpoints du backend.
