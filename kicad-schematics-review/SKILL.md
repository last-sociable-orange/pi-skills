---
name: kicad-schematics-review
description: "Use this skill to review KiCad schematic files (.kicad_sch) for correctness, best practices, and common design issues. Trigger whenever the user wants to: review a KiCad schematic for errors and improvements, perform a structured design review of an EDA schematic, check for common mistakes and generate a formal schematic review report. This is a comprehensive design review skill covering electrical, connectivity, power, signal integrity, protection and regulation aspects. Also trigger when the user mentions 'design review', 'schematic review', 'KiCad review', or similar phrases in the context of KiCad design."
---

# KiCad Schematics Review

A structured checklist for reviewing KiCad schematic files.

## Review Preparation

### 1. Export BOM

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export bom \
  --fields "Reference,Description,ManufacturerProductNumber,DNP,Exclude from BOM" \
  -o <InputFile_BOM>.csv <InputFile>.kicad_sch
```

`DNP` and `Exclude from BOM` parts can be ignored during the review.

### 2. Export netlist

```bash
# OrCAD PCB2 format, generating a *.net file
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export netlist --format orcadpcb2 FlightController.kicad_sch

# PADS format, generating a *.asc file
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export netlist --format pads FlightController.kicad_sch
```

+ Orcadpcb2 format provides connection information from component's view. It lays out how each pin of a component is connected. 
+ PADS format provides connection information from net's view. It lays out what are connected to a single net.
+ A connection tree can be established from above two netlists.

### 3. Collect component datasheets and parameters

+ Look for `Knowledge/` folder in the project directory. It is the **ONLY** source of datasheets and user manuals. Reference them during the review.
+ For passive discretes: Check component's description in BOM for value and critical parameters, e.g. capacitor type, rated voltage, resistor power rating, tolerance. Or check `Knowledge/` folder for datasheets. 
+ Ask user for datasheets if nothing is found from above sources.

### 4. Collect design requirements and existing design documents

Check `Document/` folder in the project directory for existing design requirements and documents where design procedures and decisions are documented.

+ `Document/` folder is the **ONLY** source of information for design requirements and design documents.
+ User must provide `Design Specification Document` that contains system level design requirements.

### 5. Use Mermaid Skill

Use its syntax to generate block diagrams, connections, power trees, etc.,  

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
3. Read the file and verify related item against the schematic

## Review Design Against Checklist

Below are some high level review rules:

### 1. Review Independently

Review the design independently. Don't assume design is correct. Only cross check existing design documents when review is done. 

### 2. First Step, Get Holistic View Of Design

+ Identify major components in the system.
+ Collect power requirements of each component and synthesis up a system level power architecture.
+ Collect connectivity requirements of each component and synthesis up a system level connectivity diagram.
+ Start review from high level requirements. Don't jump into design details too quickly.

### 3. Second Step, Break Down Design And Exam Details

Break down design into subsystems and exam design details. Usually Kicad schematics has already been broken down into hierarchy or flat sheets. Each sheet often contains a subsystem or circuits that are funtionally related.

Consider circuits in a signal chain as a whole during review, even they are spread out in multiple sheets, e.g.:

+ Multiple pages analog circuits that include buffer stage, amplification stage, anti-aliasing filter and ADC
+ Multiple pages power circuits that are brached out through SMPS/LDOs/power switchs/ferrite beads, e.g. 5V -> [SMPS] 3.3VCCD -> [LDO] 1.8VCCD -> [Ferrite bead] 1.8VCCA

Exam these circuits with great details, yet keep in mind that they are all related and should be reviewed from system level as well as component level.

### 4. Check Every Single Document Provided

There maybe multiple documents in `Knowledge/` folder for one components, e.g. MCU may have datasheet, user manual, application notes. Design details are scattered in these documents, e.g. IO's electrical characteristics is written in the datasheet and IO mux table is stated in the user manual. Don't miss any documents during review. 

For better tracking contents of these documents, one solution is taking table of content of each document and putting them in a summary document. During review, check this summary document first to find out which documents and which chapters are relevant to the subject being reviewed. Then dive deep into each chapters to audit the circuit against the documents.

### 5. Cover Corner Cases

+ Check not only nominal conditions, but also all corner cases to make sure design works in all circumstances.
  + Check min/max input and output conditions, e.g. min/max input voltage, output current
  + Consider component tolerance, e.g. resistor, inductor
  + Consider component derating, e.g. inductor inductance, MLCC capacitor capacitance 

+ Check design margin:
  + Generally leave 25% margin in worst case scenario, if not specified in the design, e.g. inductor rated current, resistor power rating
  + MLCC capacitor voltage rating >= 2x voltage applied
  + 5-10% margin for protection circuit, e.g. TVS standoff voltage, fuse hold current

+ Check associated circuits if their ratings are OK in all user cases, including normal operation and corner cases, and possible faulty conditions, e.g. LED driver OVP due to load open circuit, all related circuit shall be able to handle OVP voltage.

### 5. Consider External Connections

When connecting to external devices through IOs: 

+ Make sure design works on its own and doesn't rely on external circuits, e.g. I2C pull-up resistors
+ Make sure design is not susceptable to failures created by external devices. Consider fault conditions like: voltage level mismatch, IO latch-up, clock stretch, etc. Review the design to make sure in no circumstances the design would be locked up or/and damaged due to these failures. 

### 6. Protection and Safety

Design shall comply with EMC and Safety regulations outlined in design requirement document.

Also consider below protection and safety features:

+ Reverse polarity protection when generic batteries (e.g. AAA, CR2032) are used as power input
+ Overcurrent protection (fuse/PTC) caused by common component failure, e.g. TVS failure
+ ESD protection and EMI filters on external connectors
+ Flyback diode on relay/inductor drivers
+ Overvoltage protection on ports where back-EMF may occur, e.g. USB port, port with high current inductive load

### 7. Manufacturing and Assembly

Check design has below features:

+ Test points on critical signals
+ Programming/debug headers present
+ Mounting holes present and correctly connected
+ Connectors have polarization/keying

## Review Coverage Requirements

+ Review shall 100% cover all components

## Generate Well-Formatted Review Report

Some consideraton when generating the review report:

+ Use Mermaid skill to generate images when presenting diagrams or power trees to user
+ Use tables to present review results. Table shall at least have below items:
  + Design requirement
  + Your independent calculations/finding/decisions based on design requirements and datasheets
  + What's in current design
  + Pass/fail/conclusion/suggestion
+ Organize review results by functions, or by components, or by review categories, whichever best fits
+ Use severity levels

