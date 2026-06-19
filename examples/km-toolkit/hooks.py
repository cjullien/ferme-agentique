"""Hooks MkDocs pour la KB CobolCraft.

Trois comportements :

1. Réécrit, uniquement pour les pages de `specs/`, les liens relatifs qui sortent
   du `docs_dir` (ex: `../../README.md`) en URLs GitHub absolues, afin que le
   build passe en --strict sans modifier les fichiers sources de `docs/specs/`.

2. Override structuré universel : pour TOUTE page `X.md`, si `X.override.yml`
   existe, ses corrections sont appliquées au build (titre, intro, sections,
   remplacements ciblés, notes). Permet de corriger un champ faux sans toucher
   le `.md` généré.

3. Override libre universel : pour TOUTE page `X.md`, si `X.override.md` existe,
   son contenu Markdown est injecté en bas de page dans un encadré.

Les fichiers `*.override.*` sont écrits par l'humain et ne sont JAMAIS touchés par
les agents. Le `.md` généré, lui, n'est jamais touché par l'humain. Les deux
coexistent : c'est le mécanisme « human in the loop ». Application 100 % mécanique
au build → fonctionne pour toute page, quel que soit l'agent qui l'a générée.
"""
from __future__ import annotations

import os
import re

import yaml  # fourni par mkdocs (dépendance transitive)

# Base GitHub pour réécrire les liens relatifs sortants des pages `specs/`.
# Dérivée de `repo_url` dans mkdocs.yml (voir _github_base) ; surchargeable via
# la variable d'environnement KB_GITHUB_BASE. Le fallback ne sert que si aucune
# des deux sources n'est disponible.
GITHUB_BASE_FALLBACK = os.environ.get(
    "KB_GITHUB_BASE", "https://github.com/OWNER/REPO/blob/main"
)


def _github_base(config) -> str:
    """Construit la base GitHub `.../blob/<branch>` depuis `repo_url` de mkdocs.yml."""
    repo_url = (config or {}).get("repo_url") if config else None
    if repo_url:
        return repo_url.rstrip("/") + "/blob/main"
    return GITHUB_BASE_FALLBACK

# Capture les liens markdown [text](path) ou [text](path "title")
LINK_RE = re.compile(r"(\[[^\]]+\]\()(\.\./\.\./)([^)\s]+)([^)]*\))")

MARK = "*✏️ Corrigé manuellement*"


def _rewrite_specs_links(markdown: str, src: str, github_base: str) -> str:
    if not src.startswith("specs/"):
        return markdown

    def repl(match):
        prefix, _, target, suffix = match.groups()
        return f"{prefix}{github_base}/{target}{suffix}"

    return LINK_RE.sub(repl, markdown)


def _replace_section(markdown: str, name: str, new_body: str) -> tuple[str, bool]:
    """Remplace le corps sous un titre `## name` (jusqu'au prochain ## ou ---)."""
    pattern = re.compile(
        rf"(## {re.escape(name)}\n\n)(.*?)(?=\n## |\n---|\Z)", re.DOTALL
    )
    if not pattern.search(markdown):
        return markdown, False
    repl = rf"\g<1>{new_body.strip()}\n\n{MARK}\n"
    return pattern.sub(repl, markdown, count=1), True


def _apply_yaml_override(markdown: str, override_path: str) -> str:
    with open(override_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    name = os.path.basename(override_path)
    applied: list[str] = []

    # title : remplace le H1
    if data.get("title"):
        markdown = re.sub(r"^# .*$", f"# {data['title']}", markdown, count=1, flags=re.MULTILINE)
        applied.append("titre")

    # intro : inséré juste après le H1
    if data.get("intro"):
        markdown = re.sub(
            r"(^# .*$)", rf"\1\n\n{data['intro'].strip()}\n\n{MARK}", markdown, count=1, flags=re.MULTILINE
        )
        applied.append("intro")

    # sections : remplace le corps sous un titre ## donné
    for sec, body in (data.get("sections") or {}).items():
        markdown, ok = _replace_section(markdown, sec, str(body))
        if ok:
            applied.append(f"section « {sec} »")

    # replace : corrections ciblées find -> with
    for item in (data.get("replace") or []):
        find, with_ = item.get("find"), item.get("with", "")
        if find and find in markdown:
            markdown = markdown.replace(find, with_)
            applied.append(f"correction « {find[:30]} »")

    # notes : ajouté en bas dans une admonition
    notes = data.get("notes")
    notes_block = ""
    if notes:
        applied.append("notes")
        indented = "\n".join(("    " + l) if l.strip() else "" for l in notes.strip().splitlines())
        notes_block = (
            '\n\n!!! note "✏️ Notes / enrichissements manuels"\n'
            f"    Source : `{name}`\n\n{indented}\n"
        )

    # Bandeau récapitulatif en tête (après le H1)
    if applied:
        banner = (
            '\n\n!!! warning "✏️ Corrections manuelles appliquées"\n'
            f"    Champs surchargés via `{name}` : {', '.join(applied)}.\n"
            "    Le contenu généré brut reste consultable dans l'historique git.\n"
        )
        markdown = re.sub(r"(^# .*$)", rf"\1{banner}", markdown, count=1, flags=re.MULTILINE)

    return markdown.rstrip() + notes_block


def _inject_md_override(markdown: str, override_path: str) -> str:
    with open(override_path, encoding="utf-8") as fh:
        content = fh.read().strip()
    name = os.path.basename(override_path)
    indented = "\n".join(("    " + l) if l.strip() else "" for l in content.splitlines())
    banner = (
        '\n\n!!! note "✏️ Corrections / enrichissements manuels"\n'
        f"    Contenu rédigé par l'équipe dans `{name}` — non généré, "
        "préservé à chaque régénération.\n\n"
        f"{indented}\n"
    )
    return markdown.rstrip() + banner


def _apply_overrides(markdown: str, src: str, docs_dir: str) -> str:
    if src.endswith(".override.md"):
        return markdown
    base = src[:-3]  # retire ".md"

    yml = os.path.join(docs_dir, base + ".override.yml")
    if os.path.isfile(yml):
        markdown = _apply_yaml_override(markdown, yml)

    md = os.path.join(docs_dir, base + ".override.md")
    if os.path.isfile(md):
        markdown = _inject_md_override(markdown, md)

    return markdown


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_path.replace("\\", "/")
    markdown = _rewrite_specs_links(markdown, src, _github_base(config))
    markdown = _apply_overrides(markdown, src, config["docs_dir"])
    return markdown
