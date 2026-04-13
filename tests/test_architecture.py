from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_ROOT = ROOT / "src" / "voice_tts" / "domain"
APPLICATION_ROOT = ROOT / "src" / "voice_tts" / "application"


def _collect_imports(folder: Path) -> set[str]:
    imports: set[str] = set()
    for path in folder.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
    return imports


def test_domain_has_no_framework_imports() -> None:
    imports = _collect_imports(DOMAIN_ROOT)
    forbidden_prefixes = ("fastapi", "pydantic", "pydantic_settings", "typer", "torch")
    offenders = sorted(
        imported
        for imported in imports
        if imported.startswith(forbidden_prefixes)
    )
    assert offenders == []


def test_application_does_not_import_infrastructure() -> None:
    imports = _collect_imports(APPLICATION_ROOT)
    offenders = sorted(
        imported
        for imported in imports
        if imported.startswith("voice_tts.infrastructure")
    )
    assert offenders == []

