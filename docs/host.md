# Klipper host (Pi 4)

| Item | Value |
|---|---|
| Hardware | Raspberry Pi 4B 1GB |
| OS | Raspberry Pi OS Lite 64-bit (Bookworm, 2025-05-13 image) |
| Hostname / IP | `m1s.local` / 192.168.1.154 (DHCP) |
| Login | user `adam`, SSH key auth (password `m1sprinter` as fallback) |
| Boot media | 61 GB USB thumb drive (staying; a 4 GB card is too small - see below) |
| Web UI | Mainsail at http://m1s.local (nginx on 80, Moonraker API on 7125) |
| Services | `klipper`, `moonraker`, `nginx` (systemd, enabled) |
| Config dir | `~/printer_data/config/` - `printer.cfg` and `macros.cfg` deployed from this repo's `config/` |
| Also installed | OpenOCD (for the SWD flash dump via GPIO), stm32flash, dfu-util, arm-none-eabi toolchain (for building Klipper MCU firmware) |

## Config auto-backup

A systemd timer on the Pi (`config-backup.timer`, every 30 min + 5 min after boot) runs `~/config-backup.sh`: rsyncs `~/printer_data/config/` into the repo's `config/` (excluding `README.md` and the KAMP symlink), commits as "Auto-backup: printer config from Pi ...", and pushes over a repo-scoped deploy key. Deliberately NOT the klipper-backup project and not visible in Update Manager - there is nothing to update. Check it with `systemctl status config-backup.timer` or by the auto-backup commits on GitHub. Pull before editing config locally; the Pi rebases before pushing.

## Setup notes / gotchas hit

- Klipper's `install-debian.sh` fails on Bookworm (`python-dev` no longer exists). Manual equivalent: `virtualenv ~/klippy-env`, `pip install -r klipper/scripts/klippy-requirements.txt`, hand-written `klipper.service`.
- Moonraker's own installer works as-is.
- Debian 12 creates home dirs `0700`; nginx needs `chmod o+x /home/adam` to serve `~/mainsail`.
- After changing nginx sites, `systemctl enable --now nginx` does NOT reload an already-running nginx - `systemctl reload nginx`.
- Headless first boot via `custom.toml` on the boot partition worked (hostname, user, SSH key, WiFi).

## SD card migration (deferred)

The plan was to move the OS to the printer's factory 4 GB TF card. Aborted: with the ARM toolchain (~2.4 GB, needed to build `klipper.bin`) the system uses ~5.5 GB even after cleanup, vs 3.2 GB usable on the card. `rpi-clone` is installed on the Pi; when a bigger card (16 GB+) turns up, the move is `sudo ./rpi-clone/rpi-clone mmcblk0 -f -U`, then reboot (SD boots before USB). The factory card is backed up on the Mac (`~/3dPrinting/M1S-sd-backup/`, md5-verified) and on the Pi (`~/sd-backup/`), and was never overwritten.

## SWD wiring for the flash dump (pending)

Pi GPIO (OpenOCD `raspberrypi-native`) to mainboard `J6`:
GPIO25 -> TMS (SWDIO), GPIO11 -> TCK (SWCLK), GND -> GND (J3). Printer on its own PSU; no 3.3 V wire.
- Chrome on the Mac showed `ERR_ADDRESS_UNREACHABLE` for all LAN IPs (Mainsail included) while curl/ping worked fine. Cause: stale Chrome connection state after a Tailscale connect/disconnect. Fix: fully quit Chrome and relaunch - it starts working a few seconds after restart. Tailscale itself can stay connected.
- Mainsail theme: `config/.theme/` (custom.css + sidebar-logo.svg), M1S case blue on dark. Deployed to the Pi's config dir; edit CSS and hard-refresh to tweak.
