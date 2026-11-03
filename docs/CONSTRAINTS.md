# Engineering constraints and unresolved gates

This register distinguishes arithmetic closure from flight readiness. **All hardware/service qualification gates below are open.** A passing scalar model must not be presented as a functional flight prototype.

| ID | Constraint / reason | Baseline provision | Required evidence / closure criterion |
|---|---|---|---|
| C01 | 72-GPU fabric must preserve electrical topology, supported firmware and timing | Compact custom assembly, short NVLink paths | Supplier agreement and a working 72-GPU domain on actual boards/interconnects |
| C02 | Commercial parts may rely on air cooling, pressure or unsuitable materials | Fully cold-plated vacuum bay | Component-level heat-path review; materials/outgassing screening; powered vacuum testing |
| C03 | Warmer coolant can exceed individual junction limits | Conditional 30°C primary inlet | Measured thermal resistance and hot-spot map at worst workload; fallback 25°C/800 m² if needed |
| C04 | Heat rejection depends on orbit view factors and pointing | 700 m² at 26°C, 80 W/m² absorbed flux | Time-dependent nodal thermal model with Earth IR/albedo, Sun, mutual heating, degraded coatings and transient cases |
| C05 | Radiator area/mass/deployment assumptions are aggressive | 6 kg/m² including wing hardware; 50 mm stacking pitch | Full panel construction, pressure containment, mass measurement, thermal-vacuum heat rejection ≥3.698 kW under baseline conditions |
| C06 | Leaks, bubbles, cavitation, freezing and fluid incompatibility | Two primary HX modules, redundant pumps, isolated secondary branches | Pump curves, NPSH/subcooling, fluid compatibility, proof/leak tests, microgravity gas management and freeze protection |
| C07 | Small fittings and hinge hoses may dominate packing/lifetime | Four articulated 35 m radiator chains | Full interference model, hose bend/pressure cycling, deployment reliability and zero-leak life testing |
| C08 | Large flexible wings affect attitude and optical jitter | Symmetric layout; local optical pointing | Coupled flexible-body/control model, wheel/CMG jitter spectra and terminal pointing/error budget |
| C09 | 800 V in launch gas/plasma and kA local buses create electrical hazards | Isolation, precharge, branch protection, short busbars | Dielectric/arcing qualification across pressure range, plasma charging review, contact I²R and fault-energy tests |
| C10 | Average power misses startup and workload peaks | 10% load reserve, A/B converter allocation | Measured transients, sequencing, load-step stability and fault-isolation verification |
| C11 | Battery life is not established by energy capacity | Four 50 kWh strings; .8 EOL retention | Mission cycling, temperature/DoD profile, charge taper, radiation assessment, propagation/vent tests |
| C12 | COTS GPU/HBM/flash parts may fail or produce silent errors in LEO | 1,600 kg graded shielding allowance, ECC/checkpointing | Orbit-specific transport/dose model and part/board TID/SEE testing; destructive-event and availability targets agreed |
| C13 | Shielding can create secondary particles and cannot ensure reliability | Local material/geometry hypothesis | Transport analysis including penetrations; measured upset rates, no arbitrary shielding-thickness guarantee |
| C14 | Large radiator/blanket area increases impact exposure | Core debris shields, guarded hoses, isolation valves | Debris risk analysis, representative impact protection tests and degraded-mode assessment |
| C15 | Mini Laser hardware alone does not authorize network entry | Two proposed provider terminals, one link counted | SpaceX agreement: hardware/ICD, accepted orbit, provisioning, routing, reserved capacity, handover support and availability |
| C16 | Relay peer visibility and pointing may be intermittent | Opposed folding mounts; geometry calculator | Authorized ephemerides, keep-out/body masks, gimbal limits, acquisition timing, structural jitter and actual link qualification |
| C17 | Optical-only recovery depends on accurate pointing | Independent low-rate S-band | Ground support, spectrum authorization, safe-mode link budget and command recovery demonstration |
| C18 | Launch cylinder arithmetic is not cargo accommodation | Ø7.4 × 10.5 m provisional package | Current launcher ICD, tapered envelope/door/extraction/adapter, separation analysis and 600 km SSO performance |
| C19 | Stiffness, buckling, acoustics and coupled loads are uncalculated | 6 g axial and 2 g lateral concept cases | FEA, modal test, coupled-loads analysis, joint/fatigue design and launcher-approved test levels |
| C20 | Drag highly variable; Isp does not establish burn time | 500 kg xenon + 2,200 kg chemical allocation | Atmosphere/attitude ensemble, thruster selection, power/thrust budget, residuals, maneuver and disposal trajectories |
| C21 | A failed large spacecraft may not dispose itself | Chemical reserve and independent safety controller | Survivability/reentry risk assessment, disposal reliability, autonomous recovery and operational authorization |
| C22 | No technician can reseat connectors or repair leaks | Protected modular branches and independent controller | Fault tree/FMEA, hardware fault injection, restart/checkpoint policy and acceptable degraded availability |

