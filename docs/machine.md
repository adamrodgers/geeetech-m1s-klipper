# Machine: Geeetech M1S

The M1S is the M1 with a WiFi/Bluetooth module added. Mechanically and electrically the two are otherwise the same as far as any published source shows. Hardware data below is from Geeetech's wiki, product page, and the quick start guide, plus the M1 teardown photos.

## Specs

| Item | Value |
|---|---|
| Kinematics | Cartesian bed slinger (bed moves in Y) |
| Build volume | 100 x 110 x 100 mm |
| Nozzle | 0.4 mm, 1.75 mm filament only |
| Hotend | 50 W ceramic heater, "quick-release" assembly |
| Extruder | Direct drive, dual metal gears, 5:1 reduction, NEMA14 36x19.5 mm pancake motor |
| X/Y/Z motors | NEMA17, 42x42x35 mm (HEMOTORS HEM-17D2006-15/-16 seen in photos) |
| Bed | Heated, magnetic PEI flex plate |
| Leveling | 16-point automatic, load cell in the hotend (nozzle touches bed) |
| Nozzle wipe | Automatic, silicone wiper at the side of the bed, used before probing |
| Filament sensor | Yes, runout detection with "tension release" |
| Part cooling | 50x50x15 blower |
| Lighting | Built-in LED |
| Screen | 2.4" color TFT with rotary encoder |
| Speed claim | up to 250 mm/s |
| Firmware features advertised | input shaping, pressure advance, power-loss resume |
| Power | External 24 V adapter, 96 W or more, barrel jack |
| I/O | micro SD ("TF"), USB-B, WiFi + Bluetooth (M1S only) |
| Slicers | Cura, OrcaSlicer profiles from Geeetech |

## Stock software

- Firmware is unnamed in Geeetech's docs but the menus ("Prepare", "Print from Media", "Probing Failed", "GEEETECH M1S Ready") are Marlin 2.x strings. Input shaping and pressure advance are Marlin 2.1 features. Treat it as Marlin 2.1.x with a vendor config until the serial probe confirms.
- Mobile app: "Geeetech" (Android package `com.jietai.print`). Pairing is done over Bluetooth from the phone, after which the printer joins WiFi and talks to Geeetech's cloud. There is no documented LAN API.
- Firmware updates: Geeetech says "check the website for the latest firmware" but publishes nothing for the M1/M1S. Their other 32-bit boards update from a `.bin` on SD, and the mainboard has an `SD-Board` connector, so an SD bootloader is likely. Unconfirmed.

## Mechanical notes from photos

- Y axis: belt driven from a NEMA17 in the base, linear rail in the base.
- Z axis: NEMA17 in the base with a leadscrew. Z endstop is a small PCB microswitch in the base.
- X axis and extruder: driven from the mainboard through a 16-way ribbon to the printhead board.
- The base is a blue plastic shell; mainboard and both base motors live inside it.

## Sources

See [references.md](references.md).
