#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEMPLATE = ROOT / "autopilot" / "templates" / "daily_reel_v1.yaml"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


class AutopilotError(RuntimeError):
    pass


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = load_config(args.template.resolve())
    run_date = args.date or dt.date.today().isoformat()

    try:
        validate_date(run_date)
        run_autopilot(config, root, run_date, args.dry_run, args.keep_work)
    except AutopilotError as exc:
        print(f"Autopilot error: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"FFmpeg failed with exit code {exc.returncode}", file=sys.stderr)
        if exc.cmd:
            print(format_cmd(exc.cmd), file=sys.stderr)
        return exc.returncode
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a vertical ShowroomFlow Reel from local assets."
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Path to the Autopilot YAML template.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root. Defaults to the ShowroomFlowUniverse root.",
    )
    parser.add_argument(
        "--date",
        help="Daily output date in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate assets and print the plan without running FFmpeg.",
    )
    parser.add_argument(
        "--keep-work",
        action="store_true",
        help="Keep intermediate segment files in the output .work directory.",
    )
    return parser.parse_args()


def run_autopilot(
    config: dict[str, Any],
    root: Path,
    run_date: str,
    dry_run: bool,
    keep_work: bool,
) -> None:
    output_cfg = config.get("output", {})
    width = int(output_cfg.get("width", 1080))
    height = int(output_cfg.get("height", 1920))
    fps = int(output_cfg.get("fps", 30))
    crf = int(output_cfg.get("crf", 20))
    preset = str(output_cfg.get("preset", "medium"))
    daily_root = resolve_path(root, output_cfg.get("daily_dir", "video/autopilot/daily"))
    output_dir = daily_root / run_date
    work_dir = output_dir / ".work"
    font_file = find_font_file(config, root)

    ffmpeg = find_ffmpeg(config, dry_run)
    pools = collect_asset_pools(config, root)
    sequence = build_sequence(config, pools, run_date)
    total_duration = sum(float(item["duration"]) for item in sequence)

    if not 12 <= total_duration <= 18:
        raise AutopilotError(
            f"template duration is {total_duration:.1f}s; expected 12-18s"
        )

    print("ShowroomFlow Autopilot v1")
    print(f"Template: {config.get('name', 'unnamed')}")
    print(f"Output: {output_dir}")
    print(f"Format: {width}x{height}, {fps} fps, {total_duration:.1f}s")
    print("")
    print("Planned sequence:")
    for index, item in enumerate(sequence, start=1):
        print(
            f"  {index:02d}. {item['type']} "
            f"{float(item['duration']):.1f}s - {item['asset']}"
        )

    if dry_run:
        print("")
        print("Dry run only. FFmpeg commands were not executed.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    segment_paths = render_segments(
        ffmpeg,
        sequence,
        work_dir,
        width,
        height,
        fps,
        crf,
        preset,
        font_file,
    )
    assembled = work_dir / "assembled_silent.mp4"
    concat_segments(ffmpeg, segment_paths, assembled, work_dir)

    reel_path = output_dir / "reel.mp4"
    add_audio_track(
        ffmpeg,
        assembled,
        reel_path,
        config,
        root,
        total_duration,
    )
    write_cover(ffmpeg, reel_path, output_dir / "cover.png", width, height)
    write_marketing_files(config, output_dir)

    if not keep_work:
        shutil.rmtree(work_dir, ignore_errors=True)

    print("")
    print("Generated:")
    print(f"  {reel_path}")
    print(f"  {output_dir / 'cover.png'}")
    print(f"  {output_dir / 'caption.md'}")
    print(f"  {output_dir / 'hashtags.md'}")


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AutopilotError(f"template not found: {path}")

    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
    except ModuleNotFoundError:
        loaded = parse_simple_yaml(text)

    if not isinstance(loaded, dict):
        raise AutopilotError("template root must be a mapping")
    return loaded


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by the Autopilot template."""

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
                    raise AutopilotError(f"invalid YAML list item: {content}")

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
            raise AutopilotError(f"invalid YAML mapping item: {content}")

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
        raise AutopilotError("invalid YAML parent")


def looks_like_key_value(text: str) -> bool:
    return find_unquoted_colon(text) >= 0


def split_key_value(text: str) -> tuple[str, str]:
    index = find_unquoted_colon(text)
    if index < 0:
        raise AutopilotError(f"expected key: value, got: {text}")
    key = text[:index].strip()
    value = text[index + 1 :].strip()
    if not key:
        raise AutopilotError(f"empty YAML key in: {text}")
    return key, value


def find_unquoted_colon(text: str) -> int:
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
        if char == ":":
            return index
    return -1


def parse_scalar(value: str) -> Any:
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    if lower in {"null", "none", "~"}:
        return None

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


def find_ffmpeg(config: dict[str, Any], dry_run: bool) -> str:
    configured = config.get("ffmpeg")
    if configured:
        return str(configured)

    found = shutil.which("ffmpeg")
    if found:
        return found
    if dry_run:
        return "ffmpeg"

    raise AutopilotError(
        "FFmpeg is not available in PATH. Install FFmpeg, then run "
        "`ffmpeg -version` to verify it."
    )


def collect_asset_pools(config: dict[str, Any], root: Path) -> dict[str, list[Path]]:
    inputs = config.get("inputs", {})
    fallbacks = config.get("fallbacks", {})
    if not isinstance(inputs, dict):
        raise AutopilotError("inputs must be a mapping")

    pools: dict[str, list[Path]] = {}
    for name, raw_path in inputs.items():
        extensions = VIDEO_EXTS if "video" in name else IMAGE_EXTS
        primary = list_media(resolve_path(root, raw_path), extensions)
        pools[name] = primary

        if not primary and isinstance(fallbacks, dict):
            for fallback_path in as_list(fallbacks.get(name)):
                fallback_assets = list_media(resolve_path(root, fallback_path), extensions)
                if fallback_assets:
                    pools[name] = fallback_assets
                    break

    return pools


def build_sequence(
    config: dict[str, Any],
    pools: dict[str, list[Path]],
    run_date: str,
) -> list[dict[str, Any]]:
    raw_sequence = config.get("sequence")
    if not isinstance(raw_sequence, list) or not raw_sequence:
        raw_sequence = default_sequence(config)

    sequence: list[dict[str, Any]] = []
    for index, raw_item in enumerate(raw_sequence):
        if not isinstance(raw_item, dict):
            raise AutopilotError("each sequence item must be a mapping")
        media_type = str(raw_item.get("type", "")).lower()
        source = str(raw_item.get("source", ""))
        duration = float(raw_item.get("duration", 0))

        if media_type not in {"video", "image"}:
            raise AutopilotError(f"unsupported sequence item type: {media_type}")
        if duration <= 0:
            raise AutopilotError(f"invalid duration in sequence item {index + 1}")
        if source not in pools or not pools[source]:
            raise AutopilotError(
                f"no assets found for source '{source}'. Check the template paths."
            )

        item = dict(raw_item)
        item["asset"] = pick_asset(pools[source], run_date, index)
        item["duration"] = duration
        item["type"] = media_type
        if media_type == "image":
            item["motion"] = choose_motion(str(item.get("motion", "auto")), index)
        sequence.append(item)

    return sequence


def default_sequence(config: dict[str, Any]) -> list[dict[str, Any]]:
    duration = float(config.get("output", {}).get("duration_seconds", 15))
    return [
        {
            "type": "video",
            "source": "videos",
            "duration": min(5, duration),
            "overlay_text": "Il momento giusto",
            "text_position": "bottom",
        },
        {
            "type": "image",
            "source": "app_images",
            "duration": 4,
            "motion": "auto",
            "overlay_text": "Le collezioni restano disponibili",
            "text_position": "bottom",
        },
        {
            "type": "image",
            "source": "end_cards",
            "duration": max(3, duration - 9),
            "motion": "zoom_in",
        },
    ]


def render_segments(
    ffmpeg: str,
    sequence: list[dict[str, Any]],
    work_dir: Path,
    width: int,
    height: int,
    fps: int,
    crf: int,
    preset: str,
    font_file: Path | None,
) -> list[Path]:
    segments: list[Path] = []
    for index, item in enumerate(sequence, start=1):
        output = work_dir / f"segment_{index:02d}.mp4"
        filter_chain = video_filter_chain(item, width, height, fps, index, font_file)

        cmd = [ffmpeg, "-y"]
        if item["type"] == "image":
            cmd.extend(["-loop", "1", "-framerate", str(fps), "-i", str(item["asset"])])
        else:
            cmd.extend(["-stream_loop", "-1", "-i", str(item["asset"])])

        cmd.extend(
            [
                "-t",
                seconds(item["duration"]),
                "-vf",
                filter_chain,
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                preset,
                "-crf",
                str(crf),
                "-pix_fmt",
                "yuv420p",
                "-r",
                str(fps),
                str(output),
            ]
        )
        run(cmd)
        segments.append(output)
    return segments


def video_filter_chain(
    item: dict[str, Any],
    width: int,
    height: int,
    fps: int,
    index: int,
    font_file: Path | None,
) -> str:
    duration = float(item["duration"])
    frames = max(1, int(duration * fps))

    if item["type"] == "video":
        filters = [
            f"scale={width}:{height}:force_original_aspect_ratio=increase",
            f"crop={width}:{height}",
            "setsar=1",
            f"fps={fps}",
            "format=yuv420p",
        ]
    else:
        filters = [image_motion_filter(str(item.get("motion", "auto")), width, height, fps, frames)]

    overlay_text = item.get("overlay_text")
    if overlay_text:
        filters.append(
            drawtext_filter(
                str(overlay_text),
                str(item.get("text_position", "bottom")),
                int(item.get("text_size", 58)),
                font_file,
            )
        )

    overlays = item.get("overlays", [])
    if isinstance(overlays, list):
        for overlay in overlays:
            if isinstance(overlay, dict) and overlay.get("text"):
                filters.append(
                    drawtext_filter(
                        str(overlay["text"]),
                        str(overlay.get("position", "bottom")),
                        int(overlay.get("size", 58)),
                        font_file,
                        overlay.get("start"),
                        overlay.get("end"),
                    )
                )

    filters.append(f"trim=duration={seconds(duration)}")
    return ",".join(filters)


def image_motion_filter(
    motion: str,
    width: int,
    height: int,
    fps: int,
    frames: int,
) -> str:
    if motion == "zoom_in":
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},setsar=1,"
            "zoompan=z='min(zoom+0.0015,1.12)':"
            f"d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"s={width}x{height}:fps={fps},format=yuv420p"
        )

    scale_w = int(width * 1.12)
    scale_h = int(height * 1.12)
    base = f"scale={scale_w}:{scale_h}:force_original_aspect_ratio=increase"

    if motion == "pan_left":
        crop = (
            f"crop={width}:{height}:"
            f"x='(in_w-out_w)*(1-n/{frames})':y='(in_h-out_h)/2'"
        )
    elif motion == "pan_right":
        crop = (
            f"crop={width}:{height}:"
            f"x='(in_w-out_w)*n/{frames}':y='(in_h-out_h)/2'"
        )
    elif motion == "pan_up":
        crop = (
            f"crop={width}:{height}:"
            f"x='(in_w-out_w)/2':y='(in_h-out_h)*n/{frames}'"
        )
    elif motion == "pan_down":
        crop = (
            f"crop={width}:{height}:"
            f"x='(in_w-out_w)/2':y='(in_h-out_h)*(1-n/{frames})'"
        )
    else:
        crop = f"crop={width}:{height}:x='(in_w-out_w)/2':y='(in_h-out_h)/2'"

    return f"{base},{crop},setsar=1,fps={fps},format=yuv420p"


def drawtext_filter(
    text: str,
    position: str,
    size: int,
    font_file: Path | None,
    start: Any = None,
    end: Any = None,
) -> str:
    position = position.lower()
    if position == "top":
        y = "h*0.14"
    elif position == "middle":
        y = "(h-text_h)/2"
    else:
        y = "h*0.76"

    enable = ""
    if start is not None or end is not None:
        start_value = float(start or 0)
        end_value = float(end or 999)
        enable = f":enable='between(t,{seconds(start_value)},{seconds(end_value)})'"

    font_option = ""
    if font_file:
        font_option = f"fontfile='{escape_drawtext_path(font_file)}':"

    return (
        "drawtext="
        f"{font_option}"
        f"text='{escape_drawtext(text)}':"
        "fontcolor=white:"
        f"fontsize={size}:"
        "box=1:"
        "boxcolor=black@0.44:"
        "boxborderw=28:"
        "line_spacing=12:"
        "x=(w-text_w)/2:"
        f"y={y}{enable}"
    )


def concat_segments(
    ffmpeg: str,
    segment_paths: list[Path],
    assembled: Path,
    work_dir: Path,
) -> None:
    concat_file = work_dir / "concat.txt"
    lines = [f"file '{escape_concat_path(path)}'" for path in segment_paths]
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(assembled),
    ]
    run(cmd)


def add_audio_track(
    ffmpeg: str,
    assembled: Path,
    reel_path: Path,
    config: dict[str, Any],
    root: Path,
    duration: float,
) -> None:
    music_cfg = config.get("music", {})
    music_path = None
    if isinstance(music_cfg, dict) and music_cfg.get("enabled", True):
        music_path = pick_music(music_cfg, root)

    if music_path:
        volume = float(music_cfg.get("volume", 0.18))
        fade = float(music_cfg.get("fade_out_seconds", 1.2))
        fade_start = max(0, duration - fade)
        audio_filter = (
            f"[1:a]volume={volume},atrim=0:{seconds(duration)},"
            f"afade=t=out:st={seconds(fade_start)}:d={seconds(fade)}[a]"
        )
        cmd = [
            ffmpeg,
            "-y",
            "-i",
            str(assembled),
            "-stream_loop",
            "-1",
            "-i",
            str(music_path),
            "-t",
            seconds(duration),
            "-filter_complex",
            audio_filter,
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(reel_path),
        ]
    else:
        cmd = [
            ffmpeg,
            "-y",
            "-i",
            str(assembled),
            "-f",
            "lavfi",
            "-t",
            seconds(duration),
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(reel_path),
        ]
    run(cmd)


def write_cover(ffmpeg: str, reel_path: Path, cover_path: Path, width: int, height: int) -> None:
    cmd = [
        ffmpeg,
        "-y",
        "-ss",
        "00:00:01",
        "-i",
        str(reel_path),
        "-frames:v",
        "1",
        "-vf",
        f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}",
        str(cover_path),
    ]
    run(cmd)


def write_marketing_files(config: dict[str, Any], output_dir: Path) -> None:
    content = config.get("content", {})
    caption = ""
    hashtags: list[str] = []

    if isinstance(content, dict):
        caption = str(content.get("caption", "")).strip()
        hashtags = [str(tag).strip() for tag in as_list(content.get("hashtags")) if str(tag).strip()]

    if not caption:
        caption = "Lascia il tempo alla moda."
    if not hashtags:
        hashtags = ["#ShowroomFlow", "#FashionTech", "#ModaB2B"]

    (output_dir / "caption.md").write_text(caption + "\n", encoding="utf-8")
    (output_dir / "hashtags.md").write_text("\n".join(hashtags) + "\n", encoding="utf-8")


def list_media(directory: Path, extensions: set[str]) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        [
            item
            for item in directory.iterdir()
            if item.is_file() and item.suffix.lower() in extensions
        ],
        key=lambda path: path.name.lower(),
    )


def pick_asset(paths: list[Path], run_date: str, index: int) -> Path:
    seed = f"{run_date}:{index}".encode("utf-8")
    digest = hashlib.sha1(seed).hexdigest()
    return paths[int(digest[:8], 16) % len(paths)]


def pick_music(music_cfg: dict[str, Any], root: Path) -> Path | None:
    explicit = music_cfg.get("file")
    if explicit:
        path = resolve_path(root, explicit)
        return path if path.exists() else None

    directory = music_cfg.get("directory")
    if not directory:
        return None

    tracks = list_media(resolve_path(root, directory), AUDIO_EXTS)
    if not tracks:
        return None
    return tracks[0]


def find_font_file(config: dict[str, Any], root: Path) -> Path | None:
    text_cfg = config.get("text", {})
    if isinstance(text_cfg, dict) and text_cfg.get("font_file"):
        configured = resolve_path(root, text_cfg["font_file"])
        if configured.exists():
            return configured

    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def choose_motion(value: str, index: int) -> str:
    if value != "auto":
        return value
    motions = ["zoom_in", "pan_right", "pan_left", "pan_up", "pan_down"]
    return motions[index % len(motions)]


def resolve_path(root: Path, value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return root / path


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def validate_date(value: str) -> None:
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise AutopilotError("--date must use YYYY-MM-DD") from exc


def seconds(value: float) -> str:
    return f"{float(value):.3f}".rstrip("0").rstrip(".")


def escape_drawtext(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace(",", "\\,")
        .replace("%", "\\%")
        .replace("\n", "\\n")
    )


def escape_drawtext_path(path: Path) -> str:
    return escape_drawtext(path.resolve().as_posix())


def escape_concat_path(path: Path) -> str:
    return path.resolve().as_posix().replace("'", "'\\''")


def format_cmd(cmd: list[str] | tuple[str, ...] | Any) -> str:
    if isinstance(cmd, (list, tuple)):
        return " ".join(quote_arg(str(part)) for part in cmd)
    return str(cmd)


def quote_arg(value: str) -> str:
    if not value or any(char.isspace() for char in value):
        return '"' + value.replace('"', '\\"') + '"'
    return value


def run(cmd: list[str]) -> None:
    print(format_cmd(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    raise SystemExit(main())
