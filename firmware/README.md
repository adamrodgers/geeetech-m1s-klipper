# Stock firmware backup

`m1s-stock-mcu-flash.bin` - full 512 KiB dump of the APM32E103VET6 internal flash, read over SWD (Pi GPIO + OpenOCD) on 2026-08-25. Two consecutive reads matched (md5 `8da53b514545727bafc24232706af5c5`).

- Contents: Marlin 2.1.2.1, vendor build `M1S_V1.96_MCU103` (2025-11-19). ~444 KB used, no bootloader (vector table at 0x08000000, app starts at 0x0).
- This does NOT include the external W25Q64 SPI flash (Marlin EEPROM/PLR store); those settings are captured separately by the `M503` dump in `logs/`.

## Restore to stock

Printer on, SWD wired to the Pi (H1: D->GPIO24, C->GPIO25, R->GPIO23, G->GND; V left off), then:

```
sudo openocd -f ~/swd.cfg -c "init" -c "reset halt" \
  -c "flash write_image erase firmware/m1s-stock-mcu-flash.bin 0x08000000" \
  -c "reset run" -c "exit"
```

Also mirrored on the Mac at ~/3dPrinting/M1S-sd-backup/ and on the Pi at ~/flash-backup/.
