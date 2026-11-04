# Design history

| Revision | Main assumption | Change / reason |
|---|---|---|
| A | Commercial-rack-oriented, pressure-retaining compute enclosure | A way to retain air-dependent component cooling; later superseded by the user's permission to customize the hardware |
| B | Custom fully cold-plated, unpressurized compute bay | Removed reliance on internal air; retained pressurized coolant loops; added conduction paths, vacuum material/electrical constraints and custom DC power |
| C | Partner laser relay and conditional warmer radiator | Replaced direct-Earth optics/Ka with proposed Mini Lasers; kept S-band recovery; changed 25°C inlet/800 m² radiator to conditional 30°C/700 m² |
| C repository edition | Reproducible engineering package | Added editable inputs, Python calculations, scenario files, tests and explicit constraint register; corrected the drag arithmetic and stale analytical-description text |

## Preserved artifacts

- [Concept A detailed pressurized model](../archive/concept-a-pressurized.html): superseded, retained to document the earlier design assumptions.
- [Concept B vacuum model](../archive/concept-b-vacuum.html): superseded baseline before the Starlink revision.
- [Archived Concept C](../archive/concept-c-relay.html): relay/warmer-radiator baseline before detailed ion integration.
- [Current Concept D](../model/nvl72-orbital-compute.html): detailed propulsion and subsystem views, with a separate passive thermal alternative study.

Archived HTML files contain their original calculations, caveats and assumptions; they were not brought up to current requirements. Do not mix their geometry or budgets with Concept D. They are not separate validated spacecraft designs.

## C changes with numerical consequences

- Fourteen rather than sixteen radiator panels per wing: 700 rather than 800 m² total.
- Mean radiator skin rises from 21 to 26°C; primary inlet rises from 25 to 30°C, requiring component thermal approval.
- Radiator dry allocation falls 600 kg; total launch allocation falls 720 kg after dry growth, from 24.44 to 23.72 t.
- Deployed radiator span falls from 96 to 86 m; 110 m solar span and provisional launch envelope are retained.
- Lost-wing thermal margin is reduced: full-power operation no longer closes after one complete radiator wing is lost. The provisional fault-mode cap is 100 kW compute input.
- Two proposed 25 Gb/s-class Mini Laser terminals replace 100 Gb/s direct-ground optics and the Ka dish. One relay link is counted; actual usable capacity and handover support remain contractual interfaces.
- No communications mass/power reduction is claimed before supplier data. Independent low-rate S-band remains.

## Arithmetic corrections during publication

The earlier Concept C HTML stated about 67 m/s/year drag at ρ = 10⁻¹² kg/m³, Cd = 2.2, projected area 700 m² and launch mass 23.72 t. Substitution gives **58.5764 m/s/year**, or **175.7292 m/s over three years**, for constant density/area/mass. The current repository HTML is corrected; this remains a hypothetical density case, not a forecast. The propulsion allocation is unchanged.

The analytical-screening table no longer claims a pressure-shell stress calculation for the vented compute bay. Pressure qualification remains necessary for tanks and coolant hardware. The 36-minute eclipse input is explicitly identified as slightly beyond the ideal 35.43-minute geometric maximum and retained as a conservative energy stress case.

## Scope of “all workings”

The repository contains the design artifacts, equations, assumptions, source references, executable sizing code, scenario outputs and meaningful validation harness. It excludes temporary automation/transfer files, private account metadata, unrelated files and one-off text-replacement scripts. No confidential manufacturer data or inferred internal SpaceX design process is represented.

## Concept D · 4 November 2026

- Replace the generic 5 kW electric-thruster placeholder with four gridded-ion heads, two active, using historical NASA NEXT prototype performance as the numerical reference.
- Include PPU efficiency, an isolated front-end for the 800 V spacecraft bus, feed/control power, useful thrust direction and sunlit availability. Do not equate high ideal Δv with fast maneuvers.
- Raise propulsion dry allocation by 250 kg and growth by 50 kg: launch mass becomes 24.02 t. Retain 500 kg xenon and 2,200 kg chemical propellant pending mission/lifetime analysis.
- Add ion-engine cutaway, propulsion-bay, thermal-module, articulated-hinge and passive-loop views: twelve total. Gimbal and hinge motion, neutralizer, grids, PPUs, feed valves, electrical harness and service detail are conceptual geometry.
- Retain pumped baseline cooling. Add a passive-loop/hybrid trade in response to the question about heat-driven circulation, with capillary-pressure and latent-heat estimates; no unverified pump savings are credited.
