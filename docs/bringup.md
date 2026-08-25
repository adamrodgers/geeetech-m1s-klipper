# Klipper bring-up checklist

Order matters. Do not skip ahead of a failed step. Klipper console = Mainsail at http://m1s.local.

## 0. Preconditions
- [ ] Flash dump taken and verified (firmware.md), klipper.bin flashed
- [ ] Pin map filled in printer.cfg (no P?? left)
- [ ] Printer on its own PSU, USB A-to-B to the Pi
- [ ] `ls /dev/serial/by-id/` on the Pi; put the exact id in [mcu]

## 1. Connectivity
- [ ] Klipper connects (Mainsail shows "Printer ready")
- [ ] `STATUS` sane; `temperature_sensor mcu` plausible (comment out if it errors)

## 2. Sensors before any motion
- [ ] Hotend and bed temps read room temperature (+-3 C). Wrong constant reading = wrong sensor_type; swap thermistor table candidates (Generic 3950, ATC Semitec 104GT-2, EPCOS 100K)
- [ ] `QUERY_ENDSTOPS`: all open at rest. Press each by hand: X (head switch), Y, Z button, filament sensor. Fix `!` inversions until press = TRIGGERED
- [ ] `QUERY_PROBE` open; after `_PROBE_TARE` + nozzle press, probe triggers (watch for the ~2 s ready pulse false-trigger)

## 3. Heaters (still no motion)
- [ ] `M104 S60`: hotend climbs promptly, no "heating failed". Same for bed `M140 S40`
- [ ] Part fan `M106 S255` -> blower spins; hotend fan kicks in above 50 C; LED/beeper macros work

## 4. Motion, one axis at a time
- [ ] `STEPPER_BUZZ STEPPER=stepper_x` (head wiggles ~1 mm); repeat y/z/extruder
- [ ] Direction check per axis with FORCE_MOVE small +moves: +X right, +Y bed toward front (nozzle toward back), +Z up. Wrong way = invert dir_pin `!`
- [ ] `G28 X` then `G28 Y` alone; then full `G28` (Z presses the button at X115 Y0)
- [ ] Soft limits: jog to X0/X115, Y0/Y114 without grinding

## 5. Probe and leveling
- [ ] `PROBE_ACCURACY` at bed center (after _PROBE_HEAT + CLEAN_NOZZLE + _PROBE_TARE): range < 0.05 mm hoped
- [ ] Paper test at bed center after G28; adjust stepper_z position_endstop until nozzle-paper drag at Z0
- [ ] `AUTO_LEVEL_16`; mesh range should resemble stock (~0.2 mm). SAVE_CONFIG
- [ ] Verify wipe: CLEAN_NOZZLE strokes the pad, no crash into bed clip

## 6. Extruder
- [ ] Load filament, `M109 S200`, extrude 50 mm marked: measure, fix rotation_distance (570 steps/mm heritage = 5.614)
- [ ] `PID_CALIBRATE HEATER=extruder TARGET=200`, then `HEATER=heater_bed TARGET=60`; SAVE_CONFIG (replaces watermark)

## 7. First print
- [ ] Slice a 20 mm cube, Klipper flavor, label objects ON, start gcode `START_PRINT BED=[first_layer_bed_temperature] EXTRUDER=[first_layer_temperature]`
- [ ] Watch first layer; live-adjust with `SET_GCODE_OFFSET Z_ADJUST=` / babystepping in Mainsail; fold result into position_endstop
- [ ] After success: pressure advance tuning, input shaper (ADXL later), raise speeds per the TUNING comments

## Rollback
Stock restore = write the saved dump back over SWD/serial (firmware.md). EEPROM settings live in the dump too.
