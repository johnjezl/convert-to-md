"""Shared utilities for image extraction and path management."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


def image_dir_for(output_md_path: Path) -> Path:
    """Return the image subdirectory path for a given .md output file.

    For ``report.md`` this returns ``report_images/`` in the same directory.
    Does NOT create the directory.
    """
    return output_md_path.parent / f"{output_md_path.stem}_images"


def ensure_image_dir(output_md_path: Path) -> Path:
    """Create (or clear) the image subdirectory for *output_md_path* and return it."""
    img_dir = image_dir_for(output_md_path)
    if img_dir.exists():
        shutil.rmtree(img_dir)
    img_dir.mkdir(parents=True)
    return img_dir


def next_image_name(counter: int, extension: str) -> str:
    """Return a zero-padded image filename like ``image_001.png``."""
    ext = extension.lstrip(".")
    return f"image_{counter:03d}.{ext}"


def relative_image_path(image_abs: Path, md_abs: Path) -> str:
    """Compute the relative path from the .md file to an image, using forward slashes."""
    return image_abs.relative_to(md_abs.parent).as_posix()


def fix_absolute_image_paths(markdown: str, image_dir: Path, md_path: Path) -> str:
    """Replace absolute image paths in *markdown* with paths relative to *md_path*.

    pymupdf4llm writes absolute paths; this converts them to portable relative paths.
    """
    abs_prefix = re.escape(str(image_dir))

    def _replace(m: re.Match) -> str:
        alt = m.group(1)
        src = m.group(2)
        # Only fix paths that start with the absolute image dir
        if src.startswith(str(image_dir)):
            rel = Path(src).relative_to(md_path.parent).as_posix()
            return f"![{alt}]({rel})"
        return m.group(0)

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _replace, markdown)


def remove_empty_image_dir(output_md_path: Path) -> None:
    """Remove the image directory if it exists and is empty."""
    img_dir = image_dir_for(output_md_path)
    if img_dir.exists() and not any(img_dir.iterdir()):
        img_dir.rmdir()
