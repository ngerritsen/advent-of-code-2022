import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_total(has_fully_containing_section, lines))
    print(get_total(has_overlapping_section, lines))


def get_total(predicate, lines):
    total = 0

    for line in lines:
        if predicate(parse_line(line)):
            total += 1

    return total


def has_fully_containing_section(pair):
    return fully_contains(pair[0], pair[1]) or fully_contains(pair[1], pair[0])


def fully_contains(a, b):
    return b[0] >= a[0] and b[1] <= a[1]


def has_overlapping_section(pair):
    return overlaps(pair[0], pair[1]) or overlaps(pair[1], pair[0])


def overlaps(a, b):
    return a[0] <= b[0] <= a[1]


def parse_line(line):
    parts = line.strip().split(',')
    return tuple(map(lambda p: tuple(map(int, p.split('-'))), parts))


if __name__ == '__main__':
    main()
