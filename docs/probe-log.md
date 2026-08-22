# Stock firmware probe

Commands to run against the stock Marlin over USB, and a place to record what came back. Save raw output to `logs/` with a date.

## Connect

```sh
ls /dev/cu.*                       # expect cu.wchusbserial* (CH340)
system_profiler SPUSBDataType | grep -A8 -i 'ch340\|usb serial\|1a86'
```

Open a terminal at 115200 first; if output is garbage, 250000.

```sh
# picocom (brew install picocom). Ctrl-A Ctrl-X to exit.
picocom -b 115200 --imap lfcrlf /dev/cu.wchusbserial*
```

Or log everything with a script (see `scripts/` once it exists).

## Commands

| Command | What it tells us |
|---|---|
| `M115` | Firmware name/version, `MACHINE_TYPE`, board, capabilities |
| `M503` | Full settings dump: steps/mm, limits, accel, jerk, PID, probe offsets, bed mesh, advance, shaping |
| `M122` | TMC driver status. If it errors, TMC UART is not compiled in / not wired |
| `M119` | Endstop and probe state. Press the nozzle while polling to see `Level` |
| `M569` | Stepper driver modes |
| `M593` | Input shaper settings |
| `M900` | Pressure advance (linear advance) |
| `M301` / `M304` | Hotend / bed PID |
| `M43` | Pin state dump, if `PINS_DEBUGGING` is enabled |
| `M43 E1` | Watch pins for changes |
| `M105` | Temps, sanity check |
| `M106 S255` / `M107` | Fan test |
| `M42 P<pin> S<val>` | Drive a pin directly, useful for identifying LED/buzzer/Zero |
| `M81`/`M80` | Power control, probably unsupported |

Also try `M0` (pause), `G28`, and `G29` with the USB attached, and watch the output for any messages about the probe, to see what Marlin says to the head MCU.

## Results

### Session 1 - 2026-08-22

Raw output: [`logs/2026-08-22-stock-marlin-dump.txt`](../logs/2026-08-22-stock-marlin-dump.txt), [`-dump-2.txt`](../logs/2026-08-22-stock-marlin-dump-2.txt), [`-outputs-test.txt`](../logs/2026-08-22-stock-marlin-outputs-test.txt). Script: [`scripts/marlin_query.py`](../scripts/marlin_query.py).

**Connection**

- USB device: `1a86:7523` (CH340), `/dev/cu.wchusbserial10` on macOS.
- Baud: **250000**. 115200 and others get no response. The first command after opening the port is eaten by line noise; send `M110` first.
- Opening the port does not reset the board (no boot banner on DTR toggle).

**M115**

```
FIRMWARE_NAME:Marlin M1S_V1.96_MCU103 (Nov 19 2025 17:36:01)
MACHINE_TYPE:GEEETECH M1S  EXTRUDER_COUNT:1
Cap: EEPROM:1 AUTOLEVEL:1 RUNOUT:1 Z_PROBE:1 LEVELING_DATA:1 TOGGLE_LIGHTS:1
     SDCARD:1 SD_WRITE:1 LONG_FILENAME:1 ARCS:1 BABYSTEPPING:1 THERMAL_PROTECTION:1
     EMERGENCY_PARSER:0 HOST_ACTION_COMMANDS:0 CONFIG_EXPORT:0 BINARY_FILE_TRANSFER:0
```

"MCU103" in the version string matches the STM32F103-class APM32 on the board. `EEPROM:1` with `CONFIG_EXPORT:0`, `M43` is not compiled in.

**M503 highlights**

| Setting | Value |
|---|---|
| Steps/mm | X 80, Y 80, Z 830, E 570 |
| Max feed (mm/s) | X 200, Y 200, Z 25, E 60 |
| Max accel | X 3000, Y 3000, Z 500, E 5000 |
| Default accel | print 2000, retract 3000, travel 3000 |
| Jerk | X 10, Y 10, Z 0.3, E 10; min segment 20 ms |
| Travel limits (`M211`) | X 0..115, Y 0..114, Z 0..95 |
| Bed mesh | 4x4 (16 points), leveling on, fade height 10 mm |
| Probe offset (`M851`) | X0 Y0 Z0.02 (nozzle is the probe) |
| Hotend PID | P18.80 I1.39 D64.34 |
| Bed | bang-bang (`M304` not recognised) |
| TMC current (`M906`) | X 800, Y 800 (Z/E not TMC) |
| Driver mode (`M569`) | X, Y stealthChop |
| Input shaper (`M593`) | X and Y 30 Hz, damping 0.20 |
| Linear advance (`M900`) | K 0.10 |
| Firmware retract | 3 mm @ 2700 mm/min |
| Runout sensor (`M412`) | off in EEPROM, 310 mm distance; `M119` reports it `TRIGGERED` with filament loaded |
| Power-loss recovery | on |
| Preheat | PLA 190/50, TPU 200/50 |

Z at 830 steps/mm is unusual (not a 4 mm or 8 mm lead at 1/16). Check the Z drive when the base is open.

**M122 (TMC2209 UART)**

- X at UART address 0, Y at address 3. UART is wired to the MCU.
- Y answers normally (stealthChop, 16 usteps, interpolation on, 800 mA set, vsense high).
- X: "Bad response", "Testing X connection... Error: All LOW", reads 256 usteps / interp off, and stays reported as `Enabled false` even after `M17`. Marlin falls back to the driver's default standalone config for X. Either the X driver's `PDN_UART` is not actually connected, or it is on a different single-wire bus than Marlin expects. The axis still moves under stock firmware, so it works in standalone mode. Under Klipper, configure Y with `[tmc2209]` and try X; if it fails, run X without a UART section.

**M119**

```
x_max: open   y_min: open   z_min: open   z_probe: open   filament: TRIGGERED
```

X homes to **max**. Y and Z home to min. The `z_probe` input is the head MCU's `Level` line. Whether it shows TRIGGERED on nozzle contact, or only during an armed probe after `Zero`, is still to be tested.

**Outputs**

`M355` (case light), `M300` (buzzer), `M106/M107` (part fan) are all accepted. Visual confirmation pending.

**SD card**

The bundled card has Geeetech's sample G-code plus a leftover copy of a slicer install folder (FT232 drivers, libusb). Nothing that looks like a bootloader update file.
