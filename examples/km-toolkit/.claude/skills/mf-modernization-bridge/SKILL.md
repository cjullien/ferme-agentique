---
name: mf-modernization-bridge
description: Vue de la KB orientée modernisation — complexité par domaine, dépendances entrantes/sortantes, règles métier extraites, candidats au strangler pattern. La KB devient l'actif d'entrée du programme de migration.
allowed-tools: task
---

Lance l'analyse de modernisation via l'agent `mf-modernization-bridge`.

Utilise l'outil `task` avec :
- `agent_type: "mf-modernization-bridge"`
- un prompt demandant d'analyser le patrimoine pour identifier les candidats à la modernisation

L'agent produit :
- Vue par domaine : complexité, couplage, règles métier extraites
- Candidats au strangler pattern (modules bien délimités, faible fan-in entrant)
- Modules à risque (fort couplage, règles métier non extraites)
- Rapport dans `docs/kb/docs/mf/modernization-bridge.md`

Affiche l'analyse et les recommandations de migration.
