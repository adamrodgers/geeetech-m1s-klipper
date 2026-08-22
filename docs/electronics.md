# Electronics teardown

All component IDs below were read from photos of a stock M1 (not M1S) in the 0dysseusRex repo. The M1S is believed to use the same boards with the ESP32 module populated. Verify against the actual unit before trusting any of this for wiring.

Photos: [`photos/stock-m1/`](../photos/stock-m1/), zoomed chips in [`photos/crops/`](../photos/crops/).

## Overview

Three PCBs plus a rear I/O breakout:

1. **Mainboard** (`GT_FM_M1_V0.4` silkscreen on the display side) - MCU, drivers, power, bed heater MOSFET. Two boards sandwiched: a power/driver board and a display/interface board.
2. **Printhead board** (`FM_M1-HOT_Board-V0.4`) - on the toolhead. Own MCU, load-cell ADC, connectors for hotend, fans, X motor, X endstop, extruder motor. Joined to the mainboard by a 16-way ribbon.
3. **Rear I/O board** - USB-B, DC barrel jack, rocker switch, one JST. Passive.
4. **Z endstop board** - microswitch on a tiny PCB in the base.

## Mainboard, driver side

![mainboard](../photos/stock-m1/mainboard-front.jpg)

| Ref | Part | Notes |
|---|---|---|
| U1 | **Geehy APM32E103VET6** (marking `APM32 E103VET6 SPR4Y 3201 A1 2207`) | STM32F103VE clone. Cortex-M3, 72 MHz, 512 KB flash, 128 KB SRAM, LQFP100. |
| U7, U8 | **`4988ET`** (marking `4988ET A2032 030L`) | A4988-compatible step/dir driver, no UART. Likely the Z and E axes. |
| U9, U6 | **TMC2209-LA** (Trinamic, `2433 A243S GERMANY`) | Genuine Trinamic. Likely X and Y. Whether the UART pins are routed to the MCU is unknown. |
| Y1 | crystal | 8 MHz assumed (standard for F103); check with `M115`/Klipper clock. |
| - | `470 35V` electrolytic + inductor | 24 V to 5 V buck. |
| - | `CK 100 35V` x4 | Driver bulk caps. |
| - | Buzzer | Active buzzer near the MCU. |

Headers and connectors on this side:

| Label | Purpose |
|---|---|
| `+24V GND` (J2, 2-pin) | Main DC input from rear board |
| `USB_PWR` (J15 jumper) | Power board from USB 5 V (for flashing without 24 V) |
| `MCU-BOOT` (J7 jumper, bottom right) | BOOT0. Jumpered at power-up puts the APM32 into the ROM UART bootloader. |
| `MCU-J-LINK` (6 pins: `3.3V DIO / GND CLK / GND RST`) | SWD. Use for firmware dump and recovery. |
| `SD-Board` (J8) | micro SD slot daughterboard |
| `Z-M`, `Y-M` | Z and Y motor JSTs (right edge) |
| `Y-MIN` | Y endstop |
| `FAN- FAN+` (J10/J11) | Mainboard fan |
| `BED- BED+` | Bed heater output |
| `TB` | Bed thermistor |
| 16-pin box header (top right) | Ribbon to printhead board |
| `J3` 4-pin, `J5`/`J16` | Z endstop, filament sensor, LED (assignment TBD) |

## Mainboard, display side

![display side](../photos/stock-m1/mainboard-display-side.jpg)

| Ref | Part | Notes |
|---|---|---|
| - | 2.4" TFT, ~18-pin FPC | SPI TFT, controller unknown (ST7789 or ILI9341 class). Not supported by Klipper. |
| Encoder1 | Rotary encoder with push | Menu knob |
| U12 | SOP-16 next to `USB D+ D- 5.0V` pads | USB-to-UART bridge, almost certainly CH340G. Means the host sees a CH340 serial port, not a native STM32 CDC device. |
| `ESP32 UART` header | `3.3V TXD0 RXD0 GND` | Socket for the M1S WiFi/BT module. It is a UART peripheral, not a host. |
| `ESP-BOOT` | 2-pin | ESP32 boot strap, for reflashing the module. |
| U11 | SOIC-8 near the encoder | Unknown, possibly EEPROM or level shifter. |
| `DC+24V_PWR` | 2 pads | Power input pass-through |

