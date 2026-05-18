---
name: kicad-schematics-review
description: "Use this skill to review KiCad schematic files (.kicad_sch) for correctness, best practices, and common design issues. Trigger whenever the user wants to: review a KiCad schematic for errors and improvements, perform a structured design review of an EDA schematic, check for common mistakes and generate a formal schematic review report. This is a comprehensive design review skill covering electrical, connectivity, power, signal integrity, protection and regulation aspects. Also trigger when the user mentions 'design review', 'schematic review', 'KiCad review', or similar phrases in the context of KiCad design."
---

# KiCad Schematics Review

A structured checklist for reviewing KiCad schematic files.

## Workflow

### 1. Export BOM
```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export bom \
  --fields "Reference,Value,Footprint,DNP" \
  --labels "Ref,Value,Footprint,DNP" \
  -o bom.csv FlightController.kicad_sch
```

### 2. Export netlist
```bash
# OrCAD PCB2 format
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export netlist --format orcadpcb2 FlightController.kicad_sch

# PADS format
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export netlist --format pads FlightController.kicad_sch
```

### 3. Check for datasheets
Look for a `Knowledge/` folder in the project directory. If present, check it for datasheets for active components (ICs, transistors, modules) and reference them during the review.

### 4. Review with component checklists
For each active component, find the matching checklist in `design-checklists/` and verify each item.

## Review Checklist

Work through each domain. For each finding record: **Severity** (Critical/Major/Minor/Info), **Component/Net**, **Description**, **Recommendation**.

### 1. Electrical Rule Check (ERC)
- [ ] No unresolved ERC errors or warnings
- [ ] All power pins connected correctly
- [ ] No unconnected input pins (unless marked with NC symbol)
- [ ] No duplicate reference designators
- [ ] PWR_FLAG present on undriven power nets
- [ ] ERC exclusions are justified

### 2. Component Review
- [ ] Every component has a meaningful **Value** (not "R_US" or "C_Small")
- [ ] Every component has a **Footprint** assigned
- [ ] Reference designators use correct prefixes (R, C, U, Q, D, J, L, F, TP...)
- [ ] No gaps in reference numbering
- [ ] DNP components properly marked
- [ ] Component values are realistic

### 3. Connectivity Review
- [ ] No unconnected pins (unless marked NC)
- [ ] No single-node nets
- [ ] Bus connections correctly labeled
- [ ] Differential pairs use _P/_N naming
- [ ] Hierarchical sheet ports match parent/child
- [ ] Global labels match across sheets
- [ ] Important nets have meaningful names (not `Net-(C1-Pad1)`)

### 4. Power Domain
- [ ] Power nets have clear global labels
- [ ] Voltage levels match component requirements
- [ ] Different voltage domains separated and labeled
- [ ] Analog/digital power separated where appropriate
- [ ] Local power filtering present where needed

### 5. Decoupling and Bypass Capacitors
- [ ] Each IC has ≥1 decoupling cap per power pin
- [ ] Typical values: 0.1µF + 1-10µF bulk per IC
- [ ] Caps placed near IC power pins in the schematic
- [ ] Capacitor voltage rating ≥2× rail voltage

### 6. Pull-up / Pull-down / Bias Resistors
- [ ] I2C lines have pull-ups (4.7kΩ / 2.2kΩ)
- [ ] Reset/Enable pins correctly biased
- [ ] Open-drain outputs have pull-ups
- [ ] Unused logic inputs tied high/low
- [ ] LED current-limiting resistors present
- [ ] JTAG/SWD lines have appropriate biasing

### 7. Signal Integrity
- [ ] High-speed signals have series termination
- [ ] Differential pairs note impedance requirements
- [ ] Analog/digital signal separation
- [ ] Crystal oscillator load caps and layout noted
- [ ] Termination resistors correctly placed

### 8. Protection and Safety
- [ ] Reverse polarity protection on power input
- [ ] Overcurrent protection (fuse/PTC)
- [ ] ESD protection on external connectors
- [ ] Flyback diode on relay/inductor drivers
- [ ] Overvoltage protection on sensitive inputs

### 9. Documentation and Organization
- [ ] Title block complete (Title, Rev, Date, Company, Sheet)
- [ ] Schematic notes present (assumptions, version history)
- [ ] Pages logically organized
- [ ] No overlapping text/symbols
- [ ] Font sizes consistent

### 10. Manufacturing and Assembly
- [ ] Test points on critical signals
- [ ] Programming/debug headers present
- [ ] Pin 1 markings visible
- [ ] Mounting holes present and correctly connected
- [ ] Connectors have polarization/keying

## Component-Specific Design Checklists

The `design-checklists/` directory contains detailed checklists for specific component types. For each active component in the schematic, find the matching checklist and walk through it to catch device-specific issues.

Available checklists:

| Category | Checklists |
|----------|------------|
| **Power Management** | DC-DC converter, LDO, battery charger, battery management, LED driver, power switch, supervisor |
| **Control Unit** | MCU, MPU |
| **Analog** | Op-amp, instrumentation amp, ADC, DAC, audio amp |
| **Connectivity** | Bus bridge, RF module, RF transceiver, I/O expander |
| **Interface** | Electromechanical I/O, level shifter, logic gate, analog switch/mux |
| **Memory** | DDR SDRAM, Flash |
| **Timing** | RTC, crystal oscillator (XO) |
| **Opto** | LED, display, photodiode, camera |
| **Regulatory & Reliability** | EMI filter, fuse protection, isolation, ESD protection, surge protection |

**How to use:**
1. Identify all ICs and active components in the schematic from the BOM
2. For each, find the matching checklist in `design-checklists/<Category>/checklist_<type>_reviewed.md`
3. Read the file and verify each item against the schematic

## Quick 10-Check (When Time is Short)

1. Unconnected pins (ERC)
2. Missing footprints (BOM)
3. No decoupling caps per IC
4. Wrong/ambiguous net labels
5. Missing pull-ups on I2C, RESET
6. Empty title block
7. Generic values ("R_US", "C_Small")
8. DNP components not marked
9. Missing PWR_FLAG
10. Auto-generated net names on important signals
