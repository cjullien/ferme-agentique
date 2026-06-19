---
name: mpd
description: Génère le schéma ER Mermaid depuis les modèles de données dans docs/specs/mpd.md
allowed-tools: Agent, Read, Grep, Glob, Bash, Write
disable-model-invocation: true
---

Génère ou met à jour le MPD (schéma ER de la base de données) via l'agent `db-diagram`.

Utilise l'outil Agent avec `subagent_type: db-diagram`.

L'agent va lire tous les modèles de données (chemin identifié via CLAUDE.md) et écrire le diagramme Mermaid dans `docs/specs/mpd.md`.
