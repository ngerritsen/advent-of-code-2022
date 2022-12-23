import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    elves = parse_elves(lines)
    vecs = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    print(get_progress(elves.copy(), vecs.copy()))
    print(get_total_rounds(elves.copy(), vecs.copy()))


def get_progress(elves, vecs):
    for _ in range(10):
        explore(elves, vecs)

    x_points = [elf[0] for elf in elves]
    y_points = [elf[1] for elf in elves]
    width = max(x_points) - min(x_points) + 1
    height = max(y_points) - min(y_points) + 1

    return (width * height) - len(elves)


def get_total_rounds(elves, vecs):
    moved = True
    i = 0

    while moved:
        i += 1
        moved = explore(elves, vecs)

    return i


def explore(elves, vecs):
    proposals = dict()
    moved = False

    for elf in elves:
        if is_clear(elves, elf):
            continue

        for vec in vecs:
            target = add_coords(elf, vec)

            if target in elves:
                continue
            if add_coords(elf, get_diag_vec(vec, 1)) in elves:
                continue
            if add_coords(elf, get_diag_vec(vec, -1)) in elves:
                continue

            if target not in proposals:
                proposals[target] = list()

            proposals[target].append(elf)
            moved = True
            break

    for target, candidates in proposals.items():
        if len(candidates) == 1:
            elves.remove(candidates[0])
            elves.add(target)

    vecs.append(vecs.pop(0))

    return moved


def is_clear(elves, elf):
    for y in range(elf[1] - 1, elf[1] + 2):
        for x in range(elf[0] - 1, elf[0] + 2):
            if (x, y) != elf and (x, y) in elves:
                return False

    return True


def get_diag_vec(vec, d):
    if vec[0] == 0:
        return vec[0] + d, vec[1]
    else:
        return vec[0], vec[1] + d


def add_coords(a, b):
    return a[0] + b[0], a[1] + b[1]


def parse_elves(lines):
    elves = set()

    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if val == "#":
                elves.add((x, y))

    return elves


if __name__ == '__main__':
    main()
