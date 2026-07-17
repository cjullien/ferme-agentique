---
name: review
description: Revue complète avant merge — adapte les agents déclenchés selon les fichiers modifiés
disable-model-invocation: true
context: fork
---

Revue complète intelligente avant merge — adapte les agents déclenchés selon la nature des changements.

Procédure :

1. Lire `git --no-pager diff HEAD --name-only` pour identifier les fichiers modifiés

2. Lancer TOUJOURS :
   - Agent `audit` — revue qualité/sécurité/conventions sur le diff

3. Lancer SI des fichiers de routeurs/controllers OU de couche API frontend sont modifiés ET SI l'agent est installé (`.claude/agents/api-contract.md`, module `stack-python-supabase`) :
   - Agent `api-contract` — vérifier que le contrat API reste cohérent

4. Lancer SI des fichiers frontend (composants, pages) sont modifiés :
   - Agent `accessibility` — audit accessibilité limité aux fichiers modifiés

5. Lancer SI des fichiers d'authentification, de middleware ou de config sécurité sont modifiés :
   - Agent `owasp` — audit sécurité ciblé sur les fichiers sensibles modifiés

6. Lancer SI des modèles de données sont modifiés ET SI l'agent est installé (`.claude/agents/schema.md`, module `stack-python-supabase` — le socle n'a que le skill `schema`, sans agent dédié) :
   - Agent `schema` — analyse d'impact du changement de modèle

7. Lancer SI `docs/specs/details/` existe et que le diff modifie un comportement métier (pas
   uniquement refactor/style) :
   - Comparer le comportement livré au scénario Given/When/Then du fichier spec concerné.
   - Si le comportement diverge de la spec (nouveau cas non spécifié, règle de gestion modifiée) :
     le signaler dans la synthèse et proposer de lancer `product-owner` (étape 0 — détection de
     specs obsolètes) ou `docs-update` pour resynchroniser, plutôt que de laisser la spec dériver
     silencieusement.

8. **Toujours en dernier** — si la commande `/insights` est disponible dans cette session Claude Code, la lancer et lire son résultat :
   - Identifier les patterns récurrents signalés (erreurs fréquentes, fichiers souvent modifiés, anti-patterns répétés)
   - Si des patterns correspondent aux findings de la revue → les mentionner dans la synthèse comme **tendance à corriger structurellement**
   - Si `/insights` suggère des améliorations de workflow ou de config → les appliquer dans `CLAUDE.md` ou les agents concernés
   - Si `/insights` n'est pas disponible (commande inconnue) → ignorer cette étape, passer à la synthèse

Synthèse finale :
## Résultat de la revue
[Liste des agents déclenchés]
[Findings regroupés par sévérité, tous agents confondus]
[Patterns récurrents identifiés via /insights — si pertinents]
[Verdict : ✅ Prêt à merger / ⚠️ Points à corriger / 🚫 Bloquant]

> Cette revue reste volontairement légère et systématique (à lancer avant chaque merge). Pour
> un gate formel avec traçabilité critères d'acceptation ↔ tests et profil de risque sur une
> story ou une feature à enjeu (auth, paiement, données), lancer `/qa-gate` après cette revue.

## Mise à jour du backlog (si applicable)

Chemin par défaut : `docs/specs/backlog.md` (ou celui déclaré dans `CLAUDE.md` si différent). Si ce fichier n'existe pas dans le projet, ignorer cette section — ne pas le créer automatiquement.

Sinon, après la synthèse, lire `docs/specs/backlog.md` et y ajouter les findings 🔴/🟠 non encore présents.
Puis mettre à jour la section `## Note qualité globale` avec la note recalculée sur 100 et la date.

**Clôture de l'item livré (OBLIGATOIRE si verdict ✅ Prêt à merger)** : `review` est le dernier
point systématique du cycle de vie d'une feature (contrairement à `qa-gate`, réservé aux zones
à risque) — c'est donc ici, pas dans un futur rappel de `product-owner`, qu'il faut boucler le
backlog :
1. Identifier le ou les items du backlog résolus par ce diff (ID mentionné dans la branche, le
   commit, la story `docs/specs/stories/`, ou déduit du périmètre fonctionnel touché).
2. Les marquer `🟢 Done` (convention `backlog-manager`), ou appliquer l'étape "Post-implémentation"
   de `product-owner` (barrer l'item, le déplacer dans la table des features livrées) si ce
   projet utilise cette convention.
3. Si aucun item correspondant n'est trouvé avec certitude, ne rien marquer et le signaler dans
   la synthèse plutôt que de deviner.

Grille de notation :
| Axe | Poids |
|-----|-------|
| Fonctionnalités métier | 25 pts |
| Sécurité | 25 pts |
| Qualité / Maintenabilité | 20 pts |
| Accessibilité | 15 pts |
| Performance | 15 pts |
| **Total** | **100 pts** |
