---
name: tdd
disable-model-invocation: true
description: Implémentation TDD active — rétro-ingénierie des tests manquants, red-green-refactor, correction des tests fragiles/redondants
---

Lance une implémentation TDD active via l'agent `tdd`.

Utilise l'outil Agent avec `subagent_type: tdd` pour analyser puis corriger directement les
tests du projet :

Phase 1 — Analyse complète :
- Comportements observables déduits du code de production (chemins heureux, erreurs, limites)
- Tests manquants (arborescence miroir)
- Tests fragiles ou redondants
- Anti-patterns TDD détectés

Phase 2 — Corrections actives dans cet ordre :
1. Créer les fichiers de test manquants (cas nominal + cas d'erreur)
2. Refactorer les tests fragiles (couplage à l'implémentation, mocks excessifs)
3. Supprimer les doublons exacts
4. Corriger les anti-patterns TDD (assertions vides, tests dupliqués, cas limites)

Les violations d'architecture (couches, dépendances) détectées au passage sont signalées sans
être corrigées — renvoyer vers `/improve-architecture`. Les corrections trop risquées (schéma
BDD, rupture API) sont signalées sans être appliquées.
