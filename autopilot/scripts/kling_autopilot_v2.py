#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AGENT = ROOT / "autopilot" / "agents" / "kling_prompt_agent.md"
DEFAULT_SCHEMA = ROOT / "autopilot" / "schema" / "kling_scene_plan.schema.yaml"
DEFAULT_PLAN = ROOT / "episodes" / "season_01" / "episode_002" / "kling_scene_plan.yaml"


class AutopilotV2Error(RuntimeError):
    pass


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    try:
        agent_text = read_required(args.agent.resolve())
        schema = load_yaml(args.schema.resolve())
        plan = load_yaml(args.plan.resolve())

        validation_errors = validate_plan(plan, schema)
        if validation_errors:
            print("VALIDATION_FAILED", file=sys.stderr)
            for error in validation_errors:
                print(error, file=sys.stderr)
            return 2

        assets, missing_assets = resolve_assets(plan, root)
        if missing_assets:
            print("MISSING_ASSET", file=sys.stderr)
            for missing in missing_assets:
                print(missing, file=sys.stderr)
            return 3

        output_dir = root / str(plan["output"]["directory"]) / "prompts"
        output_dir.mkdir(parents=True, exist_ok=True)

        prompt_files = write_prompts(plan, assets, output_dir, agent_text)
        report = write_report(plan, assets, output_dir, prompt_files)

        print("KLING_PROMPTS_GENERATED")
        for path in prompt_files + [report]:
            print(path.relative_to(root).as_posix())
        return 0
    except AutopilotV2Error as exc:
        print(f"Autopilot v2 error: {exc}", file=sys.stderr)
        return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Kling-ready markdown prompts from a scene plan."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--agent", type=Path, default=DEFAULT_AGENT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    return parser.parse_args()


def read_required(path: Path) -> str:
    if not path.exists():
        raise AutopilotV2Error(f"required file not found: {path}")
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    text = read_required(path)
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
    except ModuleNotFoundError:
        loaded = parse_simple_yaml(text)
    if not isinstance(loaded, dict):
        raise AutopilotV2Error(f"YAML root must be a mapping: {path}")
    return loaded


def parse_simple_yaml(text: str) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        expanded = raw.expandtabs(2)
        indent = len(expanded) - len(expanded.lstrip(" "))
        lines.append((indent, expanded.strip()))

    root: dict[str, Any] = {}
    stack: list[dict[str, Any]] = [
        {"indent": -1, "container": root, "parent": None, "key": None}
    ]

    for indent, content in lines:
        while indent <= stack[-1]["indent"]:
            stack.pop()

        frame = stack[-1]
        parent = frame["container"]

        if content.startswith("- "):
            if not isinstance(parent, list):
                if isinstance(parent, dict) and not parent and frame["parent"] is not None:
                    replacement: list[Any] = []
                    replace_in_parent(frame, replacement)
                    frame["container"] = replacement
                    parent = replacement
                else:
                    raise AutopilotV2Error(f"invalid YAML list item: {content}")

            item_text = content[2:].strip()
            if not item_text:
                item: dict[str, Any] = {}
                parent.append(item)
                stack.append(
                    {
                        "indent": indent,
                        "container": item,
                        "parent": parent,
                        "key": len(parent) - 1,
                    }
                )
            elif looks_like_key_value(item_text):
                item = {}
                parent.append(item)
                key, value = split_key_value(item_text)
                if value == "":
                    item[key] = {}
                    stack.append(
                        {
                            "indent": indent,
                            "container": item[key],
                            "parent": item,
                            "key": key,
                        }
                    )
                else:
                    item[key] = parse_scalar(value)
                    stack.append(
                        {
                            "indent": indent,
                            "container": item,
                            "parent": parent,
                            "key": len(parent) - 1,
                        }
                    )
            else:
                parent.append(parse_scalar(item_text))
            continue

        if not isinstance(parent, dict):
            raise AutopilotV2Error(f"invalid YAML mapping item: {content}")

        key, value = split_key_value(content)
        if value == "":
            parent[key] = {}
            stack.append(
                {
                    "indent": indent,
                    "container": parent[key],
                    "parent": parent,
                    "key": key,
                }
            )
        else:
            parent[key] = parse_scalar(value)

    return root


