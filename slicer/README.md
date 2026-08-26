# OrcaSlicer profiles for the M1S (Klipper)

Three importable presets:

- `Geeetech M1S Klipper.json` — machine (100x110x100, Klipper flavor, START_PRINT/END_PRINT, limits matched to printer.cfg)
- `M1S 0.20mm Standard.json` — process (0.2mm layer, speeds at a conservative untuned starting point)
- `M1S Generic PLA.json` — filament (200/60, PA 0.04, 10 mm³/s volumetric cap as a placeholder)

## Import

OrcaSlicer → top bar, the small **import** icon (or File → Import → Import Configs…) → select all three JSONs. Then pick "Geeetech M1S (Klipper)" as the printer.

If OrcaSlicer rejects the custom machine on import (the `inherits` base must exist), instead create the printer once via **Printer → Add/Custom Printer** using `orcaslicer-m1s-klipper.md`, then import just the process/filament.

## Connect to the printer

Printer settings → **Physical Printer** → type: Klipper (Moonraker), Hostname `m1s.local` (or 192.168.1.154). Lets you upload/print straight from Orca.

## Notes
- `filament_max_volumetric_speed: 10` is a **placeholder** — replace with the measured max flow (see docs/benchmarks.md) once we run the flow test.
- Speeds/accel here are conservative; raise them in lockstep with printer.cfg as we tune, and keep docs/benchmarks.md updated.
- Enable **Label objects** (Others tab) — KAMP purge and exclude-object need it.
