import os

LOWERCASE_START = 97
UPPERCASE_START = 65
ALPHABET_LENGTH = 26


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_total_duplicate_priority(lines))
    print(get_total_triplet_priority(lines))


def get_total_duplicate_priority(lines):
    total = 0

    for line in lines:
        total += get_duplicate_priority(line)

    return total


def get_duplicate_priority(line):
    line = line.strip()
    length = len(line)
    half = int(length / 2)
    left = line[0:half]
    right = line[half:length]
    right_set = set(right)

    for char in left:
        if char in right_set:
            return char_to_priority(char)


def get_total_triplet_priority(lines):
    total = 0
    triplet = []

    for line in lines:
        triplet.append(line)
        if len(triplet) == 3:
            total += get_triplet_priority(triplet)
            triplet = []

    return total


def get_triplet_priority(triplet):
    first, second, third = triplet
    second_set = set(second)
    third_set = set(third)

    for char in first:
        if char in second_set and char in third_set:
            return char_to_priority(char)


def char_to_priority(char):
    n = ord(char)

    if n >= LOWERCASE_START:
        return n - LOWERCASE_START + 1
    else:
        return n - UPPERCASE_START + 1 + ALPHABET_LENGTH


if __name__ == '__main__':
    main()
