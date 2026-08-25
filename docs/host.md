# Klipper host (Pi 4)

| Item | Value |
|---|---|
| Hardware | Raspberry Pi 4B 1GB |
| OS | Raspberry Pi OS Lite 64-bit (Bookworm, 2025-05-13 image) |
| Hostname / IP | `m1s.local` / 192.168.1.154 (DHCP) |
| Login | user `adam`, SSH key auth (password `m1sprinter` as fallback) |
| Boot media | 61 GB USB thumb drive (to be migrated to the printer's old 4 GB TF card) |
| Web UI | Mainsail at http://m1s.local (nginx on 80, Moonraker API on 7125) |
| Services | `klipper`, `moonraker`, `nginx` (systemd, enabled) |
| Config dir | `~/printer_data/config/` - `printer.cfg` and `macros.cfg` deployed from this repo's `config/` |
| Also installed | OpenOCD (for the SWD flash dump via GPIO), stm32flash, dfu-util, arm-none-eabi toolchain (for building Klipper MCU firmware) |

## Setup notes / gotchas hit

- Klipper's `install-debian.sh` fails on Bookworm (`python-dev` no longer exists). Manual equivalent: `virtualenv ~/klippy-env`, `pip install -r klipper/scripts/klippy-requirements.txt`, hand-written `klipper.service`.
- Moonraker's own installer works as-is.
- Debian 12 creates home dirs `0700`; nginx needs `chmod o+x /home/adam` to serve `~/mainsail`.
- After changing nginx sites, `systemctl enable --now nginx` does NOT reload an already-running nginx - `systemctl reload nginx`.
- Headless first boot via `custom.toml` on the boot partition worked (hostname, user, SSH key, WiFi).

## SD card migration plan

The printer's factory 4 GB TF card (backed up: `sd-backup/` on the Pi and on the Mac) gets the same OS + config written to it from the running Pi. The Pi boots SD before USB, so the swap is just: write card, reboot, confirm, pull the thumb drive. ~3 GB used of 3.7 GB - tight but workable; gcodes stay small on a 100 mm printer.

## SWD wiring for the flash dump (pending)

Pi GPIO (OpenOCD `raspberrypi-native`) to mainboard `J6`:
GPIO25 -> TMS (SWDIO), GPIO11 -> TCK (SWCLK), GND -> GND (J3). Printer on its own PSU; no 3.3 V wire.
