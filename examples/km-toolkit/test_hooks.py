"""Tests minimaux du moteur d'override `hooks.py`.

But : garde-fou de non-régression sur la logique regex (réécriture des liens
`specs/`, override YAML structuré, override Markdown libre). Sans cela, une
évolution de format pourrait silencieusement cesser d'appliquer les overrides.

Lancer :
    python3 -m pytest km-toolkit/test_hooks.py        # si pytest dispo
    python3 km-toolkit/test_hooks.py                  # exécution directe

PyYAML est requis (fourni par MkDocs). Les tests qui en dépendent sont ignorés
s'il est absent de l'environnement courant.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))

try:
    import yaml  # noqa: F401
    _HAS_YAML = True
except ModuleNotFoundError:
    _HAS_YAML = False


def _load_hooks():
    if not _HAS_YAML and "yaml" not in sys.modules:
        import types

        sys.modules["yaml"] = types.SimpleNamespace(safe_load=lambda *a, **k: {})
    spec = importlib.util.spec_from_file_location("hooks", os.path.join(_HERE, "hooks.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# _github_base
# ---------------------------------------------------------------------------

def test_github_base_from_repo_url():
    hooks = _load_hooks()
    assert hooks._github_base({"repo_url": "https://github.com/foo/bar"}) == (
        "https://github.com/foo/bar/blob/main"
    )


def test_github_base_strips_trailing_slash():
    hooks = _load_hooks()
    assert hooks._github_base({"repo_url": "https://github.com/foo/bar/"}) == (
        "https://github.com/foo/bar/blob/main"
    )


def test_github_base_fallback_when_missing():
    hooks = _load_hooks()
    assert hooks._github_base({}) == "https://github.com/OWNER/REPO/blob/main"
    assert hooks._github_base(None) == "https://github.com/OWNER/REPO/blob/main"


def test_github_base_env_override(monkeypatch=None):
    os.environ["KB_GITHUB_BASE"] = "https://example.com/x/blob/main"
    try:
        hooks = _load_hooks()  # le fallback est lu à l'import du module
        assert hooks._github_base({}) == "https://example.com/x/blob/main"
    finally:
        del os.environ["KB_GITHUB_BASE"]


# ---------------------------------------------------------------------------
# _rewrite_specs_links
# ---------------------------------------------------------------------------

def test_rewrite_specs_links_only_on_specs_pages():
    hooks = _load_hooks()
    base = "https://github.com/foo/bar/blob/main"
    md = "[x](../../README.md)"
    assert hooks._rewrite_specs_links(md, "specs/foo.md", base) == (
        f"[x]({base}/README.md)"
    )
    # hors de specs/ : inchangé
    assert hooks._rewrite_specs_links(md, "concepts/foo.md", base) == md


# ---------------------------------------------------------------------------
# _apply_yaml_override / _inject_md_override / _apply_overrides
# ---------------------------------------------------------------------------

def test_yaml_override_applies_title_section_and_notes():
    if not _HAS_YAML:
        return  # ignoré si PyYAML absent
    hooks = _load_hooks()
    md = "# Ancien titre\n\n## Synthèse\n\nVieux corps.\n"
    with tempfile.TemporaryDirectory() as d:
        ov = os.path.join(d, "page.override.yml")
        with open(ov, "w", encoding="utf-8") as fh:
            fh.write(
                "title: Nouveau titre\n"
                "sections:\n"
                "  Synthèse: Corps corrigé.\n"
                "notes: Une note humaine.\n"
            )
        out = hooks._apply_yaml_override(md, ov)
    assert "# Nouveau titre" in out
    assert "Corps corrigé." in out
    assert "Vieux corps." not in out
    assert "Une note humaine." in out
    assert "Corrections manuelles appliquées" in out


def test_md_override_is_appended():
    hooks = _load_hooks()
    md = "# Page\n\nContenu généré.\n"
    with tempfile.TemporaryDirectory() as d:
        ov = os.path.join(d, "page.override.md")
        with open(ov, "w", encoding="utf-8") as fh:
            fh.write("Ajout rédigé par l'équipe.")
        out = hooks._inject_md_override(md, ov)
    assert "Contenu généré." in out
    assert "Ajout rédigé par l'équipe." in out


def test_apply_overrides_skips_override_md_pages():
    hooks = _load_hooks()
    md = "contenu"
    out = hooks._apply_overrides(md, "page.override.md", "/tmp")
    assert out == md  # une page *.override.md n'est jamais re-traitée


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL {name}: {exc}")
    print(f"\n{'OK' if failures == 0 else 'ÉCHEC'} — {failures} échec(s)")
    sys.exit(1 if failures else 0)
