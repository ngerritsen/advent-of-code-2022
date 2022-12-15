import os
import re

ROW = 2_000_000
MAX_DISTRESS = 4_000_000


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    sensors, beacons = parse_items(lines)

    print(count_covered(sensors, beacons))
    print(find_distress_freq(sensors))


def count_covered(sensors, beacons):
    min_x, max_x = get_bounds(sensors)
    y = ROW
    covered = 0

    intervals = get_intervals(sensors, y, min_x, max_x)
    intervals = merge_intervals(intervals)

    for interval in intervals:
        covered += interval[1] - interval[0] + 1

    for beacon in beacons:
        if beacon[1] == y:
            covered -= 1

    return covered


def find_distress_freq(sensors):
    for y in range(MAX_DISTRESS + 1):
        min_x = 0
        max_x = MAX_DISTRESS
        intervals = get_intervals(sensors, y, min_x, max_x)

        for interval in intervals:
            if interval[0] > min_x:
                return (interval[0] - 1) * 4_000_000 + y

            if interval[1] > min_x:
                min_x = interval[1] + 1


def get_intervals(sensors, y, min_x, max_x):
    intervals = list()

    for s in sensors:
        sx, sy, dist = s
        dy = abs(y - sy)
        dx = dist - dy

        if dist < dy:
            continue

        start_x = max(min_x, sx - dx)
        end_x = min(max_x, sx + dx)

        intervals.append((start_x, end_x))

    return sorted(intervals, key=lambda x: x[0])


def merge_intervals(intervals):
    merged = list()
    intervals = sorted(intervals, key=lambda x: x[0])

    for interval in intervals:
        if len(merged) > 0 and interval[0] <= merged[-1][1]:
            prev = merged.pop()
            merged.append((prev[0], max(prev[1], interval[1])))
        else:
            merged.append(interval)

    return merged


def get_bounds(sensors):
    min_x = min(map(lambda i: i[0] - i[2], sensors))
    max_x = max(map(lambda i: i[0] + i[2], sensors))

    return min_x, max_x


def get_dist(ax, ay, bx, by):
    return max(ax, bx) - min(ax, bx) + max(ay, by) - min(ay, by)


def parse_items(lines):
    sensors = set()
    beacons = set()

    for line in lines:
        matches = (
            re.match(r".+x=(.+), y=(.+):.+x=(.+), y=(.+)", line).groups())
        sx, sy, bx, by = map(int, matches)
        dist = get_dist(sx, sy, bx, by)
        sensors.add((sx, sy, dist))
        beacons.add((bx, by))

    return sensors, beacons


if __name__ == '__main__':
    main()
