---
name: coverage
description: Rapport de couverture de tests (JaCoCo).
disable-model-invocation: true
---

Génère un rapport de couverture de tests en local via JaCoCo.

Cible (optionnelle) : $ARGUMENTS - ex: `/coverage socle`, `/coverage service/tika`.

Sans argument : lancer sur tout le réacteur.
```bash
./mvnw -q -B -Dtest='!*E2ETest,!OcrSpringAiApplicationTest' -Dsurefire.failIfNoSpecifiedTests=false verify
```
(les tests E2E et `OcrSpringAiApplicationTest` nécessitent des clés LLM — exclus du calcul local.)

Puis lire les rapports `*/target/site/jacoco/index.html` (ou `jacoco.csv`) et afficher :
- Couverture globale par module (% instructions / branches)
- Classes sous 80 %
- Classes non couvertes du tout (hors DTO/records triviaux)
