import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    coords = list()

    for i, line in enumerate(lines):
        coords.append((i, int(line)))

    un_mix_coords(coords)

    print(get_coord_sum(coords))


def un_mix_coords(coords):
    length = len(coords)

    for i in range(length):
        curr, val = find_index_and_val(coords, i)
        move_to = (curr + val) % (length - 1)

        if move_to == curr:
            continue

        move_to = length - 1 if move_to == 0 else move_to
        coords.insert(move_to, coords.pop(curr))


def get_coord_sum(coords):
    length = len(coords)
    zero_index = find_zero_index(coords)

    x = coords[(zero_index + 1000) % length][1]
    y = coords[(zero_index + 2000) % length][1]
    z = coords[(zero_index + 3000) % length][1]

    return x + y + z


def find_index_and_val(coords, oi):
    for i, item in enumerate(coords):
        if item[0] == oi:
            return i, item[1]


def find_zero_index(coords):
    for i, item in enumerate(coords):
        if item[1] == 0:
            return i


if __name__ == '__main__':
    main()
