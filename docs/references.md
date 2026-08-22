# References

## Geeetech

- M1S wiki: https://wiki.geeetech.com/index.php/Geeetech_M1S_3D_printer (maintenance procedures, wiring diagram images, power spec)
- M1 wiki: https://wiki.geeetech.com/index.php/Geeetech_M1_3D_printer
- M1S product page: https://www.geeetech.com/products/m1s
- M1 launch post (motor sizes, heater wattage, firmware features): https://blog.geeetech.com/news/new-arrival/new-launch-mini-3d-printer-geeetech-m1/
- M1S quick start guide PDF: https://gzhls.at/blob/ldb/1/6/7/9/d552612daa712e131a37a6bca0dd4ee21e97.pdf
- M1S manual on ManualsLib: https://www.manualslib.com/manual/4184498/Geeetech-M1s.html
- Geeetech app, Android: https://play.google.com/store/apps/details?id=com.jietai.print
- Geeetech app, iOS: https://apps.apple.com/us/app/geeetech/id6751800421
- Geeetech's older ESP-based "3D WiFi module" (same cloud model as the M1S module): https://wiki.geeetech.com/index.php/3D_wifi_module
- Geeetech GitHub org (Mizar, Spark E3, Kirin sources; nothing for M1/M1S): https://github.com/Geeetech3D
- GTM32 firmware update procedure (SD `.bin`, for comparison): https://www.geeetech.com/wiki/index.php/Update_firmware

## Community

- 0dysseusRex M1 upgrade (full electronics swap; source of the teardown photos, CC0): https://github.com/0dysseusRex/Geeetech-M1-Upgrade
- MakerBuildIt M1S review: https://makerbuildit.com/blogs/3d-printing/geeetech-m1s-mini-review-a-beginner-3d-printer-that-actually-feels-beginner-friendly
- 3D Printing Professor M1 review: https://www.3dpprofessor.com/2025/09/11/geeetech-m1-review-and-beginners-guide/
- SimplyPrint M1 page: https://simplyprint.io/compatibility/geeetech-m1-mini

## Parts

- Geehy APM32E103VET6 datasheet: https://www.geehy.com/apm32?id=14 (STM32F103VE-compatible)
- Chipsea CS1237 24-bit ADC: search "CS1237 datasheet"; 2-wire SCLK/DOUT, PGA up to 128, used in many cheap load-cell front ends
- TMC2209 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf
- A4988 datasheet: https://www.allegromicro.com/en/products/motor-drivers/brush-dc-motor-drivers/a4988

## Klipper

- STM32F103 build and bootloader notes: https://www.klipper3d.org/Installation.html and https://www.klipper3d.org/Bootloaders.html
- Probe config reference: https://www.klipper3d.org/Config_Reference.html#probe
- Load cell support (not needed here, kept for reference): https://www.klipper3d.org/Load_Cell.html
