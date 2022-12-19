import os
import re
import math
from collections import deque


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    blueprints = [list(map(int, re.findall(r"\d+", l)))[1:] for l in lines]

    print(get_total_blueprint_quality(blueprints))
    print(get_max_geode_multple(blueprints[:3]))


def get_total_blueprint_quality(blueprints):
    quality_levels = list()

    for i, bp in enumerate(blueprints):
        max_geodes = run_blueprint(bp, 23)
        quality_levels.append(max_geodes * (i + 1))

    return sum(quality_levels)


def get_max_geode_multple(blueprints):
    results = list()

    for i, bp in enumerate(blueprints):
        max_geodes = run_blueprint(bp, 31)
        results.append(max_geodes)

    return math.prod(results)


def run_blueprint(bp, total_minutes):
    stack = deque()
    stack.append((total_minutes, -1, [0, 0, 0, 0], [1, 0, 0, 0], ()))
    results = set()
    max_ore_cost = max(bp[0], bp[1], bp[2], bp[4])
    max_clay_cost = bp[3]
    max_obsidian_cost = bp[5]

    while len(stack) > 0:
        minutes, build, ores, bots, skip = stack.pop()

        for r in range(len(bots)):
            ores[r] += bots[r]

        if build > -1:
            bots[build] += 1

        if minutes == 0:
            results.add(ores[3])
            continue

        can_build_geode_bot = ores[0] >= bp[4] and ores[2] >= bp[5]
        can_build_obsidian_bot = ores[0] >= bp[2] and ores[1] >= bp[3]
        can_build_clay_bot = ores[0] >= bp[1]
        can_build_ore_bot = ores[0] >= bp[0]
        at_max_ore = ores[0] + (minutes * bots[0]) >= max_ore_cost * minutes
        at_max_clay = ores[1] + (minutes * bots[1]) >= max_clay_cost * minutes

        if can_build_geode_bot:
            next_ores = ores.copy()
            next_ores[0] -= bp[4]
            next_ores[2] -= bp[5]
            stack.append((minutes - 1, 3, next_ores, bots.copy(), ()))
            continue

        if can_build_obsidian_bot and max_obsidian_cost > bots[2] and 2 not in skip:
            next_ores = ores.copy()
            next_ores[0] -= bp[2]
            next_ores[1] -= bp[3]
            stack.append((minutes - 1, 2, next_ores, bots.copy(), ()))

        if can_build_clay_bot and max_clay_cost > bots[1] and 1 not in skip and not at_max_clay:
            next_ores = ores.copy()
            next_ores[0] -= bp[1]
            stack.append((minutes - 1, 1, next_ores, bots.copy(), ()))

        if can_build_ore_bot and max_ore_cost > bots[0] and 0 not in skip and not at_max_ore:
            next_ores = ores.copy()
            next_ores[0] -= bp[0]
            stack.append((minutes - 1, 0, next_ores, bots.copy(), ()))

        skip = list()

        if can_build_obsidian_bot:
            skip.append(2)
        if can_build_clay_bot:
            skip.append(1)
        if can_build_ore_bot:
            skip.append(0)

        stack.append((minutes - 1, -1, ores.copy(), bots.copy(), skip))

    return max(results)


if __name__ == '__main__':
    main()
