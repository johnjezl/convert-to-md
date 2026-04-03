"""Tests for the CLI interface."""

from pathlib import Path

from convert_to_md.cli import main


def test_cli_single_docx(sample_docx: Path, tmp_output: Path):
    ret = main([str(sample_docx), "-o", str(tmp_output)])
    assert ret == 0
    output = tmp_output / "sample.md"
    assert output.exists()
    assert "Test Document" in output.read_text(encoding="utf-8")


def test_cli_single_pdf(sample_pdf: Path, tmp_output: Path):
    ret = main([str(sample_pdf), "-o", str(tmp_output)])
    assert ret == 0
    output = tmp_output / "sample.md"
    assert output.exists()
    assert "Test PDF Document" in output.read_text(encoding="utf-8")


def test_cli_multiple_files(sample_docx: Path, sample_pdf: Path, tmp_output: Path):
    ret = main([str(sample_docx), str(sample_pdf), "-o", str(tmp_output), "--overwrite"])
    assert ret == 0
    assert (tmp_output / "sample.md").exists()


def test_cli_overwrite_required(sample_docx: Path, tmp_output: Path):
    # First conversion
    main([str(sample_docx), "-o", str(tmp_output)])
    # Second without --overwrite should fail
    ret = main([str(sample_docx), "-o", str(tmp_output)])
    assert ret == 1


def test_cli_overwrite_flag(sample_docx: Path, tmp_output: Path):
    main([str(sample_docx), "-o", str(tmp_output)])
    ret = main([str(sample_docx), "-o", str(tmp_output), "--overwrite"])
    assert ret == 0


def test_cli_unsupported_file(tmp_path: Path, tmp_output: Path):
    bad_file = tmp_path / "test.txt"
    bad_file.write_text("hello")
    ret = main([str(bad_file), "-o", str(tmp_output)])
    assert ret == 1


def test_cli_nonexistent_file(tmp_output: Path):
    ret = main(["/nonexistent/file.docx", "-o", str(tmp_output)])
    assert ret == 1


def test_cli_no_images(sample_docx: Path, tmp_output: Path):
    ret = main([str(sample_docx), "-o", str(tmp_output), "--no-images"])
    assert ret == 0


def test_cli_quiet(sample_docx: Path, tmp_output: Path, capsys):
    main([str(sample_docx), "-o", str(tmp_output), "-q"])
    captured = capsys.readouterr()
    assert captured.out == ""
