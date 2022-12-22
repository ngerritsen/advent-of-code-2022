import os
import re

# Edge mapping example
#   X
# XXX
#   XX
# edges = [
#     [[(8, 0), (11, 0), 3], [(0, 4), (3, 4), 3], True],
#     [[(11, 0), (11, 3), 0], [(15, 8), (15, 11), 0], True],
#     [[(11, 4), (11, 7), 0], [(12, 8), (15, 8), 3], True],
#     [[(12, 11), (15, 11), 1], [(0, 4), (0, 7), 2], True],
#     [[(8, 11), (11, 11), 1], [(0, 7), (3, 7), 1], True],
#     [[(8, 8), (8, 11), 2], [(4, 7), (7, 7), 1], True],
#     [[(4, 4), (7, 4), 3], [(8, 0), (8, 3), 2], False],
# ]

# Edge mapping input
#  XX
#  X
# XX
# X
edges = [
    [[(50, 0), (99, 0), 3], [(0, 150), (0, 199), 2], False],
    [[(100, 0), (149, 0), 3], [(0, 199), (49, 199), 1], False],
    [[(149, 0), (149, 49), 0], [(99, 100), (99, 149), 0], True],
    [[(100, 49), (149, 49), 1], [(99, 50), (99, 99), 0], False],
    [[(50, 149), (99, 149), 1], [(49, 150), (49, 199), 0], False],
    [[(0, 100), (0, 149), 2], [(50, 0), (50, 49), 2], True],
    [[(0, 100), (49, 100), 3], [(50, 50), (50, 99), 2], False],
]

vecs = ((1, 0), (0, 1), (-1, 0), (0, -1))


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    path = parse_path(lines[-1])
    tiles, walls = parse_map(lines[:-2])
    dup_edges()

    print(solve_password(tiles, walls, path))
    print(solve_password(tiles, walls, path, True))


def solve_password(tiles, walls, path, cube=False):
    pos, vec = walk(tiles, walls, path, cube)
    return get_password(pos, vec)


def dup_edges():
    for i in range(len(edges)):
        a, b, inv = edges[i]
        edges.append([b, a, inv])


def walk(tiles, walls, path, cube):
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
                n_vec = vec

                if cube:
                    n_pos, n_vec = move_3d(pos, vec)
                else:
                    n_pos = move(pos, vec, board)

                if n_pos in walls:
                    break

                pos = n_pos
                vec = n_vec

    return pos, vec


def get_password(pos, vec):
    return (1000 * (pos[1] + 1)) + (4 * (pos[0] + 1)) + vecs.index(vec)


def get_start(tiles):
    x, _ = get_min_max(tiles, 0)
    return x, 0


def turn(vec, cmd):
    curr = vecs.index(vec)
    n_vec = (curr + (3 if cmd == "L" else 1)) % len(vecs)
    return vecs[n_vec]


def move(pos, vec, board):
    x, y = pos
    dx, dy = vec

    for a, b, inv in edges:
        if is_leaving_edge(pos, vec, a):
            if dy == 0:
                x = wrap(board, y, x, dx)
            else:
                y = wrap(board, x, y, dy, True)

            return x, y

    return add_coords(pos, vec)


def move_3d(pos, vec):
    for a, b, inv in edges:
        if is_leaving_edge(pos, vec, a):
            vec = inv_vec(b[2])
            return move_to_edge(a, b, pos, inv), vec

    return add_coords(pos, vec), vec


def move_to_edge(a, b, pos, inv):
    x, y = pos
    asx, asy = a[0]
    aex, aey = a[1]
    bsx, bsy = b[0]
    bex, bey = b[1]
    m = max(aex - asx, aey - asy)

    if asx == aex:
        o = y - asy
    else:
        o = x - asx

    if inv:
        o = m - o

    if bsx == bex:
        x = bsx
        y = bsy + o
    else:
        y = bsy
        x = bsx + o

    return x, y


def is_leaving_edge(pos, vec, edge):
    if vecs.index(vec) != edge[2]:
        return False

    x, y = pos
    sx, sy = edge[0]
    ex, ey = edge[1]

    return sx <= x <= ex and sy <= y <= ey


def wrap(board, n, s, d, col=False):
    min_x, max_x = get_min_max(board, n, col)
    range_x = max_x - min_x + 1
    return min_x + ((s + d) - min_x) % range_x


def add_coords(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


def inv_vec(v):
    v = (v + 2) % len(vecs)
    return vecs[v]


def get_min_max(tiles, n, col=False):
    line = filter(lambda t: t[0 if col else 1] == n, tiles)
    vals = [t[1 if col else 0] for t in line]

    return min(vals), max(vals)


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
