import math
import os
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Monkey:
    operation: Callable[[int], int]
    items: List[int]
    divisor: int
    if_true: int
    if_false: int
    inspections: int = 0


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        data = f.read()

    print(play_game(data, 20, True))
    print(play_game(data, 10000, False))


def play_game(data, rounds, calm):
    monkeys = parse_monkeys(data)
    common_divisor = math.prod(map(lambda m: m.divisor, monkeys))

    for _ in range(rounds):
        play_round(monkeys, calm, common_divisor)

    return get_monkey_business_lvl(monkeys)


def get_monkey_business_lvl(monkeys):
    inspections = list(map(lambda m: m.inspections, monkeys))
    inspections.sort()
    return math.prod(inspections[-2:])


def play_round(monkeys, calm, common_divisor):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            val = monkey.items.pop(0)
            val = monkey.operation(val)
            val = math.floor(val / 3) if calm else val % common_divisor
            passes = val % monkey.divisor == 0
            target = monkey.if_true if passes else monkey.if_false

            monkey.inspections += 1
            monkeys[target].items.append(val)


def parse_monkeys(data):
    chunks = data.split("\n\n")
    return tuple(map(create_monkey, chunks))


def create_monkey(chunk):
    cmds = chunk.split("\n")
    op = cmds[2].split("= ")[-1]

    return Monkey(
        items=list(map(int, cmds[1].split(": ")[-1].split(", "))),
        operation=eval(f"lambda old: {op}"),
        divisor=int(cmds[3].split(" ")[-1]),
        if_true=int(cmds[4].split(" ")[-1]),
        if_false=int(cmds[5].split(" ")[-1])
    )


if __name__ == '__main__':
    main()
