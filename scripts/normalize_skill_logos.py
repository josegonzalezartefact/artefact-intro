from __future__ import annotations

import argparse
import shutil
import subprocess
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops


@dataclass
class Candidate:
    src: Path
    image: Image.Image
    area: int


def content_bbox(image: Image.Image, tolerance: int) -> tuple[int, int, int, int] | None:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema()[0] < 255:
        return alpha.point(lambda px: 255 if px > tolerance else 0).getbbox()

    rgb = image.convert("RGB")
    corners = [
        rgb.getpixel((0, 0)),
        rgb.getpixel((rgb.width - 1, 0)),
        rgb.getpixel((0, rgb.height - 1)),
        rgb.getpixel((rgb.width - 1, rgb.height - 1)),
    ]
    bg = tuple(round(sum(c[i] for c in corners) / 4) for i in range(3))
    background = Image.new("RGB", rgb.size, bg)
    diff = ImageChops.difference(rgb, background).convert("L")
    return diff.point(lambda px: 255 if px > tolerance else 0).getbbox()


def render_svg(src: Path, work_dir: Path) -> Image.Image:
    out_dir = work_dir / "svg-renders"
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["qlmanage", "-t", "-s", "1400", "-o", str(out_dir), str(src)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    rendered = out_dir / f"{src.name}.png"
    if not rendered.exists():
        raise RuntimeError(f"Quick Look did not render {src}")
    return Image.open(rendered).convert("RGBA")


def load_image(src: Path, work_dir: Path) -> Image.Image | None:
    if src.name == ".DS_Store" or src.is_dir():
        return None
    if src.suffix.lower() == ".svg":
        return render_svg(src, work_dir)
    try:
        return Image.open(src).convert("RGBA")
    except Exception:
        return None


def trim_image(image: Image.Image, padding_ratio: float, tolerance: int) -> Image.Image:
    bbox = content_bbox(image, tolerance)
    cropped = image.crop(bbox).convert("RGBA") if bbox else image.convert("RGBA")
    pad = max(8, round(max(cropped.size) * padding_ratio))
    out = Image.new("RGBA", (cropped.width + pad * 2, cropped.height + pad * 2), (255, 255, 255, 0))
    out.paste(cropped, (pad, pad), cropped)
    return out


def build_normalized_folder(src_dir: Path, dst_dir: Path, work_dir: Path, padding_ratio: float, tolerance: int) -> int:
    grouped: dict[str, Candidate] = {}
    for src in sorted(src_dir.iterdir()):
        image = load_image(src, work_dir)
        if image is None:
            continue
        bbox = content_bbox(image, tolerance)
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) if bbox else image.width * image.height
        stem = src.stem
        current = grouped.get(stem)
        if current is None or area > current.area:
            grouped[stem] = Candidate(src=src, image=image, area=area)

    dst_dir.mkdir(parents=True, exist_ok=True)
    for stem, candidate in sorted(grouped.items()):
        normalized = trim_image(candidate.image, padding_ratio, tolerance)
        normalized.save(dst_dir / f"{stem}.png")
    return len(grouped)


def backup_dirs(dirs: list[Path], backup_path: Path) -> None:
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(backup_path, "w:gz") as tar:
        for directory in dirs:
            tar.add(directory, arcname=directory.name)


def replace_dir_files(target: Path, normalized: Path) -> None:
    for child in target.iterdir():
        if child.is_file():
            child.unlink()
    for src in sorted(normalized.iterdir()):
        shutil.copy2(src, target / src.name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Artefact client and consultancy logos in-place.")
    parser.add_argument("--asset-root", type=Path, default=Path("/Users/jose/Documents/artefact-html-skill/assets"))
    parser.add_argument("--backup", type=Path, default=Path("tmp/logo-library-backup-before-trim.tar.gz"))
    parser.add_argument("--padding-ratio", type=float, default=0.08)
    parser.add_argument("--tolerance", type=int, default=18)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    logo_dirs = [args.asset_root / "clients-logos", args.asset_root / "consultancy-logos"]
    normalized_root = Path("tmp/normalized-logo-library").resolve()
    if normalized_root.exists():
        shutil.rmtree(normalized_root)
    normalized_root.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix="logo-normalize-") as tmp:
        work_dir = Path(tmp)
        counts = {}
        for logo_dir in logo_dirs:
            count = build_normalized_folder(
                logo_dir,
                normalized_root / logo_dir.name,
                work_dir,
                args.padding_ratio,
                args.tolerance,
            )
            counts[logo_dir.name] = count

    print(f"Normalized clients-logos: {counts.get('clients-logos', 0)}")
    print(f"Normalized consultancy-logos: {counts.get('consultancy-logos', 0)}")
    print(f"Staged output: {normalized_root}")

    if not args.apply:
        print("Dry run only. Re-run with --apply to replace the skill asset folders.")
        return 0

    backup_dirs(logo_dirs, args.backup.resolve())
    for logo_dir in logo_dirs:
        replace_dir_files(logo_dir, normalized_root / logo_dir.name)
    print(f"Backup written: {args.backup.resolve()}")
    print("Skill logo folders replaced with normalized PNG files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
