# convert-to-md

Convert Word `.docx` and PDF files to Markdown with image extraction.

Works from the **Windows command line**, **Ubuntu command line**, and as a **right-click option in Windows File Explorer**.

## Features

- **DOCX conversion** — preserves headings, bold/italic, lists, tables, and images using [mammoth](https://github.com/mwilliamson/python-mammoth) + [markdownify](https://github.com/matthewwithanm/python-markdownify)
- **PDF conversion** — high-fidelity extraction of text, tables, and multi-column layouts using [pymupdf4llm](https://github.com/pymupdf/RAG)
- **Image extraction** — embedded images are saved to a `<filename>_images/` subfolder with relative Markdown links
- **Batch processing** — convert multiple files in one command
- **Cross-platform** — runs on Windows and Linux with the same CLI

## Requirements

Python 3.10 or later.

## Installation

```bash
pip install git+https://github.com/johnjezl/convert-to-md.git
```

Or clone and install locally:

```bash
git clone https://github.com/johnjezl/convert-to-md.git
cd convert-to-md
pip install .
```

## Usage

### Basic conversion

```bash
# Convert a single file
convert-to-md report.docx

# Convert a PDF
convert-to-md paper.pdf

# Convert multiple files
convert-to-md report.docx paper.pdf slides.docx
```

Output `.md` files are placed alongside the input files by default. Images are extracted to a `<filename>_images/` subfolder:

```
report.md
report_images/
  image_001.png
  image_002.jpg
```

### Options

```
convert-to-md [OPTIONS] FILE [FILE ...]

Options:
  -o, --output-dir DIR    Output directory (default: same directory as input)
  --overwrite             Overwrite existing .md files
  --no-images             Skip image extraction
  --image-format {png,jpg}  Image format (default: png)
  --dpi DPI               DPI for PDF image extraction (default: 150)
  -v, --verbose           Show detailed error tracebacks
  -q, --quiet             Suppress all output except errors
  --version               Show version number
  -h, --help              Show help
```

### Examples

```bash
# Output to a specific directory
convert-to-md -o ./markdown/ *.pdf

# Higher quality PDF images
convert-to-md --dpi 300 scan.pdf

# Text only, no images
convert-to-md --no-images report.docx

# Overwrite existing output
convert-to-md --overwrite report.docx
```

### Alternative invocation

```bash
python -m convert_to_md report.docx
```

## Windows File Explorer Integration

Add a "Convert to Markdown" option to the right-click context menu for `.docx` and `.pdf` files. No administrator privileges required.

### Install

Open PowerShell in the environment where `convert-to-md` is installed and run:

```powershell
.\scripts\windows\install-context-menu.ps1
```

If `convert-to-md` is not on your PATH (e.g. it's in a virtual environment), pass the path explicitly:

```powershell
.\scripts\windows\install-context-menu.ps1 -ExePath "C:\path\to\venv\Scripts\convert-to-md.exe"
```

After installation, right-click any `.docx` or `.pdf` file and select **Convert to Markdown**. On Windows 11, the option appears under "Show more options".

### Uninstall

```powershell
.\scripts\windows\uninstall-context-menu.ps1
```

## Development

```bash
git clone https://github.com/johnjezl/convert-to-md.git
cd convert-to-md
python -m venv .venv
source .venv/bin/activate   # Linux
# .venv\Scripts\activate    # Windows
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

## License

MIT
