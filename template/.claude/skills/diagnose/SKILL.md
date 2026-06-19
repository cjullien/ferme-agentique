---
name: diagnose
description: Boucle de diagnostic disciplinée pour les bugs difficiles et régressions. Reproduire → minimiser → hypothèses → instrumenter → corriger → test de non-régression. À utiliser quand l'utilisateur signale un bug, dit que quelque chose est cassé, ou décrit une régression.
allowed-tools: Agent, Read, Grep, Glob, Bash, Write, Edit
---

# Diagnose

Discipline pour les bugs difficiles. Ne sauter aucune phase sans justification explicite.

Consulter `CONTEXT.md` à la racine pour utiliser le vocabulaire métier du projet.

## Phase 1 — Construire une boucle de feedback

**C'est LE skill.** Tout le reste est mécanique. Si tu as un signal pass/fail rapide, déterministe et exécutable, tu trouveras la cause. Sinon, aucune quantité de lecture de code ne te sauvera.

Investis un effort disproportionné ici. **Sois agressif. Sois créatif. Refuse d'abandonner.**

### Moyens de construire une boucle — dans cet ordre

1. **Test en échec** au niveau approprié — unit, intégration, e2e (frameworks identifiés via CLAUDE.md).
2. **Curl / script HTTP** contre le serveur dev (`http://localhost:8000/api/...`).
3. **Invocation CLI** avec fixture, diff stdout contre snapshot connu.
4. **Script e2e** headless — drive l'UI, assertions DOM/console/réseau.
5. **Replay de trace.** Sauver une requête réseau / payload / log, la rejouer en isolation.
6. **Harness jetable.** Sous-ensemble minimal (un router, deps mockées) exerçant le code path du bug.
7. **Boucle property/fuzz.** Si le bug est "parfois mauvaise sortie", lancer 1000 inputs aléatoires.
8. **Harness de bisection.** Si le bug est apparu entre deux états connus, automatiser `git bisect run`.
9. **Boucle différentielle.** Même input sur ancienne vs nouvelle version, diff des outputs.

### Itérer sur la boucle elle-même

- Plus rapide ? (Cache setup, scope restreint)
- Signal plus net ? (Assert sur le symptôme exact, pas "n'a pas crashé")
- Plus déterministe ? (Fixer le temps, seeder le RNG, isoler le filesystem)

### Quand tu ne peux pas construire de boucle

Stop. Dis-le explicitement. Liste ce que tu as essayé. Demande à l'utilisateur : (a) accès à l'environnement qui reproduit, (b) un artefact capturé (log, HAR, screen recording), ou (c) permission d'ajouter de l'instrumentation temporaire.

Ne **pas** passer à la Phase 2 sans boucle.

## Phase 2 — Reproduire

Lancer la boucle. Observer le bug.

Confirmer :
- [ ] La boucle produit le mode de défaillance décrit par l'**utilisateur** — pas un autre bug voisin.
- [ ] L'échec est reproductible sur plusieurs runs.
- [ ] Le symptôme exact est capturé (message d'erreur, mauvaise sortie, timing lent).

## Phase 3 — Hypothèses

Générer **3–5 hypothèses classées** avant d'en tester aucune.

Chaque hypothèse doit être **falsifiable** :

> Format : "Si <X> est la cause, alors <changer Y> fera disparaître le bug / <changer Z> l'aggravera."

**Montrer la liste classée à l'utilisateur avant de tester.** Il a souvent un savoir domaine qui re-classe instantanément.

## Phase 4 — Instrumenter

Chaque sonde doit mapper à une prédiction de la Phase 3. **Changer une variable à la fois.**

Préférence d'outils :
1. **Debugger / REPL** si l'env le supporte. Un breakpoint vaut dix logs.
2. **Logs ciblés** aux frontières qui distinguent les hypothèses.
3. Jamais "logger tout et grep".

**Taguer chaque log de debug** avec un préfixe unique, ex : `[DEBUG-a4f2]`. Le cleanup devient un seul grep.

**Branche perf.** Pour les régressions de performance : mesurer d'abord (timing, profiler, query plan), corriger ensuite.

## Phase 5 — Corriger + test de non-régression

Écrire le test de non-régression **avant** le fix — mais seulement s'il existe un **bon seam** pour ça.

1. Transformer le repro minimisé en test en échec.
2. Le regarder échouer.
3. Appliquer le fix.
4. Le regarder passer.
5. Relancer la boucle Phase 1 contre le scénario original (non-minimisé).

## Phase 6 — Cleanup + post-mortem

Obligatoire avant de déclarer terminé :
- [ ] Le repro original ne reproduit plus (relancer la boucle Phase 1)
- [ ] Le test de non-régression passe
- [ ] Tous les `[DEBUG-...]` sont supprimés (`grep` le préfixe)
- [ ] Les prototypes jetables sont supprimés
- [ ] L'hypothèse correcte est indiquée dans le message de commit

**Puis demander : qu'est-ce qui aurait empêché ce bug ?** Si la réponse implique un changement architectural, le remonter via `/improve-architecture`.
