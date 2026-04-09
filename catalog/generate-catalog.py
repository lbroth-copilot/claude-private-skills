#!/usr/bin/env python3
"""Generate skill catalog JSON from SKILL.md frontmatter."""

import json
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from a SKILL.md file (no PyYAML dependency)."""
    text = filepath.read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    metadata = {}
    current_key = None
    in_metadata = False

    for line in match.group(1).splitlines():
        # Skip empty lines
        if not line.strip():
            continue

        # Top-level metadata block
        if line == "metadata:":
            in_metadata = True
            continue

        if in_metadata:
            if line.startswith("    "):
                # Nested under metadata
                m = re.match(r"    (\w[\w-]*):\s*(.*)", line)
                if m:
                    key, val = m.group(1), m.group(2).strip()
                    metadata[key] = parse_value(val)
                continue
            elif line.startswith("  ") and not line.startswith("    "):
                m = re.match(r"  (\w[\w-]*):\s*(.*)", line)
                if m:
                    key, val = m.group(1), m.group(2).strip()
                    metadata[key] = parse_value(val)
                continue
            else:
                in_metadata = False

        # Multiline value continuation
        if line.startswith("  ") and current_key and not re.match(r"  \w[\w-]*:", line):
            frontmatter[current_key] += " " + line.strip()
            continue

        # Top-level key: value
        m = re.match(r"(\w[\w-]*):\s*(.*)", line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip()
            if val == ">":
                frontmatter[current_key] = ""
            else:
                frontmatter[current_key] = parse_value(val)

    if metadata:
        frontmatter["metadata"] = metadata

    # Clean up multiline descriptions
    if "description" in frontmatter and isinstance(frontmatter["description"], str):
        frontmatter["description"] = re.sub(r"\s+", " ", frontmatter["description"]).strip()

    return frontmatter


def parse_value(val: str):
    """Parse a YAML scalar value."""
    if val.startswith("[") and val.endswith("]"):
        items = val[1:-1].split(",")
        return [item.strip().strip("'\"") for item in items if item.strip()]
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    try:
        return int(val)
    except ValueError:
        pass
    return val.strip("'\"") if val else val


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    plugins_dir = root / "plugins"
    catalog_dir = root / "catalog"
    catalog_dir.mkdir(exist_ok=True)

    skills = []

    for plugin_dir in sorted(plugins_dir.iterdir()):
        if not plugin_dir.is_dir():
            continue
        plugin_name = plugin_dir.name
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            continue

        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue

            frontmatter = parse_frontmatter(skill_file)
            if not frontmatter:
                continue

            entry = {
                "name": frontmatter.get("name", skill_dir.name),
                "plugin": plugin_name,
                "description": frontmatter.get("description", ""),
                "version": frontmatter.get("version", "0.0.0"),
                "author": frontmatter.get("author", ""),
                "user-invocable": frontmatter.get("user-invocable", False),
            }

            if "metadata" in frontmatter:
                entry["metadata"] = frontmatter["metadata"]

            skills.append(entry)

    catalog = {"generated": True, "skills": skills, "count": len(skills)}

    output = catalog_dir / "skills-catalog.json"
    output.write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"Generated catalog with {len(skills)} skill(s)")


if __name__ == "__main__":
    main()
