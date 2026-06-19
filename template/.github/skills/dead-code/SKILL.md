---
name: dead-code
disable-model-invocation: true
description: Détecte et supprime le code mort, imports inutilisés, clés i18n orphelines, commentaires obsolètes
---

Lance une détection et suppression du code mort via l'agent `dead-code`.

Utilise l'outil Agent avec `subagent_type: dead-code` pour analyser puis nettoyer :
- Imports inutilisés (Python + JS/TS)
- Fonctions, classes et composants jamais utilisés
- Clés i18n orphelines (déclarées mais jamais référencées dans le JSX)
- Blocs de code commentés
- Docstrings désynchronisées avec la signature réelle
- Specs et documentation référençant du code supprimé

Les TODO/FIXME et les éléments d'API publique sont signalés sans suppression automatique.
