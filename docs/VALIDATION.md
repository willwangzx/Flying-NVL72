# Validation scope

## Reproducible checks

`python3 analysis/calculate.py` writes baseline JSON, ten scenario results and the mass CSV using standard-library Python. `python3 -m unittest discover -s tests -v` checks energy/heat accounting, baseline arithmetic, radiator/environment limits, degraded cases, zero-service behavior, invalid time/range boundaries and generated-file consistency.

`npm install` followed by `npm test` executes the actual embedded HTML script in a controlled DOM/canvas harness. It checks all seven views, finite geometry, 56 deployed panels, laser presence/Ka removal, selection/isolation/focus, OBJ export, scenario controls, relay changes/outage/geometry, shell/explosion/wireframe/flow controls, small-screen canvas dimensions, DOM IDs and anchor links. It also compares the HTML scalar outputs with the independent Python baseline results. Rendered canvases go to `test-output/` for inspection.

These tests guard against numerical/code regressions and missing model geometry. They do not prove a physical spacecraft functions. The two implementations share the stated analytical assumptions, so their agreement is a consistency check, not independent physical validation.

## Not verified

- Real-browser CSS layout, fullscreen behavior, accessibility and input-device behavior end to end.
- Mechanical clearances in every deployed/stowed/intermediate pose; the renderer is not a collision solver.
- Flight-material properties, manufacturing tolerances, mass closure from a BOM, pressure containment, electronics compatibility or measured thermal performance.
- Radiation reliability, battery life, deployment reliability, flexible-body dynamics, optical jitter, ephemeris coverage or contracted service.
- Current Starship accommodation or launch loads.

No CI service or hosted Pages site is enabled by this initial repository publication. The commands above are runnable locally; passing them is not a qualification certificate.