def replace_in_parent(frame: dict[str, Any], value: Any) -> None:
    parent = frame["parent"]
    key = frame["key"]
    if isinstance(parent, dict):
        parent[key] = value
    elif isinstance(parent, list):
        parent[int(key)] = value
    else:
        raise AutopilotV2Error("invalid YAML parent")


def looks_like_key_value(text: str) -> bool:
    return find_mapping_colon(text) >= 0


def split_key_value(text: str) -> tuple[str, str]:
    index = find_mapping_colon(text)
    if index < 0:
        raise AutopilotV2Error(f"expected key: value, got: {text}")
    key = text[:index].strip()
    value = text[index + 1 :].strip()
    if not key:
        raise AutopilotV2Error(f"empty YAML key in: {text}")
    return key, value


def find_mapping_colon(text: str) -> int:
    quote: str | None = None
    escape = False
    for index, char in enumerate(text):
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == ":" and (index + 1 == len(text) or text[index + 1].isspace()):
            return index
    return -1


def parse_scalar(value: str) -> Any:
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    if lower in {"null", "none", "~"}:
        return None
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return ast.literal_eval(value)
    if value.startswith("[") and value.endswith("]"):
        return ast.literal_eval(value)
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def validate_plan(plan: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in schema.get("required_root_fields", []):
        if not has(plan, field):
            errors.append(f"{field}: missing required root field")

    if has(plan, "provider") and plan["provider"] not in schema.get("provider", {}).get(
        "allowed", []
    ):
        errors.append(
            f"provider: invalid value {plan['provider']!r}; "
            f"allowed: {schema.get('provider', {}).get('allowed', [])}"
        )

    episode = plan.get("episode")
    if not isinstance(episode, dict):
        errors.append("episode: must be a mapping")
    else:
        for field in schema.get("episode", {}).get("required", []):
            if not has(episode, field):
                errors.append(f"episode.{field}: missing required field")
            elif not isinstance(episode[field], str):
                errors.append(f"episode.{field}: expected string")

    scenes = plan.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes: must be a non-empty list")
    elif isinstance(scenes, list):
        for index, scene in enumerate(scenes):
            base = f"scenes[{index}]"
            if not isinstance(scene, dict):
                errors.append(f"{base}: must be a mapping")
                continue
            scene_id = str(scene.get("id", index))
            base = f"{base}.{scene_id}"
            for field in schema.get("scene", {}).get("required", []):
                if not has(scene, field):
                    errors.append(f"{base}.{field}: missing required field")
            validate_scene_fields(base, scene, schema.get("scene", {}).get("fields", {}), errors)

    output = plan.get("output")
    if not isinstance(output, dict):
        errors.append("output: must be a mapping")
    else:
        for field in schema.get("output", {}).get("required", []):
            if not has(output, field):
                errors.append(f"output.{field}: missing required field")
        if has(output, "directory") and not isinstance(output["directory"], str):
            errors.append("output.directory: expected string")

    return errors


def validate_scene_fields(
    base: str,
    scene: dict[str, Any],
    fields: dict[str, Any],
    errors: list[str],
) -> None:
    check_type(base, "id", scene.get("id"), "string", errors)
    check_type(base, "duration", scene.get("duration"), "number", errors)
    check_type(base, "environment", scene.get("environment"), "string", errors)
    check_type(base, "action", scene.get("action"), "string", errors)
    if has(scene, "mood"):
        check_type(base, "mood", scene.get("mood"), "string", errors)
    if has(scene, "negative_prompt"):
        check_type(base, "negative_prompt", scene.get("negative_prompt"), "string", errors)

    camera = scene.get("camera")
    if not isinstance(camera, dict):
        errors.append(f"{base}.camera: must be a mapping")
    else:
        check_type(f"{base}.camera", "shot", camera.get("shot"), "string", errors)
        check_type(
            f"{base}.camera", "movement", camera.get("movement"), "string", errors
        )

    references = scene.get("references")
    if not isinstance(references, dict):
        errors.append(f"{base}.references: must be a mapping")
    else:
        characters = references.get("characters")
        props = references.get("props")
        environment = references.get("environment")
        if not isinstance(characters, list):
            errors.append(f"{base}.references.characters: expected list")
        elif not all(isinstance(item, str) for item in characters):
            errors.append(f"{base}.references.characters: every item must be a string")
        if not isinstance(props, list):
            errors.append(f"{base}.references.props: expected list")
        elif not all(isinstance(item, str) for item in props):
            errors.append(f"{base}.references.props: every item must be a string")
        if not isinstance(environment, str):
            errors.append(f"{base}.references.environment: expected string")


def check_type(
    base: str,
    field: str,
    value: Any,
    expected: str,
    errors: list[str],
) -> None:
    if value is None:
        return
    if expected == "string" and not isinstance(value, str):
        errors.append(f"{base}.{field}: expected string")
    elif expected == "number" and not (
        isinstance(value, (int, float)) and not isinstance(value, bool)
    ):
        errors.append(f"{base}.{field}: expected number")


def has(obj: Any, key: str) -> bool:
    return isinstance(obj, dict) and key in obj and obj[key] is not None


def resolve_assets(
    plan: dict[str, Any], root: Path
) -> tuple[dict[str, dict[str, list[Path] | Path]], list[str]]:
    assets_root = (root / "assets").resolve()
    by_scene: dict[str, dict[str, list[Path] | Path]] = {}
    missing: list[str] = []

    for scene in plan["scenes"]:
        scene_id = str(scene["id"])
        references = scene["references"]
        characters: list[Path] = []
        props: list[Path] = []

        for raw in references.get("characters", []):
            path = resolve_asset_path(root, assets_root, raw, missing, scene_id, "character")
            if path:
                characters.append(path)

        environment = resolve_asset_path(
            root,
            assets_root,
            references.get("environment"),
            missing,
            scene_id,
            "environment",
        )

        for raw in references.get("props", []):
            path = resolve_asset_path(root, assets_root, raw, missing, scene_id, "prop")
            if path:
                props.append(path)

        if environment is not None:
            by_scene[scene_id] = {
                "characters": characters,
                "environment": environment,
                "props": props,
            }

    return by_scene, missing


def resolve_asset_path(
    root: Path,
    assets_root: Path,
    raw_value: Any,
    missing: list[str],
    scene_id: str,
    role: str,
) -> Path | None:
    if not isinstance(raw_value, str) or not raw_value.strip():
        missing.append(f"{scene_id}.{role}: empty asset path")
        return None

    raw = Path(raw_value)
    candidate = raw if raw.is_absolute() else root / raw
    resolved = candidate.resolve()

    try:
        resolved.relative_to(assets_root)
    except ValueError:
        missing.append(f"{scene_id}.{role}: {raw_value} (outside assets/)")
        return None

    if not resolved.exists():
        missing.append(f"{scene_id}.{role}: {raw_value}")
        return None

    return resolved


def write_prompts(
    plan: dict[str, Any],
    assets: dict[str, dict[str, list[Path] | Path]],
    output_dir: Path,
    agent_text: str,
) -> list[Path]:
    prompt_files: list[Path] = []
    for scene in plan["scenes"]:
        scene_id = str(scene["id"])
        path = output_dir / f"{scene_id}_kling_prompt.md"
        path.write_text(
            render_prompt(plan, scene, assets[scene_id], agent_text),
            encoding="utf-8",
        )
        prompt_files.append(path)
    return prompt_files


def render_prompt(
    plan: dict[str, Any],
    scene: dict[str, Any],
    scene_assets: dict[str, list[Path] | Path],
    agent_text: str,
) -> str:
    characters = scene_assets["characters"]
    props = scene_assets["props"]
    environment = scene_assets["environment"]
    assert isinstance(characters, list)
    assert isinstance(props, list)
    assert isinstance(environment, Path)

    subject = subject_from_assets(characters, props, scene)
    character_lines = format_paths(characters)
    prop_lines = format_paths(props)
    mood = scene.get("mood", "premium cinematic")
    negative = scene.get("negative_prompt", "")

    return "\n".join(
        [
            f"# Kling Prompt - {scene['id']}",
            "",
            f"Episode: {plan['episode']['id']} - {plan['episode']['title']}",
            f"Provider: {plan['provider']}",
            f"Duration: {scene['duration']} seconds",
            "",
            "Use the listed repository reference assets only. Maintain canonical character identity and outfit continuity.",
            "",
            "## Subject",
            subject,
            "",
            "## Action",
            str(scene["action"]),
            "",
            "## Environment",
            str(scene["environment"]),
            "",
            "## Reference Assets",
            "Characters:",
            character_lines,
            "",
            "Environment:",
            f"- {environment.relative_to(ROOT).as_posix()}",
            "",
            "Props:",
            prop_lines,
            "",
            "## Camera",
            f"Shot: {scene['camera']['shot']}",
            f"Motion: {scene['camera']['movement']}",
            "",
            "## Mood",
            str(mood),
            "",
            "## Kling Prompt",
            build_kling_prompt(scene, subject),
            "",
            "## Negative Prompt",
            build_negative_prompt(negative),
            "",
        ]
    )


def subject_from_assets(characters: list[Path], props: list[Path], scene: dict[str, Any]) -> str:
    names: list[str] = []
    for path in characters:
        text = path.as_posix()
        if "marco_rinaldi" in text:
            names.append("Marco Rinaldi")
        elif "/laura/" in text:
            names.append("Laura")
        else:
            names.append(path.parent.name.replace("_", " ").title())

    if names:
        unique_names = list(dict.fromkeys(names))
        return ", ".join(unique_names)

    if props:
        return "ShowroomFlow brand closing card using the provided brand assets"
    return str(scene["environment"])


def format_paths(paths: list[Path]) -> str:
    if not paths:
        return "- None"
    return "\n".join(f"- {path.relative_to(ROOT).as_posix()}" for path in paths)


def build_kling_prompt(scene: dict[str, Any], subject: str) -> str:
    return (
        f"{subject}. {scene['action']} "
        f"Environment: {scene['environment']}. "
        f"Camera: {scene['camera']['shot']}, {scene['camera']['movement']}. "
        f"Mood: {scene.get('mood', 'premium cinematic')}. "
        "Luxury minimal fashion-tech visual style, cinematic editorial lighting, "
        "realistic natural motion, premium commercial video. "
        f"Duration: {scene['duration']} seconds."
    )


def build_negative_prompt(scene_negative: str) -> str:
    base = (
        "Do not change character identity. Do not change outfit. "
        "Do not invent new characters, environments, props, logos, or text. "
        "No cartoon style. No glitch. No exaggerated motion. No TikTok effects. "
        "No watermark."
    )
    if scene_negative:
        return f"{base} {scene_negative}"
    return base


def write_report(
    plan: dict[str, Any],
    assets: dict[str, dict[str, list[Path] | Path]],
    output_dir: Path,
    prompt_files: list[Path],
) -> Path:
    report = output_dir / "kling_prompt_report.md"
    lines = [
        "# Kling Prompt Report",
        "",
        f"episode: {plan['episode']['id']}",
        f"provider: {plan['provider']}",
        "validation_result: passed",
        "missing_assets: none",
        f"scenes: {len(plan['scenes'])}",
        "",
        "## Prompt Files",
    ]
    for path in prompt_files:
        lines.append(f"- {path.relative_to(ROOT).as_posix()}")

    lines.extend(["", "## Assets Used"])
    for scene in plan["scenes"]:
        scene_id = str(scene["id"])
        lines.append(f"### {scene_id}")
        scene_assets = assets[scene_id]
        for role in ("characters", "environment", "props"):
            value = scene_assets[role]
            if isinstance(value, list):
                if value:
                    for path in value:
                        lines.append(f"- {role}: {path.relative_to(ROOT).as_posix()}")
                else:
                    lines.append(f"- {role}: none")
            else:
                lines.append(f"- {role}: {value.relative_to(ROOT).as_posix()}")

    lines.extend(["", "## Warnings", "- none"])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    raise SystemExit(main())
