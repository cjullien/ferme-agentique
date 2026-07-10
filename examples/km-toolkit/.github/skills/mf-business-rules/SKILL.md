---
name: mf-business-rules
description: Extrait les règles métier enfouies dans le COBOL procédural — EVALUATE/IF imbriqués, tables de décision, constantes et valeurs 88. Restitue en langage naturel avec citation du paragraphe source.
allowed-tools: Agent
---

Lance l'extraction des règles métier via l'agent `mf-business-rules`.

Utilise l'outil Agent avec `subagent_type: mf-business-rules`, en lui transmettant :
- un prompt demandant d'extraire les règles métier depuis les programmes COBOL (ou un programme/domaine précis si spécifié)

L'agent produit :
- Extraction des EVALUATE/WHEN et IF/ELSE imbriqués en règles lisibles
- Identification des tables de décision implicites
- Décodage des constantes et valeurs 88 en énumérations métier
- Chaque règle citée avec son paragraphe source (programme + ligne)
- Aucune règle inventée : tout est tracé vers le code source
- Catalogue dans `docs/kb/docs/mf/business-rules.md`

Affiche le nombre de règles extraites par programme et les zones avec la plus forte densité de logique métier.
