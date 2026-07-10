---
name: improve-architecture
description: Trouve les opportunités d'approfondissement architectural dans le codebase (modules shallow, seams manquants, couplages excessifs, violations de couches) et applique le refactoring choisi après validation.
allowed-tools: Agent, Read, Grep, Glob, Bash, Write, Edit
---

# Improve Architecture

Surface les frictions architecturales et propose des **opportunités d'approfondissement** — refactorings qui transforment des modules shallow en modules profonds.

Commence par lire `CLAUDE.md` à la racine pour identifier la stack et les conventions.
Si un `CONTEXT.md` existe, utiliser son vocabulaire de domaine. Si `docs/ARCHITECTURE.md`
existe (généré par `/architect`), l'utiliser comme référence de la cible visée plutôt que de
déduire l'architecture attendue uniquement de l'organisation actuelle du code.

## Vocabulaire

- **Module** — tout ce qui a une interface et une implémentation
- **Profondeur** — beaucoup de comportement derrière une petite interface = profond
- **Seam** — point où un comportement peut être modifié sans éditer en place
- **Test de suppression** — imaginer supprimer le module. Si la complexité disparaît, c'est un pass-through.
- **Localité** — changement, bugs, connaissance concentrés en un seul endroit

## Processus

### 1. Explorer
Explorer le codebase organiquement. Noter les frictions :
- Modules **shallow** (interface ≈ implémentation)
- Fonctions pures extraites juste pour la testabilité
- Couplages qui fuient entre les seams
- Parties non testées ou difficiles à tester
- **Si le projet suit une architecture en couches** (domain/application/services/routers ou
  équivalent, identifiée via `docs/ARCHITECTURE.md` ou l'arborescence réelle) : violations du
  sens de dépendance autorisé, logique métier dans la couche transport (routers/controllers),
  services "fourre-tout" mêlant règle métier + accès BDD + I/O externe

### 2. Présenter les candidats
Liste numérotée : Fichiers · Problème · Solution · Bénéfices (localité + levier + tests).

Ne PAS proposer d'interfaces. Demander : "Lequel voulez-vous explorer ?"

### 3. Session de questionnement
Quand l'utilisateur choisit, engager une conversation :
- Contraintes, dépendances, forme du module approfondi
- Mise à jour de `CONTEXT.md` si nouveau concept
- Proposition d'ADR si choix important rejeté avec raison durable

### 4. Appliquer

Une fois la forme du refactoring validée par l'utilisateur : appliquer chirurgicalement,
respecter les conventions de lint/format du projet (identifiées via `CLAUDE.md`), vérifier que
les tests existants passent toujours après coup. Si le refactoring implique un changement de
schéma BDD ou une rupture d'API, signaler sans appliquer.
