---
name: farm-update
description: Compare les agents et skills installés sur ce projet avec la ferme source et propose d'appliquer les mises à jour. À lancer après une mise à jour de la ferme ou périodiquement pour rester en sync.
allowed-tools: Bash, Read, Write, Glob
---

# Farm Update — Synchronisation avec la ferme source

Met à jour les agents et skills du projet depuis la ferme source.

---

## Phase 0 — Localiser la ferme source

```bash
cat .claude/.farm-source 2>/dev/null
```

- Si `.claude/.farm-source` existe → utiliser ce chemin comme `<FERME>`
- Sinon → demander : "Quel est le chemin vers la ferme agentique ? (ex: /Users/moi/ferme_agentic)"

Vérifier que `<FERME>/template/.claude/agents/` existe.

---

## Phase 1 — Analyser les diffs

### Agents

```bash
diff -rq --exclude="*.pyc" "<FERME>/template/.claude/agents/" .claude/agents/ 2>/dev/null
```

Classer les résultats :
- `Only in <FERME>` → **nouveau** dans la ferme, absent du projet
- `Files differ` → **mis à jour** dans la ferme
- `Only in .claude/agents/` → **local uniquement** (agent projet, à conserver)

### Skills

```bash
diff -rq --exclude="*.pyc" "<FERME>/template/.claude/skills/" .claude/skills/ 2>/dev/null
```

Même classification.

---

## Phase 2 — Présenter le rapport de diff

```
## Farm Update — Rapport de synchronisation

### Agents
| Agent | Statut | Action proposée |
|---|---|---|
| decision-index.md | 🆕 Nouveau dans la ferme | Ajouter |
| audit.md | 🔄 Mis à jour | Mettre à jour |
| mon-agent-local.md | 📌 Local uniquement | Conserver (ne pas toucher) |

### Skills
| Skill | Statut | Action proposée |
|---|---|---|
| farm-init/ | 🔄 Mis à jour | Mettre à jour |
| mon-skill-local/ | 📌 Local uniquement | Conserver |

X nouveaux · Y mises à jour · Z locaux conservés
```

Si aucun diff : "✅ Le projet est à jour avec la ferme source." — s'arrêter là.

---

## Phase 3 — Demander confirmation

> "Voulez-vous appliquer toutes les mises à jour ? (tout / sélection / non)"

- **tout** → appliquer tous les 🆕 et 🔄
- **sélection** → lister les items numérotés, attendre les numéros à appliquer
- **non** → s'arrêter

Les items 📌 (locaux uniquement) ne sont **jamais** touchés.

---

## Phase 4 — Appliquer

Pour chaque item confirmé :

```bash
# Agent nouveau ou mis à jour
cp "<FERME>/template/.claude/agents/<agent>.md" .claude/agents/

# Skill nouveau ou mis à jour
cp -R "<FERME>/template/.claude/skills/<skill>/" .claude/skills/
```

Mettre à jour le miroir `.github/` si le script est disponible :

```bash
python3 "<FERME>/scripts/generate_github_mirror.py" --write 2>/dev/null \
  || echo "Script generate_github_mirror.py non disponible — mettre à jour .github/ manuellement."
```

---

## Phase 5 — Résumé

```
✅ Farm Update terminé

Appliqué : X agents, Y skills
Conservé (local) : Z items
Prochaine étape : /farm-init pour valider la configuration complète
```

Mettre à jour `.claude/.farm-source` avec le chemin utilisé (pour les prochaines invocations).
