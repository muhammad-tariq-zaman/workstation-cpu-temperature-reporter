"""Report CPU temperatures from a sensors-style CSV.

Usage: python3 main.py temps.csv [--max-temp 80]
CSV columns: workstation,core,temperature_c. Each reading is
reported hottest first, with an over-threshold flag:
- OVER: temperature above --max-temp (default 80 C).
- OK: temperature at or below --max-temp.
The summary names the hottest core overall. Rows with a
non-numeric temperature_c are reported as skipped, not
silently dropped.
"""
import argparse, csv, sys

def report(rows, max_temp=80):
    out = []
    skipped = 0
    for row in rows:
        try:
            workstation = row["workstation"].strip()
            core = row["core"].strip()
            temp = int(row["temperature_c"])
            if not workstation or not core:
                raise ValueError("missing value")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        verdict = "OVER" if temp > max_temp else "OK"
        detail = (f"{temp} C - over {max_temp} C limit" if verdict == "OVER"
                  else f"{temp} C - within {max_temp} C limit")
        out.append((workstation, core, temp, verdict, detail))
    out.sort(key=lambda r: (-r[2], r[0], r[1]))
    return out, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--max-temp", type=int, default=80)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, skipped = report(list(csv.DictReader(f)), args.max_temp)
    for workstation, core, _, verdict, detail in results:
        print(f"{workstation} core {core}: {verdict} - {detail}")
    if results:
        hottest = results[0]
        print(f"Hottest core: {hottest[0]} core {hottest[1]} at {hottest[2]} C.")
    over = sum(1 for *_, verdict, _ in results if verdict == "OVER")
    print(f"{over} over limit, {len(results) - over} ok out of "
          f"{len(results)} reading(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
