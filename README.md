# Geeetech M1S on Klipper

Notes, teardown data, and configs for converting a stock Geeetech M1S mini printer to Klipper, keeping the original mainboard and printhead electronics.

## Status

| Stage | State |
|---|---|
| Research and teardown data | done (from photos and docs; not yet verified on this unit) |
| Serial probe of stock Marlin (`M115`/`M503`/`M122`) | not started |
| Stock firmware backup | not started |
| Pin map | partial, see [docs/pinmap.md](docs/pinmap.md) |
| Klipper MCU build and flash | not started |
| `printer.cfg` | not started |
| Load-cell probe under Klipper | not started |

## Summary of findings so far

- Main MCU is a **Geehy APM32E103VET6**, an STM32F103VE clone. Klipper's STM32F103 target should run on it.
- Drivers are soldered: **2x TMC2209** and **2x A4988-class** parts.
- The board has a **BOOT0 jumper** and an **SWD header**, so it can be flashed over the USB serial bootloader or with an ST-Link. No board swap needed.
- The printhead has its own small MCU plus a **CS1237 load-cell ADC**. It outputs the probe as a plain digital `Level` line and takes a `Zero` (tare) input. Klipper can treat it as an ordinary `[probe]`.
- USB to the host goes through a CH340-class USB-UART on the display board. The M1S WiFi/Bluetooth ESP32 module hangs off a UART header on the same board and is only useful with the vendor app.
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
  stock-m1/        board and internals photos (from 0dysseusRex, CC0)
  crops/           zoomed chip markings
config/            printer.cfg and Klipper build config, once they exist
logs/              raw serial dumps from the stock firmware
```

## Credits

Internal photos are from the [0dysseusRex/Geeetech-M1-Upgrade](https://github.com/0dysseusRex/Geeetech-M1-Upgrade) repo (CC0), which documents a full electronics swap on the M1. This project takes the other route and keeps the stock boards. Research and write-up were done with help from Claude.
