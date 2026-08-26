# MCU pin map

Target: APM32E103VET6 (STM32F103VE pinout, LQFP100). Fill in as pins are confirmed. Sources are marked so guesses don't get mistaken for measurements.

Source key: **M** = measured with a meter/scope, **D** = derived from Marlin output (`M122`, pins debug) or disassembly, **G** = guess from board layout.

## Steppers

| Function | STEP | DIR | EN | UART | Driver | Src |
|---|---|---|---|---|---|---|
| X | ? | PB12 | PB0 | addr 0, no response | TMC2209 | M |
| Y | ? | PA0 | PC7 | addr 3, works | TMC2209 | M |
| Z | ? | PC15 | PC13 | - | 4988ET | M |
| E | ? | PE4 | PB7 | - | 4988ET | M |

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
