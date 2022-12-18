import math
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

        # Not really sure how this offset works, but it does. Might have to do
        # with how cycles "lock" into each other (since you don't end with a
        # flat top) but not sure why it doesn't scale with the rock count then.
        offset = simulate(jets, 10_000) - simulate(jets, 10_000, True)

        print(simulate(jets, 1_000_000_000_000, True) + offset)


def simulate(jets, rounds, detect_cycle=False):
    rocks = set()
    height = 0
    r, j, i = 0, 0, 0
    states = dict()
    rock_state = list(-1 for _ in range(WIDTH))
    extra_height = 0

    while i < rounds:
        x, y = 2, height + 3
        rock = ROCKS[r]

        while True:
            nx = x + jets[j]

            if not collides(nx, y, rock, rocks):
                x = nx

            if collides(x, y - 1, rock, rocks):
                height = max(y + get_height(rock), height)

                for unit in rock:
                    (rock_x, rock_y) = add_coords(unit, (x, y))
                    rock_state[rock_x] = height - rock_y
                    rocks.add((rock_x, rock_y))
                break
            else:
                y -= 1

            j = cycle(j, jets)

        if detect_cycle:
            state = (j, r, tuple(rock_state))

            if extra_height == 0 and state in states:
                state_round, state_height = states[state]
                cycle_length = i - state_round
                cycle_height = height - state_height
                cycles_left = math.floor((rounds - i) / cycle_length)
                i += (cycles_left * cycle_length)
                extra_height = cycles_left * cycle_height
            else:
                states[state] = (i, height)
                i += 1
        else:
            i += 1

        j = cycle(j, jets)
        r = cycle(r, ROCKS)

    return height + extra_height


def get_state(rocks, height):
    state = list()

    for i in range(WIDTH):
        col = list(filter(lambda r: r[0] == i, rocks))

        if len(col) == 0:
            state.append(-1)
        else:
            state.append(height - max([r[1] for r in col]))

    return tuple(state)


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
