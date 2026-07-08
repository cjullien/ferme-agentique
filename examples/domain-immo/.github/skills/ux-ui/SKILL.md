---
name: ux-ui
description: Audit et amélioration UX/UI du frontend — cohérence visuelle, ergonomie mobile, design system, micro-interactions.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

> Exemple concret, spécifique à ce projet — voir la version générique du socle :
> `template/.claude/skills/ux-ui/SKILL.md`.

Lance un audit UX/UI complet via l'agent `ux-ui`.

Utilise l'outil Agent avec `subagent_type: ux-ui` en transmettant un prompt demandant explicitement :
- d'analyser le composant ou la page ciblée (ou tout le code source frontend si pas de périmètre précisé),
- de relever les problèmes de cohérence visuelle (couleurs, tailles d'icônes, espacements, arrondis),
- de vérifier l'ergonomie mobile (touch targets, responsive, overflow),
- de vérifier le respect du design system (composants UI, tokens de design),
- d'identifier les micro-interactions manquantes (loading, états vides, feedback),
- une restitution structurée par sévérité (🔴 Critique / 🟠 Majeur / 🟡 Mineur),
- d'appliquer les corrections chirurgicalement,
- de s'assurer que les textes passent par i18n (`fr.js` + `en.js`).
