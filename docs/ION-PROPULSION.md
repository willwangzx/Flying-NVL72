# Ion propulsion revision · Concept D

## Decision

Use a **candidate gridded-ion system for drag compensation and slow orbit control**, while retaining chemical propulsion for urgent maneuvers and disposal. Four heads are installed as two diagonal pairs; only one pair operates at a time. The geometry shows pair A as heads 1/4 and pair B as heads 2/3.

The numerical reference is a historical NASA NEXT prototype test point: 0.237 N thrust, 6.9 kW thruster input and 4,190 s specific impulse per head. These are published test results, not a selection of commercially available hardware or an assurance of this installation's performance. [NASA reference](https://ntrs.nasa.gov/citations/20080012739). A Hall thruster is also electric propulsion, but uses a different acceleration mechanism; its typical lower-Isp/higher-thrust-per-power trade must be assessed using an actual throttle map rather than substituting the same numbers.

## Electrical power and heat

```text
P_pair,thruster = 2 × 6.9 = 13.8 kW
P_pair,bus = 13.8 / (.95 PPU efficiency × .97 front-end efficiency)
             + .30 kW feed/control allocation
           = 15.2756 kW
P_bus,105kW compute = 105/.96 + 13 + 15.2756 = 137.6506 kW
```

An 800 V spacecraft bus must feed a compatible isolated front-end. The historical NEXT PPU documentation describes a different input-voltage range; do not connect it directly to this bus. The .95/.97 efficiencies, front-end architecture, branch protection and integration mass remain allocations. Four PPUs limit engine fault propagation; common tanks/regulators, bus adapters and structural supports still create common-cause failures.

The scalar screening conservatively counts all EP electrical input as spacecraft heat and assumes it persists throughout the orbit for charging/thermal analysis, even though the thrust schedule is sunlit-only. This bounds the incremental propulsion heat under the assumed properties. Jet kinetic power estimated from F·v_e/2 is ~9.74 kW for the pair; the remaining ~5.54 kW is a first-order non-jet power estimate, not a measured heat map. Where thruster-body heat radiates, returns through mounts or strikes surfaces requires actual plume/thermal analysis. No radiator-area saving is credited.

| Operating case | Nominal bus | Sunlit generation required | Conservative peak heat |
|---|---:|---:|---:|
| 120 kW compute; ion off | 138.00 kW | 251.82 kW | 161.55 kW |
| 105 kW compute; two ion heads | 137.65 kW | 251.18 kW | 161.14 kW |
| 120 kW compute; two ion heads | 153.28 kW | 279.70 kW | 179.43 kW |

All three pass the current scalar solar, charger, battery and radiator screens. The 105 kW burn cap is selected to preserve the earlier nominal electrical envelope and margin. This does not validate transient rails or control interactions.

## Thrust and time

Use initial mass m = 24,020 kg and assumed useful-direction factor 0.95. The direction factor represents thrust projected onto the desired maneuver direction, not electrical efficiency. It requires a propagated attitude solution; it cannot be assumed merely because the engine can gimbal.

```text
F_pair = .474 N
F_useful = .474 × .95 = .4503 N
a_on = F_useful/m = 1.87469e−5 m/s²
t_on(1 m/s) = m/F_useful = 14.8173 h
Sunlit fraction = 60.5389/96.5389 = .627093
Available firing fraction = .627093 × .85 = .533029 of the orbit
Average useful thrust = .4503 × .533029 = .240023 N
```

The 85% usable fraction of sunlight is an operational assumption for pointing, coast intervals and other constraints. Eclipse operation is not credited for propulsion. Solar tracking and radiator view factors during a tangential burn are unsolved: the illustrated Sun-normal +Z attitude and body-axis −Z exhaust are not a proof that the schedule can be flown. A ±12° gimbal visualization cannot solve an arbitrary 90° pointing conflict.

At density 10⁻¹² kg/m³, projected area 700 m², Cd 2.2 and circular speed 7,561.733 m/s, drag is 0.044028 N. Average net thrust is 0.195995 N; 1 m/s net increase then takes about **34.04 hours elapsed**. Without drag but including duty, it takes 27.80 hours. These are initial-mass constant-environment estimates; a real orbit change changes mass, density, geometry and opportunity.

