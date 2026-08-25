# Geeetech M1S on Klipper

Notes, teardown data, and configs for converting a stock Geeetech M1S mini printer to Klipper, keeping the original mainboard and printhead electronics.

## Status

| Stage | State |
|---|---|
| Research and teardown data | done (from photos and docs; not yet verified on this unit) |
| Serial probe of stock Marlin (`M115`/`M503`/`M122`) | done, see [docs/probe-log.md](docs/probe-log.md) |
| Stock firmware backup | not started |
| Pin map | partial, see [docs/pinmap.md](docs/pinmap.md) |
| Klipper host (Pi 4, Mainsail at http://m1s.local) | done, see [docs/host.md](docs/host.md) |
| Klipper MCU build and flash | not started |
| `printer.cfg` | not started |
| Load-cell probe under Klipper | not started |

## Summary of findings so far

- Mainboard is `GT_FM_M1S_V0.2` (single board, in the top of the frame), not the M1's two-board stack. Main MCU is a **Geehy APM32E103VET6**, an STM32F103VE clone, 8 MHz crystal. Klipper's STM32F103 target should run on it.
- Stock firmware is Marlin `M1S_V1.96_MCU103`, 250000 baud over a CH340.
- Drivers are soldered: **2x TMC2209** (X, Y; UART wired, Y responds) and **2x A4988-class** (Z, E).
- JTAG/SWD header `J6` is populated, so the flash can be dumped and Klipper flashed with an ST-Link. No board swap needed.
- The printhead has its own small MCU plus a **CS1237 load-cell ADC**. It outputs the probe as a plain digital `Level` line and takes a `Zero` (tare) input. Klipper can treat it as an ordinary `[probe]`.
- USB to the host goes through a CH340C. An ESP32-WROOM-32E is soldered on for WiFi/Bluetooth and only talks to the vendor app; two 74*257 muxes near it probably switch the MCU UART between USB and the ESP32.
- The 2.4" TFT and encoder are not usable under Klipper; Mainsail/Fluidd replaces them.

## Layout

```
docs/
  machine.md       printer specs, mechanicals, stock software
  electronics.md   mainboard / display board / printhead board teardown
  firmware.md      stock firmware, bootloader, flashing routes
  pinmap.md        MCU pin assignments (fill in as discovered)
  klipper-plan.md  conversion plan, host setup, open questions
  probe-log.md     commands to run on the stock firmware and results
  references.md    links
photos/
  m1s/             this unit's mainboard
  stock-m1/        board and internals photos (from 0dysseusRex, CC0)
  crops/           zoomed chip markings
scripts/           serial query helper
config/            printer.cfg and Klipper build config, once they exist
logs/              raw serial dumps from the stock firmware
```

## Credits

Internal photos are from the [0dysseusRex/Geeetech-M1-Upgrade](https://github.com/0dysseusRex/Geeetech-M1-Upgrade) repo (CC0), which documents a full electronics swap on the M1. This project takes the other route and keeps the stock boards.
