import os

BASE = 5
SYMBOLS = "=-012"
VALUES = (-2, -1, 0, 1, 2)


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    tot = 0

    for line in lines:
        dec = snafu_to_dec(line)
        tot += dec

    print(dec_to_snafu(tot))


def dec_to_snafu(dec):
    s = ""
    pos = 0
    offset = VALUES.index(0)

    while dec > 0:
        m = BASE ** pos
        mm = BASE ** (pos + 1)
        i = int((((dec % mm) / m) + offset) % len(VALUES))
        dec -= VALUES[i] * m
        s = SYMBOLS[i] + s
        pos += 1

    return s


def snafu_to_dec(s):
    dec = 0
    slr = list(reversed(s))

    for i, c in enumerate(slr):
        v = VALUES[SYMBOLS.index(c)]
        dec += v * (BASE ** i)

    return dec


if __name__ == '__main__':
    main()
