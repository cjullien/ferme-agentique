#!/usr/bin/env python3
"""Convertit un module « Copilot uniquement » (agents/skills à plat) en module
à deux versions miroir (`.claude/` + `.github/`), comme les autres modules
`examples/`.

Cas d'usage : `examples/km-toolkit` a été extrait d'un projet Copilot et
n'a jamais eu de version Claude Code — juste `agents/*.agent.md` et
`skills/*/SKILL.md` à plat, destinés à être copiés tels quels dans le
`.github/` d'un projet cible (voir son `INSTALL.md` d'origine).

Ce script :
1. déplace `agents/` et `skills/` vers `.github/agents/` et `.github/skills/`
   (contenu Copilot inchangé) ;
2. génère `.claude/agents/*.md` en traduisant le frontmatter `tools:` de la
   syntaxe Copilot vers les noms Claude Code, corps copié à l'identique ;
3. copie `skills/` vers `.claude/skills/` (contenu strictement identique,
   comme pour tous les autres modules de la ferme).

Usage :
    python3 scripts/import_copilot_module.py examples/km-toolkit [--write]

Sans `--write`, affiche seulement ce qui serait fait.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

COPILOT_TO_CLAUDE = {
    "read_file": "Read",
    "create_file": "Write",
    "replace_string_in_file": "Edit",
    "insert_edit_into_file": "Edit",
    "run_in_terminal": "Bash",
    "get_terminal_output": "Bash",
    "list_directory": "Glob",
    "file_search": "Glob",
    "grep_search": "Grep",
    # get_errors : diagnostics IDE Copilot, aucun équivalent Claude Code — abandonné.
}
CANONICAL_ORDER = ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]


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


def translate_tools(copilot_tools: str) -> str:
    tokens = [t.strip().strip("[]") for t in copilot_tools.replace("[", "").replace("]", "").split(",") if t.strip()]
    claude_tools = {COPILOT_TO_CLAUDE[t] for t in tokens if t in COPILOT_TO_CLAUDE}
    return ", ".join(t for t in CANONICAL_ORDER if t in claude_tools)


def convert_agent(github_path: Path) -> str:
    fm_lines, fm, body = split_frontmatter(github_path.read_text(encoding="utf-8"))
    out_lines = ["---"]
    for line in fm_lines:
        key = line.split(":", 1)[0].strip()
        if key == "tools" and "tools" in fm:
            out_lines.append(f"tools: {translate_tools(fm['tools'])}")
        else:
            out_lines.append(line)
    out_lines.append("---")
    return "\n".join(out_lines) + "\n\n" + body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module", help="Chemin du module, ex: examples/km-toolkit")
    parser.add_argument("--write", action="store_true", help="Applique (défaut : affiche seulement)")
    args = parser.parse_args()

    module_dir = (ROOT / args.module).resolve()
    flat_agents = module_dir / "agents"
    flat_skills = module_dir / "skills"
    if not flat_agents.exists() and not flat_skills.exists():
        print(f"Rien à convertir : ni {flat_agents} ni {flat_skills} n'existent.")
        return 1

    github_agents = module_dir / ".github/agents"
    github_skills = module_dir / ".github/skills"
    claude_agents = module_dir / ".claude/agents"
    claude_skills = module_dir / ".claude/skills"

    actions: list[str] = []
    if flat_agents.exists():
        actions.append(f"déplacer {flat_agents.relative_to(ROOT)} -> {github_agents.relative_to(ROOT)}")
    if flat_skills.exists():
        actions.append(f"déplacer {flat_skills.relative_to(ROOT)} -> {github_skills.relative_to(ROOT)}")
    actions.append(f"générer {claude_agents.relative_to(ROOT)}/*.md depuis {github_agents.relative_to(ROOT)}")
    actions.append(f"copier {github_skills.relative_to(ROOT)} -> {claude_skills.relative_to(ROOT)}")

    print("Actions prévues :")
    for a in actions:
        print(f"  - {a}")

    if not args.write:
        print("\n(relancer avec --write pour appliquer)")
        return 0

    if flat_agents.exists():
        github_agents.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(flat_agents), str(github_agents))
    if flat_skills.exists():
        github_skills.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(flat_skills), str(github_skills))

    claude_agents.mkdir(parents=True, exist_ok=True)
    for github_path in sorted(github_agents.glob("*.agent.md")):
        name = github_path.name.removesuffix(".agent.md")
        (claude_agents / f"{name}.md").write_text(convert_agent(github_path), encoding="utf-8")

    if claude_skills.exists():
        shutil.rmtree(claude_skills)
    shutil.copytree(github_skills, claude_skills)

    print(f"\n✅ {module_dir.relative_to(ROOT)} converti en module à deux versions miroir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
