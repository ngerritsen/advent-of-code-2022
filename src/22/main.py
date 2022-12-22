import os
import re


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    path = parse_path(lines[-1])
    tiles, walls = parse_map(lines[:-2])
    pos, vec = walk(tiles, walls, path)

    print(get_password(pos, vec))


def walk(tiles, walls, path):
    pos = get_start(tiles)
    board = tiles.union(walls)
    vec = (1, 0)

    for _ in range(12):
        pos = move(pos, vec, board)

    for cmd in path:
        if cmd in ("L", "R"):
            vec = turn(vec, cmd)
        else:
            for _ in range(int(cmd)):
                nxt = move(pos, vec, board)

                if nxt in walls:
                    break

                pos = nxt

    return pos, vec


def get_password(pos, vec):
    return (1000 * (pos[1] + 1)) + (4 * (pos[0] + 1)) + score_vec(vec)


def score_vec(vec):
    cmp = (1, 0)
    for s in range(4):
        if cmp == vec:
            return s

        cmp = rotate(cmp)


def get_start(tiles):
    x, _ = get_min_max(tiles, 0)
    return x, 0


def turn(vec, cmd):
    times = 3 if cmd == "L" else 1

    for _ in range(times):
        vec = rotate(vec)

    return vec


def move(pos, vec, board):
    x, y = pos
    dx, dy = vec

    if dy == 0:
        x = wrap(board, y, x, dx)
    else:
        y = wrap(board, x, y, dy, True)

    return x, y


def wrap(board, n, s, d, col=False):
    min_x, max_x = get_min_max(board, n, col)
    range_x = max_x - min_x + 1
    return min_x + ((s + d) - min_x) % range_x


def get_min_max(tiles, n, col=False):
    line = filter(lambda t: t[0 if col else 1] == n, tiles)
    vals = [t[1 if col else 0] for t in line]

    return min(vals), max(vals)


def add_coord(a, b):
    return a[0] + b[0], a[1] + b[1]


def rotate(vec):
    x, y = vec
    x += -1 if x > 0 or y > 0 else 1
    y += -1 if y > 0 or vec[0] < 0 else 1
    return x, y


def parse_path(line):
    return re.findall(r"(\d+|[RL])", line)


def parse_map(lines):
    tiles, walls = set(), set()

    for y, line in enumerate(lines):
        for x, v in enumerate(line):
            if v == ".":
                tiles.add((x, y))
            if v == "#":
                walls.add((x, y))

    return tiles, walls


if __name__ == '__main__':
    main()
