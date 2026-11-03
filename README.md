# Flying NVL72 — ORBIT / 72

A preliminary spacecraft concept for a **custom, unpressurized, fully cold-plated 72-GPU / 36-CPU GB200-class NVLink domain**, with solar power, pumped liquid cooling and proposed Starlink Mini Laser relay connectivity.

**Status: analytical concept and interactive geometric prototype. No flight hardware has been built or tested.** Scalar budgets close under selected assumptions; this does not establish that the spacecraft is buildable, flight-qualified, connected to Starlink or accepted for Starship launch. This is an independent study, with no SpaceX or NVIDIA affiliation or endorsement.

## Explore the design

Download the repository and open **[model/nvl72-orbital-compute.html](model/nvl72-orbital-compute.html)** in a modern browser. It is one self-contained HTML file and works offline. GitHub's file view shows source; it does not execute the model. No hosted website is configured by this publication.

The model includes seven views: core, exploded assembly, compute rack, compute tray, radiator panel, deployed spacecraft and stowed spacecraft. Rotate, pan, zoom, select components, inspect dimensions, isolate assemblies and export visible geometry as OBJ. The page also contains power/thermal controls, a relay calculator, sources and qualification gates.

## Concept C baseline

| Quantity | Allocation / calculated result |
|---|---:|
| Compute topology | 72 Blackwell GPUs, 36 Grace CPUs, one local NVLink domain |
| Conditioned compute input | 120 kW |
| Nominal / reserved spacecraft bus | 138 / 151.8 kW |
| Solar area / EOL generation | 1,100 m² / 298.0 kW |
| Battery nameplate / deliverable energy | 200 / 114 kWh |
| Eclipse design case | 36 minutes at a 600 km circular orbit |
| Primary coolant | 30°C supply / 40°C return; conditional on component limits |
| Radiator | 700 m², one emitting face, 26°C mean skin |
| Peak heat / net rejection | 161.6 / 207.1 kW at 80 W/m² absorbed environment |
| Launch mass allocation | 23.72 t including dry growth and propellant |
| Stowed allocation | Ø7.4 × 10.5 m; current launcher compatibility unverified |
| Deployed span | Approximately 110 × 86 m |
| Optical relay | Two proposed Mini Lasers; one 25 Gb/s-class active link counted |
| Useful average throughput | 18 Gb/s **only if** 25 Gb/s allocation, 80% efficiency and 90% usable service are supplied |

## Engineering package

- [Detailed calculations](docs/CALCULATIONS.md): equations, substitutions, units, margins and failure cases.
- [System architecture](docs/ARCHITECTURE.md): compute, power, cooling, mechanics, communications and operations.
- [Engineering constraints](docs/CONSTRAINTS.md): unresolved interfaces, physical limits and evidence required before flight.
- [Sources](docs/SOURCES.md): published facts separated from original allocations.
- [Design history](docs/DESIGN-HISTORY.md): pressurized Concept A → custom vacuum Concept B → relay/warmer-radiator Concept C.
- [Editable inputs](analysis/inputs.json), [calculation code](analysis/calculate.py), [baseline results](analysis/results/baseline.json), [scenario results](analysis/results/scenarios.json), [mass budget CSV](analysis/results/mass-budget.csv).
- [Validation scope](docs/VALIDATION.md): what automated checks do and do not establish.

## Reproduce the arithmetic

Python 3.10 or later; no Python dependencies:

```sh
python3 analysis/calculate.py
python3 -m unittest discover -s tests -v
```

For the optional canvas/interaction harness, install the Node development dependency and run:

```sh
npm install
npm test
```

Rendered inspection images are written under `test-output/` and are not committed. This is a DOM/canvas harness, not a real browser end-to-end test. The HTML itself needs neither Node nor Python.

The Python model recalculates mass for a newly sized design. HTML sliders change operating scenarios while retaining the baseline geometry and mass. Failure scenarios deliberately omit rescaled mass/trajectory outputs because an electrically failed wing does not disappear from the launch mass.

## Main open gates

1. Supplier-supported custom board, firmware, power and NVLink integration.
2. Full vacuum cooling of **every** heat-producing device, including memory, regulators and power electronics.
3. Radiation suitability of the actual compute and storage parts; shielding is not a reliability guarantee.
4. Coupled orbital thermal, deployment, structural and optical-pointing analysis of the approximately 100 m structure.
5. Contracted Starlink terminal/service access and verified peer geometry; public compatibility information is not mission approval.
6. Current launcher interface, disposal design, endurance and integrated environmental qualification.

The 2020 Starship guide only supports a historical volume comparison. Exact cargo geometry, extraction path and 600 km SSO performance remain open. No current Starship payload capability is assumed from the vehicle's external diameter.

## Provenance and use

This repository publishes the design developed in the accompanying project conversation, including AI-assisted drafting, modeling and arithmetic. Public manufacturer/NASA references are linked rather than copied. Archived concepts are superseded and must not be used as current requirements. One-off editing scripts, temporary transfer files and unrelated workspace content are excluded.

No license has been selected for this initial publication. Public visibility alone does not grant a general reuse license; third-party names and documents retain their respective rights.
