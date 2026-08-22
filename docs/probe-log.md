# Stock firmware probe

Commands to run against the stock Marlin over USB, and a place to record what came back. Save raw output to `logs/` with a date.

## Connect

```sh
ls /dev/cu.*                       # expect cu.wchusbserial* (CH340)
system_profiler SPUSBDataType | grep -A8 -i 'ch340\|usb serial\|1a86'
```

Open a terminal at 115200 first; if output is garbage, 250000.

```sh
# picocom (brew install picocom). Ctrl-A Ctrl-X to exit.
picocom -b 115200 --imap lfcrlf /dev/cu.wchusbserial*
```

Or log everything with a script (see `scripts/` once it exists).

## Commands

| Command | What it tells us |
|---|---|
| `M115` | Firmware name/version, `MACHINE_TYPE`, board, capabilities |
| `M503` | Full settings dump: steps/mm, limits, accel, jerk, PID, probe offsets, bed mesh, advance, shaping |
| `M122` | TMC driver status. If it errors, TMC UART is not compiled in / not wired |
| `M119` | Endstop and probe state. Press the nozzle while polling to see `Level` |
| `M569` | Stepper driver modes |
| `M593` | Input shaper settings |
| `M900` | Pressure advance (linear advance) |
| `M301` / `M304` | Hotend / bed PID |
| `M43` | Pin state dump, if `PINS_DEBUGGING` is enabled |
| `M43 E1` | Watch pins for changes |
| `M105` | Temps, sanity check |
| `M106 S255` / `M107` | Fan test |
| `M42 P<pin> S<val>` | Drive a pin directly, useful for identifying LED/buzzer/Zero |
| `M81`/`M80` | Power control, probably unsupported |

Also try `M0` (pause), `G28`, and `G29` with the USB attached, and watch the output for any messages about the probe, to see what Marlin says to the head MCU.

## Results

_Empty. Fill in after the first session._

### Session 1 - date

- Port:
- Baud:
- `M115`:
- `M503` saved to `logs/`
- `M122`:
- Notes:
