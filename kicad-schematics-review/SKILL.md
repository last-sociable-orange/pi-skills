---
name: kicad-schematics-review
description: "Use this skill to review KiCad schematic files (.kicad_sch) for correctness, best practices, and common design issues. Trigger whenever the user wants to: review a KiCad schematic for errors and improvements, perform a structured design review of an EDA schematic, check for common mistakes and generate a formal schematic review report. This is a comprehensive design review skill covering electrical, connectivity, power, signal integrity, protection and regulation aspects. Also trigger when the user mentions 'design review', 'schematic review', 'KiCad review', or similar phrases in the context of KiCad design."
---

# KiCad Schematics Review

A structured checklist for reviewing KiCad schematic files.

## Review Preparation

### 1. Export BOM

If BOM is not ready in the project folder, you can generate it using `kicad-cli`. Command may vary depending on your project setup and Kicad installation method and location. 

```bash
flatpak run --command=/app/bin/kicad-cli org.kicad.KiCad sch export bom \
  --fields "Reference,Description,ManufacturerProductNumber,DNP,Exclude from BOM" \
  -o <InputFile_BOM>.csv <InputFile>.kicad_sch
```

`Exclude from BOM` parts can be ignored during the review, however you need to check if `DNP` parts are set correctly.

### 2. Export netlist

If netlists ( Orcadpcb2 and PADS format) are not ready, you can generate them using below commands.

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

### 5. Use Drawio Skill

Use it to generate block diagrams, power trees, circuits if you want to show component level connections, etc.,  Insert pictures in the markdown file and keep the original .drawio for user's future use.

## Review Design Like a Pro

Below are some high level review rules that professionals use. You should follow these rules.

### 1. Review Independently

1. Do not assume the design is correct.
2. Start from the design requirements only.
3. Study the datasheet and related documents.
4. Design your own circuits independently.
5. Finally, compare your design with the one under review.

### 2. First, Get Holistic View Of Design

Before diving into details, build a high-level understanding of the system:

1. **Identify major components** in the system.
2. **Start aggregating power requirements** from major components and synthesize a system-level power architecture.
3. **Start aggregating connectivity requirements** from major components and synthesize a system-level connectivity diagram.
4. **Start the review from high-level requirements** — avoid jumping into design details too early.

### 3. Break Down Design And Examine Details

#### 3.1 Decompose Into Subsystems

Decompose the design into subsystems and examine each in detail. In KiCad schematics, the design is often already organized into hierarchical sheets or flat sheets, where each sheet typically represents a functionally related subsystem or circuit.

**Review by signal chain, not just by sheet.** Even if related circuits are spread across multiple sheets, treat them as a whole during review. Examples include:

- **Analog signal chains** spanning multiple pages: buffer stage → amplification stage → anti-aliasing filter → ADC
- **Power distribution chains** branching through SMPS, LDOs, power switches, and ferrite beads, e.g.:
  `5V → [SMPS] 3.3VCCD → [LDO] 1.8VCCD → [Ferrite bead] 1.8VCCA`

**Examine these circuits with great attention to detail**, but always keep in mind that they are interconnected. Review them from **both** a system level (how they work together) and a component level (individual part correctness).

#### 3.2 Examine Details With Checklists

To examine details thoroughly, use the component-specific checklists in the `design-checklists/` directory. For each active component in the schematic, find the matching checklist and walk through it to catch device-specific details that a high-level review might miss.

**Available checklists for detailed examination:**

| Category                     | Checklists                                                   |
| :--------------------------- | :----------------------------------------------------------- |
| **Power Management**         | DC-DC converter, LDO, battery charger, battery management, LED driver, power switch, supervisor |
| **Control Unit**             | MCU, MPU                                                     |
| **Analog**                   | Op-amp, instrumentation amp, ADC, DAC, audio amp             |
| **Connectivity**             | Bus bridge, RF module, RF transceiver, I/O expander          |
| **Interface**                | Electromechanical I/O, level shifter, logic gate, analog switch/mux |
| **Memory**                   | DDR SDRAM, Flash                                             |
| **Timing**                   | RTC, crystal oscillator (XO)                                 |
| **Opto**                     | LED, display, photodiode, camera                             |
| **Regulatory & Reliability** | EMI filter, fuse protection, isolation, ESD protection, surge protection |

**How to examine details with checklists:**

1. Identify all ICs and active components in the schematic from the BOM
2. For each component, find the matching checklist in `design-checklists/<Category>/checklist_<type>_reviewed.md`
3. Walk through each checklist item and verify against the schematics — pin by pin, cap by cap, resistor by resistor

### 4. The Devil Hides In The Details.

