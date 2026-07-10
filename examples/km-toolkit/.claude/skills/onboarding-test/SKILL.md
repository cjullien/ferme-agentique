---
name: onboarding-test
description: Suit littéralement le parcours d'onboarding développeur et rapporte chaque étape qui échoue — comme un test d'intégration sur la documentation.
allowed-tools: Agent
---

Lance le test du parcours d'onboarding via l'agent `onboarding-test`.

Utilise l'outil Agent avec `subagent_type: onboarding-test`, en lui transmettant :
- un prompt demandant de suivre le parcours onboarding développeur depuis `docs/kb/docs/onboarding/developer.md`

L'agent :
- Suit chaque étape du parcours dans l'ordre
- Tente d'exécuter les commandes indiquées
- Rapporte les étapes qui échouent ou sont ambiguës

Affiche le rapport d'onboarding avec les étapes cassées.