Pin labels along the top edge of this board are the ribbon signals, documented under the printhead board below.

## Printhead board (`FM_M1-HOT_Board-V0.4`)

![front](../photos/stock-m1/printhead-board-front.jpg)
![back](../photos/stock-m1/printhead-board-back.jpg)

| Ref | Part | Notes |
|---|---|---|
| U1 | TSSOP-20 MCU, marking unreadable | Has a programming header `J10`: `RST TDI TCK 3.3V GND`, plus `TP1 TX` / `TP2 RX` test points. TDI/TCK labeling suggests a 2-wire debug interface on a small 8-bit or Cortex-M0 part. Identify when the unit is open. |
| U2 | **Chipsea CS1237** (SOIC-8, marking `CS1237-SO`) | 24-bit load-cell ADC, 2-wire (SCLK/DOUT) interface to U1. |
| U3 | SOT-23 | Likely 3.3 V LDO. |
| J7 `S+ E- S- E+` | 4-pin | Load cell (strain gauge) input |
| J9 `HED` | 2-pin | Hotend heater (24 V) |
| J3 `TH0`, J5 `TH1` | 2-pin each | Hotend thermistor and a second thermistor (bed-side? chamber? check) |
| J4 `FAN`, `Blower` | 2-pin each | Hotend fan and part cooling blower |
| J8 `E-M` | 4-pin | Extruder motor |
| J6 `X-M` | 4-pin | X motor |
| J2 `X-MIN` | 2-pin | X endstop |
| J1 | 16-pin box header | Ribbon to mainboard |

### Ribbon pinout (from silkscreen on both boards)

Two rows of 8. Labels as printed:

| Pin | Row A | Row B |
|---|---|---|
| 1 | `Zero` | `5V` |
| 2 | `Level` | `5V` |
| 3 | `TH0` | `TH0` |
| 4 | `TH1` | `TH1` |
| 5 | `X_MIN` | `GND` |
| 6 | `GND` | `GND` |
| 7 | `X-2B` | `24V` |
| 8 | `X-1B` | `24V` |
| 9 | `X-1A` | `24V` |
| 10 | `X-2A` | `24V` |
| 11 | `HED` | `HED` |
| 12 | `E-2B` | `HED` |
| 13 | `E-2A` | `GND` |
| 14 | `E-1A` | `FAN2` |
| 15 | `E-1B` | `FAN1` |

(15 labelled columns are printed; the 16th is probably a second ground. Confirm with a meter.)

What this tells us:

- **The printhead MCU owns the load cell.** It reads the CS1237 and presents the probe to the mainboard as one digital output, `Level`, and accepts one digital input, `Zero`, to tare. The mainboard's Marlin sees a normal endstop-style probe. For Klipper this means `[probe] pin:` on whatever MCU pin `Level` lands on, and a macro that toggles `Zero` before probing. No need for Klipper's `[load_cell]` support and no need to touch the head MCU's firmware.
- Step/dir for X and E do **not** go to the head; the motor phases do. All four drivers are on the mainboard. The head board is a breakout with a probe controller on it, not a CAN/serial toolhead.
- Thermistors, heater, and both fans are driven directly from the mainboard through the ribbon. `FAN1`/`FAN2` on the ribbon map to the hotend `FAN` and `Blower` connectors.
- Polarity of `Level` (active high or low) and the `Zero` pulse requirement are unknown. Scope them or read from Marlin's `M119` while pressing the nozzle.

## Rear I/O board

![rear](../photos/stock-m1/rear-io-board.jpg)

USB-B, 5.5 mm barrel jack, rocker switch, one JST back to the mainboard. Nothing active.

## Things to check on the real M1S

- [ ] Confirm mainboard revision string and that it matches `V0.4`
- [ ] Read the printhead MCU marking
- [ ] Read U12 marking (CH340G?) and U11
- [ ] Which driver drives which axis
- [ ] Whether TMC2209 `PDN_UART` pins are routed (look for a trace/resistor from pin 5 of each TMC to the MCU)
- [ ] Identify J3/J5/J16 on the mainboard
- [ ] Crystal frequency
- [ ] What is on the ESP32 module (chip, antenna, any markings)
