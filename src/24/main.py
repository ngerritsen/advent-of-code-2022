import math
import os
from collections import deque

R, D, L, U = 0, 1, 2, 3
VECS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIR_SYMBOLS = ">v<^"


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    walls, blizzards, occupied, size, start, end = parse_valley(lines)

    print(find_path(start, end, blizzards, walls, occupied, size))
    print(find_path(start, end, blizzards, walls, occupied, size, True))


def find_path(start, end, blizzards, walls, occupied, size, get_snacks=False):
    queue = deque([(start, 0)])
    width, height = size
    period = math.lcm(width - 2, height - 2)
    blizz_states = [(blizzards, occupied)]
    visited = set()
    has_snacks = False
    getting_snacks = False
    try_vecs = set(VECS).union([(0, 0)])

    while len(queue) > 0:
        pos, minute = queue.popleft()

        if pos == end:
            if not get_snacks or has_snacks:
                return minute
            elif not getting_snacks:
                queue.clear()
                getting_snacks = True
        elif pos == start and getting_snacks and not has_snacks:
            queue.clear()
            has_snacks = True

        minute += 1
        curr_period = minute % period
        prev_period = (minute - 1) % period

        if curr_period > len(blizz_states) - 1:
            prev_blizz_state = blizz_states[prev_period][0]
            result = progress_blizzard(prev_blizz_state, walls, size)
            blizz_states.append(result)

        occupied = blizz_states[curr_period][1]

        for vec in try_vecs:
            next_pos = add_coords(pos, vec)

            if next_pos not in occupied and (next_pos, minute) not in visited:
                visited.add((next_pos, minute))
                queue.append((next_pos, minute))


def progress_blizzard(blizzards, walls, size):
    next_blizzards, occupied = set(), set(walls)

    for blizzard in blizzards:
        pos, v = blizzard
        next_pos = add_coords(pos, get_vec(v))

        if next_pos in walls:
            vec = mul_vec(get_vec(inv_vec(v)), size[v % 2] - 3)
            next_pos = add_coords(pos, vec)

        next_blizzards.add((next_pos, v))
        occupied.add(next_pos)

    return next_blizzards, occupied


def parse_valley(lines):
    walls, blizzards, occupied = set(), set(), set()
    width, height = len(lines[0]), len(lines)
    start, end = (1, 0), (width - 2, height - 1)
    walls.add(add_coords(start, VECS[U]))
    walls.add(add_coords(end, VECS[D]))

    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if val == "#":
                walls.add((x, y))
            elif val in DIR_SYMBOLS:
                blizzards.add(((x, y), DIR_SYMBOLS.index(val)))
                occupied.add((x, y))

    return walls, blizzards, occupied, (width, height), start, end


def get_vec(d):
    return VECS[d]


def mul_vec(vec, n):
    return vec[0] * n, vec[1] * n


def inv_vec(d):
    return (d + 2) % len(VECS)


def add_coords(a, b):
    return a[0] + b[0], a[1] + b[1]


if __name__ == '__main__':
    main()
