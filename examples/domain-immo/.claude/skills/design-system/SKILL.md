---
name: design-system
description: Audit et application du design system frontend - cohérence visuelle, tokens, patterns datatable/toolbar/tabs, prévention des erreurs graphiques.
allowed-tools: Agent, Read, Grep, Glob, Bash, Edit, Write
disable-model-invocation: true
---

> Exemple concret, spécifique à ce projet — voir la version générique du socle :
> `template/.claude/skills/design-system/SKILL.md`.

Lance un audit design system via l'agent `design-system`.

Utilise l'outil Agent avec `subagent_type: design-system` en transmettant un prompt demandant explicitement :
- d'analyser le fichier/dossier ciblé (ou tout `frontend/src/pages/` + `frontend/src/components/` si pas de périmètre),
- de vérifier les tokens de couleur (interdiction de hex, `text-*-500` sur fond clair, `bg-white`, `text-gray-*`),
- de vérifier le respect du pattern datatable F-081 (ordre tabs → toolbar → table, composants `DataTableToolbar` / `SortableHeader` / `SortChips`),
- de vérifier les conteneurs standards (`bg-card border border-border rounded-xl p-3 sm:p-4` etc.),
- de vérifier l'absence de tirets cadratin `—` dans le code et les traductions,
- de vérifier les tailles d'icônes Lucide et la présence d'`aria-hidden`,
- de classer les findings par sévérité (🔴 Critique / 🟠 Majeur / 🟡 Mineur),
- d'appliquer les corrections chirurgicalement,
- de lancer `pnpm eslint src/` + `pnpm test --run` et reporter les décomptes,
- de mettre à jour `docs/specs/details/TECHNIQUE/F-081-datatable-regles.md` (ou créer une spec `UI-XXX-*.md`) si une nouvelle règle est introduite.

Retourne ensuite un résumé : nombre de violations corrigées par sévérité + état tests/lint.
