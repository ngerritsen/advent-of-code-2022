import itertools
import os
import re
from functools import cache
from dataclasses import dataclass

START = "AA"


@dataclass
class Valve:
    name: str
    rate: int
    neighbours: set[str]


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    valves = parse_valves(lines)

    print(release_pressure(valves))
    print(release_pressure(valves, True))


def release_pressure(valves, with_elephant=False):
    @cache
    def find_max_pressure(curr, minutes, opened):
        if minutes < 2:
            return 0

        max_pressure = 0

        for n in valves[curr].neighbours:
            pressure = find_max_pressure(n, minutes - 1, opened)

            if n not in opened and valves[n].rate > 0:
                added_pressure = (minutes - 2) * valves[n].rate
                next_opened = opened.union({n})
                next_pressure = find_max_pressure(n, minutes - 2, next_opened)
                pressure = max(next_pressure + added_pressure, pressure)

            max_pressure = max(pressure, max_pressure)

        return max_pressure

    if with_elephant:
        relevant_valves = filter(lambda v: v.rate > 0, valves.values())
        relevant_valves = [v.name for v in relevant_valves]
        partitions = set()

        for i in range(len(relevant_valves)):
            for c in itertools.combinations(relevant_valves, i):
                partitions.add(tuple(sorted(c)))

        max_combined_pressure = 0

        for i, pa in enumerate(partitions):
            pb = filter(lambda v: v not in pa, relevant_valves)
            pressure_a = find_max_pressure(START, 26, frozenset(pa))
            pressure_b = find_max_pressure(START, 26, frozenset(pb))
            max_combined_pressure = max(max_combined_pressure, pressure_a + pressure_b)

        return max_combined_pressure
    else:
        return find_max_pressure(START, 30, frozenset())


def parse_valves(lines):
    valves = dict()

    for line in lines:
        name, *neighbours = re.findall(r"([A-Z]{2})", line)
        rate = int(re.search(r"(\d+)", line).group())
        valves[name] = Valve(name, rate, set(neighbours))

    return valves


if __name__ == '__main__':
    main()
