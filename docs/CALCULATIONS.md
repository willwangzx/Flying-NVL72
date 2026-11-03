# Detailed engineering calculations

Baseline: Concept C, 3 November 2026. Decimal kB/GB/TB/PB and SI units unless stated otherwise. Values are rounded here; JSON outputs retain numerical precision. All results are first-order sizing, not measured performance. The executable model is [calculate.py](../analysis/calculate.py); inputs are [inputs.json](../analysis/inputs.json).

## 1. Orbit and operating boundary

Select a 600 km circular orbit and a dawn–dusk sun-synchronous preference. The approximate 97.8° inclination in the concept is not independently propagated here. A 36-minute eclipse is retained as a conservative operating case; dawn–dusk does not mean zero eclipse for every season or attitude.

Using Earth radius 6,371 km and μ = 3.986004418 × 10¹⁴ m³/s²:

```text
r = (6371 + 600) × 1000 = 6,971,000 m
T = 2π √(r³/μ) = 96.5389 min
t_sun = T − 36 = 60.5389 min
v_circular = √(μ/r) ≈ 7.562 km/s
t_eclipse,max(beta = 0) = T/π × asin(R_E/r) ≈ 35.4 min
```

The 36-minute input is slightly above the ideal cylindrical-shadow, zero-beta geometric maximum at this radius. It is an energy-sizing stress case, not a propagated contact/eclipse schedule. Sun angular size, actual orbit and operational transitions require a time-domain mission analysis. The HTML permits this conservative case with a small geometric tolerance.

The Python relay geometry uses the selected orbit altitude. The HTML relay calculator explicitly uses the fixed 600 km baseline independently of its power-calculator altitude slider. Neither model derives radiation, density, contacts or radiator view factors from altitude.

## 2. Bus power and current

The 120 kW compute allocation is downstream of the main converter and includes local conversion losses, GPUs/CPUs, NVLink, NIC and rack management. It is not a claim about measured custom hardware.

```text
P_converter,input = 120 / 0.96 = 125 kW
P_converter,loss  = 125 − 120 = 5 kW
P_overhead = 6 thermal + 3 communications + 2 cache/management
             + 1 flight/attitude + 1 miscellaneous = 13 kW
P_bus = 125 + 13 = 138 kW
P_design = 138 × 1.10 = 151.8 kW
I_compute,800V = 125,000/800 = 156.25 A
I_compute,50V = 120,000/50 = 2,400 A aggregate
I_branch = 2,400/8 = 300 A for eight equal branches
```

Each independently isolatable 150 kW converter train needs about 3,000 A output capability at 50 V. A/B redundancy cannot be claimed until bus faults, cross-strapping, startup and common-cause failures are addressed. No assumption of negligible conductor/contact losses is permissible: I²R and transient impedance must be included in the actual design.

The 5 kW electric thruster is outside this nominal continuous allocation. Reduce compute input by at least 10 kW during burns and verify full spacecraft transients. Safe mode has a separate ≤8 kW target, not the full-load 13 kW overhead applied unchanged.

## 3. Solar generation and orbital energy closure

```text
P_array = A × S × η_cell × coverage × EOL/temperature × tracking × delivery
        = 1100 × 1361 × .30 × .90 × .80 × .97 × .95 / 1000
        = 297.9888 kW at the defined sun-normal condition
```

The 0.80 factor combines cell temperature and end-of-life degradation; it must be replaced with a vendor and orbit model. The 0.97 tracking factor is an assumed time-averaged performance, not a gimbal specification. Array self-heating is radiated by the blankets, not assigned wholesale to the compute radiator. Excess generation is curtailed at the arrays; it is not shunted into the liquid loop.

With charge and discharge efficiencies both 0.95:

```text
η_cycle = .95² = .9025
E_eclipse,load = 151.8 × 36/60 = 91.08 kWh
E_recharge,bus = 91.08/.9025 = 100.9197 kWh
P_charge,required = E_recharge,bus / (60.5389/60) = 100.0213 kW
P_solar,required = 151.8 + 100.0213 = 251.8213 kW
P_charge,available = min(120, 297.9888 − 151.8) = 120 kW
Generation margin = 297.9888/251.8213 − 1 = 18.33%
```

Both generation and charger power must close. Plenty of array area cannot overcome a battery converter charge-power limit. Eclipse-free operation needs 151.8 kW reserved generation, but still needs safe-mode/startup battery capacity.

## 4. Battery sizing, SOC and failure

