import os

WIDTH = 7
ROCKS = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2), (1, 0), (0, 0)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
)


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        jets = tuple(map(lambda j: -1 if j == "<" else 1, list(f.read())))

        print(simulate(jets, 2022))


def simulate(jets, rounds):
    rocks = set()
    height = 0
    r, j = 0, 0

    for i in range(rounds):
        x, y = 2, height + 3
        rock = ROCKS[r]

        while True:
            nx = x + jets[j]

            if not collides(nx, y, rock, rocks):
                x = nx

            if collides(x, y - 1, rock, rocks):
                height = max(y + get_height(rock), height)

                for unit in rock:
                    rocks.add(add_coords(unit, (x, y)))
                break
            else:
                y -= 1

            j = cycle(j, jets)

        j = cycle(j, jets)
        r = cycle(r, ROCKS)

    return height


def collides(x, y, rock, rocks):
    w = get_width(rock)

    if not 0 <= x <= WIDTH - w or y < 0:
        return True

    for unit in rock:
        ux, uy = add_coords(unit, (x, y))
        if (ux, uy) in rocks:
            return True

    return False


def add_coords(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


def cycle(i, it):
    return (i + 1) % len(it)


def get_width(rock):
    return max([r[0] for r in rock]) + 1


def get_height(rock):
    return max([r[1] for r in rock]) + 1


if __name__ == '__main__':
    main()
