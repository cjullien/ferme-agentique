---
name: check
description: Vérifie que le code est prêt à committer — tests, lint et checks du projet
disable-model-invocation: true
context: fork
---

Vérifie que le code est prêt à committer :

1. Lance les tests backend et frontend en parallèle (comme /test)
2. SI l'agent `translations` est installé (`.claude/agents/translations.md`, module `feature-i18n`) : l'utiliser pour vérifier la cohérence des traductions entre les fichiers de langue
3. SI l'agent `api-contract` est installé (`.claude/agents/api-contract.md`, module `stack-python-supabase`) : l'utiliser pour vérifier l'alignement frontend ↔ backend
4. Retourne : ✅ prêt / ❌ problèmes listés