| Case | Two active heads | One active head |
|---|---:|---:|
| Raw thrust | .474 N | .237 N |
| Bus input including controls | 15.276 kW | 7.788 kW |
| Xenon flow inferred from F/(g₀Isp) | 11.536 mg/s | 5.768 mg/s |
| Usable orbit fraction required to balance reference drag | 9.78% | 19.56% |
| 1 m/s firing time, without drag | 14.82 h | 29.63 h |
| 1 m/s elapsed, after reference drag | 34.04 h | 87.81 h |
| Density at which assumed average thrust just balances drag | 5.45 × 10⁻¹² kg/m³ | 2.73 × 10⁻¹² kg/m³ |

One-head operation is a contingency calculation, not an approved mode: off-axis torque can overwhelm attitude/momentum control unless the thrust vector passes through the instantaneous center of mass or another actuator balances it. At ten times reference density, the pair's average useful thrust is insufficient even though its instantaneous raw thrust is slightly larger than drag.

An initial-mass 100 m/s change requires ~61.74 days of effective firing or ~115.83 calendar days at the assumed duty without drag. This is why ion propulsion cannot replace a time-critical chemical response. The ~157 m/s impulsive disposal result cannot be used as a low-thrust spiral trajectory.

## Propellant, lifetime and mass

```text
v_e = 9.80665 × 4190 = 41,089.8635 m/s
Ideal ion Δv = v_e ln(24020/23520) = 864.354 m/s
Chemical Δv after xenon use = 9.80665 × 230 ln(23520/21320)
                             = 221.505 m/s
```

The 500 kg xenon allocation is retained rather than immediately banking the apparent Isp saving. At the reference drag and direction factor, ideal drag compensation consumes ~35.59 kg/year. Consuming all 500 kg at pair full power takes ~12,040 pair firing hours (~250 kg per head if shared equally). This is demand, not a qualified erosion/neutralizer/lifetime rating. Residuals, startup flow, other maneuvers, redundancy, storage pressure and actual throughput must be accounted for.

| Dry propulsion allocation | kg | Basis |
|---|---:|---|
| Four ion heads | 60 | 15 kg/head sizing allowance; not manufacturer CAD/mass |
| Four gimbals / launch restraints | 40 | Preliminary |
| Four PPUs | 60 | Preliminary |
| Two isolated bus front-ends | 30 | Preliminary |
| Xenon storage hardware | 100 | Pressure/temperature/volume unqualified |
| Feed / valves / controls | 60 | Preliminary |
| Retained chemical hardware | 200 | Tanks, engine and feed allocation; no vendor selection |
| Harness / mount integration | 100 | Preliminary |
| **Propulsion dry subtotal** | **650** | Replaces the earlier 400 kg allowance |

The increase is 250 kg dry + 50 kg growth = 300 kg launch mass, giving **24.02 t**. These entries define the intended boundary inside the propulsion line, not an additional mass budget to add twice. General spacecraft harness/structure allocations cover hardware outside this subsystem.

## Model detail and remaining tests

The four engine heads show chamber shells, two grid planes, neutralizers, gimbal brackets, mount bolts and wiring. The engine cutaway removes a sector to expose the discharge region; it is not an operating opening. Grid pitch/gap, voltages, engine housing, gimbal travel and 20° wire plume cones are illustrative. The 0.36 m beam scale comes from the heritage design, but no full manufacturer CAD is represented.

The service view includes retained chemical tank volumes, xenon storage, isolation/regulator/metering blocks, independent PPUs, bus adapters, orange electrical harness and silver feed branches. The stowed envelope has not been collision-qualified around fittings and gimbal travel. Wire plume keep-outs do not solve charge-exchange backflow, sputtering, contamination or array erosion.

Required closure: supplier-compatible thruster/PPU/feed system; performance/throttle map; front-end input/thermal/EMC qualification; pressure-safe xenon storage; lifetime/start-cycle analysis; gimbal alignment and center-of-mass tracking; orbit/attitude schedule; plume-surface and optical contamination analysis; torque/failure control and retained disposal capability.

Reproduce with `python3 analysis/calculate.py`; inspect `analysis/results/ion-propulsion.json` and the `ion_burn_105kw` / `ion_burn_120kw` scenarios.
