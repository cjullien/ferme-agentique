---
name: karate-tnr
description: Vérifie et complète la couverture des TNR Karate pour tout endpoint/comportement HTTP nouveau ou modifié.
---

Lance l'agent `karate-tnr`.

Utilise l'outil Agent avec `subagent_type: karate-tnr` pour croiser les endpoints backend
(un ou plusieurs runtimes derrière le même contrat HTTP, cf. `CLAUDE.md`) avec les scénarios
Karate existants, et **ajouter directement** les scénarios manquants (cas nominal + limite +
erreurs).

À invoquer dès qu'un endpoint/comportement HTTP est ajouté ou modifié, ou sur toute demande
mentionnant les TNR/tests de non-régression Karate.