Do not focus solely on high-level design concepts and methods. You **must** review the use and connection of **every single pin** of every component.

**Action:** Check component connections pin by pin — **including NC, unused pin,** no exceptions.

### 5. Check Every Single Document Provided

A single component may have multiple documents in the `Knowledge/` folder (e.g., for an MCU: datasheet, user manual, application notes). Design details are often scattered across these documents. For example:

- I/O electrical characteristics → typically in the **datasheet**
- I/O mux table → typically in the **user manual**

Do **not** miss any documents during your review.

**Recommended method for tracking document contents:**

1. **Create a summary document** containing the table of contents from each relevant document.
2. **During review**, first consult this summary document to identify:
   - Which documents are relevant to the subject being reviewed
   - Which chapters within those documents contain the needed information
3. **Then**, dive deep into each identified chapter to audit the circuit against the document specifications.

### 6. Cover Corner Cases

Do not limit your review to nominal conditions. Verify that the design works correctly under **all circumstances**, including corner cases, tolerances, derating, and fault conditions.

#### 6.1 Check Min/Max and Tolerance Limits

- **Input/output conditions:** Verify min/max input voltage, output current, etc.
- **Component tolerance:** Consider tolerances for resistors, inductors, capacitors, etc.
- **Component derating:** Account for derating effects (e.g., inductance drop in inductors, capacitance loss in MLCCs under DC bias).

#### 6.2 Verify Design Margins

Apply these margins unless otherwise specified in the design:

| Scenario                                                     | Margin Requirement   |
| :----------------------------------------------------------- | :------------------- |
| General worst-case (e.g., inductor rated current, resistor power rating) | ≥ 25% margin         |
| MLCC capacitor voltage rating                                | ≥ 2× voltage applied |
| Protection circuits (e.g., TVS standoff voltage, fuse hold current) | [5–10]% margin       |

#### 6.3 Check Possible fault conditions

**Example:** If an LED driver triggers overvoltage protection (OVP) due to an open load, ensure all associated circuits can safely handle the OVP voltage.

### 7. Consider External Connections

When the design connects to external devices through I/Os, verify both **self-sufficiency** and **fault tolerance**.

#### 7.1 Ensure Self-Sufficiency

The design must work on its own and **not rely on external circuits** for basic operation.

> **Example:** I2C pull-up resistors must be included on the board — do not assume they are provided by an external device.

#### 7.2 Ensure Tolerance to External Faults

The design must not be susceptible to failures caused by external devices. Review for fault conditions including:

| Fault Condition            | Description                                                  |
| :------------------------- | :----------------------------------------------------------- |
| Voltage level mismatch     | External device operates at different logic levels (e.g., 5V vs 3.3V) |
| I/O latch-up               | External voltage or current injection causes parasitic SCR activation |
| Clock stretching           | External device holds clock line low longer than expected    |
| Overvoltage / undervoltage | External supply or signal exceeds safe limits                |
| Back-powering              | External device powers the design through I/O pins unintentionally |
| Stuck-at faults            | External signal stuck high or low indefinitely               |

Confirm that **in no circumstances** can the design b damaged due to any of the above external fault conditions.

### 8. Protection and Safety

The design **shall** comply with all EMC and Safety regulations outlined in the design requirements document.

In addition, verify the following protection and safety features:

#### Mandatory Checks

| Feature                                 | Condition / Application                                      | Notes                                                      |
| :-------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------- |
| **Reverse polarity protection**         | Required when generic batteries (e.g., AAA, CR2032) are used as power input | Prevents damage from incorrect battery installation        |
| **Overcurrent protection** (fuse / PTC) | Required when common component failures are possible (e.g., TVS short-circuit failure) | Protects against sustained overcurrent events              |
| **ESD protection**                      | Required on all external connectors                          | Use TVS diodes, ESD arrays, etc.                           |
| **EMI filters**                         | Required on external connectors (especially for regulatory compliance) | Common mode chokes, ferrite beads, RC filters              |
| **Flyback diode**                       | Required across relay coils, inductor drivers, solenoids, motors | Prevents inductive kickback damage to switching elements   |
| **Thermal protection**                  | Required for high-current or power-dissipating components    | Ensure adequate derating, thermal shutdown, or heatsinking |
| **Overvoltage protection** (OVP)        | Required for sensitive inputs or when external supplies are unpredictable | Crowbar circuit, TVS, or clamping diodes                   |
| **Undervoltage lockout** (UVLO)         | Required for battery-powered designs or when supply brownout could cause erratic behavior | Prevent system malfunction during low voltage              |

#### Verification Goal

