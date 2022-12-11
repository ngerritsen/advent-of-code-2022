import math
import os

MOVES = {
    "U": [0, 1],
    "R": [1, 0],
    "D": [0, -1],
    "L": [-1, 0]
}


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_tail_visited_position_count(lines, 2))
    print(get_tail_visited_position_count(lines, 10))


def get_tail_visited_position_count(lines, length):
    knots = [[0, 0] for _ in range(length)]
    tail_positions = set()
    tail_positions.add(tuple(knots[-1]))

    for line in lines:
        direction, times = line.split(" ")
        move_vect = MOVES[direction]

        for _ in range(int(times)):
            knots[0][0] += move_vect[0]
            knots[0][1] += move_vect[1]

            for i in range(1, length):
                hx, hy = knots[i - 1]
                tx, ty = knots[i]
                dx = abs(hx - tx)
                dy = abs(hy - ty)

                if dx > 1 or dy > 1:
                    tx += sign(hx, tx)
                    ty += sign(hy, ty)

                knots[i] = [tx, ty]

            tail_positions.add(tuple(knots[-1]))

    return len(tail_positions)


def sign(a, b):
    return 0 if a == b else math.copysign(1, a - b)


if __name__ == '__main__':
    main()
