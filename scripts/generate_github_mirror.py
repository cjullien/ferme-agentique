#!/usr/bin/env python3
"""Génère la version Copilot (`.github/`) depuis la source Claude Code (`.claude/`).

La ferme documente des contenus « identiques » entre les deux miroirs, mais les
deux versions ont dérivé manuellement au fil des projets d'origine (agents
avec les mauvais noms d'outils dans un sens ou dans l'autre, corps de texte
désynchronisés). Ce script élimine la classe de bug « double maintenance
manuelle » en dérivant `.github/` depuis `.claude/`, qui devient la source de
vérité :

- **Agents** (`agents/*.md` → `agents/*.agent.md`) : le corps est copié tel
  quel, seul le frontmatter `tools:` est traduit (noms Claude Code → noms
  Copilot). Quelques agents Copilot embarquent des outils spécifiques à une
  extension (ex: `a11y_audit` pour l'extension accessibility) qui n'ont pas
  d'équivalent Claude Code — voir EXTRA_COPILOT_TOOLS ci-dessous pour les
  conserver explicitement plutôt que les perdre silencieusement.
- **Skills** (`skills/*/SKILL.md`) : copiés à l'identique (aucune syntaxe
  spécifique à une plateforme dans ces fichiers).

Usage :
    python3 scripts/generate_github_mirror.py           # affiche les diffs, ne modifie rien (défaut)
    python3 scripts/generate_github_mirror.py --write   # applique les diffs

Le script parcourt `template/` et chaque module de `examples/`.
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Traduction outils Claude Code -> outils Copilot. Un agent en lecture seule
# (ex: Read, Grep, Glob) ne produira donc pas run_in_terminal/create_file.
CLAUDE_TO_COPILOT = {
    "Read": ["read_file"],
    "Write": ["create_file"],
    "Edit": ["replace_string_in_file", "insert_edit_into_file"],
    "Bash": ["run_in_terminal", "get_terminal_output"],
    "Grep": ["grep_search"],
    "Glob": ["list_directory", "file_search"],
}
# Un agent avec au moins un outil d'édition/exécution reçoit aussi get_errors
# (diagnostics IDE Copilot), comme c'était le cas dans tous les agents
# d'origine dotés du toolset complet.
EDIT_TOOLS = {"Write", "Edit", "Bash"}

# Outils Copilot spécifiques à une extension, sans équivalent Claude Code :
# à ajouter explicitement par nom d'agent plutôt que dérivés automatiquement.
EXTRA_COPILOT_TOOLS: dict[str, list[str]] = {
    "accessibility": ["a11y_audit", "a11y_check_file"],
}


def split_frontmatter(text: str) -> tuple[list[str], dict[str, str], str]:
    if not text.startswith("---"):
        return [], {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [], {}, text
    fm_lines = parts[1].strip("\n").splitlines()
    fm: dict[str, str] = {}
    for line in fm_lines:
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm_lines, fm, parts[2].lstrip("\n")


# Ordre canonique observé dans les agents .agent.md d'origine : Read, Write,
# Edit, Bash, puis les outils de recherche (Glob avant Grep), puis get_errors.
CANONICAL_ORDER = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]


def translate_tools(claude_tools: str, agent_name: str) -> str:
    tokens = {t.strip() for t in claude_tools.split(",") if t.strip()}
    copilot_tokens: list[str] = []
    for tok in CANONICAL_ORDER:
        if tok in tokens:
            copilot_tokens.extend(CLAUDE_TO_COPILOT[tok])
    if tokens & EDIT_TOOLS:
        copilot_tokens.append("get_errors")
    copilot_tokens.extend(EXTRA_COPILOT_TOOLS.get(agent_name, []))
    return "[" + ", ".join(copilot_tokens) + "]"


def generate_agent(claude_path: Path, agent_name: str) -> str:
    fm_lines, fm, body = split_frontmatter(claude_path.read_text(encoding="utf-8"))
    out_lines = ["---"]
    for line in fm_lines:
        key = line.split(":", 1)[0].strip()
        if key == "tools" and "tools" in fm:
            out_lines.append(f"tools: {translate_tools(fm['tools'], agent_name)}")
        else:
            out_lines.append(line)
    out_lines.append("---")
    return "\n".join(out_lines) + "\n\n" + body


def diff_or_write(target: Path, new_content: str, write: bool, changed: list[str]) -> None:
    old_content = target.read_text(encoding="utf-8") if target.exists() else ""
    if old_content == new_content:
        return
    changed.append(str(target.relative_to(ROOT)))
    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_content, encoding="utf-8")
    else:
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{target.relative_to(ROOT)}",
            tofile=f"b/{target.relative_to(ROOT)}",
        )
        sys.stdout.writelines(diff)


def process_module(module_dir: Path, write: bool, changed: list[str]) -> None:
    claude_agents = module_dir / ".claude/agents"
    github_agents = module_dir / ".github/agents"
    if claude_agents.exists():
        for claude_path in sorted(claude_agents.glob("*.md")):
            name = claude_path.stem
            new_content = generate_agent(claude_path, name)
            diff_or_write(github_agents / f"{name}.agent.md", new_content, write, changed)

    claude_skills = module_dir / ".claude/skills"
    github_skills = module_dir / ".github/skills"
    if claude_skills.exists():
        for claude_path in sorted(claude_skills.glob("*/SKILL.md")):
            name = claude_path.parent.name
            new_content = claude_path.read_text(encoding="utf-8")
            diff_or_write(github_skills / name / "SKILL.md", new_content, write, changed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Applique les changements (défaut : affiche les diffs)")
    args = parser.parse_args()

    changed: list[str] = []
    process_module(ROOT / "template", args.write, changed)
    for example_dir in sorted((ROOT / "examples").iterdir()):
        if example_dir.is_dir():
            process_module(example_dir, args.write, changed)

    if not changed:
        print("✅ .github/ est déjà à jour vis-à-vis de .claude/.")
        return 0

    verb = "Modifié(s)" if args.write else "À modifier (relancer avec --write pour appliquer)"
    print(f"\n{verb} : {len(changed)} fichier(s)")
    for c in changed:
        print(f"  - {c}")
    return 0 if args.write else 1


if __name__ == "__main__":
    sys.exit(main())
