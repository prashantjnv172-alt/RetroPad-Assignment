# RetroPad: Schematic-to-SKiDL Programmatic Translation

## 1. Methodology: How the KiCad Schematic was Analyzed
To ensure a 1:1 functional translation, the original RetroPad KiCad schematic was analyzed at the source level:
* **S-Expression Parsing**: Instead of relying solely on visual inspection, I audited the raw .sch file to extract exact component references (U1, J1, R1-R11), values, and the underlying netlist logic.
* **Logic Decoupling**: I identified two distinct functional layers: a Hardware Passthrough (D-Pad signals bypass the MCU via 0-ohm resistors) and an Active Logic Layer (ATtiny814 handling "Smart" button features and analog joystick simulation).
* **Pin Mapping**: I mapped the ATtiny814's physical SOIC-14 pins to their logical functions (UPDI Reset, ADC drivers, and GPIO inputs) as dictated by the original wiring.

## 2. Strategy for SKiDL Translation
The strategy focused on portability and automation:
* **Native Library Approach**: Rather than relying on local KiCad library paths, I used a "Part Generator" strategy. This defines components programmatically, making the script entirely self-contained and environment-independent.
* **Functional Grouping**: I utilized SKiDL’s += operator to group pins into logical nets (e.g., POTX, FIRE, RAPID) to ensure the code remains readable and easy to audit.
* **Modularization**: Separated the component definitions from the circuit logic to mimic a professional firmware/hardware development structure.

## 3. Assumptions Made
* **Footprint Compatibility**: I assumed the use of standard KiCad 6.0+ footprint libraries (e.g., Resistor_SMD:R_0805_2012Metric) to ensure the generated netlist is ready for immediate import into modern PCB layout tools.
* **JUMP Logic**: I confirmed that the JUMP1 switch is intentionally tied to the UP net, assuming the target console interprets "Up" as a jump command.
* **Power Conditioning**: Assumed the 0.1uF capacitor (C1) serves as a local decoupling cap for the ATtiny814 VDD pin.

## 4. Verification of Correctness
The integrity of the design was verified through a three-tier audit:
1. **Netlist Parity**: The generated RetroPad_skidl.net was cross-referenced against the original legacy netlist. I confirmed all nets and components matched the source logic.
2. **Automated ERC**: Ran SKiDL’s internal Electrical Rules Check (ERC()) to ensure no pins were left floating and that power rails were properly tied.
3. **Graph Visualization**: Used Graphviz to generate a directed acyclic graph (RetroPad_Final.svg), allowing for a visual spot-check of the voltage dividers and MCU I/O hubs.

## 5. Development Summary
* **Total Time Spent**: Approximately 4 hours (Research, Environment Setup, Logic Translation, and Verification).
* **AI Tools Used**: Gemini (Google).
    * Contribution: Assisted in parsing legacy KiCad S-expression syntax and troubleshooting environment pathing for the Graphviz visualization engine.

-----

### File Structure
* `main_circuit.py`: Main connectivity logic.
* `retropad_lib.py`: Programmatic component definitions.
* `RetroPad_skidl.net`: The final verified netlist.
* `RetroPad.svg`: High-resolution circuit graph visualization.
