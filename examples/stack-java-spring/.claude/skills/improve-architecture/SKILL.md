---
name: improve-architecture
description: Trouve les opportunités d'approfondissement architectural - modules shallow, seams manquants, couplages excessifs.
allowed-tools: Agent, Read, Grep, Glob, Bash, Write, Edit
---

# Improve Architecture

Surface les frictions architecturales et propose des **opportunités d'approfondissement**.

Lire `CLAUDE.md` pour découvrir les modules Maven du projet (multi-module Spring Boot — noms et responsabilités déclarés dans `CLAUDE.md`, ex : un module socle partagé et des modules de service par domaine).

## Vocabulaire
- **Module profond** : beaucoup de comportement derrière une petite interface.
- **Shallow** : interface ≈ implémentation (pass-through).
- **Seam** : point d'extension sans édition en place.
- **Test de suppression** : si on supprime le module et que la complexité disparaît, c'est un pass-through.

## Processus
1. **Explorer** le code, noter les frictions : modules shallow, classes extraites juste pour la testabilité, couplages qui fuient entre modules, zones difficiles à tester, beans Spring eager fragiles (instanciés au démarrage alors qu'ils dépendent d'une config ou d'un service externe).
2. **Présenter les candidats** : liste numérotée — Fichiers · Problème · Solution · Bénéfices (localité + levier + testabilité). Ne PAS imposer d'interface. Demander : « Lequel approfondir ? »
3. **Session de questionnement** sur le choix : contraintes, dépendances, forme cible. Proposer un ADR si un choix structurant est tranché.
4. **Appliquer** le refactoring choisi une fois la forme validée.
