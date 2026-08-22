# Stock firmware and flashing

## What is on the board

Inferred, not yet confirmed:

- Confirmed: Marlin, vendor build `M1S_V1.96_MCU103` (2025-11-19), 250000 baud. Marlin 2.1.x by feature set.
- Possibly behind a Geeetech SD-card bootloader. Their GTM32 line (STM32F103 based) updates from a `.bin` on SD, and this board has an SD daughterboard. If a bootloader exists, the application starts at an offset (commonly 0x8000 = 32 KiB on Geeetech boards; BTT uses 0x7000 or 0x2000). Klipper must be built with the same offset or the bootloader must be bypassed.
- The serial console is Marlin G-code over the CH340 at 250000 baud. EEPROM is enabled; whether it is flash-emulated or the SOIC-8 on the display board is not known.

## Ways to get firmware on and off the chip

### 1. SWD (preferred for the first dump)

On the M1S board the header is `J6` (`TDO TCK TDI TMS`): SWDIO = `TMS`, SWCLK = `TCK`, GND from `J3`. (The M1 board has a separate `MCU-J-LINK` header.) Any ST-Link V2 clone, a Pi Pico running picoprobe, or a Raspberry Pi's GPIO with OpenOCD works.

Dump everything before writing anything:

```sh
# ST-Link + OpenOCD. APM32 reports as STM32F1 to the debugger.
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg \
  -c "init; reset halt; flash read_bank 0 stock-m1s-flash.bin 0 0x80000; exit"
```

Check `logs/` for the dump. Confirm size is 512 KiB and that it is not all `0xFF` or all zeros. If readout protection (RDP) is set the read will fail; note that and stop. Removing RDP wipes the chip, which is acceptable only once we have accepted losing the stock firmware.

Inspect the dump to find the bootloader:

```sh
# Vector table at 0x0 is the bootloader or the app. A second vector table
# (a plausible SP value 0x2000xxxx followed by a 0x0800xxxx reset vector) at
# 0x2000/0x7000/0x8000 means a bootloader is present at that offset.
xxd -s 0 -l 16 stock-m1s-flash.bin
xxd -s 0x8000 -l 16 stock-m1s-flash.bin
strings -n 8 stock-m1s-flash.bin | grep -iE 'marlin|geeetech|m1s|boot|firmware\.bin' | head
```

### 2. ROM UART bootloader over USB

The STM32F103 (and APM32) ROM bootloader lives in system memory and talks on USART1 (PA9/PA10). If the CH340 is wired to USART1, which is the normal layout, then:

1. Power off. Fit the `MCU-BOOT` jumper (BOOT0 high).
2. Power on (24 V or `USB_PWR` jumper with only USB connected).
3. `stm32flash -r stock.bin /dev/cu.wchusbserial*` to read, `stm32flash -w klipper.bin -v /dev/cu.wchusbserial*` to write.
4. Remove jumper, power cycle.

Note: the jumper labelled `MCU-BOOT` is the one near the bottom right corner of the driver board, next to `J7`. The other small jumper near the SWD header is `USB_PWR`, do not confuse them.

If the CH340 is on a different USART this will not work; fall back to SWD.

### 3. SD card bootloader

If the dump shows a Geeetech bootloader, it probably looks for a fixed filename on the SD root. Candidates from their other products: `firmware.bin`, `GTM32.bin`, `M1.bin`. The strings in the bootloader region of the dump will say. If present, Klipper goes on as a renamed `klipper.bin` at the right offset with no extra hardware.

## Klipper build settings (provisional)

```
make menuconfig
  Micro-controller Architecture:  STMicroelectronics STM32
  Processor model:                STM32F103
  Bootloader offset:              (match the dump; 'No bootloader' if flashing via SWD/ROM)
  Clock Reference:                8 MHz crystal   (Y1 marked D8.000C, confirmed)
  Communication interface:        Serial (on USART1 PA10/PA9)
  Baud rate:                      250000   (matches stock, and the CH340 handles it)
```

Klipper's STM32F103 build is known to run on APM32F103 clones. The E103 variant has more flash and RAM than the F103C8 Klipper assumes, which is harmless. If the crystal turns out to be something other than 8 MHz, set it here or the serial baud will be wrong.

Choose the serial interface, not USB: the MCU has no native USB path to the host on this board; everything goes through the CH340.

## Rollback

Keep `stock-m1s-flash.bin` from step 1 in `logs/` (and off-machine). Restoring is `flash write_image erase stock-m1s-flash.bin 0x08000000` through OpenOCD. Without that dump there is no way back, since Geeetech publishes no firmware images.
