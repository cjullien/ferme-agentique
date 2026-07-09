---
name: migrate
description: Génère la migration l'outil de migration après modification de modèle - upgrade/downgrade, backfill, risques
disable-model-invocation: true
---

Génère et vérifie la migration de base de données via l'agent `migrate`.

À utiliser après `/schema` pour passer de l'analyse à l'exécution.

Utilise l'outil Agent avec `subagent_type: migrate` pour :
- Analyser la modification de modèle en cours (git diff)
- Évaluer les risques sur les données existantes (🔴 destructif, 🟡 à surveiller)
- Générer le contenu complet de la migration (upgrade + downgrade)
- Proposer un script de backfill si nécessaire
- Fournir les commandes exactes à exécuter dans l'ordre
