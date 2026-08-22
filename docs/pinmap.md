# MCU pin map

Target: APM32E103VET6 (STM32F103VE pinout, LQFP100). Fill in as pins are confirmed. Sources are marked so guesses don't get mistaken for measurements.

Source key: **M** = measured with a meter/scope, **D** = derived from Marlin output (`M122`, pins debug) or disassembly, **G** = guess from board layout.

## Steppers

| Function | STEP | DIR | EN | UART | Driver | Src |
|---|---|---|---|---|---|---|
| X | | | | addr 0, no response | TMC2209 | D |
| Y | | | | addr 3, works | TMC2209 | D |
| Z | | | | - | 4988ET | D |
| E | | | | - | 4988ET | D |

## Endstops and probe

| Function | Pin | Pull / polarity | Src |
|---|---|---|---|
| X endstop (`X_MIN` on ribbon, but Marlin homes X to **max**) | | | D |
| Y_MIN | | | |
| Z_MIN (base microswitch) | | | |
| `Level` (probe trigger from head MCU) | | Marlin `z_probe`, reads open at rest | D |
| `Zero` (tare output to head MCU) | | | |
| Filament runout | | reads TRIGGERED with filament loaded | D |

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
| USART to CH340 (TX/RX) | PA9/PA10 | G (250000 baud confirmed) |
| USART to ESP32 header | | |
| Buzzer | | |
| LED | | |
| TFT SPI (SCK/MOSI/CS/DC/RST/BL) | | |
| Encoder A/B/button | | |
| SD card SPI or SDIO | | |

## How to fill this in

1. Marlin: `M122` done (see probe log). `M43` is not compiled in, so pin numbers have to come from the hardware or from the firmware dump.
2. If `M43` is compiled out, disassemble the stock dump around the GPIO init calls, or just meter it: every driver has STEP/DIR/EN pads next to it; beep from each to the MCU.
3. For `Level` and `Zero`, follow the ribbon pins on the driver board to the MCU. Both should be plain GPIO, probably with a series resistor.
