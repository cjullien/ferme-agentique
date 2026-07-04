## FinOps — Routage modèle & hygiène token

> Coller cette section à la fin du `CLAUDE.md` du projet après installation du module `examples/finops/`.

### Routage modèle par défaut

| Type de tâche | Modèle par défaut | Escalader vers |
|---|---|---|
| Explorer / lire / grep / classifier | `claude-haiku-4-5-20251001` | Sonnet si raisonnement complexe |
| Générer / corriger / refactoriser / tester | `claude-sonnet-4-6` | — |
| Architecturer / planifier / audit complet | `claude-opus-4-8` | — uniquement haute valeur |

Règle : commencer par Sonnet, descendre vers Haiku si la tâche est purement lecture/recherche,
monter vers Opus uniquement quand la sortie pilote plusieurs décisions aval.

### Hygiène prompt

- Ne pas relire un fichier déjà lu dans le tour courant.
- Garder les prompts de sous-agents sous 500 mots ; exclure les fichiers déjà en contexte.
- Ancres de cache : lire `CLAUDE.md` et `CONTEXT.md` en premier — ils sont probablement en cache ;
  les référencer symboliquement ensuite.
- Éviter les instructions "lis tout le codebase" — scoper aux répertoires pertinents pour la tâche.
- Préférer les sorties concises : utiliser `/caveman` pour les explorations (−75 % tokens sortie).

### Fork vs inline

| Situation | Patron |
|---|---|
| Édition < 3 fichiers | Inline — pas de sous-agent |
| Lecture > 500 lignes à traiter | Fork Haiku — résumer puis retourner |
| Génération > 3 fichiers | Fork Sonnet avec spec resserrée |
| Audit complet / architectural | Fork Opus — passer résumé contexte, pas dump de fichiers |
| Tâches indépendantes en parallèle | Plusieurs sous-agents Haiku en parallèle |

### Checklist pré-sous-agent

Avant de spawner un Agent ou Task :

- [ ] La tâche est-elle vraiment indépendante ? (si elle partage l'état du tour courant, inline est plus sûr)
- [ ] Le prompt est-il < 500 mots et exclut-il les fichiers déjà en contexte ?
- [ ] Le tier de modèle est-il approprié ? (Explorer → Haiku, Générer → Sonnet, Architecturer → Opus)
- [ ] La sortie sera-t-elle réutilisée pour plusieurs décisions aval ? (Oui → Opus ; Non → Sonnet ou Haiku)
- [ ] La session a-t-elle déjà > 10 appels Agent/Task ? (Oui → lancer `/cost-check` d'abord)

### Skills FinOps installés

| Skill | Quand l'utiliser |
|---|---|
| `/token-budget` | Vérification mid-session : burn rate + recommandation modèle |
| `/cost-check` | Avant une tâche longue : verdict continuer vs résumer |
| `/model-pick` | Sélection interactive modèle avec tableau coût/qualité |
