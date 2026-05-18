---
name: kicad-cli
description: "Use the KiCad command-line interface (kicad-cli) to automate PCB, schematic, footprint, and symbol tasks. Use this skill whenever a user wants to run KiCad operations from the terminal — generating Gerber/ drill/ BOM/ netlist/ PDF/ SVG/DXF/ STEP/ STL/ GLB/ VRML/ IPC-2581/ ODB++/ position files, running DRC or ERC checks, converting or upgrading board/schematic/symbol/footprint files, importing non-KiCad board formats (Altium/EAGLE/CADSTAR/ PADS/PCAD), rendering raytraced board images, or executing jobsets — without opening the KiCad GUI. Trigger on any mention of kicad-cli, KiCad automation, PCB fabrication output, or batch processing of KiCad files."
---

# KiCad CLI Skill

The `kicad-cli` tool provides batch/automated access to KiCad operations without the GUI. The executable is `kicad-cli`.

**Run kicad-cli using flatpak:** `flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad <subcommand> [options] INPUT_FILE_OR_DIR`

## 6 Subcommands

| Subcommand | Purpose |
|---|---|
| `fp` | Footprint export/upgrade |
| `jobset` | Run predefined jobsets |
| `pcb` | DRC, exports (fabrication, 3D, graphics), import, render, upgrade |
| `sch` | ERC, exports (BOM, netlist, graphics), upgrade |
| `sym` | Symbol export/upgrade |
| `version` | Print KiCad version info |

Use `kicad-cli <subcommand> -h` for help on any command.

---

## Footprint commands (`fp`)

### `fp export svg` — Export footprint(s) to SVG

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad fp export svg [options] INPUT_FILE_OR_DIR
```

**Input:** `.kicad_mod` file or `.pretty` directory.

**Options:**
- `-o <dir>` — Output directory (default: current dir)
- `-l <layers>` — Comma-separated layers (e.g. `F.Cu,B.Cu`). Default: all layers
- `-D <key>=<value>` — Define project variable (repeatable)
- `-t <theme>` — Theme name
- `--fp <footprint>` — Specific footprint name (default: all footprints)
- `--sp` — Sketch pads on fab layers
- `--hdnp` — Hide DNP footprints on fab layers
- `--sdnp` — Sketch DNP footprints
- `--cdnp` — Cross out DNP footprints
- `--black-and-white`

### `fp upgrade` — Upgrade footprint library format

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad fp upgrade [options] INPUT_FILE_OR_DIR
```

**Options:** `-o <dir>` (output dir), `--force` (re-save even if current).

**Supported input formats:** KiCad (.kicad_mod, .pretty), pre-5.0 (.mod, .emp), Altium (.PcbLib, .IntLib), CADSTAR (.cpa), EAGLE (.lbr), EasyEDA (.json, .elibz/.epro/.zip), GEDA/PCB (.fp).

---

## Jobset commands (`jobset`)

### `jobset run` — Execute a predefined jobset

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad jobset run [options] INPUT_FILE
```

**Input:** A KiCad project file (`.kicad_pro` or `.kicad_sch` or `.kicad_pcb`).

**Options:**
- `--stop-on-error` — Stop after a job fails
- `-f <jobset file>` — The `.kicad_jobset` file to run
- `--output <destination>` — Destination description or ID (if omitted, all destinations are generated)

---

## PCB commands (`pcb`)

### `pcb drc` — Design Rule Check

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb drc [options] INPUT_FILE
```

**Options:**
- `-o <file>` — Output file (default: same as input with `.rpt` or `.json`)
- `-D <key>=<value>` — Define project variable (repeatable)
- `--format report|json` — Output format (default: report)
- `--all-track-errors` — Report all errors per track
- `--schematic-parity` — Check PCB vs schematic consistency
- `--units mm|in|mils` — Units (default: mm)
- `--severity-all|--severity-error|--severity-warning|--severity-exclusions`
- `--exit-code-violations` — Exit 0 if clean, 5 if violations found
- `--refill-zones` — Refill zones before DRC
- `--save-board` — Save board after DRC (only with `--refill-zones`)

### `pcb export` — PCB exports (fabrication, 3D, graphics)

See `references/pcb-export.md` for all export commands and their options.

Quick summary of available export formats:

| Command | Output format | Typical use |
|---|---|---|
| `pcb export gerbers` | Gerber RS-274X | PCB fabrication |
| `pcb export drill` | Excellon / Gerber drill | PCB fabrication |
| `pcb export pdf` | PDF | Documentation |
| `pcb export svg` | SVG | Documentation |
| `pcb export dxf` | DXF | CAD exchange |
| `pcb export pos` | Position file (ASCII/CSV/Gerber) | Pick-and-place |
| `pcb export ipc2581` | IPC-2581 XML | Fabrication |
| `pcb export odb` | ODB++ (zip/tgz) | Fabrication |
| `pcb export step` | STEP 3D | Mechanical CAD |
| `pcb export stpz` | GZIP-compressed STEP | Mechanical CAD |
| `pcb export stl` | STL 3D | 3D printing |
| `pcb export glb` | GLB (glTF binary) | 3D viewing |
| `pcb export ply` | PLY 3D | 3D mesh |
| `pcb export brep` | BREP (OCCT) | Mechanical CAD |
| `pcb export vrml` | VRML 3D | 3D viewing |
| `pcb export xao` | XAO (SALOME/Gmsh) | Simulation |
| `pcb export 3dpdf` | PDF with embedded 3D | Documentation |
| `pcb export u3d` | PDF with embedded 3D (U3D) | Documentation |
| `pcb export stats` | Statistics report (.rpt/.json) | Design analysis |
| `pcb export gencad` | GenCAD | Assembly |
| `pcb export ipcd356` | IPC-D-356 netlist | Testing |
| `pcb export ps` | PostScript | Documentation |
| `pcb export hpgl` | *(not functional in KiCad 10)* | — |

**Common cross-cutting options** (many export commands share these):
- `-D <key>=<value>` — Define project variable (repeatable)
- `--variant <name>` — Board variant (use `${VARIANT}` in output path)
- `--layers <list>` or `-l <list>` — Comma-separated layer names
- `--common-layers <list>` or `--cl <list>` — Layers to include on all outputs
- `--drawing-sheet <path>` — Override drawing sheet
- `--check-zones` — Refill zones before export (not saved)
- `--drill-origin` — Use drill origin
- `--grid-origin` — Use grid origin
- `--user-origin XxY` — Custom origin (e.g. `1x1in`, `25.4x25.4mm`)

### `pcb import` — Import non-KiCad board file

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb import [options] INPUT_FILE
```

**Options:**
- `-o <file>` — Output (default: input with `.kicad_pcb` extension)
- `--format auto|pads|altium|eagle|cadstar|fabmaster|pcad|solidworks` (default: auto-detect)
- `--report-format none|json|text` (default: none)
- `--report-file <file>` — Report output (default: stdout)

### `pcb render` — Raytraced 3D board rendering (PNG/JPEG)

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb render [options] INPUT_FILE
```

**Options:**
- `-o <file>` — **Required.** Must end in `.png`, `.jpg`, or `.jpeg`
- `-D <key>=<value>` — Define project variable (repeatable)
- `--variant <name>` — Board variant
- `-w <pixels>` — Width (default: 1600)
- `-h <pixels>` — Height (default: 900)
- `--side top|bottom|left|right|front|back` (default: top)
- `--background default|transparent|opaque`
- `--quality basic|high|user` (default: basic)
- `--preset follow_pcb_editor|follow_plot_settings|legacy_preset_flag`
- `--use-board-stackup-colors`
- `--floor` — Enable floor/shadows
- `--perspective` — Perspective (vs. orthogonal) projection
- `--zoom <n>` — Camera zoom (default: 1)
- `--pan X,Y,Z` — Camera pan (mm)
- `--pivot X,Y,Z` — Pivot point (cm, relative to board center)
- `--rotate X,Y,Z` — Rotation in degrees (e.g. `-45,0,45` for isometric)
- `--light-top|--light-bottom|--light-side|--light-camera <R,G,B|intensity>` — Light colors (0-1 range)
- `--light-side-elevation <degrees>` — Side light elevation (0-90)

### `pcb upgrade` — Upgrade board file format

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb upgrade [options] INPUT_FILE
```

**Options:** `--force` — Re-save even if already current format.

---

## Schematic commands (`sch`)

### `sch erc` — Electrical Rule Check

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch erc [options] INPUT_FILE
```

**Options:** Same severity/format pattern as `pcb drc`:
- `-o <file>`, `-D <key>=<value>`, `--format report|json`
- `--units mm|in|mils`, `--exit-code-violations`
- `--severity-all|--severity-error|--severity-warning|--severity-exclusions`

### `sch export bom` — Bill of Materials (modern)

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export bom [options] INPUT_FILE
```

**Options:**
- `-o <file>` — Output (default: `.csv`)
- `--variant <name>` — Variant
- `--preset <preset>` — Named BOM preset from schematic (e.g. "Grouped By Value")
- `--format-preset <preset>` — Named format preset (e.g. "CSV")
- `--fields <fields>` — Ordered field list. `*` = all fields. Virtual fields: `${DNP}`, `${EXCLUDE_FROM_BOARD}`. Default: `"Reference,Value,Footprint,QUANTITY,DNP"`
- `--labels <labels>` — Labels for fields. Default: `"Refs,Value,Footprint,Qty,DNP"`
- `--group-by <fields>` — Fields to group by
- `--sort-field <field>` — Sort field (default: "Reference")
- `--sort-asc` — Ascending sort
- `--filter <pattern>` — Wildcard filter on refdes (`*` and `?` supported)
- `--exclude-dnp` — Exclude "Do not populate" components
- `--field-delimiter <char>` — Column separator (default: `","`)
- `--string-delimiter <char>` — Field quoting character
- `--ref-delimiter <char>` — Reference separator (default: `","`)
- `--ref-range-delimiter <char>` — Range separator (default: `"-"`)
- `--keep-tabs` / `--keep-line-breaks`

### `sch export python-bom` — BOM via legacy XML (for custom scripts)

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export python-bom [options] INPUT_FILE
```