- All required protection features are present and correctly implemented
- Safety and EMC regulations from the design requirements are met

### 9. Design For Manufacturing, Test and Assembly

+ **Test points** on: power rails, GND, communication buses, critical GPIOs (interrupts, control signals)
+ **Multiple GND test points** distributed on board
+ **Ferrite beads / current sense resistors / zero-ohm links** to isolate power sections for troubleshooting
+ **SWD/JTAG header** for programming/debug
+ **UART header** for debug console
+ **Mounting holes** — correct size, position, and ground connection (or isolation) as required

## Review Coverage Requirements

Review shall **100% cover all components and all pins**

## Generate Well-Formatted Review Report

After completing all review sections, generate a comprehensive review report following the guidelines below.

### Use Diagrams for Visual Clarity

When presenting system architecture, power trees, connectivity diagrams, or signal chains, **use drawio skill** to generate diagrams. This helps the user visualize complex relationships clearly.

### Use Tables for Review Results

Present findings using **two complementary table formats** — one organized by subsystem with line-item breakdown, and one by component with pin-level detail.

#### Table A: Review by Subsystem (with Line Items)

Organize findings by logical subsystems. Within each subsystem, break down the review into individual **items** (e.g., components or design aspects).

**Example — Buck Converter Subsystem:**

| Subsystem                 | Item                | Design Requirement                                           | Independent Calculation / Finding                            | Current Design                       | Pass / Fail / Conclusion / Suggestion                   | Severity |
| :------------------------ | :------------------ | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------- | :------------------------------------------------------ | :------- |
| Buck Converter (12V → 5V) | Input capacitor     | Low ESR, handle ripple current. Typically 10µF recommended per datasheet | Required C_in ≥ 10µF, voltage rating ≥ 2× V_in_max = 25V min | 10µF, 25V, X7R                       | **Pass**                                                | -        |
| Buck Converter (12V → 5V) | Output capacitor    | 22µF min, low ESR for stability                              | Calculated C_out = 22µF, voltage rating ≥ 10V                | 22µF, 16V, X5R                       | **Pass**                                                | -        |
| Buck Converter (12V → 5V) | Inductor            | 4.7µH ±20%, saturation current ≥ load current + ½ ripple     | I_sat_req = 1.2A + 0.3A = 1.5A min                           | 4.7µH, I_sat = 1.8A                  | **Pass**                                                | -        |
| Buck Converter (12V → 5V) | Feedback resistors  | V_out = V_ref × (1 + R1/R2), V_ref = 0.8V, target 5V → R1/R2 = 5.25 | R1 = 52.5kΩ, R2 = 10kΩ → 5.0V                                | R1 = 51kΩ, R2 = 10kΩ → V_out = 4.88V | **Fail:** Change R1 to 52.5kΩ (use 52.3kΩ 1% or 52.5kΩ) | Medium   |
| Buck Converter (12V → 5V) | Bootstrap capacitor | 100nF recommended per datasheet                              | 100nF, 10V min rating                                        | 100nF, 10V                           | **Pass**                                                | -        |
| Buck Converter (12V → 5V) | Enable pin          | EN threshold: >1.2V to enable, <0.4V to disable              | Connect to V_in via voltage divider for UVLO or direct to V_in | Pulled directly to V_in              | **Pass** (UVLO not required for this design)            | -        |

**Example — I2C Communication Subsystem:**

| Subsystem     | Item               | Design Requirement                               | Independent Calculation / Finding                      | Current Design         | Pass / Fail / Conclusion / Suggestion                        | Severity |
| :------------ | :----------------- | :----------------------------------------------- | :----------------------------------------------------- | :--------------------- | :----------------------------------------------------------- | :------- |
| I2C Subsystem | Pull-up resistors  | Rp = 4.7kΩ for 3.3V @ 400kHz                     | Rp = 4.7kΩ (max bus cap ~200pF from 2 devices + trace) | No pull-ups on SDA/SCL | **Fail:** Add 4.7kΩ resistors                                | High     |
| I2C Subsystem | Series termination | Optional for EMI reduction, 33Ω–100Ω recommended | 47Ω on SCL, 47Ω on SDA (close to master)               | No series resistors    | **Suggestion:** Add 0Ω resistors (optional populate 47Ω if needed) | Low      |

#### Table B: Review by Component (Pin-by-Pin)

For **all active components and passive components with polarity, provide a pin-by-pin review** using the table below.

**Example:**

