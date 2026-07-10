---
name: farm-new-module
description: Crée un nouveau module examples/stack-<nom> pour une stack non encore couverte par la ferme, et propose de le committer dans la ferme source. Invoqué par /farm-init quand une stack non couverte est détectée, ou directement si le besoin apparaît en cours de projet.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Farm New Module — scaffolding d'un module de stack

Crée un module `examples/stack-<nom>/` dans la ferme source (`<FERME>`, chemin sauvegardé dans
`.claude/.farm-source` si `/farm-init` a déjà tourné, sinon à demander).

## Procédure

1. **Identifier ce qui est spécifique à cette stack** dans le projet :
   - Commandes de build/test/lint propres à la stack
   - Outils de migration / gestion de dépendances
   - Patterns de test spécifiques
   - Agents utiles au-delà du socle (ex : agent `rails-migration`, `flutter-build`, `dotnet-publish`)

2. **Créer la structure** dans `<FERME>/examples/stack-<nom>/` :
   ```bash
   mkdir -p "<FERME>/examples/stack-<nom>/.claude/agents"
   mkdir -p "<FERME>/examples/stack-<nom>/.claude/skills"
   ```

3. **Générer a minima** :
   - `settings.json` avec les permissions build/test/lint de la stack
   - 1-2 skills spécifiques (ex : `coverage` adapté à l'outil de la stack)
   - Optionnellement 1 agent si un workflow récurrent mérite d'être capturé

4. **Générer le miroir `.github/`** :
   ```bash
   python3 "<FERME>/scripts/generate_github_mirror.py" --write
   python3 "<FERME>/scripts/validate_farm.py"
   ```

5. **Documenter dans `<FERME>/catalog.md`** et proposer un commit dans la ferme :
   > "Module `stack-<nom>` créé. Voulez-vous committer ce module dans la ferme pour que les prochains projets en bénéficient ?"

   Si oui :
   ```bash
   cd "<FERME>" && git add examples/stack-<nom>/ catalog.md && git commit -m "feat: ajoute module stack-<nom> depuis projet {{NOM_DU_PROJET}}"
   ```

6. **Récapitulatif** : afficher "✅ Module `stack-<nom>` ajouté à la ferme — les prochains projets sur cette stack en bénéficieront directement."
