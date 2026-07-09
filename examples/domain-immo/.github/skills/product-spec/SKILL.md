---
name: product-spec
description: Analyse PO avec session de questionnement (grill), spécialisée gestion locative immobilière — vérifie l'usage cohérent du glossaire métier (bail/bailleur/locataire/loyer...), challenge les décisions, met à jour ADRs et specs.
allowed-tools: Agent, Read, Grep, Glob, Bash, Write, Edit
---

> Variante domaine (gestion locative immobilière) du skill générique `product-spec` du socle —
> surcharge automatiquement à l'installation, même nom. Value ajoutée par rapport au générique :
> le glossaire métier ci-dessous, utilisé même en l'absence de `CONTEXT.md` dans le projet.

Lance une analyse PO via l'agent `product-owner` enrichie d'une session de questionnement et
du glossaire métier de la gestion locative.

Utilise l'outil Agent avec `subagent_type: product-owner` en lui transmettant :

$ARGUMENTS

## Glossaire métier (gestion locative)

Si `CONTEXT.md` n'existe pas encore dans le projet, ce glossaire sert de référence par défaut —
proposer de créer/enrichir `CONTEXT.md` avec ces termes dès la première invocation.

| Terme | Définition | Champ/variable (code) | Ne pas confondre avec |
|---|---|---|---|
| Bail | Contrat de location (loi du 6 juillet 1989) | `lease` | "Contrat" seul — trop générique, ambigu avec un contrat de prestation (artisan) |
| Bailleur | Propriétaire qui loue le bien | `landlord` | "Propriétaire" seul — un propriétaire non loué n'est pas un bailleur |
| Locataire | Personne qui loue le bien | `tenant` | "Preneur" — vocabulaire de bail commercial, pas résidentiel ici |
| Loyer | Somme due hors charges | `rent` | "Charges" — somme distincte, apparaît séparément sur la quittance |
| IRL | Indice de référence des loyers, base de la révision annuelle | `rentIndex` | "Indice" seul, ou "loyer révisé" (résultat, pas l'indice) |
| Dépôt de garantie | Somme versée à l'entrée, plafonnée par la loi (voir `/legal-check`) | `deposit` | "Caution" — engagement d'un tiers garant, notion différente |
| DPE | Diagnostic de performance énergétique | `energyRating` | "Classe énergie" — résultat du DPE (A à G), pas le diagnostic lui-même |
| Quittance | Justificatif de paiement du loyer remis par le bailleur | `receipt` | "Facture" — non émise à ce titre par un bailleur particulier |
| Artisan | Prestataire d'intervention/maintenance sur un bien | `contractor` | "Locataire" ou "Bailleur" — tiers externe, pas partie au bail |

Pour la conformité légale de ces notions (durées de bail, plafonds, mentions obligatoires),
voir `/legal-check` — `product-spec` ne vérifie que la cohérence terminologique et
fonctionnelle, pas la conformité juridique.

## Processus enrichi (grill-with-docs)

1. **Contexte** - Lire `CLAUDE.md`, `CONTEXT.md` (si existant, sinon le glossaire ci-dessus) et `docs/adr/`
2. **Grill** - Challenger le plan question par question. Signaler les termes flous, contradictions avec le code ou le glossaire.
3. **Mise à jour inline** - Enrichir `CONTEXT.md` avec les termes résolus. Proposer un ADR si décision architecturale importante.
4. **Spec + Backlog** - Générer la spec détaillée, mettre à jour le backlog.
5. **PRD** - Problem Statement · Solution · User Stories · Decisions · Out of Scope
