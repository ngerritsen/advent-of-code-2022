import os
import sys
from collections import deque

LOWERCASE_START = 97
START = "S"
END = "E"

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    grid, start, goal = create_grid(lines)
    print(get_shortest_path(grid, start, goal))
    print(get_shortest_hike(grid, goal))


def get_shortest_hike(grid, goal):
    shortest_hike = sys.maxsize
    queue = deque([(goal, 0)])
    visited = set()
    visited.add(goal)

    while len(queue) > 0:
        curr, cost = queue.popleft()

        if get(grid, curr) == 0:
            shortest_hike = min(shortest_hike, cost)

        for d in dirs:
            nxt = add(curr, d)

            if is_accessible(grid, nxt, curr) and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, cost + 1))

    return shortest_hike


def get_shortest_path(grid, start, goal):
    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)

    while len(queue) > 0:
        curr, cost = queue.popleft()

        if curr == goal:
            return cost

        for d in dirs:
            nxt = add(curr, d)

            if is_accessible(grid, curr, nxt) and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, cost + 1))

    return sys.maxsize


def is_accessible(grid, curr, nxt):
    if not in_bounds(grid, nxt) or not in_bounds(grid, curr):
        return False

    return get(grid, curr) >= get(grid, nxt) - 1


def in_bounds(grid, coords):
    x, y = coords
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def get(grid, coords):
    x, y = coords
    return grid[y][x]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def create_grid(lines):
    start, goal = (0, 0), (0, 0)
    grid = [[] for _ in lines]

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start = x, y
            elif char == "E":
                goal = x, y

            grid[y].append(char_to_elevation(char))

    return grid, start, goal


def char_to_elevation(char):
    if char == "S":
        return 0
    elif char == "E":
        return char_to_elevation("z")
    else:
        return ord(char) - LOWERCASE_START


if __name__ == '__main__':
    main()
