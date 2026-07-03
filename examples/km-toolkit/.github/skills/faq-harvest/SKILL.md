---
name: faq-harvest
description: Mine les questions réellement posées dans les issues, tickets et revues de code — transforme les récurrentes en entrées FAQ et troubleshooting dans la KB.
allowed-tools: task
---

Lance la collecte des questions récurrentes via l'agent `faq-harvest`.

Utilise l'outil `task` avec :
- `agent_type: "faq-harvest"`
- un prompt indiquant où chercher (issues GitHub, tickets, commentaires de revues)

L'agent produit :
- Un inventaire des questions posées plus d'une fois
- Les entrées FAQ correspondantes dans `docs/kb/docs/faq.md`
- Les entrées troubleshooting dans `docs/kb/docs/troubleshooting.md`

Affiche les questions identifiées et les pages mises à jour.
