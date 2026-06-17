---
name: digikey-search
description: "Search the DigiKey API for electronic components, extract part information (MPN, manufacturer, package, pricing, parameters), and download datasheet PDFs with fast-fail validation. Use this skill whenever the user needs to look up a component on DigiKey — by keyword, part number, or description — and optionally download its official datasheet. Also triggers when the user says 'search DigiKey', 'find a part on Digikey', 'get datasheet from Digikey', 'look up component', or needs to research parts for a design. Do NOT use for general web searches, competitor distributor searches, or non-component lookups."
allowed-tools: Bash(uv:*), Bash(curl:*), Bash(python3:*)
---

# DigiKey Search — Part Lookup & Datasheet Download

This skill provides a two-step workflow for looking up electronic components on DigiKey and downloading their official datasheets.

## Prerequisites

### 1. Environment & Authentication

The DigiKey Search API uses OAuth2 tokens stored in a `.token` file. This file is located in the project's `kicad_lib_gen/` directory:

```
<Project>/kicad_lib_gen/.token
```

**If the `.token` file does not exist or authentication fails:**
Run the DigiKey authentication flow:

```bash
cd <project>/kicad_lib_gen
uv run digikey_auth.py --user <client_id> --secret <client_secret>
```

The user must provide valid DigiKey API credentials (Client ID and Client Secret from [DigiKey Developer Portal](https://developer.digikey.com/)). Follow the on-screen instructions to authorize via browser and paste back the redirect URL.

### 2. Tool Locations

All DigiKey tools are in `<Project>/kicad_lib_gen/`. Always use `uv run` from that directory:

```bash
cd <Project>/kicad_lib_gen
uv run digikey_search.py "<keywords>" [--limit N] [--offset N] [--json]
```

---

## Workflow 1: Search DigiKey for a Part

**Use this when the user needs to find a component, get pricing, check availability, or research alternatives.**

### Step 1: Determine Search Keywords

Ask the user what they're looking for. Keywords can be:
- A full or partial **manufacturer part number** (e.g., `TJA1051TK/3`, `BAT54`)
- A **product description** (e.g., `CAN transceiver 5V 8-pin`)
- A **product series** (e.g., `TPS62870`)
- A **component type** + **specs** (e.g., `10kΩ 0603 1% thick film resistor`)

If the user provides a partial or vague keyword, suggest refining it for better results.

### Step 2: Run the Search

```bash
cd <Project>/kicad_lib_gen
uv run digikey_search.py "<keywords>" --limit 10 --json
```

**Parameters:**
- `keywords` (required) — Search term(s) in quotes
- `--limit` (optional, default: 10) — Max results to return (max 50)
- `--offset` (optional, default: 0) — Pagination offset
- `--json` (required for agent use) — Output clean summarized JSON to stdout

### Step 3: Parse the Results

The `--json` flag produces a structured JSON output on stdout:

```json
{
  "keywords": "TJA1051TK/3",
  "limit": 10,
  "offset": 0,
  "total_products": 1,
  "products": [
    {
      "main_category": "Integrated Circuits (ICs)",
      "id": "Integrated Circuits (ICs)/Interface/Drivers, Receivers, Transceivers/TJA1051TK/3",
      "description": "IC TRANSCEIVER HALF 1/1 8HVSON",
      "keywords": "TJA1051TK/3",
      "value": "TJA1051TK/3",
      "manufacturer": "NXP USA Inc.",
      "manufacturer_product_number": "TJA1051TK/3",
      "package": "8-VDFN Exposed Pad",
      "kicad_symbol_library": "",
      "kicad_footprint_library": "",
      "part_status": "Active",
      "qty_available": "5726",
      "distributor": "Digikey",
      "distributor_product_number": "568-15748-1-ND",
      "unit_price": "1.56000@1",
      "product_url": "https://www.digikey.com/product-detail/en/...",
      "datasheet_url": "https://www.nxp.com/docs/en/data-sheet/TJA1051.pdf",
      "parameters": [
        {"param": "Type", "value": "Transceiver"},
        {"param": "Protocol", "value": "CANbus"},
        {"param": "NumberofDrivers/Receivers", "value": "1/1"},
        {"param": "Package/Case", "value": "8-VDFNExposedPad"}
      ]
    }
  ]
}
```

**Key fields for the agent:**
| Field | Description |
|-------|-------------|
| `manufacturer_product_number` | Manufacturer's part number (MPN) |
| `manufacturer` | Manufacturer name |
| `description` | Short product description |
| `package` | Package type |
| `datasheet_url` | URL to the official datasheet PDF |
| `product_url` | DigiKey product page URL |
| `qty_available` | Current stock quantity |
| `unit_price` | Pricing info (price@breakQty format) |
| `part_status` | Active/Obsolete/NotForNewDesigns |
| `parameters` | Array of {param, value} with detailed specs |

**Normalization note:** The `datasheet_url` field may come with or without a protocol prefix. If it starts without `http`, prepend `https:`.

### Step 4: Present Results to the User

If multiple results are returned, present them in a table with the most relevant fields and ask the user to select the correct one:

| # | MPN | Manufacturer | Description | Package | Status | Qty |
|---|-----|-------------|-------------|---------|--------|-----|
| 1 | TJA1051TK/3 | NXP | CAN Transceiver 1/1 | 8-HVSON | Active | 5,726 |
| 2 | TJA1051T/3 | NXP | CAN Transceiver 1/1 | 8-SOIC | Active | 12,340 |

If the user's keyword is an exact MPN and there's exactly 1 result, proceed directly.

### Step 5: Advanced Filtering (Optional)

If too many results are returned, ask the user to refine their search with more specific keywords (e.g., add package type, specs, or manufacturer name). Run the search again with refined keywords.

---

## Workflow 2: Download a Datasheet PDF (Fast-Fail)

**Use this when the user wants to download the official datasheet PDF for a component found in Workflow 1.**

### Fast-Fail Principle

"Fail fast" means:
1. **Validate the URL** before attempting download — reject empty, malformed, or non-http URLs immediately.
2. **Check HTTP accessibility** — use a HEAD request to verify the URL returns a 200 status with the correct Content-Type.
3. **Abort on HTTP errors** — any 4xx or 5xx response is treated as immediate failure.
4. **Verify downloaded content** — check the file is non-empty and starts with the PDF magic bytes `%PDF`.

### Method A: Using the Helper Script (Recommended)

Use the provided Python helper script for robust download with full validation:

```bash
python3 scripts/download_datasheet.py <datasheet_url> <output_path>
```

The script performs all fast-fail checks and returns a clear exit code:

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success — valid PDF downloaded |
| 1 | HTTP error — URL not accessible (4xx/5xx, DNS failure, connection refused) |
| 2 | Content-Type mismatch — server did not return a PDF |
| 3 | File validation failed — empty file or missing PDF header |
| 4 | Invalid URL — empty, malformed, or non-http scheme |

**Example:**

```bash
python3 scripts/download_datasheet.py \
  "https://www.nxp.com/docs/en/data-sheet/TJA1051.pdf" \
  "./IC-TJA1051-DS.pdf"
```

### Method B: Manual Download with curl (Fallback)

If the helper script is unavailable, use `curl` with strict flags:

```bash
# Check URL is accessible (HEAD request)
curl --fail --location --head --silent --output /dev/null \
  --write-out "%{http_code}" \
  "<datasheet_url>"

# Download with fast-fail flags
curl --fail --fail-early --location --output "<output>.pdf" "<datasheet_url>"

# Verify downloaded file
file "<output>.pdf"        # Should say "PDF document"
stat --format="%s" "<output>.pdf"  # Should be > 0 bytes
```

**curl flags explained:**
- `--fail` — Fail silently on HTTP errors (no output, non-zero exit)
- `--fail-early` — Fail on the first network error (no retries)
- `--location` — Follow redirects (most datasheet URLs redirect)
- `--output` — Save to file

### URL Normalization

If the `datasheet_url` from the search result does not start with `http`, prepend `https:`:

```
Before:  //www.nxp.com/docs/en/data-sheet/TJA1051.pdf
After:   https://www.nxp.com/docs/en/data-sheet/TJA1051.pdf
```

### Handling Download Failures

If the download fails (exit code ≠ 0):

1. **Log the failure** — print the URL and error to stderr.
2. **Check the product URL** — the `product_url` field from search results points to the DigiKey product page. The datasheet link may be embedded there as an alternative.
3. **Ask the user** — inform them that the datasheet URL is not accessible and ask for:
   - An alternative source (manufacturer website, another distributor)
   - Or to manually download and place the PDF in `WIP/` for processing

---

## Workflow 3: Full Pipeline — Search + Download + File Processing

**Use this when the user asks to find a part AND save its datasheet into the project.**

### Step 1: Search

Run the search with the user's keywords. Confirm the correct part with the user.

### Step 2: Download

Extract the `datasheet_url` from the selected product. Use the helper script to download with fast-fail validation.

### Step 3: Move to Project Datasheet Workflow

Follow the project's file processing stages:

1. **Rename** the downloaded PDF to follow naming conventions:
   - Format: `<ProductType>-<ProductNumber>-DS.pdf`
   - Example: `IC-TJA1051-DS.pdf`
   - Product types follow reference designator conventions (IC, D, Q, R, C, L, etc.)
   - Ask the user if the product type is not in the standard list
2. **Move** to `Datasheet/.wip/` (WIP stage).
3. **Report** to the user that the datasheet has been downloaded and is ready for document processing (PDF → Markdown).
4. If the project has a dedicated document processing agent (e.g., `kicad-worker`, `doc-agent`), hand off the file to them for conversion.

### Step 4: Report to User

Provide a summary:

```
## DigiKey Search Complete

**Part:** TJA1051TK/3 — NXP USA Inc.
**Package:** 8-HVSON
**Status:** Active
**Qty Available:** 5,726
**Datasheet:** IC-TJA1051-DS.pdf (downloaded, in Datasheet/.wip/)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError: Authentication token not found` | The `.token` file is missing or in the wrong location. Run `uv run digikey_auth.py --user <id> --secret <key>` from `kicad_lib_gen/`. |
| `401 Unauthorized` | Token expired. The search script handles auto-refresh, but if refresh token has expired, re-run `digikey_auth.py`. |
| `No results found` | Try broader keywords, remove filters, check spelling of the MPN. |
| `Download returns HTML instead of PDF` | Some manufacturers serve a landing page instead of direct PDF. Try the `product_url` to find the actual datasheet link, or ask the user for an alternative source. |
| `curl: (22) The requested URL returned error: 404` | The datasheet URL is broken or outdated. Use the `product_url` to find the correct link on the DigiKey product page. |
| Download succeeds but file is 0 bytes | The server returned an empty response. Try downloading again or from an alternative source. |

## Best Practices

- **Do** present search results in a clear table for the user to choose from.
- **Do** ask the user to confirm the correct part before downloading.
- **Do** normalize the datasheet URL (prepend `https:` if missing).
- **Do** verify downloaded files with `file` command and size check.
- **Do** report all failures with specific error messages — don't summarize failures away.
- **Do NOT** guess the correct part if multiple results are returned — always ask.
- **Do NOT** retry failed downloads automatically — fail fast and report.
- **Do NOT** use the search API without valid authentication — guide the user through auth setup.
- **Do NOT** modify the `.token` file manually.
