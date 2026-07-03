---
name: spec-drift
description: Compare les comportements décrits dans les specs et la KB aux interfaces et modules réels du code — liste les divergences avec gravité.
allowed-tools: task
---

Lance l'audit de dérive specs/code via l'agent `spec-drift`.

Utilise l'outil `task` avec :
- `agent_type: "spec-drift"`
- un prompt demandant de comparer la KB et les specs au code source réel

L'agent produit :
- Liste des divergences entre ce qui est documenté et ce qui existe dans le code
- Gravité par divergence (critique / majeure / mineure)
- Pages KB à corriger

Affiche le rapport de dérive.
