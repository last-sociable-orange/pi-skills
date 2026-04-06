#!/usr/bin/env python3
"""
Markdown Post-Process Script

Removes image OCR text marked with delimiters from extracted Markdown files.

Deletes text between "**----- Start of picture text -----**" and 
"**----- End of picture text -----**" (inclusive).
"""

import argparse
import re
import sys


def remove_image_ocr_text(markdown_text: str) -> str:
    """
    Remove image OCR text between the delimiters.
    
    Args:
        markdown_text: The input Markdown content
        
    Returns:
        Cleaned Markdown content with OCR text removed
    """
    # Pattern to match the start and end delimiters with anything in between
    # The delimiters are: **----- Start of picture text -----** and **----- End of picture text -----**
    pattern = r'\*\*----- Start of picture text -----\*\*.*?\*\*----- End of picture text -----\*\*'
    
    # Use re.DOTALL to make . match newlines as well
    cleaned_text = re.sub(pattern, '', markdown_text, flags=re.DOTALL)
    
    # Clean up multiple blank lines that may result from removal
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text


def process_file(input_path: str, output_path: str = None) -> None:
    """
    Process a Markdown file and remove image OCR text.
    
    Args:
        input_path: Path to input Markdown file
        output_path: Path to output Markdown file (if None, overwrites input)
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    cleaned_content = remove_image_ocr_text(content)
    
    # Determine output path
    output_path = output_path or input_path
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Successfully cleaned: {output_path}")
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Remove image OCR text from Markdown files.'
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output Markdown file path (default: overwrites input)'
    )
    
    args = parser.parse_args()
    process_file(args.input, args.output)


if __name__ == '__main__':
    main()