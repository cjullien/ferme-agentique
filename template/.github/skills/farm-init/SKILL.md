---
name: farm-init
description: Vérifie qu'un projet est correctement configuré pour la ferme agentique — CLAUDE.md complet, agents/skills installés, settings.json adapté à la stack, hooks actifs. À lancer après installation du socle ou en début de session sur un projet repris.
allowed-tools: Bash, Read, Glob
---

# Farm Init — Diagnostic de configuration

Vérifie que la ferme agentique est correctement installée et configurée sur ce projet.

## Checks

### 1. CLAUDE.md

```bash
ls CLAUDE.md 2>/dev/null && echo "présent" || echo "absent"
grep -c '{{' CLAUDE.md 2>/dev/null || echo "0"
```

- Fichier présent ?
- Placeholders `{{...}}` non remplacés ? (chaque occurrence = configuration manquante)

### 2. Agents et skills

```bash
ls .claude/agents/*.md 2>/dev/null | wc -l
ls .claude/skills/*/SKILL.md 2>/dev/null | wc -l
```

- Au moins 1 agent et 1 skill installés ?
- Comparer au socle : le template contient 18 agents et 36 skills. Moins = installation partielle.

### 3. settings.json

```bash
jq . .claude/settings.json 2>/dev/null && echo "JSON valide" || echo "JSON invalide ou absent"
jq -r '.permissions.allow[]' .claude/settings.json 2>/dev/null | grep -iE "(npm|pip|mvn|cargo|go |make|gradle|pytest|jest|dotnet)" | head -5
jq 'has("hooks")' .claude/settings.json 2>/dev/null
```

- Fichier présent et JSON valide ?
- Commandes de build/test de la stack présentes dans `permissions.allow` ?
- Section `hooks` configurée ?

### 4. Git

```bash
grep -E "^(node_modules|__pycache__|\.env|venv|\.venv|target/|dist/|build/)$" .gitignore 2>/dev/null | wc -l
git ls-files --others --exclude-standard | grep -iE "\.(env|key|pem|p12|pfx|secret)" | head -5
```

- `.gitignore` couvre-t-il les répertoires sensibles courants ?
- Fichiers potentiellement sensibles non ignorés ?

## Output

Produire un tableau récapitulatif :

```
## Farm Init — Rapport de configuration

| Section        | Statut | Notes                                          |
|----------------|--------|------------------------------------------------|
| CLAUDE.md      | ✅/⚠️/❌ | [détail]                                      |
| Agents         | ✅/⚠️/❌ | X agents installés (18 dans le socle complet) |
| Skills         | ✅/⚠️/❌ | X skills installés (36 dans le socle complet) |
| settings.json  | ✅/⚠️/❌ | [détail]                                      |
| Hooks          | ✅/⚠️/❌ | [détail]                                      |
| .gitignore     | ✅/⚠️/❌ | [détail]                                      |

Légende : ✅ OK  ⚠️ incomplet  ❌ absent ou invalide
```

Suivi de **Actions recommandées** listant uniquement les points ⚠️ et ❌, avec la correction concrète :

- "CLAUDE.md absent → `cp <ferme>/template/CLAUDE.template.md ./CLAUDE.md`"
- "3 placeholders `{{` non remplacés dans CLAUDE.md → compléter la stack et les commandes"  
- "settings.json sans commandes stack → ajouter les commandes build/test (voir `examples/stack-*/`)"
- "Hooks absents → copier la section `hooks` depuis `<ferme>/template/.claude/settings.json`"
