import os
import time

SAND_START = (500, 0)


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    filled = parse_rocks(lines)
    print(simulate_sand(filled))
    print(simulate_sand(filled, True))


def simulate_sand(start_filled, with_floor=False):
    filled = set(start_filled)
    max_y = max([coord[1] for coord in filled])
    x, y = SAND_START

    while True:
        if (not with_floor and y > max_y) or (x, y) in filled:
            break
        elif with_floor and y == max_y + 1:
            filled.add((x, y))
            x, y = SAND_START
        elif not (x, y + 1) in filled:
            y += 1
        elif not (x - 1, y + 1) in filled:
            y += 1
            x -= 1
        elif not (x + 1, y + 1) in filled:
            y += 1
            x += 1
        else:
            filled.add((x, y))
            x, y = SAND_START

    return len(filled) - len(start_filled)


def parse_rocks(lines):
    filled = set()

    for line in lines:
        coords = tuple(map(lambda c: tuple(map(int, c.split(","))),
                           line.split(" -> ")))

        for i in range(1, len(coords)):
            cx, cy = coords[i]
            px, py = coords[i - 1]

            if (cx, cy) == (494, 9):
                print()

            if cy != py:
                for y in range(min(cy, py), max(cy, py) + 1):
                    filled.add((cx, y))

            if cx != px:
                for x in range(min(cx, px), max(cx, px) + 1):
                    filled.add((x, cy))

    return filled


if __name__ == '__main__':
    main()
