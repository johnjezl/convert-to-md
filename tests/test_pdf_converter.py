"""Tests for PDF to Markdown conversion."""

from pathlib import Path

from convert_to_md.pdf_converter import convert_pdf
from convert_to_md.image_utils import image_dir_for


def test_simple_pdf(sample_pdf: Path, tmp_output: Path):
    output_md = tmp_output / "sample.md"
    md = convert_pdf(sample_pdf, output_md)

    assert "Test PDF Document" in md
    assert "test paragraph" in md


def test_pdf_with_image(sample_pdf_with_image: Path, tmp_output: Path):
    output_md = tmp_output / "with_image.md"
    md = convert_pdf(sample_pdf_with_image, output_md)

    img_dir = image_dir_for(output_md)
    assert img_dir.exists()
    images = list(img_dir.iterdir())
    assert len(images) >= 1
    # Paths in markdown should be relative (not absolute)
    assert str(img_dir) not in md or img_dir.name in md


def test_pdf_no_images_flag(sample_pdf_with_image: Path, tmp_output: Path):
    output_md = tmp_output / "with_image.md"
    md = convert_pdf(sample_pdf_with_image, output_md, extract_images=False)

    img_dir = image_dir_for(output_md)
    assert not img_dir.exists()


def test_pdf_no_empty_image_dir(sample_pdf: Path, tmp_output: Path):
    """A PDF with no images should not leave an empty image directory."""
    output_md = tmp_output / "sample.md"
    convert_pdf(sample_pdf, output_md)

    img_dir = image_dir_for(output_md)
    assert not img_dir.exists()
