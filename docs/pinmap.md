# MCU pin map

Target: APM32E103VET6 (STM32F103VE pinout, LQFP100). Fill in as pins are confirmed. Sources are marked so guesses don't get mistaken for measurements.

Source key: **M** = measured with a meter/scope, **D** = derived from Marlin output (`M122`, pins debug) or disassembly, **G** = guess from board layout.

## Steppers

| Function | STEP | DIR | EN | UART | Driver | Src |
|---|---|---|---|---|---|---|
| X | PB3 or PB5 | PB12 | PB0 | addr 0, no response | TMC2209 | DIR/EN=M, STEP=candidate |
| Y | PA1 (adj to DIR) or PA4/PA11 | PA0 | PC7 | addr 3, works | TMC2209 | DIR/EN=M, STEP=candidate |
| Z | PC2/PC4/PC5/PC6 | PC15 | PC13 | - | 4988ET | DIR/EN=M, STEP=candidate |
| E | PE2 or PE6 | PE4 | PB7 | - | 4988ET | DIR/EN=M, STEP=candidate |

STEP candidates come from the unmapped push-pull output pins (config-register decode). STEP could NOT be caught live: pulses rest low and are ~2 us wide (~0.4% duty), invisible to slow SWD sampling, and STEP is not on the same port as its DIR. **Confirm each at bring-up:** with SWD off (motion allowed), set the candidate as step_pin and `STEPPER_BUZZ STEPPER=stepper_x` - the motor moves only with the right pin. All remaining unmapped outputs: PA1 PA4 PA11 PB3 PB5 PC2 PC4 PC5 PC6 PD3 PD7 PD13 PE2 PE6 (also include probe Zero/tare output, TFT/SPI, beeper, ESP32 UART).

DIR + EN measured live (SWD ODR diff during small moves). STEP pins can't be caught by slow SWD polling (pulses rest low, ~2 us wide) - extract from firmware/m1s-stock-mcu-flash.bin by anchoring on the known DIR/EN pins.

## Endstops and probe

| Function | Pin | Pull / polarity | Src |
|---|---|---|---|
| X endstop (head switch, homes to max) | PB4 | | M |
| Y endstop | PC14 | | M |
| Z endstop (frame reference button) | PD6 | | M |
| `Level` (probe trigger, Marlin z_probe) | ? | needs arming to test live; get from binary | - |
| `Zero` (tare output to head MCU) | ? | get from binary | - |
| Filament runout | PA15 | | M |

## Heaters, thermistors, fans

| Function | Pin | Notes | Src |
|---|---|---|---|
| Hotend heater `HED` | PB9 | | M |
| Bed heater | PE0 | | M |
| TH0 (hotend) | PC0 or PC1 | analog; assign by heating | M |
| Bed thermistor | PC0 or PC1 | the other of the two | M |
| (only two analog pins exist: PC0, PC1) | | | M |
| Part cooling fan | PE1 | | M |
| Hotend fan (auto, on with hotend temp) | PB8 | | M |
| (mainboard has no separate controllable fan pin found) | | | |

## Misc

| Function | Pin | Src |
|---|---|---|
| USART to CH340 (TX/RX) | PA9/PA10 | G (250000 baud confirmed) |
| USART to ESP32 header | | |
| Buzzer | ? (PWM, not caught) | M300 |
| Case light | PB15 | M |
| TFT SPI (SCK/MOSI/CS/DC/RST/BL) | | |
| Encoder A/B/button | | |
| SD card SPI or SDIO | | |

## How to fill this in

1. Marlin: `M122` done (see probe log). `M43` is not compiled in, so pin numbers have to come from the hardware or from the firmware dump.
2. If `M43` is compiled out, disassemble the stock dump around the GPIO init calls, or just meter it: every driver has STEP/DIR/EN pads next to it; beep from each to the MCU.
3. For `Level` and `Zero`, follow the ribbon pins on the driver board to the MCU. Both should be plain GPIO, probably with a series resistor.

## Probe Level/Zero hunt (pending)

Load-cell probe via the printhead MCU: `Level` (trigger, input to mainboard MCU) and `Zero` (tare, output). Narrowed from the Marlin GPIO register capture to unmapped pins:

**FOUND (2026-08-26, no SWD - via Klipper output_pin/gcode_button sweep):** Level = **PA8** (^PA8, LATCHES on contact), Zero/tare = **PB5** (pulse to reset+re-arm). Probe repeatability 0.005mm. 16-point mesh working, range ~0.13mm.

Original candidate lists:
- Level (inputs): PA8, PA12, PB2, PB13, PB14, PC3, PD12, PE3, PE5
- Zero (outputs): PA4, PB5, PC2, PC4, PC6, PD3, PD7, PD13, PE2, PE6

Plan: over SWD, pulse each Zero candidate (tare) and watch Level candidates for the head MCU's "ready pulse" (~2 s post-tare, no press needed - seen under Marlin after M401). Match = both pins. Then `[probe] pin:<Level>` + `[output_pin]` tare on `<Zero>` + re-enable `[bed_mesh]`.
