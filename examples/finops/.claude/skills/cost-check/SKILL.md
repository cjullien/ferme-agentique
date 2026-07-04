---
name: cost-check
description: Checkpoint coût rapide — compte les appels Agent/Task de la session, lit les économies rtk, rend un verdict CONTINUE / CAUTION / STOP avec handoff prêt-à-coller si besoin.
allowed-tools: Bash
---

Évalue si la session courante est encore économiquement saine avant de lancer un agent long ou coûteux.

## Procédure

1. **Lire la télémétrie locale** :
   ```bash
   # Compter les appels Agent/Task loggés (cumulatif toutes sessions)
   LOG="$(git rev-parse --show-toplevel 2>/dev/null || echo .)/.claude/finops.log"
   if [ -f "$LOG" ]; then
     wc -l "$LOG"
     tail -5 "$LOG"
   else
     echo "finops.log absent — hook PostToolUse non installé"
   fi
   ```

   Si `finops.log` est absent, afficher : "Verdict indisponible — installer le hook PostToolUse de `settings.finops.json` pour activer la télémétrie." et s'arrêter là.

2. **Économies RTK** :
   ```bash
   rtk gain 2>/dev/null || echo "rtk non disponible"
   ```

3. **Afficher la matrice de décision** avec les valeurs réelles collectées :

   ```
   Appels Agent/Task (cumulatif toutes sessions) : <N>
   Économies RTK rapportées                      : <X tokens / ~$Y>

   Verdict :
   ─────────────────────────────────────────────────────
   < 5 appels  → ✅ CONTINUE   — session encore légère
   5–15 appels → ⚠️  CAUTION   — envisager de résumer avant la prochaine grosse tâche
   > 15 appels → 🛑 STOP      — démarrer une nouvelle session
   ─────────────────────────────────────────────────────
   ```

4. **Si verdict STOP**, générer un handoff prêt-à-coller pour la prochaine session :
   ```bash
   git status
   git log --oneline -5
   ```

   Puis produire :
   ```
   ## Handoff session (coller au début de la prochaine session)
   Contexte : <1 phrase décrivant la tâche en cours>
   Fait      : <liste à puces des étapes terminées>
   À faire   : <prochaine action concrète>
   Fichiers  : <liste depuis git status>
   ```

5. **Rappels hygiène** (toujours afficher en clôture) :
   - Ne pas relire un fichier déjà lu dans le tour courant
   - Garder les prompts sous-agents sous 500 mots, exclure les fichiers déjà en contexte
   - Préfixer les nouvelles sessions par la lecture de `CLAUDE.md` et `CONTEXT.md` (cache-friendly)
   - `/caveman` réduit les tokens de sortie de ~75 % en mode exploration
