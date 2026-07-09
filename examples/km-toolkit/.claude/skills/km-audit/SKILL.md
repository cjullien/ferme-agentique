---
name: km-audit
description: Audit de fraîcheur de la KB — croise l'historique des pages avec celui du code qu'elles décrivent. Signale pages périmées, liens morts, pages orphelines. Score par section.
allowed-tools: Agent
---

Lance l'audit de fraîcheur de la KB via l'agent `km-audit`.

Utilise l'outil Agent avec `subagent_type: km-audit`, en lui transmettant :
- un prompt demandant d'auditer la fraîcheur de la base de connaissances

L'agent produit :
- Pages dont le code source a évolué depuis la dernière mise à jour de la page
- Liens morts dans la KB
- Pages orphelines (non référencées dans la nav)
- Score de fraîcheur par section (0-100)

Affiche le rapport d'audit avec les pages à régénérer en priorité.
