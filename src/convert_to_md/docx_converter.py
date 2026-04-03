"""Convert DOCX files to Markdown using mammoth and markdownify."""

from __future__ import annotations

import mimetypes
from pathlib import Path

import mammoth
import mammoth.images
from markdownify import markdownify

from .image_utils import ensure_image_dir, image_dir_for, next_image_name, remove_empty_image_dir


# Map content-types to file extensions
_CONTENT_TYPE_TO_EXT = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/tiff": "tiff",
    "image/svg+xml": "svg",
    "image/webp": "webp",
}


def convert_docx(
    input_path: Path,
    output_md_path: Path,
    *,
    extract_images: bool = True,
    image_format: str = "png",
) -> str:
    """Convert a DOCX file to Markdown and return the markdown string.

    Images are written to ``<stem>_images/`` next to *output_md_path*.
    """
    convert_image = None

    if extract_images:
        img_dir = ensure_image_dir(output_md_path)
        counter = 0

        @mammoth.images.img_element
        def convert_image(image):
            nonlocal counter
            counter += 1

            ext = _CONTENT_TYPE_TO_EXT.get(image.content_type, image_format)
            filename = next_image_name(counter, ext)
            dest = img_dir / filename

            with image.open() as f:
                dest.write_bytes(f.read())

            rel_path = img_dir.name + "/" + filename
            return {"src": rel_path}

    with open(input_path, "rb") as f:
        result = mammoth.convert_to_html(f, convert_image=convert_image)

    md_text = markdownify(
        result.value,
        heading_style="ATX",
        bullets="-",
    )

    if extract_images:
        remove_empty_image_dir(output_md_path)

    return md_text
