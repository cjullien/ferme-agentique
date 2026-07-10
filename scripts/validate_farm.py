#!/usr/bin/env python3
"""Validation de la ferme agentic.

Vérifie les classes de bugs déjà rencontrées dans ce dépôt :
- un `.claude/agents/*.md` qui utilise des noms d'outils Copilot au lieu des
  noms Claude Code (le bug corrigé sur 13 agents du socle) ;
- un `.github/agents/*.agent.md` qui utilise des noms d'outils Claude Code
  au lieu des noms Copilot (le même bug, dans l'autre sens) ;
- une désynchronisation entre `.claude/` et `.github/` : agent ou skill
  présent d'un côté et absent de l'autre, ou corps de texte différent
  (le frontmatter `tools:` a le droit de différer, pas le reste) ;
- un `settings.json` qui n'est pas un JSON valide ;
- un corps de fichier `.claude/` (pas seulement le frontmatter `tools:`)
  qui contient de la syntaxe Copilot (noms d'outils ou `agent_type:`) —
  le bug trouvé sur 25/26 skills de km-toolkit (FERME-12), non détecté
  par le check de frontmatter seul ;
- un `subagent_type:` qui ne correspond à aucun agent réellement présent
  dans le dépôt (socle ou un module `examples/`) — référence cassée.

Usage :
    python3 scripts/validate_farm.py [--verbose]

Sort avec un code non nul si au moins une erreur est détectée. Les
avertissements n'affectent pas le code de sortie.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Noms d'outils Copilot qui n'ont pas d'équivalent Claude Code : leur
# présence dans un frontmatter `tools:` signale un fichier copié tel quel
# depuis la version Copilot sans traduction.
COPILOT_TOOL_MARKERS = {
    "read_file", "create_file", "replace_string_in_file", "insert_edit_into_file",
    "run_in_terminal", "get_terminal_output", "list_directory", "file_search",
    "grep_search", "get_errors",
}

# Noms d'outils Claude Code qui n'ont pas d'équivalent Copilot direct : leur
# présence dans un `.agent.md` Copilot signale l'erreur inverse.
CLAUDE_TOOL_MARKERS = {"Read", "Write", "Edit", "Bash", "Grep", "Glob"}

# Fichiers .claude/ qui documentent intentionnellement les deux syntaxes
# (Copilot ET Claude Code) côte à côte pour un usage cross-outil — pas un
# bug de fichier copié sans traduction. Chemin relatif à ROOT.
INTENTIONAL_DUAL_SYNTAX_FILES = {
    "template/.claude/skills/audit-360/SKILL.md",
}

SUBAGENT_TYPE_RE = re.compile(r"subagent_type:\s*[\"']?([a-zA-Z0-9_-]+)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Retourne (frontmatter dict, corps) pour un fichier markdown avec en-tête ---."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw, body = parts[1], parts[2]
    fm: dict[str, str] = {}
    for line in fm_raw.strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body.lstrip("\n")


def check_tools_frontmatter(path: Path, report: Report, expect: str) -> None:
    text = path.read_text(encoding="utf-8")
    fm, _ = split_frontmatter(text)
    tools = fm.get("tools", "")
    if not tools:
        return
    tokens = {t.strip().strip("[]") for t in tools.replace("[", "").replace("]", "").split(",")}
    if expect == "claude":
        leaked = tokens & COPILOT_TOOL_MARKERS
        if leaked:
            report.error(
                f"{path.relative_to(ROOT)}: frontmatter `tools:` contient des noms "
                f"d'outils Copilot non traduits : {sorted(leaked)}"
            )
    elif expect == "copilot":
        leaked = tokens & CLAUDE_TOOL_MARKERS
        if leaked:
            report.error(
                f"{path.relative_to(ROOT)}: frontmatter `tools:` contient des noms "
                f"d'outils Claude Code au lieu des noms Copilot : {sorted(leaked)}"
            )


def compare_agent_mirrors(claude_dir: Path, github_dir: Path, report: Report) -> None:
    if not claude_dir.exists() or not github_dir.exists():
        return
    claude_agents = {p.stem: p for p in claude_dir.glob("*.md")}
    github_agents = {p.name.removesuffix(".agent.md"): p for p in github_dir.glob("*.agent.md")}

    for name, path in claude_agents.items():
        check_tools_frontmatter(path, report, expect="claude")
    for name, path in github_agents.items():
        check_tools_frontmatter(path, report, expect="copilot")

    for name in claude_agents.keys() - github_agents.keys():
        report.warn(f"{claude_agents[name].relative_to(ROOT)}: aucun miroir .github/agents/{name}.agent.md")
    for name in github_agents.keys() - claude_agents.keys():
        report.warn(f"{github_agents[name].relative_to(ROOT)}: aucun miroir .claude/agents/{name}.md")

    for name in claude_agents.keys() & github_agents.keys():
        _, claude_body = split_frontmatter(claude_agents[name].read_text(encoding="utf-8"))
        _, github_body = split_frontmatter(github_agents[name].read_text(encoding="utf-8"))
        if claude_body.strip() != github_body.strip():
            report.error(
                f"{claude_agents[name].relative_to(ROOT)} et "
                f"{github_agents[name].relative_to(ROOT)} : corps différents "
                f"(seul le frontmatter `tools:` doit différer entre miroirs)"
            )


def compare_skill_mirrors(claude_dir: Path, github_dir: Path, report: Report) -> None:
    if not claude_dir.exists() or not github_dir.exists():
        return
    claude_skills = {p.parent.name: p for p in claude_dir.glob("*/SKILL.md")}
    github_skills = {p.parent.name: p for p in github_dir.glob("*/SKILL.md")}

    for name in claude_skills.keys() - github_skills.keys():
        report.warn(f"{claude_skills[name].relative_to(ROOT)}: aucun miroir .github/skills/{name}/SKILL.md")
    for name in github_skills.keys() - claude_skills.keys():
        report.warn(f"{github_skills[name].relative_to(ROOT)}: aucun miroir .claude/skills/{name}/SKILL.md")

    for name in claude_skills.keys() & github_skills.keys():
        claude_text = claude_skills[name].read_text(encoding="utf-8")
        github_text = github_skills[name].read_text(encoding="utf-8")
        if claude_text != github_text:
            report.error(
                f"{claude_skills[name].relative_to(ROOT)} et "
                f"{github_skills[name].relative_to(ROOT)} : contenus différents "
                f"(un SKILL.md doit être identique dans les deux miroirs)"
            )


def check_module_mirror_symmetry(module_dir: Path, report: Report) -> None:
    """Un module qui n'a qu'une des deux versions (.claude/ ou .github/) casse la
    promesse « deux versions miroir » du README — cas réel : examples/km-toolkit
    n'a jamais eu de version .claude/, silencieusement ignoré par les checks
    par-agent ci-dessus puisqu'ils ne s'exécutent que si les deux dossiers existent.
    """
    has_claude = (module_dir / ".claude").exists()
    has_github = (module_dir / ".github").exists()
    has_flat_content = (module_dir / "agents").exists() or (module_dir / "skills").exists()

    if has_claude and not has_github:
        report.error(f"{module_dir.relative_to(ROOT)}: a une version .claude/ mais aucune .github/")
    elif has_github and not has_claude:
        report.error(
            f"{module_dir.relative_to(ROOT)}: a une version .github/ mais aucune .claude/ "
            f"(le README annonce deux versions miroir pour chaque module — documenter l'exception ou combler l'écart)"
        )
    elif has_flat_content and not has_claude and not has_github:
        report.error(
            f"{module_dir.relative_to(ROOT)}: agents/skills à plat, sans wrapper .claude/ ni .github/ "
            f"(module Copilot-only non migré — utiliser import_copilot_module.py ou ajouter les deux miroirs)"
        )


def check_copilot_leaks_in_claude_body(report: Report) -> None:
    """Cherche des noms d'outils Copilot ou de la syntaxe `agent_type:` dans le
    CORPS (pas juste le frontmatter `tools:`) des fichiers `.claude/`. C'est la
    classe de bug qui a affecté 25/26 skills de km-toolkit (FERME-12) : le
    frontmatter était correct mais le corps invoquait encore la syntaxe Copilot,
    invisible pour `check_tools_frontmatter`.
    """
    marker_re = re.compile(
        r"\b(" + "|".join(re.escape(m) for m in COPILOT_TOOL_MARKERS) + r")\b"
    )
    agent_type_re = re.compile(r"\bagent_type\s*[:=]")

    paths = list(ROOT.glob("template/.claude/agents/*.md"))
    paths += list(ROOT.glob("template/.claude/skills/*/SKILL.md"))
    for example_dir in sorted((ROOT / "examples").iterdir()):
        if not example_dir.is_dir():
            continue
        paths += list(example_dir.glob(".claude/agents/*.md"))
        paths += list(example_dir.glob(".claude/skills/*/SKILL.md"))

    for path in paths:
        rel = str(path.relative_to(ROOT))
        if rel in INTENTIONAL_DUAL_SYNTAX_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        _, body = split_frontmatter(text)
        tool_hits = sorted(set(marker_re.findall(body)))
        has_agent_type = bool(agent_type_re.search(body))
        if tool_hits or has_agent_type:
            details = list(tool_hits)
            if has_agent_type:
                details.append("agent_type:")
            report.error(
                f"{rel}: corps de fichier contient de la syntaxe Copilot non "
                f"traduite : {details}"
            )


def check_subagent_type_references(report: Report) -> None:
    """Vérifie que chaque `subagent_type:` cité dans un skill/agent correspond à
    un agent réellement présent quelque part dans le dépôt (socle ou un module
    `examples/`) — les modules peuvent référencer un agent conditionnel d'un
    autre module (cf. `audit-360`, `review`), donc la recherche est repo-wide,
    pas limitée au module courant.
    """
    all_agent_names: set[str] = {p.stem for p in ROOT.glob("template/.claude/agents/*.md")}
    for example_dir in (ROOT / "examples").iterdir():
        if example_dir.is_dir():
            all_agent_names |= {p.stem for p in example_dir.glob(".claude/agents/*.md")}

    paths = list(ROOT.glob("template/.claude/skills/*/SKILL.md"))
    paths += list(ROOT.glob("template/.claude/agents/*.md"))
    for example_dir in sorted((ROOT / "examples").iterdir()):
        if not example_dir.is_dir():
            continue
        paths += list(example_dir.glob(".claude/skills/*/SKILL.md"))
        paths += list(example_dir.glob(".claude/agents/*.md"))

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for match in SUBAGENT_TYPE_RE.finditer(text):
            name = match.group(1)
            if name not in all_agent_names:
                report.error(
                    f"{path.relative_to(ROOT)}: `subagent_type: {name}` ne correspond "
                    f"à aucun agent existant (socle ou examples/)"
                )


def check_settings_json(report: Report) -> None:
    for path in ROOT.rglob("settings*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(f"{path.relative_to(ROOT)}: JSON invalide ({exc})")


def check_catalog_consistency(report: Report) -> None:
    catalog = ROOT / "catalog.md"
    if not catalog.exists():
        return
    catalog_text = catalog.read_text(encoding="utf-8")

    template_agents = {p.stem for p in (ROOT / "template/.claude/agents").glob("*.md")}
    for name in template_agents:
        if f"`{name}`" not in catalog_text:
            report.warn(f"catalog.md : l'agent socle `{name}` n'est mentionné nulle part")

    for example_dir in sorted((ROOT / "examples").iterdir()):
        agents_dir = example_dir / ".claude/agents"
        if not agents_dir.exists():
            continue
        module_name = example_dir.name
        for agent_path in agents_dir.glob("*.md"):
            name = agent_path.stem
            if f"`{name}`" not in catalog_text and module_name not in catalog_text:
                report.warn(
                    f"catalog.md : l'agent `{name}` du module {module_name} "
                    f"n'est mentionné nulle part (ni l'agent ni le module)"
                )


def main() -> int:
    report = Report()

    compare_agent_mirrors(ROOT / "template/.claude/agents", ROOT / "template/.github/agents", report)
    compare_skill_mirrors(ROOT / "template/.claude/skills", ROOT / "template/.github/skills", report)

    for example_dir in sorted((ROOT / "examples").iterdir()):
        if not example_dir.is_dir():
            continue
        check_module_mirror_symmetry(example_dir, report)
        compare_agent_mirrors(example_dir / ".claude/agents", example_dir / ".github/agents", report)
        compare_skill_mirrors(example_dir / ".claude/skills", example_dir / ".github/skills", report)

    check_settings_json(report)
    check_catalog_consistency(report)
    check_copilot_leaks_in_claude_body(report)
    check_subagent_type_references(report)

    if report.warnings:
        print(f"⚠️  {len(report.warnings)} avertissement(s) :")
        for w in report.warnings:
            print(f"  - {w}")
        print()

    if report.errors:
        print(f"❌ {len(report.errors)} erreur(s) :")
        for e in report.errors:
            print(f"  - {e}")
        return 1

    print("✅ Aucune erreur détectée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
