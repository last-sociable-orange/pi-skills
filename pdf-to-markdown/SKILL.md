---
name: pdf-to-markdown
description: Extract PDF files to Markdown format using pymupdf4llm. Supports text extraction, table conversion, image extraction with page chunking output to JSON for future cross-referencing.
---

# PDF to Markdown Extractor

This skill extracts PDF content to Markdown format using the `pymupdf4llm` library. `pdf_to_markdown.py` is included in `./scripts`.

## Features

- Extracts text with formatting (bold, italic, headers)
- Converts tables to Markdown table format
- Extracts images with references in Markdown
- Outputs page chunks as JSON (same filename as input PDF)
- Configurable page ranges
- Headers/footers excluded by default

## Usage

```bash
python pdf_to_markdown.py <input.pdf> [options]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `pdf` | Input PDF file path (required) | - |
| `-o, --output` | Output Markdown file path | `<input>.md` |
| `-p, --pages` | Page numbers to extract (e.g., `1,3,5` or `1-5`) | All pages |
| `--no-images` | Do not extract images | Images extracted |
| `--image-dir` | Directory for extracted images | `images/` |
| `--tables-only` | Note for post-processing tables | False |

### Examples

```bash
# Basic extraction
python pdf_to_markdown.py document.pdf

# Specific output file
python pdf_to_markdown.py document.pdf -o output.md

# Extract specific pages
python pdf_to_markdown.py document.pdf --pages 1,3,5
python pdf_to_markdown.py document.pdf --pages 1-5
python pdf_to_markdown.py document.pdf --pages 1-3,7,10

# No images
python pdf_to_markdown.py document.pdf --no-images

# Custom image directory
python pdf_to_markdown.py document.pdf --image-dir my_images
```

## Output Files

| File | Description |
|------|-------------|
| `<input>.md` | Extracted Markdown content |
| `<input>.json` | Page chunks as JSON array (one object per page) |
| `<image_dir>/` | Directory containing extracted images |

## Markdown Post Process

Delete image OCR text  marked with "**----- Start of picture text -----**" and "**----- End of picture text -----**",  and any text in between.

Example:

**----- Start of picture text -----**

MODE<br>CONTROL<br>5<br>EN [(2)]<br>4<br>**----- End of picture text -----**<br>



## JSON Output Format

The JSON file contains a list of page chunk dictionaries:

```json
[
  {
    "page": 0,
    "text": "Markdown text for page 1...",
    ...
  },
  {
    "page": 1,
    "text": "Markdown text for page 2...",
    ...
  }
]
```

## Requirements

Install the required dependency:

```bash
pip install pymupdf4llm
```
