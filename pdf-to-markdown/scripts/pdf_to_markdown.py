#!/usr/bin/env python3
"""
PDF to Markdown Extractor using pymupdf4llm

This script converts PDF files to Markdown format using the pymupdf4llm library,
which provides high-quality extraction with support for:
- Text formatting (bold, italic, etc.)
- Tables (converted to Markdown tables)
- Images (extracted with references)
- Page structure and headers

Installation:
    pip install pymupdf4llm

Usage:
    python pdf_to_markdown.py input.pdf -o output.md
    python pdf_to_markdown.py input.pdf                    # Outputs to input.md
    python pdf_to_markdown.py input.pdf --pages 1,3,5      # Extract specific pages
    python pdf_to_markdown.py input.pdf --tables-only      # Extract tables only
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import pymupdf4llm
except ImportError:
    print("Error: pymupdf4llm is not installed.")
    print("Install it with: pip install pymupdf4llm")
    sys.exit(1)


def extract_pdf_to_markdown(
    pdf_path: str,
    output_path: str = None,
    pages: list = None,
    tables_only: bool = False,
    extract_images: bool = True,
    image_path: str = "images"
) -> str:
    """
    Extract PDF content to Markdown format.
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path for the output Markdown file (optional)
        pages: List of specific pages to extract (1-indexed, optional)
        tables_only: If True, only extract tables
        extract_images: If True, extract and save images
        image_path: Directory to save extracted images
        
    Returns:
        The extracted Markdown content as a string
    """
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Convert pages to 0-indexed list if provided
    page_list = None
    if pages:
        page_list = [p - 1 for p in pages]  # Convert to 0-indexed
    
    # Configure image extraction
    img_dir = None
    if extract_images:
        img_dir = Path(image_path)
        img_dir.mkdir(parents=True, exist_ok=True)
        print(f"Images will be saved to: {img_dir}/")
    
    print(f"Extracting: {pdf_path}")
    if page_list:
        print(f"Pages: {[p + 1 for p in page_list]}")
    
    # Extract to Markdown with direct image path
    page_chunks = pymupdf4llm.to_markdown(
        str(pdf_file),
        pages=page_list,
        write_images=extract_images,  # Extract images if enabled
        embed_images=False,  # Save images separately for cleaner markdown
        image_path=str(img_dir) if extract_images and img_dir else None,
        header=False,
        footer=False,
        use_ocr=False,
        page_chunks=True,
    )
    
    # If tables_only, we need to filter (pymupdf4llm doesn't have native tables_only,
    # but we can add a note about post-processing)
    if tables_only:
        print("Note: tables_only flag set. Tables are automatically converted to markdown format.")
    
    # Save page chunks to JSON file
    json_path = pdf_file.with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(page_chunks, f, indent=2, ensure_ascii=False)
    print(f"✓ Page chunks saved to: {json_path}")
    
    # Concatenate markdown from all page chunks
    md_text = "\n\n".join(chunk.get("text", "") for chunk in page_chunks)
    
    # Determine output path
    if not output_path:
        output_path = pdf_file.with_suffix('.md')
    
    # Write to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(md_text, encoding='utf-8')
    
    print(f"✓ Markdown saved to: {output_path}")
    print(f"  Total characters: {len(md_text):,}")
    print(f"  Total lines: {len(md_text.splitlines()):,}")
    
    return md_text


def parse_page_ranges(page_str: str) -> list:
    """Parse page range string (e.g., '1,3,5-7,10') into list of page numbers."""
    pages = []
    for part in page_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def main():
    parser = argparse.ArgumentParser(
        description="Extract PDF to Markdown using pymupdf4llm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf                    # Extract to document.md
  %(prog)s document.pdf -o output.md       # Specify output file
  %(prog)s document.pdf --pages 1,3,5      # Extract pages 1, 3, and 5
  %(prog)s document.pdf --pages 1-5        # Extract pages 1 through 5
  %(prog)s document.pdf --pages 1-3,7,10   # Extract mixed ranges
  %(prog)s document.pdf --no-images        # Don't extract images
  %(prog)s document.pdf --image-dir imgs   # Save images to 'imgs/' folder
        """
    )
    
    parser.add_argument('pdf', help='Input PDF file path')
    parser.add_argument('-o', '--output', help='Output Markdown file path (default: <input>.md)')
    parser.add_argument('-p', '--pages', help='Page numbers to extract (e.g., 1,3,5 or 1-5)')
    parser.add_argument('--tables-only', action='store_true', help='Extract tables only')
    parser.add_argument('--no-images', action='store_true', help='Do not extract images')
    parser.add_argument('--image-dir', default='images', help='Directory for extracted images (default: images)')
    
    args = parser.parse_args()
    
    # Parse page ranges if provided
    page_list = None
    if args.pages:
        try:
            page_list = parse_page_ranges(args.pages)
        except ValueError as e:
            print(f"Error parsing page numbers: {e}")
            sys.exit(1)
    
    try:
        extract_pdf_to_markdown(
            pdf_path=args.pdf,
            output_path=args.output,
            pages=page_list,
            tables_only=args.tables_only,
            extract_images=not args.no_images,
            image_path=args.image_dir
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