## Numerical operating boundaries

| Case | Calculated implication | Operational interpretation |
|---|---|---|
| Baseline | 298.0 kW solar vs 251.8 required; 114 kWh vs 91.08 needed; 207.1 kW rejection vs 161.6 heat | Four scalar checks pass; qualification still open |
| Absorbed environment 180 W/m² | 144.1 kW rejection | Full workload fails thermal closure |
| Absorbed environment ~152.27 W/m² | Rejection equals peak heat | Zero thermal reserve; not a flight operating target |
| One radiator wing unavailable | 155.3 kW rejection at baseline conditions | Provisional 100 kW compute cap restores margin |
| One solar wing unavailable | 223.5 kW generation | Full-power eclipse cycle is energy-negative |
| One battery string unavailable | 85.5 kWh deliverable | Full-power 36-minute eclipse fails |
| 10 Gb/s relay allocation | 77.76 TB/day at .8 efficiency and .9 usable fraction | Lower than prior 121 TB/day direct-ground planning assumption |
| No relay service | Zero egress | Cache eventually fills unless output generation stops |
| Tenfold density | Tenfold illustrative drag demand | Three-year allocation may fail; propagate actual conditions |

Loss of a radiator/solar wing here means loss of usable capacity. The model does not determine whether the mechanical structure remains attached, whether fluid inventory survives, or whether a damaged appendage interferes with others.

## Prototype sequence and stop conditions

1. **Interface gate:** obtain supported compute and optical terminal interfaces. If supported hardware/service cannot be obtained, revise the architecture before claiming a complete mission.
2. **Representative thermal-vacuum article:** cold-plate one compute tray, switch tray and power module, instrument every critical part, then exercise at full workload without ambient convection. A proposed 72-hour initial demonstration is only screening, not lifetime qualification.
3. **Radiator/hose article:** build a 5 × 2.5 m panel and actual joint/hose; measure mass, gradients, rejection, pressure drop and leak behavior under representative environmental heating.
4. **Full wing:** deployment with gravity offload, pressure, thermal cycles, latch instrumentation and realistic harnesses. Stop if packing or safe intermediate motion cannot be demonstrated.
5. **Full compute domain:** verify all 72 GPUs, power transients, thermal mapping, fault isolation and restart behavior in vacuum.
6. **Radiation gate:** irradiate representative parts/boards against an orbit-specific environment. If destructive-event rate or availability is unacceptable, change the hardware/orbit or stop this compute mission.
7. **Integrated power/thermal/dynamics:** energy-positive cycles, battery ageing, spacecraft modes, jitter and optical handovers with the supported service interfaces.
8. **Flight qualification:** approved launch loads/acoustics/vibration, thermal balance/vacuum, EMC, pressure/vent tests, fault injection, disposal analysis and mission acceptance.

## Missing deliverables

No manufacturing drawings, supplier BOM/prices, finite-element meshes, CFD/thermal nodes, detailed harness/pipe schedule, radiation transport results, terminal ICD, actual ephemeris coverage study, flight code, launch agreement or experimental dataset exists in this repository. The OBJ export is concept geometry, not a pressure-qualified or manufacturable CAD assembly.
