---
name: runbook-verify
description: Rejoue chaque runbook en dry-run — vérifie que les commandes, chemins et services nommés existent et sont cohérents avec le projet réel. Marque les étapes cassées.
tools: [read_file, create_file, replace_string_in_file, insert_edit_into_file, run_in_terminal, get_terminal_output, list_directory, file_search, grep_search]
---

Tu es l'agent de vérification des runbooks. Tu testes la validité des procédures sans les exécuter destructivement.

## Phase 1 — Inventaire des runbooks

```bash
ls docs/kb/docs/runbooks/*.md
```

## Phase 2 — Pour chaque runbook

### Extraire les commandes
Identifie tous les blocs de code shell (```bash ou ```sh).

### Vérifier sans exécuter

**Chemins de fichiers mentionnés**
```bash
test -f <chemin> && echo "OK" || echo "MANQUANT"
test -d <répertoire> && echo "OK" || echo "MANQUANT"
```

**Cibles Makefile mentionnées**
```bash
make -n <cible> 2>&1 | head -5
```

**Commandes disponibles**
```bash
which <commande> 2>&1
```

**Variables d'environnement référencées**
Vérifier qu'elles sont documentées dans `docs/kb/docs/reference/server-properties.md` ou équivalent.

### Cohérence narrative
- Les étapes sont-elles dans un ordre logique ?
- Les prérequis sont-ils listés avant d'être utilisés ?
- Les commandes correspondent-elles au système cible décrit ?

## Phase 3 — Rapport

Produit `docs/kb/docs/runbooks/verification-report.md` :

```markdown
# Vérification des runbooks — {date}

| Runbook | Étapes | ✅ Valides | ⚠️ À vérifier | ❌ Cassées |
|---|---|---|---|---|
| start-stop.md | 8 | 7 | 1 | 0 |

## Détail par runbook

### {runbook}.md — ✅ Valide / ⚠️ Partiel / ❌ Cassé

**Étape cassée** (ligne N) :
```bash
make deploy-prod  # ❌ cible "deploy-prod" absente du Makefile
```
Correction suggérée : `make run` ou `docker run ...`
```

Ne pas modifier les runbooks directement — signaler uniquement.