```text
E_EOL = 200 × .80 = 160 kWh
E_allowed = 160 × .75 = 120 kWh stored energy
E_delivered = 120 × .95 = 114 kWh
Energy margin = 114/91.08 − 1 = 25.16%
Maximum eclipse from stored energy alone = 114/151.8 × 60 = 45.06 min
Installed battery mass = 200/.12 = 1,666.67 kg
```

The 45-minute figure is an energy limit, not a physically predicted eclipse. The SOC chart starts at 95% of EOL capacity and permits a 20% floor. At the design eclipse, stored energy used is 91.08/.95 = 95.8737 kWh and ending SOC is about 35.08%. Return to starting SOC requires adequate sunlit charging. Charge taper, temperature limits, cell balancing and battery degradation beyond the selected retention factor are omitted.

One of four 50 kWh strings lost leaves 150 × .80 × .75 × .95 = 85.5 kWh deliverable, below 91.08 kWh. Full-power eclipse operation fails. Approximately 112 kW compute input is the energy-only ceiling; use additional operational margin. Repeated 36-minute eclipses over three years imply roughly 16,345 orbital cycles, so an actual duty-cycle/endurance qualification is essential.

## 5. Peak heat accounting

Almost all compute electrical input eventually becomes spacecraft heat. Treating all reserved bus load as heat is conservative for tiny exported optical/RF power. Main DC conversion loss is already included in P_bus and must not be counted twice.

```text
Battery cycle loss per orbit = E_eclipse,load × (1/η_cycle − 1)
                             = 9.8397 kWh
Assign all cycle loss to sunlight for thermal sizing:
Q_peak = P_design + E_cycle,loss/t_sun_hours
       = 151.8 + 9.7521 = 161.5521 kW
```

Discharge loss really occurs in eclipse and charging loss in sunlight. Putting all cycle loss in sunlight overstates the sunlit peak under this simplified model and bounds the eclipse loss for this case. An integrated nodal/transient model is still required, particularly for batteries with different temperature limits from the compute loop.

## 6. Radiator sizing from first principles

For one credited emitting face:

```text
q_net = η_area [εσ(T_skin⁴ − T_space⁴) − q_absorbed]
T_space contribution ≈ 0 for this sizing case
T_skin = 26 + 273.15 = 299.15 K
ε = .90; η_area = .90; q_absorbed = 80 W/m²
q_net = .90[.90 × 5.670374419e−8 × 299.15⁴ − 80]
      = 295.8348 W/m² of physical area
Q_rad = 700 × 295.8348 / 1000 = 207.0843 kW
A_min = 161,552.1 / 295.8348 = 546.09 m² before margin
Capacity margin = 207.0843/161.5521 − 1 = 28.18%
```

The area factor represents fin efficiency/obstruction; emissivity is distinct. `q_absorbed` is defined on the effective emitting area in this model. Applying absorbed flux to a different area convention changes the result; resolve that in a nodal model. Do not count the second face without establishing its temperature, coating and unobstructed view factors.

Four wings × fourteen panels × 12.5 m² = 700 m². Each panel rejects 3.6979 kW under the selected conditions, each wing 51.7711 kW. The ≥60 kW branch equipment rating is a fluid-system sizing intent, not an assertion that a wing rejects 60 kW at the baseline temperature.

The 80 W/m² environment allowance is illustrative: 20 direct solar + 40 Earth IR + 20 albedo/mutual heating. With solar absorptivity .10, normal sunlight alone gives .10 × 1361 = 136.1 W/m². To keep the direct solar contribution at 20 W/m² without shade, cosine incidence must be ≤20/136.1 ≈ .147 (incidence at least 81.5° from the surface normal). This demands attitude and radiator articulation; it cannot be inferred from the word “vacuum.”

```text
q_absorbed,max = εσT⁴ − Q_peak/(Aη_area)
              = 152.2734 W/m²
At 180 W/m²: Q_rad = 144.0843 kW < 161.5521 kW: FAIL
```

This maximum has **zero remaining scalar margin**. Flight operation needs a lower bound plus uncertainty allowance. Near the baseline, dQ/dT = 4Aη_area εσT³ ≈ 3.44 kW/K and dQ/dq_absorbed = −Aη_area/1000 = −0.63 kW per W/m². Environmental uncertainty can dominate a few kelvin of radiator optimization.

### Conditional warmer-loop optimization

Concept B used 21°C skin and 800 m²: 217.4820 kW. Its minimum area at the same demand is about 594.26 m². Concept C raises skin temperature by 5 K and removes 100 m². The new area still has 28.18% scalar margin but less failure reserve than Concept B.

