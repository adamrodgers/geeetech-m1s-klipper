#!/usr/bin/env python3
"""Send a list of G-code commands to a Marlin printer over serial and log the replies.

usage: marlin_query.py PORT [BAUD] [CMD ...]
With no commands, runs the standard probe set. Output goes to stdout; redirect to logs/.
"""
import sys, time, serial

DEFAULT = ["M115", "M503", "M122", "M119", "M569", "M593", "M900", "M301", "M304",
           "M105", "M43", "M20"]

def run(port, baud, cmds, quiet=1.5):
    with serial.Serial(port, baud, timeout=0.2) as s:
        time.sleep(2.0)               # CH340 DTR resets many boards; wait for boot
        t0 = time.time()
        boot = b""
        while time.time() - t0 < 3:
            boot += s.read(4096)
        print(f"# port={port} baud={baud}")
        print("# --- boot banner ---")
        print(boot.decode(errors="replace"))
        for c in cmds:
            s.reset_input_buffer()
            s.write((c + "\n").encode())
            print(f"\n> {c}")
            buf, last = b"", time.time()
            while time.time() - last < quiet:
                chunk = s.read(4096)
                if chunk:
                    buf += chunk; last = time.time()
                    if buf.rstrip().endswith(b"ok"):
                        break
            print(buf.decode(errors="replace"))

if __name__ == "__main__":
    port = sys.argv[1]
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else 115200
    cmds = sys.argv[3:] or DEFAULT
    run(port, baud, cmds)
