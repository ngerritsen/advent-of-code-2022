import os
import re
from collections import deque


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    blueprints = [list(map(int, re.findall(r"\d+", l)))[1:] for l in lines]

    print(get_total_blueprint_quality(blueprints))


def get_total_blueprint_quality(blueprints):
    quality_levels = list()

    for i, bp in enumerate(blueprints):
        max_geodes = run_blueprint(bp, 23)
        quality_levels.append(max_geodes * (i + 1))

    return sum(quality_levels)


def run_blueprint(bp, total_minutes):
    stack = deque()
    stack.append((total_minutes, -1, [0, 0, 0, 0], [1, 0, 0, 0]))
    results = set()
    max_ore_cost = max(bp[0], bp[1], bp[2], bp[4])
    max_clay_cost = bp[3]
    max_obsidian_cost = bp[5]

    while len(stack) > 0:
        minutes, build, ores, bots = stack.pop()

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

        if can_build_geode_bot:
            next_ores = ores.copy()
            next_ores[0] -= bp[4]
            next_ores[2] -= bp[5]
            stack.append((minutes - 1, 3, next_ores, bots.copy()))
            continue

        if can_build_obsidian_bot and max_obsidian_cost > bots[2]:
            next_ores = ores.copy()
            next_ores[0] -= bp[2]
            next_ores[1] -= bp[3]
            stack.append((minutes - 1, 2, next_ores, bots.copy()))
            continue

        if can_build_clay_bot and max_clay_cost > bots[1]:
            next_ores = ores.copy()
            next_ores[0] -= bp[1]
            stack.append((minutes - 1, 1, next_ores, bots.copy()))

        if can_build_ore_bot and max_ore_cost > bots[0]:
            next_ores = ores.copy()
            next_ores[0] -= bp[0]
            stack.append((minutes - 1, 0, next_ores, bots.copy()))

        stack.append((minutes - 1, -1, ores.copy(), bots.copy()))

    return max(results)


if __name__ == '__main__':
    main()
