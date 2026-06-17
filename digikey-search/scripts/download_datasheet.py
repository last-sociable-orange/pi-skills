#!/usr/bin/env python3
"""
DigiKey Datasheet Downloader — Fast-Fail Helper Script

Downloads a datasheet PDF from a URL with strict validation at every step.
Returns a clear exit code so the calling agent can determine the next action.

Exit Codes:
    0 — Success: valid PDF downloaded and verified
    1 — HTTP error: URL not accessible (4xx, 5xx, DNS failure, connection refused, timeout)
    2 — Content-Type mismatch: server response is not a PDF
    3 — File validation failed: empty file or missing PDF header (%PDF)
    4 — Invalid URL: empty, malformed, or non-http/https scheme

Usage:
    python3 download_datasheet.py <datasheet_url> <output_path> [--timeout SECONDS]
"""

import os
import sys
import argparse

import requests


def validate_url(url: str) -> str | None:
    """Validate and normalize the datasheet URL.
    
    Returns normalized URL or None if invalid.
    """
    if not url or not url.strip():
        return None

    url = url.strip()

    # Normalize: prepend https: if missing protocol
    if url.startswith("//"):
        url = "https:" + url
    elif url.startswith("http://"):
        pass  # keep as-is, though https is preferred
    elif not url.startswith("http"):
        # Some URLs come without any scheme — try https
        url = "https://" + url

    # Reject non-http schemes
    if not (url.startswith("http://") or url.startswith("https://")):
        return None

    return url


def download_pdf(url: str, output_path: str, timeout: int = 30) -> int:
    """Download a PDF with fast-fail validation at each stage.
    
    Returns exit code (0 = success).
    """
    # --- Stage 1: URL Validation ---
    normalized_url = validate_url(url)
    if normalized_url is None:
        print(f"ERROR [exit=4]: Invalid URL — empty, malformed, or non-http scheme", file=sys.stderr)
        print(f"       Original: {url!r}", file=sys.stderr)
        return 4

    url = normalized_url

    # --- Stage 2: HEAD request to check accessibility ---
    try:
        head_resp = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; CircuitPilot/1.0; +https://circuithub.com)"
            },
        )
        head_resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        print(f"ERROR [exit=1]: HTTP {status} — HEAD request failed for {url}", file=sys.stderr)
        return 1
    except requests.exceptions.ConnectionError:
        print(f"ERROR [exit=1]: Connection refused — unable to reach {url}", file=sys.stderr)
        return 1
    except requests.exceptions.Timeout:
        print(f"ERROR [exit=1]: Timeout — HEAD request timed out ({timeout}s) for {url}", file=sys.stderr)
        return 1
    except requests.exceptions.TooManyRedirects:
        print(f"ERROR [exit=1]: Too many redirects for {url}", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"ERROR [exit=1]: HEAD request failed — {e}", file=sys.stderr)
        return 1

    # --- Stage 3: Content-Type validation ---
    content_type = (head_resp.headers.get("Content-Type", "") or "").lower()
    if "application/pdf" not in content_type and "application/octet-stream" not in content_type:
        # Some servers return text/html for direct PDF links but the actual
        # redirect chain ends at a PDF. We'll be lenient here and let the
        # GET request determine the final content type, but we'll warn.
        if "text/html" in content_type:
            print(f"WARNING: HEAD returned Content-Type: text/html (may be a landing page, not a direct PDF)", file=sys.stderr)
            print(f"       URL: {url}", file=sys.stderr)
            # Don't fail here — the GET might follow a redirect to the actual PDF
        else:
            print(f"ERROR [exit=2]: Content-Type is '{content_type}' — expected 'application/pdf'", file=sys.stderr)
            print(f"       URL: {url}", file=sys.stderr)
            # Still try the GET to be sure
            print(f"       Attempting GET anyway to verify...", file=sys.stderr)

    # --- Stage 4: Full GET download with streaming ---
    try:
        response = requests.get(
            url,
            stream=True,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; CircuitPilot/1.0; +https://circuithub.com)"
            },
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        print(f"ERROR [exit=1]: HTTP {status} — GET request failed for {url}", file=sys.stderr)
        return 1
    except requests.exceptions.ConnectionError:
        print(f"ERROR [exit=1]: Connection refused during download — {url}", file=sys.stderr)
        return 1
    except requests.exceptions.Timeout:
        print(f"ERROR [exit=1]: Timeout during download ({timeout}s) for {url}", file=sys.stderr)
        return 1
    except requests.exceptions.TooManyRedirects:
        print(f"ERROR [exit=1]: Too many redirects during download for {url}", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"ERROR [exit=1]: Download failed — {e}", file=sys.stderr)
        return 1

    # --- Stage 5: Check final Content-Type from GET response ---
    final_content_type = (response.headers.get("Content-Type", "") or "").lower()
    if "application/pdf" not in final_content_type and "application/octet-stream" not in final_content_type:
        print(f"ERROR [exit=2]: Final Content-Type is '{final_content_type}' — not a PDF", file=sys.stderr)
        print(f"       URL: {url}", file=sys.stderr)
        # We could still save it if the user insists, but fail fast by default
        return 2

    # --- Stage 6: Write to disk ---
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
    except OSError as e:
        print(f"ERROR [exit=3]: Failed to write file — {e}", file=sys.stderr)
        return 3

    # --- Stage 7: Verify file on disk ---
    if not os.path.exists(output_path):
        print(f"ERROR [exit=3]: File was not created at {output_path}", file=sys.stderr)
        return 3

    file_size = os.path.getsize(output_path)
    if file_size == 0:
        print(f"ERROR [exit=3]: Downloaded file is empty (0 bytes) — {output_path}", file=sys.stderr)
        os.remove(output_path)
        return 3

    # Check PDF magic bytes: %PDF
    with open(output_path, "rb") as f:
        header = f.read(4)
    if header != b"%PDF":
        print(f"ERROR [exit=3]: File does not start with PDF header (%PDF). Header: {header!r}", file=sys.stderr)
        print(f"       This is likely not a valid PDF file.", file=sys.stderr)
        os.remove(output_path)
        return 3

    # --- Success ---
    file_size_kb = file_size / 1024
    print(f"SUCCESS: Downloaded {file_size_kb:.1f} KB to {output_path}", file=sys.stderr)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Download a datasheet PDF with fast-fail validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exit Codes:\n"
            "  0  Success — valid PDF downloaded and verified\n"
            "  1  HTTP/network error — URL not accessible\n"
            "  2  Content-Type mismatch — response is not a PDF\n"
            "  3  File validation failed — empty or invalid PDF\n"
            "  4  Invalid URL — empty, malformed, or non-http scheme"
        ),
    )
    parser.add_argument("url", help="Datasheet URL to download")
    parser.add_argument("output", help="Output file path")
    parser.add_argument(
        "--timeout", type=int, default=30,
        help="Request timeout in seconds (default: 30)"
    )
    args = parser.parse_args()

    exit_code = download_pdf(args.url, args.output, timeout=args.timeout)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