If any device cannot meet its temperature limit at 30°C primary inlet, use the 25°C inlet / 21°C skin / 800 m² fallback or reduce load. The fallback requires physically different radiator hardware; moving an HTML slider does not enlarge deployed panels.

### Lost radiator wing

```text
A_remaining = 3 × 175 = 525 m²
Q_remaining = 155.3133 kW < 161.5521 kW
Q_peak = 1.1(P_compute/.96 + 13)
         × [1 + (36/60.5389)(1/.9025 − 1)]
```

Solving the inequality gives about 114.88 kW compute for zero capacity reserve, or about 103.30 kW for 10% capacity reserve. Adopt a provisional 100 kW fault-mode cap. This is workload throttling on installed hardware, not guaranteed preservation of full NVLink functionality after a damaged compute tray.

## 7. Temperature ladder, flow and pressure

| Location | Cold / hot |
|---|---|
| Primary liquid | 30 / 40°C |
| External secondary liquid | 23 / 33°C |
| Mean secondary fluid | 28°C |
| Mean radiator skin | 26°C |
| Heat-exchanger terminal approach | approximately 7 K |

The 4 K offset from skin to compute inlet follows the selected ladder, not a universal cooling law. No heat pump is credited.

```text
ṁ_primary = 120/(4.18 × 10) = 2.8708 kg/s
V̇ ≈ 172.25 L/min at assumed 1000 kg/m³
P_pump = Δp V̇ / η = 200000 × .0028708/.60 = .9569 kW
ṁ_secondary = 161.5521/(4.7 × 10) = 3.4373 kg/s
Secondary per wing ≈ .8593 kg/s under equal full-load sharing
```

These flow estimates do not specify pipe diameters or validate pressure drop. The 6 kW thermal subsystem allocation includes both circuits, valve/instrument loads and uncertainty. Parallel branch balancing, fluid viscosity/density at temperature, pump curves, bend losses and gas handling remain open.

Primary inlet target: 0.4 MPa absolute; approximately 0.6 MPa discharge at the assumed pressure drop. External ammonia target: 2 MPa absolute near 33°C. These are operating targets, **not** proof pressure, maximum allowable working pressure or relief settings. Determine cavitation margin and saturation/subcooling using validated fluid data. Qualify double-wall exchangers, corrosion, freeze/thaw, accumulators, rotating hoses and transient pressures.

For each device: T_junction = T_local_fluid + P_device × R_total. A 30°C rack inlet does not establish junction temperature or cooling of adjacent low-power devices. At 151.8 kW, two minutes without heat rejection stores 18.216 MJ. Immediate protection is required on loss of flow; no such passive buffer is credited.

## 8. Mass and structural allocation

The complete itemized budget is [mass-budget.csv](../analysis/results/mass-budget.csv).

```text
Solar: 1100 × 2.5 = 2,750 kg
Radiator/wing hardware: 700 × 6 = 4,200 kg
Battery: 200/.12 = 1,666.67 kg
Other fixed allocations: 8,900 kg
Dry subtotal = 17,516.67 kg
Dry growth = .20 × 17,516.67 = 3,503.33 kg
Propellant = 500 xenon + 2200 chemical = 2,700 kg
Launch total = 23,720 kg
```

The fixed subtotal includes custom compute 2,000 kg, vented frame/MMOD 1,500 kg, shielding 1,600 kg and all remaining service allocations. The radiator density includes panels/deployment hardware; the separate 1,200 kg thermal allocation includes pumps, exchangers, fluid and extra cold plates. Actual equipment boundaries must prevent omission or double counting.

Removing 100 m² at 6 kg/m² saves 600 kg dry and 720 kg after 20% growth. No savings from new lasers are credited without a supplier interface/mass budget.

```text
6 g axial load = 23720 × 9.80665 × 6 = 1.3957 MN
2 g lateral load = 0.4652 MN
```

These are separate provisional limit-load cases; no load combination, stiffness, stress concentration, buckling, modal or ultimate-load calculation has been performed. They are not current Starship requirements.

## 9. Stowage and deployment arithmetic

```text
14 panels/wing × 0.05 m pitch = 0.70 m stack
+ .20 m root allowance + .10 m reserve = 1.00 m pack allocation
Two 5 × 2.5 m packs side-by-side → 5 × 5 m deck
Deck diagonal = √(5² + 5²) = 7.0711 m
Radial allowance inside Ø7.4 m = (7.4 − 7.0711)/2 = .1645 m
Assumed launcher radial allowance = (8 − 7.4)/2 = .30 m
Axial stack = .5 adapter + 1.4 service + 6.0 bay + 2.2 packs + .4 clearance
            = 10.5 m
```

