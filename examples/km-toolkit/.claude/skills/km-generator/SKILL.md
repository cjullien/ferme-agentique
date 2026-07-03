---
name: km-generator
description: Génère ou met à jour la base de Knowledge Management (wiki MkDocs Material sous `docs/kb/`) via l'agent `km-generator`.
allowed-tools: task
---

Lance la génération ou mise à jour de la KB via l'agent `km-generator`.

Utilise l'outil `task` avec :
- `agent_type: "km-generator"`
- `name: "km-generator-run"`
- un prompt précisant :
  - **Mode** : `bootstrap` (créer la KB) ou `update` (mettre à jour). Si l'utilisateur ne précise pas, détecter via présence de `docs/kb/`.
  - **Scope** éventuel (ex: seulement les ADR, seulement l'onboarding).
  - **Audiences** ciblées si l'utilisateur veut restreindre (défaut : les 5).
  - **Langue** (fr/en) si différente du défaut projet.

L'agent suit la procédure complète (cadrage → arborescence → config → rédaction par batches parallèles → validation strict → restitution) reproduisant fidèlement la démarche utilisée pour bootstrap `docs/kb/` sur ce projet.
