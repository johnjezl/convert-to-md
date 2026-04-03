"""Command-line interface for convert-to-md."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .converter import convert_file


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="convert-to-md",
        description="Convert .docx and .pdf files to Markdown.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        metavar="FILE",
        help="One or more .docx or .pdf files to convert",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: same directory as input file)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files without prompting",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip image extraction",
    )
    parser.add_argument(
        "--image-format",
        choices=["png", "jpg"],
        default="png",
        help="Image output format (default: png)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="DPI for PDF image extraction (default: 150)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the CLI. Returns exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    succeeded = 0
    failed = 0
    total = len(args.files)

    for input_path in args.files:
        try:
            output_md = convert_file(
                input_path,
                output_dir=args.output_dir,
                overwrite=args.overwrite,
                extract_images=not args.no_images,
                image_format=args.image_format,
                dpi=args.dpi,
            )
            succeeded += 1
            if not args.quiet:
                print(f"Converted: {input_path} -> {output_md}")
        except Exception as exc:
            failed += 1
            print(f"Error: {input_path}: {exc}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()

    if not args.quiet and total > 1:
        print(f"\nConverted {succeeded} of {total} files.")

    return 1 if failed else 0