Each solar blanket is 5.5 × 50 m; four give 1,100 m². Opposed roots at X = ±5 m plus 50 m extension produce a 110 m span. Radiator roots at Y = ±8 m plus 35 m extension produce an 86 m span. Radiator 5 m width is shown vertically, with the credited emitting faces directed outward. Intermediate deployment poses and gimbal rotations can intersect even if this final planform does not.

No launchable packing claim follows from a bounding cylinder alone. Check tapered payload volume, cargo opening, extraction/separation path, adapter, deflections, fittings and all intermediate deployments. Folded laser mounts and hoses need detailed accommodation CAD.

## 10. Propulsion, drag and disposal

Using the ideal rocket equation and a sequence of xenon consumption followed by chemical disposal:

```text
Δv_electric = 9.80665 × 1600 × ln(23720/23220) ≈ 334 m/s
Δv_chemical = 9.80665 × 230 × ln(23220/21020) ≈ 225 m/s
```

Tank residuals, usable fraction, thruster performance at operating points, finite-burn loss, attitude expenditures and leak margins are omitted. Isp alone does not establish thrust or burn duration at 5 kW.

```text
F_drag = 0.5 ρ Cd A v²
Δv_year ≈ F_drag/m × seconds_per_year
ρ = 1e−12 kg/m³; Cd = 2.2; A_projected = 700 m²
→ approximately 59 m/s/year using v ≈ 7.562 km/s and 23.72 t
```

The earlier HTML narrative rounded this to 67 m/s/year; the reproducible script exposes and corrects that arithmetic in the repository edition. This is an illustrative constant-density calculation, not an atmosphere forecast. Tenfold density means tenfold demand under otherwise identical assumptions. A 250 m/s drag allocation plus 40 m/s maneuver allocation leaves approximately 44 m/s ideal contingency; it does not prove a three-year lifetime.

For an impulsive reduction from a circular 600 km orbit to 50 km perigee:

```text
r_a = R_E + 600 km; r_p = R_E + 50 km; a = (r_a+r_p)/2
Δv = √(μ/r_a) − √[μ(2/r_a − 1/a)] ≈ 157 m/s
```

Reserve about 175 m/s for disposal plus 25 m/s operational allowance as planning targets. Disposal corridor, timing, finite burn, break-up, surviving fragments and authorization remain unverified. Electrical power cannot be assumed available after a major spacecraft failure.

## 11. Optical relay and data budget

Public partner Mini Laser material describes a 25 Gb/s design class. Count one active link; the second is reserved for handover or redundancy. Two terminals do not establish 50 Gb/s service. SpaceX must supply an approved terminal and agree orbit acceptance, access, routing and capacity.

```text
Useful average = min(allocated rate, terminal rating) × payload efficiency × usable fraction
               = 25 × .80 × .90 = 18 Gb/s
Data/day = 18 × 86400 / 8 / 1000 = 194.4 TB/day
1 PB = 1000 TB; transfer time = 1000/194.4 = 5.144 days
10 Gb/s allocation → 7.2 Gb/s average → 77.76 TB/day
Zero service → zero throughput; transfer time undefined, not zero
```

The same 5.144-day cache figure applies to filling an empty 1 PB cache at 18 Gb/s with no egress. At other generation/egress rates, buffer time is free capacity divided by net accumulation. No workload generation rate is inferred from GPU count.

For a 100 km atmospheric limb-clearance shell and ideal spherical Earth:

```text
R_clear = 6371 + 100 km
r_ours = 6371 + 600 km; r_peer = 6371 + 550 km
R_max = √(r_ours² − R_clear²) + √(r_peer² − R_clear²)
t_one_hop = 2500/299792.458 = 8.339 ms
ω_stress ≈ 15/2500 rad/s = .344°/s
```

This establishes only geometric possibility, not a peer at that location or a supported pointing rate. It excludes spacecraft masks, Sun limits, jitter, ephemeris error, link acquisition and scheduled capacity. End-to-end latency also includes other mesh hops, gateway downlink, queues and ground routing. Optical power, aperture, wavelength, receiver sensitivity and link margin are deliberately left unspecified pending the terminal interface.

## 12. Interpretation of margins

Capacity margin means capacity/demand − 1, not unused capacity/capacity. Power reserve is already inside demand; dry-mass growth is separate. Do not add these percentages as if they represented the same uncertainty.

The 20% mass growth is an allocation, not a probabilistic confidence bound. No Monte Carlo reliability claim, full thermal model, detailed finite-element model, radiation transport, manufacturer CAD or actual flight qualification data is included.
