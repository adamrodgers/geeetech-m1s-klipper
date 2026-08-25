# Conversion plan

Goal: Klipper on the stock mainboard, stock printhead board left as-is, a small Linux host running Klipper/Moonraker/Mainsail. Nothing cut or unsoldered, fully reversible with the firmware backup.

## Phase 0 - probe the stock firmware (USB)

Why USB and not WiFi: the WiFi path only reaches the vendor cloud app. USB gets the Marlin serial console, which tells us firmware version, board name, steps/mm, limits, PID, driver status, and probe config.

Steps are in [probe-log.md](probe-log.md). Results go in `logs/`.

## Phase 1 - backup

Dump the flash over SWD (see [firmware.md](firmware.md)). Find out whether there is a bootloader and at what offset. Store the dump.

Hardware: ST-Link V2 clone or Pi Pico with picoprobe. Four wires to `MCU-J-LINK`.

## Phase 2 - pin map

Fill in [pinmap.md](pinmap.md). Most of it comes from `M122`/`M43` if available, the rest from a meter with the case open.

## Phase 3 - Klipper MCU firmware

Build per [firmware.md](firmware.md). Flash via SWD (simplest, no bootloader questions) or ROM bootloader over USB. Verify with `ls /dev/serial/by-id/` on the host and `STATUS` in Klipper.

## Phase 4 - printer.cfg

Start minimal: steppers, endstops, heaters, thermistors, fans. Home X/Y only. Then:

- `[probe]` on the `Level` pin, `[output_pin zero_tare]` on the `Zero` pin, and a `PROBE_PREP` macro that heats (nozzle 140 C, bed 50 C, same as stock), wipes the nozzle on the silicone pad, and pulses `Zero`. Probe with the nozzle, like the stock firmware does. Mesh 4x4 over X 10..95, Y 10..100 matches stock.
- Measure `Level` polarity and timing first. If the head MCU only asserts `Level` for a short pulse, a `[gcode_button]` or a latch won't be enough and the probe may need `deactivate_on_each_sample` games. Unknown until scoped.
- TMC2209 UART if routed. If not, run them like the A4988s on hardware Vref.
- Bed mesh 4x4 to match the stock 16 points.
- Input shaper with an ADXL345 on the toolhead, pressure advance tuning.

## Phase 5 - quality of life

- LED and buzzer as `[output_pin]`.
- Filament sensor as `[filament_switch_sensor]`.
- Decide what to do with the ESP32 module: leave it unpowered, remove it, or reflash it as a transparent WiFi-serial bridge so the host does not need to be next to the printer.
- Mount the host inside the base if there is room near the Y motor.

## Host hardware

Anything that runs Klipper. A Pi Zero 2 W is enough and fits inside. Power it from the mainboard's 5 V rail only after checking the buck can supply the extra ~1 A; otherwise a separate 24 V to 5 V module off the barrel jack input.

## Risks and unknowns

| Risk | Impact | Mitigation |
|---|---|---|
| Readout protection on the APM32 | No stock firmware backup; conversion becomes one-way | Decide before unlocking whether that is acceptable |
| `Level` signal is a pulse rather than a level | Probe needs extra handling | Scope it; worst case a 74-series latch on a perf board |
| TMC UART not routed | No stealthChop config, no sensorless | Hardware Vref is fine for this machine |
| Printhead MCU expects a handshake/heartbeat from Marlin | Probe never arms | Sniff `Zero`/`Level` while stock Marlin does an auto-level |
| CH340 on a USART other than USART1 | ROM bootloader over USB fails | SWD |
| Unknown crystal | Serial garbage | Read the crystal marking, or compute from Marlin's reported clock |

## Screen

Lost. There is no Klipper driver for a SPI TFT with this board's encoder. Options later: leave it blank, or wire a KlipperScreen-capable display to the host. Not worth effort on a 100 mm printer.

## Internal USB harness (later mod)

The rear USB-B jack lives on the passive rear I/O board and reaches the mainboard over a 4-wire JST (near the `D+ GND` / `J16 5V PWR` silkscreen). For a fully internal Pi: unplug that JST, cut the A-end off a USB cable and terminate it with a matching JST (red 5V, white D-, green D+, black GND - verify with a meter, and verify the board-side pinout by continuity to the rear B jack: pin 1 VBUS, 2 D-, 3 D+, 4 GND). Pi USB-A then plugs straight into the mainboard and the external B port goes dead. Do this only after the conversion is proven over a normal external cable. Power the Pi from its own 2.4 A+ supply, never from the printer's 5 V rail.
