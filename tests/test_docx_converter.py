"""Tests for DOCX to Markdown conversion."""

from pathlib import Path

from convert_to_md.docx_converter import convert_docx
from convert_to_md.image_utils import image_dir_for


def test_simple_docx(sample_docx: Path, tmp_output: Path):
    output_md = tmp_output / "sample.md"
    md = convert_docx(sample_docx, output_md)

    assert "# Test Document" in md
    assert "test paragraph" in md
    assert "**Bold text**" in md
    assert "## Section Two" in md
    assert "Item one" in md
    assert "Item two" in md


def test_docx_with_image(sample_docx_with_image: Path, tmp_output: Path):
    output_md = tmp_output / "with_image.md"
    md = convert_docx(sample_docx_with_image, output_md)

    img_dir = image_dir_for(output_md)
    assert img_dir.exists()
    images = list(img_dir.iterdir())
    assert len(images) >= 1
    # Markdown should reference the image
    assert "with_image_images/" in md


def test_docx_no_images_flag(sample_docx_with_image: Path, tmp_output: Path):
    output_md = tmp_output / "with_image.md"
    md = convert_docx(sample_docx_with_image, output_md, extract_images=False)

    img_dir = image_dir_for(output_md)
    assert not img_dir.exists()


def test_docx_with_table(sample_docx_with_table: Path, tmp_output: Path):
    output_md = tmp_output / "with_table.md"
    md = convert_docx(sample_docx_with_table, output_md)

    assert "Name" in md
    assert "Value" in md
    assert "Alpha" in md
    assert "100" in md


def test_docx_no_empty_image_dir(sample_docx: Path, tmp_output: Path):
    """A docx with no images should not leave an empty image directory."""
    output_md = tmp_output / "sample.md"
    convert_docx(sample_docx, output_md)

    img_dir = image_dir_for(output_md)
    assert not img_dir.exists()
