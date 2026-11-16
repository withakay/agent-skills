#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml>=6,<7"]
# ///
"""
OpenAI YAML Generator - Creates agents/openai.yaml for a skill folder.

Usage:
    generate_openai_yaml.py <skill_dir> [--name <skill_name>] [--interface key=value]
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yaml

ACRONYMS = {
    "GH",
    "MCP",
    "API",
    "CI",
    "CLI",
    "LLM",
    "PDF",
    "PR",
    "UI",
    "URL",
    "SQL",
    "TDD",
}

BRANDS = {
    "openai": "OpenAI",
    "openapi": "OpenAPI",
    "github": "GitHub",
    "pagerduty": "PagerDuty",
    "datadog": "DataDog",
    "sqlite": "SQLite",
    "fastapi": "FastAPI",
}

SMALL_WORDS = {"and", "or", "to", "up", "with"}

ALLOWED_INTERFACE_KEYS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}


def yaml_quote(value):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def format_display_name(skill_name):
    words = [word for word in skill_name.split("-") if word]
    formatted = []
    for index, word in enumerate(words):
        lower = word.lower()
        upper = word.upper()
        if upper in ACRONYMS:
            formatted.append(upper)
            continue
        if lower in BRANDS:
            formatted.append(BRANDS[lower])
            continue
        if index > 0 and lower in SMALL_WORDS:
            formatted.append(lower)
            continue
        formatted.append(word.capitalize())
    return " ".join(formatted)


def generate_short_description(display_name):
    candidates = (
        f"Help with {display_name} tasks",
        f"Help with {display_name} tasks and workflows",
        f"Help with {display_name}",
        f"{display_name} helper",
        f"{display_name} tools",
    )
    for description in candidates:
        if 25 <= len(description) <= 64:
            return description
    return f"{display_name[:57].rstrip()} helper"


def read_frontmatter(skill_dir):
    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_dir}")
        return None
    content = skill_md.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print("[ERROR] Invalid SKILL.md frontmatter format.")
        return None
    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        print(f"[ERROR] Invalid YAML frontmatter: {exc}")
        return None
    if not isinstance(frontmatter, dict):
        print("[ERROR] Frontmatter must be a YAML dictionary.")
        return None
    name = frontmatter.get("name", "")
    if not isinstance(name, str) or not name.strip():
        print("[ERROR] Frontmatter 'name' is missing or invalid.")
        return None
    return frontmatter


def read_frontmatter_name(skill_dir):
    frontmatter = read_frontmatter(skill_dir)
    return frontmatter["name"].strip() if frontmatter else None


def parse_interface_overrides(raw_overrides):
    """Parse raw key=value strings into an overrides dict.

    Raises ValueError with a human-readable message on the first malformed,
    empty-key, or unknown-key override.
    """
    overrides = {}
    for item in raw_overrides:
        if "=" not in item:
            raise ValueError(f"Invalid interface override '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"Invalid interface override '{item}'. Key is empty.")
        if key not in ALLOWED_INTERFACE_KEYS:
            allowed = ", ".join(sorted(ALLOWED_INTERFACE_KEYS))
            raise ValueError(f"Unknown interface field '{key}'. Allowed: {allowed}")
        overrides[key] = value
    return overrides


def derive_short_description(description, display_name):
    """Condense a SKILL.md description into a 25-64 character phrase."""
    if isinstance(description, str) and description.strip():
        text = description.strip()
        for prefix in (
            "Use only when the user asks to",
            "Use when the user asks to",
            "Use when the user asks for",
            "Use only when",
            "Use only to",
            "Use when",
            "Use for",
            "Use to",
            "Use",
        ):
            if text.lower().startswith(prefix.lower()):
                text = text[len(prefix) :].strip()
                break
        text = text.split(". ")[0].split(";")[0].split(" - ")[0].strip().rstrip(".")
        if text:
            text = text[0].upper() + text[1:]
            if len(text) > 64:
                text = text[:64].rsplit(" ", 1)[0].rstrip(",")
            if 25 <= len(text) <= 64:
                return text
    return generate_short_description(display_name)


def render_openai_yaml(
    skill_name, raw_overrides, description=None, allow_implicit=True
):
    """Parse interface overrides and render the full agents/openai.yaml text.

    Raises ValueError if overrides are invalid or short_description is out
    of the allowed length range.
    """
    overrides = parse_interface_overrides(raw_overrides)

    display_name = overrides.get("display_name") or format_display_name(skill_name)
    short_description = overrides.get("short_description") or derive_short_description(
        description, display_name
    )

    if not (25 <= len(short_description) <= 64):
        raise ValueError(
            f"short_description must be 25-64 characters (got {len(short_description)})."
        )

    interface_lines = [
        "interface:",
        f"  display_name: {yaml_quote(display_name)}",
        f"  short_description: {yaml_quote(short_description)}",
    ]

    for key, value in overrides.items():
        if key not in ("display_name", "short_description"):
            interface_lines.append(f"  {key}: {yaml_quote(value)}")

    interface_lines.extend(
        (
            "policy:",
            f"  allow_implicit_invocation: {'true' if allow_implicit else 'false'}",
        )
    )

    return "\n".join(interface_lines) + "\n"


def write_openai_yaml(
    skill_dir, skill_name, raw_overrides, description=None, allow_implicit=True
):
    """Render openai.yaml content and write it to skill_dir/agents/openai.yaml."""
    try:
        content = render_openai_yaml(
            skill_name, raw_overrides, description, allow_implicit
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return None

    agents_dir = Path(skill_dir) / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    output_path = agents_dir / "openai.yaml"
    with tempfile.NamedTemporaryFile(
        "w", dir=agents_dir, prefix=".openai-", delete=False
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)
    try:
        temporary_path.replace(output_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    print("[OK] Created agents/openai.yaml")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Create agents/openai.yaml for a skill directory.",
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--name",
        help="Skill name override (defaults to SKILL.md frontmatter)",
    )
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Interface override in key=value format (repeatable)",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"[ERROR] Skill directory not found: {skill_dir}")
        sys.exit(1)
    if not skill_dir.is_dir():
        print(f"[ERROR] Path is not a directory: {skill_dir}")
        sys.exit(1)

    frontmatter = read_frontmatter(skill_dir) or {}
    skill_name = args.name or (frontmatter.get("name") or "").strip()
    if not skill_name:
        sys.exit(1)

    result = write_openai_yaml(
        skill_dir,
        skill_name,
        args.interface,
        description=frontmatter.get("description"),
        allow_implicit=not frontmatter.get("disable-model-invocation", False),
    )
    if result:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