Produces `-bom.xml` file for post-processing with Python scripts.

### `sch export netlist` — Netlist export

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export netlist [options] INPUT_FILE
```

**Options:**
- `--format kicadsexpr|kicadxml|cadstar|orcadpcb2|spice|spicemodel|pads|allegro` (default: kicadsexpr)

### `sch export pdf` / `sch export svg` / `sch export dxf` / `sch export ps`

These all follow a similar pattern:

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export pdf [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export svg [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export dxf [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export ps [options] INPUT_FILE
```

**Common options:**
- `-o <path>` — Output file (PDF) or directory (SVG/DXF/PS)
- `--drawing-sheet <path>` — Override drawing sheet
- `-D <key>=<value>` — Define project variable
- `--variant <name>` — Schematic variant
- `-t <theme>` — Theme name
- `-b` / `--black-and-white`
- `-e` / `--exclude-drawing-sheet`
- `--default-font <name>` (default: "KiCad Font")
- `--draw-hop-over` — Hop-overs at wire crossings
- `--pages <list>` — Comma-separated page numbers to export (default: all)
- `--no-background-color` (SVG, PS)

**PDF-specific options:**
- `--exclude-pdf-property-popups`
- `--exclude-pdf-hierarchical-links`
- `--exclude-pdf-metadata`

### `sch upgrade` — Upgrade schematic file format

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch upgrade [options] INPUT_FILE
```

**Options:** `--force`. Note: only upgrades the root sheet, not child sheets.

---

## Symbol commands (`sym`)

### `sym export svg` — Export symbol(s) to SVG

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sym export svg [options] INPUT_FILE
```

**Input:** Symbol library file (e.g. `.kicad_sym`).

**Options:**
- `-o <dir>` — Output directory (default: current dir)
- `-t <theme>` — Theme name
- `-s <symbol>` — Specific symbol (default: all)
- `--black-and-white`
- `--include-hidden-pins`
- `--include-hidden-fields`

### `sym upgrade` — Upgrade symbol library format

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sym upgrade [options] INPUT_FILE_OR_DIR
```

**Supported input formats:** KiCad (.kicad_sym), pre-6.0 (.lib), Altium (.SchLib, .IntLib), CADSTAR (.lib), EAGLE (.lbr), EasyEDA (.json, .elibz/.epro/.zip).

**Options:**
- `-o <file_or_dir>` — Output file (packed) or directory (unpacked)
- `--force`

---

## Version command

### `version` — Print KiCad version

```
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad version [options]
```

**Options:**
- `--format plain|commit|about` — `plain` prints version number (e.g. `7.0.7`), `commit` prints git hash, `about` prints full version+library+system info (use for bug reports)

---

## Recipes / Common workflows

### Generate Gerber + drill files for fabrication

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export gerbers -o gerbers/ --layers F.Cu,B.Cu,F.Silkscreen,F.Mask,B.Silkscreen,B.Mask,Edge.Cuts board.kicad_pcb
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export drill -o gerbers/ --format excellon --drill-origin plot --generate-map --map-format pdf board.kicad_pcb
```

### Generate BOM from schematic

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export bom --fields "Reference,Value,Footprint,QUANTITY,DNP,MPN" --labels "Refs,Value,Footprint,Qty,DNP,MPN" -o bom.csv schematic.kicad_sch
```

### Export STEP 3D model of PCB with components

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export step -o board.step --include-tracks --include-pads board.kicad_pcb
```

### Run DRC and get JSON report

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb drc --format json --exit-code-violations -o drc.json board.kicad_pcb
echo "Exit code: $?"  # 0 = clean, 5 = violations
```

### Render isometric board image

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb render -o render.png --rotate "-45,0,45" --side top --width 1920 --height 1080 --quality high board.kicad_pcb
```

### Import Altium PCB to KiCad

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb import --format altium --report-format text board.PcbDoc
```

### Run a jobset

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad jobset run -f my_jobset.kicad_jobset project.kicad_pro
```

### Export all footprints from a library

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad fp export svg -o footprints_svg/ my_lib.pretty
```

### Upgrade an entire symbol library

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sym upgrade -o upgraded_lib/ legacy_lib.lib
```
