# PCB Export Commands Reference

This file documents all `flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export` commands and their options in detail. Read this when the user needs specific PCB export options beyond the quick summary in SKILL.md.

---

## `pcb export gerbers` — Gerber RS-274X

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export gerbers [options] INPUT_FILE
```

**Output:** One file per layer.

**Options:**
- `-o <dir>` — Output directory (default: current dir)
- `-l <layers>` — Layers to plot (default: all). Comma-separated, e.g. `F.Cu,B.Cu`
- `--cl <layers>` — Common layers to include on all output files
- `--drawing-sheet <path>` — Override drawing sheet
- `-D <key>=<value>` — Define variable (repeatable)
- `--erd` — Exclude refdes
- `--ev` — Exclude values
- `--ibt` — Include border/title
- `--sp` — Sketch pads on fab layers
- `--hdnp` — Hide DNP footprints on fab
- `--sdnp` — Sketch DNP footprints on fab
- `--cdnp` — Cross out DNP footprints on fab
- `--no-x2` — Don't use extended X2 format
- `--no-netlist` — Omit netlist attributes
- `--subtract-soldermask` — Remove silkscreen where no soldermask
- `--disable-aperture-macros`
- `--use-drill-file-origin`
- `--precision 5|6` — Digits (default: 6)
- `--no-protel-ext` — Use `.gbr` extension instead of `.gbl/.gtl/...`
- `--check-zones` — Refill zones before export
- `--variant <name>` — Board variant
- `--board-plot-params` — Use plot settings from board file

---

## `pcb export drill` — Drill/NC files

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export drill [options] INPUT_FILE
```

**Options:**
- `-o <dir>` — Output directory
- `--format excellon|gerber` (default: excellon)
- `--drill-origin absolute|plot` (default: absolute)
- `--excellon-zeros-format decimal|suppressleading|suppresstrailing|keep`
- `--excellon-oval-format route|alternate`
- `--excellon-units mm|in`
- `--excellon-mirror-y`
- `--excellon-min-header`
- `--excellon-separate-th` — Separate files for plated/non-plated
- `--generate-map` — Create map file
- `--generate-report` — Create hit report
- `--report-path <file>` — Report filename
- `--generate-tenting` — Separate files for tented hits (Gerber X2 only)
- `--map-format pdf|gerberx2|ps|dxf|svg`
- `--gerber-precision 5|6` (default: 6)

---

## `pcb export pos` — Position file (pick-and-place)

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export pos [options] INPUT_FILE
```

**Options:**
- `--side front|back|both` (default: both)
- `--format ascii|csv|gerber` (default: ascii)
- `--units in|mm` (default: in; no effect for Gerber)
- `--bottom-negate-x`
- `--use-drill-file-origin`
- `--smd-only`
- `--exclude-fp-th` — Exclude through-hole footprints
- `--exclude-dnp`
- `--gerber-board-edge`
- `--variant <name>`

---

## `pcb export pdf` — PCB to PDF

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export pdf [options] INPUT_FILE
```

