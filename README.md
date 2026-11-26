# workstation-cpu-temperature-reporter

Report CPU temperatures from a sensors-style CSV: the input CSV lists workstation, core and temperature_c — each reading is reported hottest first, with OVER when the temperature is above --max-temp (default 80 C) and OK at or below it, and the summary names the hottest core overall. Rows with a non-numeric temperature_c are reported as skipped, not silently dropped.

Sample input is included (sample.csv with eight readings, one invalid row).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
WS-01 core 0: OVER - 94 C - over 80 C limit
WS-03 core 0: OVER - 83 C - over 80 C limit
WS-01 core 1: OK - 72 C - within 80 C limit
WS-01 core 2: OK - 68 C - within 80 C limit
WS-02 core 1: OK - 61 C - within 80 C limit
WS-02 core 0: OK - 55 C - within 80 C limit
WS-03 core 1: OK - 49 C - within 80 C limit
Hottest core: WS-01 core 0 at 94 C.
2 over limit, 5 ok out of 7 reading(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
