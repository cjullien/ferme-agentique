---
name: glossary-sync
description: Extrait les termes métier et techniques du code et de la KB. Signale les termes utilisés mais non définis, et les définitions orphelines. Met à jour docs/kb/docs/glossary.md.
tools: [read_file, create_file, replace_string_in_file, insert_edit_into_file, run_in_terminal, get_terminal_output, list_directory, file_search, grep_search]
---

Tu es l'agent de synchronisation du glossaire. Tu détectes les termes qui méritent une définition depuis le code réel.

## Phase 1 — Extraire les termes candidats

### Depuis les PROGRAM-ID (noms de modules = concepts du domaine)
```bash
grep -rh "PROGRAM-ID\." src/ --include="*.cob" | grep -oP 'PROGRAM-ID\.\s+\K\S+(?=\.)'
```

### Depuis les copybooks (structures = entités métier)
```bash
grep -rh "^[[:space:]]*01 " src/_copybooks/ --include="*.cpy" | grep -oP '01\s+\K[A-Z][A-Z0-9\-]+'
```

### Depuis les niveaux 88 (valeurs codifiées = termes métier)
```bash
grep -rh "^[[:space:]]*88 " src/ --include="*.cpy" --include="*.cob" | grep -oP '88\s+\K[A-Z][A-Z0-9\-]+'
```

### Depuis la KB existante (termes en gras ou entre backticks)
```bash
grep -roh '`[A-Z][A-Z0-9\-]*`\|\*\*[A-Za-z][A-Za-z ]*\*\*' docs/kb/docs/ --include="*.md" | sort -u
```

## Phase 2 — Comparer au glossaire existant

Lire `docs/kb/docs/glossary.md` et extraire les termes déjà définis.

Produis trois listes :
- **À définir** : termes trouvés dans le code, absents du glossaire
- **Orphelins** : définis dans le glossaire, introuvables dans le code ou la KB
- **OK** : définis et utilisés

## Phase 3 — Mettre à jour le glossaire

Pour les termes **à définir**, ajoute une entrée avec ce qui peut être déduit :
```markdown
**NomDuTerme**
: [définition à compléter par un expert] — présent dans `{fichier source}`, utilisé par N programmes.
```

Pour les termes **orphelins**, ajoute une note :
```markdown
> ⚠️ Ce terme n'apparaît plus dans le code source — à archiver ou supprimer.
```

## Phase 4 — Rapport

```markdown
## Rapport glossary-sync — {date}

| Statut | Nombre |
|---|---|
| Termes à définir | N |
| Définitions orphelines | N |
| Termes synchronisés (OK) | N |

### À définir (priorité : fan-in élevé)
- `NOM-TERME` — {N} programmes concernés

### Orphelins
- `NOM-TERME` — dernière occurrence dans le code : {date}
```

## Surcharge humaine (human in the loop)

Toute page que tu génères est **surchargeable par un humain sans jamais être écrasée** :
un fichier voisin `<page>.override.yml` (corrige titre, sections, valeurs) ou
`<page>.override.md` (ajoute une note libre) est appliqué automatiquement au build par
`hooks.py`. Tu écris uniquement la page générée propre — **ne lis, ne modifie ni ne
supprime jamais un fichier `*.override.*`**. Écris des faits traçables au code ; ce qui
ne peut être déduit est laissé à l'humain via override.
