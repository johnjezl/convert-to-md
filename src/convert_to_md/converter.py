"""Dispatch logic: detect file type and call the appropriate converter."""

from __future__ import annotations

import sys
from pathlib import Path

from .docx_converter import convert_docx
from .pdf_converter import convert_pdf

SUPPORTED_EXTENSIONS = {".docx", ".pdf"}


def convert_file(
    input_path: Path,
    *,
    output_dir: Path | None = None,
    overwrite: bool = False,
    extract_images: bool = True,
    image_format: str = "png",
    dpi: int = 150,
) -> Path:
    """Convert a single .docx or .pdf file to Markdown.

    Returns the path to the output .md file.
    """
    input_path = input_path.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    ext = input_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext} (expected {', '.join(SUPPORTED_EXTENSIONS)})")

    dest_dir = (output_dir or input_path.parent).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    output_md = dest_dir / (input_path.stem + ".md")

    if output_md.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists (use --overwrite): {output_md}")

    if ext == ".docx":
        md_text = convert_docx(
            input_path,
            output_md,
            extract_images=extract_images,
            image_format=image_format,
        )
    else:
        md_text = convert_pdf(
            input_path,
            output_md,
            extract_images=extract_images,
            image_format=image_format,
            dpi=dpi,
        )

    output_md.write_text(md_text, encoding="utf-8")
    return output_md
