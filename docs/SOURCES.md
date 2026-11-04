# Sources and evidence boundaries

Design reference date: 3 November 2026. These public references informed the concept; they do not certify this spacecraft. Links may change. No proprietary SpaceX or NVIDIA engineering data is included.

1. [NVIDIA — DGX GB rack hardware guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html). Commercial reference topology and cooling architecture; the custom DC and fully cold-plated layout is an original proposal, not a published NVIDIA product.

2. [NVIDIA — GB200 NVL72](https://www.nvidia.com/en-us/data-center/gb200-nvl72/). 72 Blackwell GPUs and 36 Grace CPUs; identifies the selected computing platform.

3. [NVIDIA — Power shelf integration](https://docs.nvidia.com/base-command-manager/product-manuals/11/nvidia-mission-control/powershelf). Reference power-shelf arrangement and electrical context. Confirm final purchased-rack wiring independently.

4. [NASA — State of the Art: Thermal Control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/). Radiative heat exchange, optical surface properties and environmental heat inputs.

5. [NASA — TBIRD mission results](https://www.nasa.gov/missions/small-satellite-missions/nasas-record-breaking-laser-demo-completes-mission/). Demonstrated 200 Gb/s optical downlink; rate-class precedent only.

6. [NASA NTRS — ISS external coolant leak investigation](https://ntrs.nasa.gov/citations/20220010221). Pumped single-phase ammonia heritage and the importance of leak isolation.

7. [NASA NTRS — Thermal radiator pointing for ISS](https://ntrs.nasa.gov/citations/20000032541). Precedent for changing radiator pointing to manage the orbital heat environment.

8. [SpaceX — Starship Users Guide, revision 1.0, March 2020](https://spacex.relayto.com/e/starship-users-guide-37uiuuepbks0x). Historical preliminary payload-volume reference. Its old 8 m dynamic diameter is not a current mission-specific cargo guarantee.

9. [NASA NESC — Mitigating Risks of Single-Event Effects in Space Applications](https://ntrs.nasa.gov/citations/20210024100). Need for actual radiation characterization and mitigation of electronic components.

10. [NASA — State of the Art: Power](https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/). Background on spacecraft array/battery technology; this concept’s area density and efficiencies remain independent design assumptions.

11. [NASA NTRS — Interface Conductance Under a Real Electronics Box](https://ntrs.nasa.gov/citations/20190030287). Conductive thermal interfaces between electronics and cold plates in vacuum.

12. [NASA — Vacuum Stability](https://www.nasa.gov/centers-and-facilities/white-sands/vacuum-stability/). Material and component outgassing evaluation.

13. [NASA — Thermal Vacuum](https://www.nasa.gov/reference/jsc-thermal-vacuum/). Environmental test capabilities for components and systems.

14. [Starlink — Technology](https://starlink.com/technology). Public descriptions of compact packaging, mesh links and third-party Mini Lasers; partner terminal design rate is 25 Gb/s.

15. [Muon Space — Starlink Mini Laser integration partnership, 21 October 2025](https://www.muonspace.com/starlink-lasers-halo/). Third-party integration precedent; not a service commitment to this concept.

16. [Muon Space press release — Mini Laser integration](https://www.prnewswire.com/news-releases/muon-space-to-integrate-spacexs-starlink-mini-space-lasers-into-its-halo-satellite-platform-302589505.html). Partner statement of 25 Gb/s at up to 4,000 km; mission-specific support must be verified.

## Evidence classes

- **Published fact:** reference computing topology; existence and advertised design rate of third-party Mini Laser terminals; established spacecraft cooling mechanisms.
- **Calculated:** results derived from explicitly selected assumptions in `analysis/inputs.json`.
- **Allocation:** electrical input, mass, dimensions, coolant temperatures, array/radiator properties, service fraction and lifetime. No supplier guarantees are implied.
- **Unverified:** flight reliability, component vacuum/radiation tolerance, complete deployment, optical service access and current launcher fit.

The 2020 Starship guide is historical and cannot establish current cargo-door clearance or payload performance. TBIRD is a historical direct-ground reference, not the Concept C communications system. Public Starlink internal mesh rates must not be substituted for the partner-terminal rating.

## Additional references · 4 November 2026

17. [NASA — NEXT prototype performance, 2008](https://ntrs.nasa.gov/citations/20080012739). Reference operating point: 6.9 kW, 0.237 N, 4,190 s per head. Historical test data, not this spacecraft hardware.

18. [NASA — Electric propulsion principles](https://www.nasa.gov/humans-in-space/the-propulsion-were-supplying-its-electrifying/). Low continuous thrust and the distinction between Hall and gridded-ion acceleration.

19. [NASA — Technology infusion study, NEXT system appendix](https://ntrs.nasa.gov/api/citations/20140017777/downloads/20140017777.pdf). Heritage PPU input-interface context; spacecraft bus adaptation is separately allocated.

20. [NASA — Thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/). Heat-pipe and capillary return principles.

21. [NASA — Investigation of Capillary Limit in a Loop Heat Pipe](https://ntrs.nasa.gov/citations/20020014292). Observed capillary-limit and dryout behavior.

22. [NASA — CAPL-3 flight experiment](https://ntrs.nasa.gov/citations/20030025293). Multiple evaporators and deployable-radiator heritage; historical tested loads are far below this platform.
