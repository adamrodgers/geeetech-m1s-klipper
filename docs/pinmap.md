# MCU pin map

Target: APM32E103VET6 (STM32F103VE pinout, LQFP100). Fill in as pins are confirmed. Sources are marked so guesses don't get mistaken for measurements.

Source key: **M** = measured with a meter/scope, **D** = derived from Marlin output (`M122`, pins debug) or disassembly, **G** = guess from board layout.

## Steppers

| Function | STEP | DIR | EN | UART | Driver | Src |
|---|---|---|---|---|---|---|
| X | | | | | TMC2209? | |
| Y | | | | | TMC2209? | |
| Z | | | | - | 4988ET? | |
| E | | | | - | 4988ET? | |

## Endstops and probe

| Function | Pin | Pull / polarity | Src |
|---|---|---|---|
| X_MIN (via ribbon) | | | |
| Y_MIN | | | |
| Z_MIN (base microswitch) | | | |
| `Level` (probe trigger from head MCU) | | | |
| `Zero` (tare output to head MCU) | | | |
| Filament runout | | | |

## Heaters, thermistors, fans

| Function | Pin | Notes | Src |
|---|---|---|---|
| Hotend heater `HED` | | MOSFET on mainboard, via ribbon | |
| Bed heater | | | |
| TH0 (hotend) | | ADC | |
| TH1 | | ADC, purpose unknown | |
| TB (bed) | | ADC | |
| FAN1 | | | |
| FAN2 | | | |
| Mainboard fan | | | |

## Misc

| Function | Pin | Src |
|---|---|---|
| USART to CH340 (TX/RX) | PA9/PA10 (G) | |
| USART to ESP32 header | | |
| Buzzer | | |
| LED | | |
| TFT SPI (SCK/MOSI/CS/DC/RST/BL) | | |
| Encoder A/B/button | | |
| SD card SPI or SDIO | | |

## How to fill this in

1. Marlin: `M122` gives driver status and whether TMC UART is working. Some vendor builds keep `PINS_DEBUGGING`; try `M43` to dump pin states and `M43 E1` to watch for changes while toggling endstops and the probe.
2. If `M43` is compiled out, disassemble the stock dump around the GPIO init calls, or just meter it: every driver has STEP/DIR/EN pads next to it; beep from each to the MCU.
3. For `Level` and `Zero`, follow the ribbon pins on the driver board to the MCU. Both should be plain GPIO, probably with a series resistor.
