import os
import re

R, D, L, U = 0, 1, 2, 3
VECS = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAPPINGS = {
    'example.txt': (
        4,
        [
            [[(2, 0), (3, 0), U], [(1, 1), (0, 1), U]],  # A
            [[(3, 0), (3, 1), R], [(4, 3), (4, 2), R]],  # B
            [[(3, 1), (3, 2), R], [(4, 2), (3, 2), U]],  # C
            [[(3, 3), (4, 3), D], [(0, 2), (0, 1), L]],  # D
            [[(2, 3), (3, 3), D], [(1, 2), (0, 2), D]],  # E
            [[(2, 2), (2, 3), L], [(2, 2), (1, 2), D]],  # F
            [[(1, 1), (2, 1), U], [(2, 0), (2, 1), L]],  # G
        ]
    ),
    'input.txt': (
        50,
        [
            [[(1, 0), (2, 0), U], [(0, 3), (0, 4), L]],  # A
            [[(2, 0), (3, 0), U], [(0, 4), (1, 4), D]],  # B
            [[(3, 0), (3, 1), R], [(2, 3), (2, 2), R]],  # C
            [[(2, 1), (3, 1), D], [(2, 1), (2, 2), R]],  # D
            [[(1, 3), (2, 3), D], [(1, 3), (1, 4), R]],  # E
            [[(0, 2), (0, 3), L], [(1, 1), (1, 0), L]],  # F
            [[(0, 2), (1, 2), U], [(1, 1), (1, 2), L]],  # G
        ]
    )
}


def main():
    file_name = "input.txt"

    with open(os.path.dirname(__file__) + "/" + file_name) as f:
        lines = f.read().split("\n")

    path = parse_path(lines[-1])
    tiles, walls = parse_map(lines[:-2])
    edges = get_edges(file_name)

    print(solve_password(tiles, walls, path, list()))
    print(solve_password(tiles, walls, path, edges))


def solve_password(tiles, walls, path, edges):
    pos, vec = walk(tiles, walls, path, edges)
    return get_password(pos, vec)


def walk(tiles, walls, path, edges):
    pos = get_start(tiles)
    board = tiles.union(walls)
    vec = (1, 0)

    for cmd in path:
        if cmd in ("L", "R"):
            vec = turn(vec, cmd)
        else:
            for _ in range(int(cmd)):
                n_pos, n_vec = move(pos, vec, board, edges)

                if n_pos in walls:
                    break

                pos = n_pos
                vec = n_vec

    return pos, vec


def get_password(pos, vec):
    return (1000 * (pos[1] + 1)) + (4 * (pos[0] + 1)) + vec_idx(vec)


def move(pos, vec, board, edges):
    n_pos = add_coords(pos, vec)

    if n_pos in board:
        return n_pos, vec

    for edge in edges:
        for i in range(2):
            a, b = edge[i], edge[inv_bin(i)]

            if is_leaving_edge(pos, vec, a):
                n_vec = inv_vec(b[2])
                return move_to_edge(a, b, pos), n_vec

    return wrap_around(pos, vec, board), vec


def wrap_around(pos, vec, board):
    x, y = pos
    dx, dy = vec

    if dy == 0:
        x = wrap(board, y, x, dx)
    else:
        y = wrap(board, x, y, dy, True)

    return x, y


def move_to_edge(a, b, pos):
    pos = list(pos)
    from_axis = int(a[0][0] == a[1][0])
    to_axis = int(b[0][0] == b[1][0])
    val = pos[from_axis]
    from_start = a[0][from_axis]
    to_start, to_end = b[0][to_axis], b[1][to_axis]

    n_pos = [0, 0]
    n_pos[inv_bin(to_axis)] = b[0][inv_bin(to_axis)]
    n_pos[to_axis] = map_index(from_start, to_start, to_end, val)

    return tuple(n_pos)


def get_start(tiles):
    x, _ = get_min_max(tiles, 0)
    return x, 0


def turn(vec, cmd):
    n_vec = (vec_idx(vec) + (3 if cmd == "L" else 1)) % len(VECS)
    return VECS[n_vec]


def map_index(a_from, b_from, b_to, val):
    offset = abs(a_from - val)

    if b_from > b_to:
        return b_from - offset
    else:
        return b_from + offset


def is_leaving_edge(pos, vec, edge):
    if vec_idx(vec) != edge[2]:
        return False

    sx, ex = order_coords(edge[0][0], edge[1][0])
    sy, ey = order_coords(edge[0][1], edge[1][1])

    return sx <= pos[0] <= ex and sy <= pos[1] <= ey


def wrap(board, n, s, d, col=False):
    min_x, max_x = get_min_max(board, n, col)
    range_x = max_x - min_x + 1
    return min_x + ((s + d) - min_x) % range_x


def get_min_max(tiles, n, col=False):
    line = filter(lambda t: t[0 if col else 1] == n, tiles)
    vals = [t[1 if col else 0] for t in line]

    return min(vals), max(vals)


def cap_tail(edge):
    a, b, v = edge

    if v in (R, L):
        if a[1] > b[1]:
            edge[0] = add_coords(a, VECS[U])
        else:
            edge[1] = add_coords(b, VECS[U])
    else:
        if a[0] > b[0]:
            edge[0] = add_coords(a, VECS[L])
        else:
            edge[1] = add_coords(b, VECS[L])

    return edge


def get_edges(key):
    size, edges = MAPPINGS[key]

    for i, mapping in enumerate(edges):
        for j in range(2):
            for k in range(2):
                mapping[j][k] = mul_coord(mapping[j][k], size)

                if mapping[j][2] == R:
                    mapping[j][k] = add_coords(mapping[j][k], VECS[L])
                elif mapping[j][2] == D:
                    mapping[j][k] = add_coords(mapping[j][k], VECS[U])

            mapping[j] = cap_tail(mapping[j])

    return edges


def order_coords(a, b):
    return (b, a) if a > b else (a, b)


def inv_vec(v):
    v = (v + 2) % len(VECS)
    return VECS[v]


def inv_bin(n):
    return abs(n - 1)


def parse_path(line):
    return re.findall(r"(\d+|[RL])", line)


def vec_idx(vec):
    return VECS.index(vec)


def add_coords(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


def mul_coord(coord, n):
    x, y = coord
    return x * n, y * n


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
