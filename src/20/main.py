import os

KEY = 811589153
IDX = [1000, 2000, 3000]


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    coords = [(i, int(line)) for i, line in enumerate(lines)]
    decrypted = [(c[0], c[1] * KEY) for c in coords]

    print(get_coord_sum(un_mix_coords(list(coords))))
    print(get_coord_sum(un_mix_coords(decrypted, 10)))


def un_mix_coords(coords, times=1):
    for _ in range(times):
        for i in range(len(coords)):
            curr, val = find_index_and_val(coords, i)
            move_to = (curr + val) % (len(coords) - 1)
            move_to = len(coords) - 1 if move_to == 0 else move_to
            coords.insert(move_to, coords.pop(curr))

    return coords


def get_coord_sum(coords):
    zero_index = [c[1] for c in coords].index(0)
    return sum([coords[(zero_index + m) % len(coords)][1] for m in IDX])


def find_index_and_val(coords, oi):
    for i, item in enumerate(coords):
        if item[0] == oi:
            return i, item[1]


if __name__ == '__main__':
    main()
