import os
from collections import deque


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        coords = parse_coords(f.read().split("\n"))

    print(get_area(coords))
    print(get_area(coords, True))


def get_area(coords, only_exposed=False):
    area = 0
    bounds = get_bounds(coords)
    cache = dict()

    for coord in coords:
        for i in range(len(coord)):
            for d in (-1, 1):
                next = move(coord, i, d)

                if next in coords:
                    continue

                if only_exposed and next not in cache:
                    cache[next] = is_exposed(coords, next, bounds, cache)

                if not only_exposed or cache[next]:
                    area += 1

    return area


def is_exposed(coords, coord, bounds, cache):
    stack = deque([coord])
    visited = set()

    while len(stack) > 0:
        curr = stack.pop()
        visited.add(curr)

        for i in range(len(coord)):
            for d in (-1, 1):
                next = move(curr, i, d)

                if next in cache:
                    return cache[next]

                if next in coords or next in visited:
                    continue

                if next[i] < 0 or next[i] > bounds[i]:
                    return True

                stack.append(next)

    return False


def move(coord, i, d):
    mut = list(coord)
    mut[i] += d
    return tuple(mut)


def get_bounds(coords):
    bounds = [0, 0, 0]

    for coord in coords:
        for i, v in enumerate(coord):
            bounds[i] = max(bounds[i], coord[i])

    return bounds


def parse_coords(lines):
    return set([tuple(map(int, line.split(","))) for line in lines])


if __name__ == '__main__':
    main()
