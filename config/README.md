# Klipper config

- `printer.cfg` - hardware config. All settings that came from the stock Marlin dump are filled in. Every `P??` is an MCU pin still to be measured (see `docs/pinmap.md`); Klipper will not start until they are replaced.
- `macros.cfg` - included by printer.cfg.

## Macros

| Macro | What it does |
|---|---|
| `AUTO_LEVEL_16` (also `G29`) | Heat nozzle 140 C / bed 50 C, home, wipe nozzle, tare probe, 4x4 mesh, save as profile `default`. Same sequence as the stock auto-level. |
| `AUTO_LEVEL_4` | Same, 2x2 mesh, saved as profile `quick`. |
| `CLEAN_NOZZLE [HEAT=0]` | Wipe on the silicone pad. Pad position is in `_M1S_VARS`. |
| `START_PRINT BED= EXTRUDER= MESH=` | `MESH` is a profile name, or `new4` / `new16` to re-level first, or `none`. |
| `END_PRINT`, `PAUSE`, `RESUME`, `CANCEL_PRINT` | Usual. |
| `LOAD_FILAMENT`, `UNLOAD_FILAMENT`, `M600` | Filament handling. |
| `M300`, `M355`, `LIGHT_ON`, `LIGHT_OFF` | Buzzer and case light. |

Run `SAVE_CONFIG` after a leveling macro to persist the mesh.

## Things to tune after first boot

1. Wipe pad position: jog to it, then `SET_GCODE_VARIABLE MACRO=_M1S_VARS VARIABLE=wipe_x_start VALUE=...` etc. Copy the numbers into `macros.cfg`.
2. Thermistor type for hotend and bed (placeholders are EPCOS 100K).
3. `PROBE_CALIBRATE` for the real Z offset, then `Z_OFFSET_APPLY_PROBE`.
4. `PID_CALIBRATE HEATER=heater_bed TARGET=60`.
5. Pressure advance and input shaper.
