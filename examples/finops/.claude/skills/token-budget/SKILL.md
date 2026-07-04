---
name: token-budget
description: Rapport de burn rate tokens de la session — plafond configuré, appels Agent/Task loggés, économies rtk, recommandation de modèle selon le type de tâche inféré.
allowed-tools: Bash
---

Produit un rapport d'état de la session courante pour piloter les coûts LLM en temps réel.

## Procédure

1. **Collecter les données disponibles** :
   ```bash
   # Plafond de tokens configuré
   echo "CLAUDE_CODE_MAX_OUTPUT_TOKENS=${CLAUDE_CODE_MAX_OUTPUT_TOKENS:-non défini}"

   # Télémétrie locale
   LOG="$(git rev-parse --show-toplevel 2>/dev/null || echo .)/.claude/finops.log"
   if [ -f "$LOG" ]; then
     echo "=== Derniers appels Agent/Task (cumulatif toutes sessions) ==="
     tail -20 "$LOG"
     echo "=== Total appels ==="
     wc -l "$LOG"
   else
     echo "finops.log absent (hook PostToolUse non installé)"
   fi

   # Économies RTK
   rtk gain 2>/dev/null || echo "rtk non disponible"
   ```

2. **Afficher le rapport structuré** :

   ```
   ## Token Budget — état session

   Plafond output configuré : <valeur ou "non défini">
   Appels Agent/Task loggés : <N ou "hook non installé">
   Économies RTK cumulées   : <sortie rtk gain ou "rtk non disponible">
   ```

3. **Tableau de routage modèle** (toujours affiché) :

   ```
   | Type de tâche              | Modèle recommandé           | Ratio coût |
   |----------------------------|-----------------------------|------------|
   | Explorer / grep / classify | claude-haiku-4-5-20251001   | 1×         |
   | Générer / coder / corriger | claude-sonnet-4-6           | ~5×        |
   | Architecturer / planifier  | claude-opus-4-8             | ~15×       |
   ```

4. **Inférer le type de tâche** depuis le dernier message utilisateur (déjà en contexte) :
   - Mots-clés "explore", "trouve", "lit", "liste", "qu'est-ce", "cherche", "grep" → **Haiku**
   - Mots-clés "écris", "génère", "implémente", "corrige", "refactorise", "crée" → **Sonnet**
   - Mots-clés "conçois", "architecture", "plan", "revue complète", "audit global" → **Opus**

   Afficher : `Tâche inférée : <type> → Recommandation : <model-id>`

5. **Alerte si journal chargé** — appliquer la même grille que `/cost-check` :
   - < 5 appels → ✅ CONTINUE
   - 5–15 appels → ⚠️ CAUTION — envisager `/cost-check` avant la prochaine tâche longue
   - > 15 appels → 🛑 STOP — lancer `/cost-check` pour obtenir le handoff

   Note : les colonnes `in=` / `out=` peuvent afficher `0` si Claude Code ne peuple pas `tool_response.usage` pour les appels Agent/Task — le comptage des appels reste fiable.
