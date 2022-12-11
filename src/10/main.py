import math
import os

CRT_WIDTH = 40
CRT_HEIGHT = 6
SIGNAL_INTERVAL = 40
SIGNAL_OFFSET = 20
NOOP = "noop"
DARK_PX = "."
LIGHT_PX = "#"


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    crt = [[DARK_PX for _ in range(CRT_WIDTH)] for _ in range(CRT_HEIGHT)]

    signals = []
    cycle = 0
    x = 1
    for line in lines:
        update_crt(crt, cycle, x)
        cycle += 1
        append_if_interesting_cycle(signals, cycle, x)
        if line != NOOP:
            update_crt(crt, cycle, x)
            cycle += 1
            append_if_interesting_cycle(signals, cycle, x)
            x += int(line.split()[1])

    print(sum(signals))
    print(render_crt(crt))


def render_crt(crt):
    return "\n".join(map(lambda row: "".join(row), crt))


def update_crt(crt, cycle, x):
    row = math.floor(cycle / CRT_WIDTH)
    col = cycle % CRT_WIDTH

    if abs(x - col) <= 1:
        crt[row][col] = LIGHT_PX


def append_if_interesting_cycle(signals, cycle, signal):
    if is_interesting_cycle(cycle):
        signals.append(cycle * signal)


def is_interesting_cycle(n):
    return (n + SIGNAL_OFFSET) % SIGNAL_INTERVAL == 0


if __name__ == '__main__':
    main()
