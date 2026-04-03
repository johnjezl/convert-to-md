"""Convert PDF files to Markdown using pymupdf4llm."""

from __future__ import annotations

from pathlib import Path

import pymupdf4llm

from .image_utils import ensure_image_dir, fix_absolute_image_paths, remove_empty_image_dir


def convert_pdf(
    input_path: Path,
    output_md_path: Path,
    *,
    extract_images: bool = True,
    image_format: str = "png",
    dpi: int = 150,
) -> str:
    """Convert a PDF file to Markdown and return the markdown string.

    Images are written to ``<stem>_images/`` next to *output_md_path*.
    """
    if extract_images:
        img_dir = ensure_image_dir(output_md_path)
        md_text = pymupdf4llm.to_markdown(
            str(input_path),
            write_images=True,
            image_path=str(img_dir) + "/",
            image_format=image_format,
            dpi=dpi,
            show_progress=False,
        )
        md_text = fix_absolute_image_paths(md_text, img_dir, output_md_path)
        remove_empty_image_dir(output_md_path)
    else:
        md_text = pymupdf4llm.to_markdown(
            str(input_path),
            write_images=False,
            show_progress=False,
        )

    return md_text
