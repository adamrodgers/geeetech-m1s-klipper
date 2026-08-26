# M1S performance log

Tracking the printer as we tune it. "Kid's printer" baseline → wherever we can push it.

## 3DBenchy times

| Date | Firmware / setup | Time | Notes |
|---|---|---|---|
| (stock) | Marlin M1S_V1.96, stock profile | **58 min** | factory baseline |
| | Klipper, first tuned pass | _tbd_ | |

## Max volumetric flow (mm³/s)

Measured by extruding at increasing rates until under-extrusion (the "flow rate test": push filament faster and faster, watch where the extruder skips or output drops).

| Date | Setup | Max flow | Method |
|---|---|---|---|
| | stock hotend, 50 W ceramic, 200 °C PLA | _tbd_ | |

## Speed / acceleration

Stock Marlin values (baseline): max_accel 3000, X/Y feed 200 mm/s, SCV 5, input shaper 30 Hz.

| Date | max_velocity | max_accel | SCV | shaper (X/Y) | flow limit | Notes |
|---|---|---|---|---|---|---|
| stock | 200 | 3000 | 5 (jerk 10) | 30 Hz mzv | — | Marlin baseline |
| Klipper start | 300 | 4000 | 8 | 30 Hz mzv | — | untuned starting point in printer.cfg |

## TEST_SPEED results (skip/torque ceiling)

Ellis TEST_SPEED, comparing mcu stepper positions before/after (skip = delta > 16 microsteps). These are the SKIP limit, NOT the print-quality limit - real print accel is far lower (ringing on a plastic frame). Shows the motors have huge torque headroom.

| Speed (mm/s) | Accel (mm/s2) | X delta | Y delta | Result |
|---|---|---|---|---|
| 200 | 5000 | 0 | 0 | pass |
| 200 | 7500 | 0 | 0 | pass |
| 300 | 7500 | 1 | 1 | pass |
| 500 | 10000 | 0 | 0 | pass |
| 500 | 15000 | 0 | 0 | pass |
| 500 | 20000 | 2 | 2 | pass |
| 600 | 20000 | 0 | 0 | pass |
| 600 | 25000 | 1 | 2 | pass |
| 750 | 25000 | 1 | 2 | pass |
| 700 | 30000 | ok | ok | pass |
| 700 | 32000 | ok | ok | pass |
| 700 | 35000 | - | - | SKIPPED |

Ceiling is between accel 32000 (pass) and 35000 (fail); speed fine to 750+. Next test: SPEED=700 ACCEL=34000.

## Tuning plan / method

1. **Max flow** — extrude-only test at 200/210/220 °C: `G1 E<n> F<rate>` ramps; find where actual < commanded (or extruder skips). Sets a hard ceiling on print speed for a given layer.
2. **Pressure advance** — PA tower or the KAMP/Klipper PA test; tune per filament.
3. **Input shaper** — needs an ADXL345 on the toolhead for a resonance sweep; without it, keep the stock 30 Hz and raise cautiously.
4. **Speed/accel** — raise max_accel + SCV together after shaper; re-run Benchy each pass and log here.
5. Frame is plastic (kid's printer) — watch for ringing/artifacts as the limits go up; that, not the motors, is likely the ceiling.
