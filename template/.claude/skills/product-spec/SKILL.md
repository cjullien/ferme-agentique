---
name: product-spec
description: Analyse PO avec session de questionnement (grill). Vérifie cohérence contre le glossaire domaine (CONTEXT.md), challenge les décisions, met à jour ADRs et specs.
allowed-tools: Agent, Read, Grep, Glob, Bash, Write, Edit
---

Lance une analyse PO via l'agent `product-owner` enrichie d'une session de questionnement.

Utilise l'outil Agent avec `subagent_type: product-owner` en lui transmettant :

$ARGUMENTS

## Processus enrichi (grill-with-docs)

1. **Contexte** - Lire `CLAUDE.md`, `CONTEXT.md` (si existant) et `docs/adr/`
2. **Grill** - Challenger le plan question par question. Signaler les termes flous, contradictions avec le code ou le glossaire.
3. **Mise à jour inline** - Enrichir `CONTEXT.md` avec les termes résolus. Proposer un ADR si décision architecturale importante.
4. **Spec + Backlog** - Générer la spec détaillée, mettre à jour le backlog.
5. **PRD** - Problem Statement · Solution · User Stories · Decisions · Out of Scope