| Component         | Pin Name / Number         | Design Requirement                         | Independent Finding (from datasheet)                         | Current Connection                                    | Pass / Fail / Conclusion / Suggestion                      | Severity |
| :---------------- | :------------------------ | :----------------------------------------- | :----------------------------------------------------------- | :---------------------------------------------------- | :--------------------------------------------------------- | :------- |
| MCU (STM32F103)   | PA9 / USART1_TX (Pin 30)  | 3.3V logic level, 8mA drive typical        | Need pull-up? No, push-pull output ok                        | Connected to UART header pin 2 via 0Ω series resistor | **Pass**                                                   | -        |
| MCU (STM32F103)   | PA10 / USART1_RX (Pin 31) | 3.3V logic input, 5V tolerant              | Input high: 0.7×VDD=2.31V min                                | Connected to UART header pin 3                        | **Pass**                                                   | -        |
| MCU (STM32F103)   | PB2 / BOOT1 (Pin 54)      | Should be low at boot for normal operation | Internal pull-down weak. Recommend external 10k pull-down for stability | Left floating                                         | **Fail:** Add 10k pull-down resistor to GND                | Medium   |
| LDO (AMS1117-3.3) | VIN (Pin 1)               | Input 4.5V to 12V (per datasheet)          | Input cap: 10µF min, output cap: 22µF (tantalum recommended) | VIN from 5V rail. Input cap: 1µF only                 | **Fail:** Increase input cap to 10µF. Add output cap 22µF. | High     |

------

#### Summary of Table Usage

| Table Type                             | When to Use                                            | Primary Focus                                                |
| :------------------------------------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| **Table A: By Subsystem (with Items)** | Overall review organization, subsystem-level breakdown | Item-by-item verification within each subsystem (e.g., input cap, inductor, feedback resistors) |
| **Table B: By Component (Pin-by-Pin)** | Deep-dive on ICs, connectors, or polarized components  | Every single pin connection, configuration, and electrical compatibility |

------

### Organize Review Results Logically

Structure the report by **subsystem**, as this aligns with Table A. Within each subsystem, present Table A entries for line items, followed by Table B entries for any critical components requiring pin-level review.

**Recommended report structure:**

text

```
## Review Report

### System overview
System overview with diagrams and power trees

### Subsystem: Buck Converter (12V → 5V)
[Table A entries for this subsystem — input cap, output cap, inductor, feedback resistors, etc.]
[Table B for components used in buck converter]

### Subsystem: Digital Control (MCU)
[Table A entries for high-level MCU subsystem items]
[Table B for MCU — all pins reviewed]

### Subsystem: ADC
[Table A entries for this subsystem — ADC, Opamps, Clock]
[Table B for components used]
```

------

### Use Severity Levels for Issues

For each finding that is **not a Pass**, assign a severity level:

| Severity          | Meaning                                                      | Action Required                 |
| :---------------- | :----------------------------------------------------------- | :------------------------------ |
| **Critical**      | Will cause damage, safety hazard, or complete non-function   | Must fix before prototype       |
| **High**          | Likely to cause malfunction or reliability issue             | Should fix before next revision |
| **Medium**        | May cause issue under corner cases or marginal conditions    | Recommend to fix                |
| **Low**           | Minor issue, best practice violation, or improvement opportunity | Nice to fix or note for future  |
| **Informational** | Observation, not an issue                                    | No action required              |

------

### Include a Report Summary

| Subsystem                 | Critical | High  | Medium | Low   | Informational |
| :------------------------ | :------- | :---- | :----- | :---- | :------------ |
| Buck Converter (12V → 5V) | 0        | 0     | 1      | 0     | 0             |
| I2C Subsystem             | 0        | 1     | 0      | 1     | 0             |
| Digital Control (MCU)     | 0        | 0     | 1      | 0     | 0             |
| LDO (5V → 3.3V)           | 0        | 1     | 0      | 0     | 0             |
| **Total**                 | **0**    | **2** | **2**  | **1** | **0**         |

## A Practical Review Work Flow

Here is a practical review work flow putting everything mentioned above together:

1. Check BOM/Netlist/Documents readiness
2. High level grasp of system level design requirements, connectivity and power tree
3. Break down into subsystems and **independently design your circuitry based on high level information you collected**, then compare it against the design:
   1. Follow the datasheet and any available documents to do the functional design, e.g. power input/output capacitors, inductor selection. 
      - **Consider corner cases, tolerances, faulty conditions caused by other circuits, protection and safety circuits, DFM/DFT/DFA mentioned in section 6, 7, 8, 9**
      - **Consider signal interconnection and interaction between circuits**
   2. Check component connection pin-by-pin
   3. Check design against checklist **thoroughly**, making sure everything is well considered and covered even it is not mentioned in the datasheet
4. Check review coverage
5. Generate report
