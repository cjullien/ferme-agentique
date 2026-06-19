---
name: seed
description: Maintient les données de seed/démo cohérentes avec les modèles de données
disable-model-invocation: true
---

Maintient les données de seed cohérentes avec les modèles via l'agent `seed`.

Utilise l'outil Agent avec `subagent_type: seed` pour :
- Détecter les champs manquants, FK invalides et champs supprimés dans demo_data.py / fixtures
- Appliquer les corrections directement (valeurs réalistes, ordre FK respecté)
- Mettre à jour les fixtures de test de la même façon
