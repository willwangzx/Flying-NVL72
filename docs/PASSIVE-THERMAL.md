# Can the heat drive its own coolant circulation?

**Yes. An electrically driven circulation pump is not inherently required.** Heat pipes, loop heat pipes (LHPs) and capillary-pumped loops use phase change and capillary pressure to transfer heat in microgravity. They are established mechanisms, but that does not qualify a 160 kW system spanning long, articulated radiator wings. [NASA thermal-control overview](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/).

This document evaluates an alternative. The current Concept D mass, power and thermal baseline still includes pumped cold plates and the full 6 kW thermal-control allocation. The model's **Passive loop concept** view is a separate schematic; its block dimensions and pipe diameters are not integrated flight geometry.

## Mechanism

1. Heat reaches a dedicated evaporator and vaporizes fluid at a porous wick.
2. Vapor travels to a cooler condenser connected to the radiator.
3. Vapor condenses, releasing latent heat; the radiator emits that heat to space.
4. Capillary pressure associated with curved liquid menisci returns liquid through the wick/return line.

The wick is the pumping mechanism, but it has no rotating motor or impeller. A loop heat pipe normally separates the capillary evaporator from the transport lines and includes a compensation chamber to manage inventory and operating state. Reliable startup and temperature regulation may still require heaters, valves and sensors. “Passive circulation” does not necessarily mean “zero electrical power in every mode.”

An ordinary gravity thermosiphon uses buoyancy and liquid head, which are not reliable restoring forces in orbital free fall. Residual accelerations and spacecraft maneuvers may disturb the loop rather than provide useful continuous circulation. A heat-driven two-phase design cannot be obtained by simply removing the pump from the existing single-phase GPU circuit.

## Capillary pressure and the central tradeoff

For an idealized fully wetting pore:

```text
Δp_cap,max = 2σ cosθ / r_pore
Δp_required = Δp_liquid + Δp_vapor + Δp_wick + Δp_fittings
              + acceleration/gravity head where relevant
Need Δp_cap,max > Δp_required with operating margin
```

Illustrative properties, **not a qualified fluid specification**: σ = 0.020 N/m, cosθ = 1.

| Effective pore radius | Ideal capillary head |
|---|---:|
| 10 μm | 4 kPa |
| 5 μm | 8 kPa |
| 1 μm | 40 kPa |
| 0.2 μm | 200 kPa |

The current primary hydraulic estimate is 200 kPa. The 5 μm example cannot replace that pump head; the passive alternative needs a much lower-loss network. Choosing a much smaller pore is not a free solution. In Darcy form, wick pressure drop scales as μL·V̇/(K A); permeability K generally decreases as pores become finer. The additional pressure loss can offset the increased capillary pressure. Wick thickness, area, conductivity and heat leak to the compensation chamber also matter.

Pressure closure is only one requirement. Heat-flux/boiling limits, dryout, vapor/sonic/entrainment limits, fluid inventory, non-condensable gas, wetting stability, startup and load-sharing must be checked. [NASA capillary-limit experiments](https://ntrs.nasa.gov/citations/20020014292) demonstrate why increasing transport resistance can cause temperature excursions and partial evaporator dryout.

## First-order scale at this spacecraft's load

For an illustrative latent heat h_fg = 1.1 MJ/kg:

```text
ṁ_phase_change = Q / h_fg = 161,552 W / 1,100,000 J/kg
               = .1469 kg/s total
```

That is less mass flow than the selected single-phase secondary loop's ~3.44 kg/s at a 10 K rise. It does **not** establish lower pipe mass or pressure loss: the vapor's volumetric flow can be large, and pressure/temperature/fluid choice controls both density and saturation temperature. Replace these illustrative properties with validated values for the actual fluid and temperature. The 2 MPa single-phase ammonia pressure target cannot automatically be reused in a two-phase loop.

One modular planning example is 5 kW per independently qualified circuit:

```text
Operating circuits = ceil(161.552/5) = 33
One-circuit-out capacity provision → 34 installed circuits
```

This is capacity arithmetic, not a demonstrated 5 kW circuit design, a reliability result or a selected BOM. Each circuit needs allocated evaporator area, heat flux, line length, routing, condenser surface and fault isolation. Independently isolating 34 long loops can increase fittings, inventory and deployment complexity. It also does not guarantee that heat can redistribute after one circuit fails.

For perspective, NASA's [CAPL-3 flight experiment](https://ntrs.nasa.gov/citations/20030025293) exercised multiple evaporators and deployable-radiator hardware up to about 1.45 kW. This establishes useful heritage for the mechanism, not a scaling law or a present-day upper limit for all LHP technology. A complete ~160 kW system requires its own qualification.

## Candidate architectures

| Architecture | What changes | Main unresolved issue | Current disposition |
|---|---|---|---|
| Pumped single-phase baseline | Existing cold plates/HX/secondary branches | Pump reliability, leaks, power and freeze control | Retained for sizing |
| Local passive heat spreading | Heat pipes spread heat within trays or panels | Interfaces, local heat flux, thermal contact and redundancy | First hybrid development candidate |
| Pumped GPU loop + passive long-distance transport | Primary circulation retained; multiple capillary circuits connect HX to radiators | Long lines, capillary head, temperature ladder, flexible joints and load sharing | Worth prototyping before full passive conversion |
| Fully passive payload-to-radiator loops | Custom evaporators at compute/services; distributed dedicated circuits | Chip heat flux, supported packaging, startup and coupled thermal stability | Open alternative; requires substantial redesign |
| Heat engine/TEG driving a pump | Waste heat converted to mechanical/electrical power | Small temperature difference, added thermal resistance, mass and reliability | No performance credit in this concept |

For the last option, even a reversible heat engine between 40°C and 26°C has η_Carnot = 1 − 299.15/313.15 = 4.47%. Real conversion is lower, and device interface temperature drops reduce the available gradient. It may be physically possible to supply a modest pump, but the added thermal path and hardware must outperform simply powering it from the solar bus. Capillary heat transport avoids an intermediate electricity-generation stage.

## Why radiator area and most of the power budget remain

Heat transport and heat rejection are different steps. At the same surface temperature, emissivity, view factors and environmental heating, the radiator still needs approximately the same 700 m². Eliminating circulation power only reduces the heat load by the actual eliminated electrical losses.

The selected primary pump hydraulic estimate is ~0.96 kW. The 6 kW thermal-control allocation includes secondary pumps, valves, instrumentation and other losses; it cannot all be removed as “pump power.” A passive alternative can still require control/startup/freeze-protection heaters. No savings are entered before the replacement design has a measured mass/power budget.

## Prototype and decision gate

Build an instrumented evaporator/wick/compensation-chamber circuit at representative device heat flux and transport length. Measure fluid/wick properties, evaporator temperature, dryout margin, pressure losses and condenser performance. Test cold startup, low-load restart, fast workload changes, freeze/thaw, partial condenser obstruction, loss of a circuit and acceleration disturbances. Include a real deployment hinge/hose or a qualified thermal joint; do not infer long-wing operation from a short bench pipe.

Then assess a distributed hybrid against the baseline for total mass, electrical power, thermal margins, deployment complexity and availability. Move to a fully passive design only after these measurements close the hydraulic and thermal constraints. The current comparison leaves both the opportunity and the open work explicit.
