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

3. Lancer SI des fichiers de routeurs/controllers OU de couche API frontend sont modifiés :
   - Agent `api-contract` — vérifier que le contrat API reste cohérent

4. Lancer SI des fichiers frontend (composants, pages) sont modifiés :
   - Agent `a11y` — audit accessibilité limité aux fichiers modifiés

5. Lancer SI des fichiers d'authentification, de middleware ou de config sécurité sont modifiés :
   - Agent `owasp` — audit sécurité ciblé sur les fichiers sensibles modifiés

6. Lancer SI des modèles de données sont modifiés :
   - Agent `schema` — analyse d'impact du changement de modèle

7. **Toujours en dernier** — si la commande `/insights` est disponible dans cette session Claude Code, la lancer et lire son résultat :
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

## Mise à jour du backlog (si applicable)

Chemin par défaut : `docs/specs/backlog.md` (ou celui déclaré dans `CLAUDE.md` si différent). Si ce fichier n'existe pas dans le projet, ignorer cette section — ne pas le créer automatiquement.

Sinon, après la synthèse, lire `docs/specs/backlog.md` et y ajouter les findings 🔴/🟠 non encore présents.
Puis mettre à jour la section `## Note qualité globale` avec la note recalculée sur 100 et la date.

Grille de notation :
| Axe | Poids |
|-----|-------|
| Fonctionnalités métier | 25 pts |
| Sécurité | 25 pts |
| Qualité / Maintenabilité | 20 pts |
| Accessibilité | 15 pts |
| Performance | 15 pts |
| **Total** | **100 pts** |
