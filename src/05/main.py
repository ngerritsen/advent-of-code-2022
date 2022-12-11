import re
import os
from collections import deque

CRATEMOVER_9000 = 9000
CRATEMOVER_9001 = 9001


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_final_positions(lines, CRATEMOVER_9000))
    print(get_final_positions(lines, CRATEMOVER_9001))


def get_final_positions(lines, cratemover_version):
    initial_position_lines, move_lines = split_lines(lines)
    positions = parse_initial_positions(initial_position_lines)
    apply_moves(positions, move_lines, cratemover_version)
    return get_top_crates(positions)


def apply_moves(positions, move_lines, cratemover_version):
    for line in move_lines:
        res = re.match(r"move (\d+) from (\d+) to (\d+)", line)
        count, from_pos, to_pos = tuple(map(int, res.groups()))

        if cratemover_version == CRATEMOVER_9000:
            apply_move_9000(positions, count, from_pos, to_pos)
        else:
            apply_move_9001(positions, count, from_pos, to_pos)


def apply_move_9000(positions, count, from_pos, to_pos):
    for i in range(count):
        positions[to_pos - 1].append(positions[from_pos - 1].pop())


def apply_move_9001(positions, count, from_pos, to_pos):
    stack = deque()

    for i in range(count):
        stack.append(positions[from_pos - 1].pop())

    while len(stack) > 0:
        positions[to_pos - 1].append(stack.pop())


def get_top_crates(positions):
    res = ""

    for pos in positions:
        res += pos.pop()

    return res


def split_lines(lines):
    split_index = 0
    for index, line in enumerate(lines):
        if line.strip() == "":
            split_index = index

    return lines[0:split_index - 1], lines[split_index + 1:]


def parse_initial_positions(lines):
    lines.reverse()
    cols = int((len(lines[0]) + 1) / 4)
    positions = []

    for i in range(cols):
        positions.append(deque())

    for line in lines:
        for i in range(cols):
            crate = line[i * 4 + 1]

            if crate != " ":
                positions[i].append(crate)

    return positions

if __name__ == '__main__':
    main()