**Options:**
- `-o <dir|file>` — Output dir (separate mode) or file (single/multipage)
- `-l <layers>` — Layers to plot (required for separate/multipage)
- `--cl <layers>` — Common layers on all pages
- `--drawing-sheet <path>`
- `-D <key>=<value>`
- `-m` / `--mirror`
- `--erd`, `--ev`, `--ibt`
- `--subtract-soldermask`
- `--sp`, `--hdnp`, `--sdnp`, `--cdnp`
- `-n` / `--negative`
- `--black-and-white`
- `-t <theme>`
- `--drill-shape-opt 0|1|2` (0=none, 1=small, 2=actual)
- `--mode-single` — All layers on one page
- `--mode-separate` — One file per layer
- `--mode-multipage` — One file, one page per layer
- `--scale <n>` — Scale factor (0 = autoscale)
- `--bg-color <color>` — Hex (#rrggbb or #rrggbbaa) or CSS
- `--check-zones`
- `--variant <name>`

---

## `pcb export svg` — PCB to SVG

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export svg [options] INPUT_FILE
```

**Options:** Similar to PDF export but with these unique options:
- `--page-size-mode 0|1|2` — 0=fit sheet, 1=match page, 2=fit board
- `--fit-page-to-board` — Equivalent to `--page-size-mode 2`
- `--exclude-drawing-sheet`
- `--mode-single` / `--mode-multi`

---

## `pcb export step` / `stpz` / `stl` / `glb` / `ply` / `brep` / `xao` — 3D model exports

These all share a very similar set of options. The common pattern:

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export step [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export stpz [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export stl [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export glb [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export ply [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export brep [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export xao [options] INPUT_FILE
```

**Extensions:** `.step`, `.stpz`, `.stl`, `.glb`, `.ply`, `.brep`, `.xao`

**Shared options:**
- `-o <file>` — Output filename
- `-D <key>=<value>` — Define variable (repeatable)
- `-f` / `--force` — Overwrite existing file
- `--no-unspecified` — Exclude "unspecified" footprint type 3D models
- `--no-dnp` — Exclude "Do not populate" components
- `--variant <name>` — Board variant
- `--grid-origin` / `--drill-origin` — Origin selection
- `--subst-models` — Replace VRML with STEP/IGS
- `--board-only` — Exclude component models
- `--cut-vias-in-body` — Cut via holes in board body
- `--no-board-body` — Exclude board body
- `--no-components` — Exclude all component 3D models
- `--component-filter <list>` — Only include matching refdes (comma-separated, wildcards)
- `--include-tracks` — Include tracks/vias on outer layers (time-consuming)
- `--include-pads` — Include pads (time-consuming)
- `--include-zones` — Include zones (time-consuming)
- `--include-inner-copper` — Include inner layer copper
- `--include-silkscreen` — Silkscreen as flat faces
- `--include-soldermask` — Soldermask as flat faces
- `--fuse-shapes` — Fuse overlapping geometry (time-consuming)
- `--fill-all-vias` — Don't cut via holes in conductor layers
- `--no-extra-pad-thickness` — Don't add 0.005mm pad thickness
- `--min-distance <n>` — Coincident point tolerance (default: 0.01mm)
- `--net-filter <wildcard>` — Only copper items matching net
- `--user-origin <XxY>` — Custom origin (e.g. `1x1in`, `25.4x25.4mm`)

**STEP/stpz-only:**
- `--no-optimize-step` — Write parametric curves (smaller files, less compatible)

**VRML-only:**
- `--user-origin <XxY>` — Custom origin (default: board center)
- `--units mm|m|in|tenths` (default: in)
- `--models-dir <dir>` — Copy models into directory
- `--models-relative` — Use relative paths in output

---

## `pcb export ipc2581` — IPC-2581

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export ipc2581 [options] INPUT_FILE
```

**Options:**
- `--precision <n>` — Decimal digits (default: 6)
- `--compress` — ZIP output
- `--version B|C` — Standard version (default: C)
- `--units mm|in` (default: mm)
- `--bom-col-int-id <field>` — BOM Internal ID field
- `--bom-col-mfg-pn <field>` — BOM Manufacturer Part Number field
- `--bom-col-mfg <field>` — BOM Manufacturer field
- `--bom-col-dist-pn <field>` — BOM Distributor Part Number field
- `--bom-col-dist <field>` — BOM Distributor field
- `--bom-rev <revision>` — BOM revision
- `--variant <name>`, `--drawing-sheet <path>`, `-D <key>=<value>`

---

## `pcb export odb` — ODB++

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export odb [options] INPUT_FILE
```

**Options:**
- `--precision <n>` (default: 2)
- `--compression none|zip|tgz` (default: zip)
- `--units mm|in` (default: mm)
- `--variant <name>`, `--drawing-sheet <path>`, `-D <key>=<value>`

---

## `pcb export ipcd356` — IPC-D-356 netlist

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export ipcd356 [options] INPUT_FILE
```

Minimal options: `-o <file>`, `-h`.

---

## `pcb export gencad` — GenCAD

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export gencad [options] INPUT_FILE
```

**Options:**
- `--flip-bottom-pads`
- `--unique-pins`
- `--unique-footprints`
- `--use-drill-origin`
- `--store-origin-coord`
- `-D <key>=<value>`

---

## `pcb export stats` — Board statistics

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export stats [options] INPUT_FILE
```

**Options:**
- `--format report|json` (default: report)
- `--units mm|in` (default: mm)
- `--exclude-footprints-without-pads`
- `--subtract-holes-from-board`
- `--subtract-holes-from-copper`

---

## `pcb export dxf` — DXF

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export dxf [options] INPUT_FILE
```

**Options:** Similar to SVG export with these additions:
- `--ou mm|in` — Output units (default: in)
- `--uc` / `--use-contours` — Plot using contours
- `--udo` / `--use-drill-origin`
- `--mode-single` / `--mode-multi`

---

## `pcb export ps` — PostScript

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export ps [options] INPUT_FILE
```

**Options:** Similar to PDF export with these additions:
- `-C <mm>` — Track width correction
- `-X <factor>` — X scale adjust
- `-Y <factor>` — Y scale adjust
- `-A` / `--force-a4`
- `--mode-single` / `--mode-multi`

---

## `pcb export 3dpdf` / `u3d` — 3D PDF

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export 3dpdf [options] INPUT_FILE
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad pcb export u3d [options] INPUT_FILE
```

Both share the same options as the 3D model exports (STEP family) listed above.
