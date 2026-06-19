---
name: changelog
description: Génère un résumé non-technique des nouveautés pour les utilisateurs
allowed-tools: Agent, Read, Grep, Glob, Bash
disable-model-invocation: true
---

Génère le résumé mensuel des nouveautés via l'agent `changelog`.

Utilise l'outil Agent avec `subagent_type: changelog` pour produire un résumé non-technique des changements du mois en cours, destiné aux utilisateurs finaux.
