---
name: check
description: Vérifie que le code est prêt à committer — tests, lint et checks du projet
disable-model-invocation: true
context: fork
---

Vérifie que le code est prêt à committer :

1. Lance les tests backend et frontend en parallèle (comme /test)
2. Utilise l'agent `translations` pour vérifier la cohérence des traductions entre fr.js et en.js
3. Lance l'agent `api-contract` pour vérifier l'alignement frontend ↔ backend
4. Retourne : ✅ prêt / ❌ problèmes listés
