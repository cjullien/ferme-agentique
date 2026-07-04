---
name: model-pick
description: Sélecteur de modèle interactif — demande le type de tâche, retourne le modèle recommandé avec tableau coût/qualité et guide fork-vs-inline.
allowed-tools: []
---

Aide à choisir le bon modèle LLM avant de lancer un agent ou une tâche coûteuse.

## Procédure

1. Poser exactement cette question à l'utilisateur et attendre sa réponse avant de continuer :

   > "Quel type de tâche vas-tu exécuter ?
   > (1) Explorer / lire / chercher / classifier
   > (2) Générer / coder / corriger / refactoriser
   > (3) Réviser / auditer / tester
   > (4) Architecturer / planifier / design complet"

2. En fonction de la réponse, afficher le tableau complet puis la recommandation :

   ```
   | Tier      | Model ID                    | Input $/1M tok | Output $/1M tok | Idéal pour                          |
   |-----------|-----------------------------|----------------|-----------------|--------------------------------------|
   | Rapide    | claude-haiku-4-5-20251001   |     ~$0,80     |     ~$4,00      | Explore, grep, classify, triage      |
   | Équilibré | claude-sonnet-4-6           |     ~$3,00     |    ~$15,00      | Code, fix, refactor, tests           |
   | Puissant  | claude-opus-4-8             |    ~$15,00     |    ~$75,00      | Architect, audit complet, planning   |
   ```

   **Recommandation** : `<model-id>` — `<justification en une phrase>`

   Ratio de coût : `<modèle choisi>` coûte `<X>×` plus que Haiku pour cette tâche.

3. Afficher le guide fork-vs-inline adapté au type de tâche :

   | Situation | Patron recommandé |
   |---|---|
   | Lecture < 500 lignes, edit < 3 fichiers | Inline, pas de sous-agent |
   | Lecture > 500 lignes à résumer | Fork vers Haiku — résumer puis retourner |
   | Génération > 3 fichiers | Fork vers Sonnet avec spec resserrée |
   | Audit complet / architectural | Fork vers Opus — passer un résumé contexte, pas un dump de fichiers |
   | Tâches indépendantes parallèles | Plusieurs sous-agents Haiku en parallèle |

4. Terminer par le conseil hygiène spécifique au modèle choisi :
   - **Haiku** : "Garde le prompt sous 2 000 tokens — Haiku dégrade sur les longs contextes."
   - **Sonnet** : "Scope le prompt à la tâche précise ; évite de relire les fichiers déjà en contexte."
   - **Opus** : "Utilise des ancres de cache (`CLAUDE.md`, `CONTEXT.md` lus en premier) ; le coût d'entrée est élevé, amortis-le avec une tâche à forte valeur."
