---
name: glossary-sync
description: Extrait les termes métier du code et des specs — signale les termes utilisés mais non définis dans le glossaire, et les définitions orphelines (définies mais jamais utilisées).
allowed-tools: task
---

Lance la synchronisation du glossaire via l'agent `glossary-sync`.

Utilise l'outil `task` avec :
- `agent_type: "glossary-sync"`
- un prompt demandant d'analyser le code et la KB pour synchroniser le glossaire

L'agent produit :
- Liste des termes métier détectés dans le code (noms de PROGRAM-ID, copybooks, niveaux 88)
- Termes non définis dans `docs/kb/docs/glossary.md` → à définir
- Définitions orphelines (dans le glossaire mais absentes du code) → à retirer ou conserver
- Glossaire mis à jour

Affiche le rapport de synchronisation.
