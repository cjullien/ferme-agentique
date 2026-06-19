---
name: clean-tdd
disable-model-invocation: true
description: Revue et corrections actives de la clean architecture et de la couverture TDD
---

Lance une revue et correction active de la clean architecture et du TDD via l'agent `clean-tdd`.

Utilise l'outil Agent avec `subagent_type: clean-tdd` pour analyser puis corriger directement le code backend (sources et tests) :

Phase 1 — Analyse complète :
- Inventaire de migration par module (domain/application/services/routers)
- Violations de la règle de dépendance (sens interdit)
- Logique métier hors couche domain
- Fichiers de test manquants (arborescence miroir)
- Anti-patterns TDD détectés

Phase 2 — Corrections actives dans cet ordre :
1. Corriger les violations de dépendance critiques (imports interdits, mauvaise couche)
2. Extraire la logique métier inline des routers vers domain/ ou application/
3. Créer les fichiers de test manquants (cas nominal + cas d'erreur)
4. Corriger les anti-patterns TDD (assertions vides, tests dupliqués, cas limites)

Les corrections trop risquées (schéma BDD, décision d'architecture, rupture API) sont signalées sans être appliquées.
