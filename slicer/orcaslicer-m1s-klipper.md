# OrcaSlicer machine profile for the Klipper M1S

Create a new printer in Orca (nozzle 0.4) with:

- Printable area: 100 x 110, height 100. Origin front-left.
- G-code flavor: Klipper
- Machine start G-code:
  `START_PRINT BED=[first_layer_bed_temperature] EXTRUDER=[first_layer_temperature]`
- Machine end G-code: `END_PRINT`
- Enable "Exclude objects" / label objects (KAMP needs it)
- Machine limits: 200 mm/s, 4000 mm/s2 (match printer.cfg; Klipper clamps anyway)
- Retraction: use firmware retraction (G10/G11) OR slicer 0.8 mm @ 45 mm/s direct-drive starting point
- Physical printer (print host): type Moonraker/Klipper, host http://m1s.local
