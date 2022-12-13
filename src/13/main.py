import os
from functools import cmp_to_key

DPS = ["[[2]]", "[[6]]"]


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_in_order_scores(lines))
    print(get_decoder_key(lines))


def get_decoder_key(lines):
    for dp in DPS:
        lines.append(dp)

    lines = list(filter(lambda l: l != "", lines))
    key = 1

    lines.sort(key=cmp_to_key(cmp_lines))

    for i, line in enumerate(lines):
        if line in DPS:
            key *= (i + 1)

    return key


def get_in_order_scores(lines):
    total = 0
    left = ""

    for i, line in enumerate(lines):
        if (i - 1) % 3 == 0:
            if cmp_lines(left, line) == -1:
                total += ((i - 1) + 3) / 3
        if i % 3 == 0:
            left = line

    return int(total)


def cmp_lines(left, right):
    return cmp_packets(eval(left), eval(right))


def cmp_packets(left, right):
    for i, r in enumerate(right):
        if i >= len(left):
            return -1

        l = left[i]

        if is_list(l) or is_list(r):
            res = cmp_packets(as_list(l), as_list(r))

            if res != 0:
                return res
            else:
                continue

        if l == r:
            continue
        else:
            return -1 if r > l else 1

    if len(right) == len(left):
        return 0
    else:
        return -1 if len(right) > len(left) else 1


def as_list(val):
    return val if is_list(val) else [val]


def is_list(val):
    return type(val) == list


if __name__ == '__main__':
    main()
