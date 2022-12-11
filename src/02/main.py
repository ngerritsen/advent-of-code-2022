import os

ROCK = "A"
PAPER = "B"
SCISSORS = "C"
WIN = "Z"
DRAW = "Y"
LOSE = "X"
MOVE_SCORES = {ROCK: 1, PAPER: 2, SCISSORS: 3}
RESULT_SCORES = {WIN: 6, DRAW: 3, LOSE: 0}
WINS = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
LOSSES = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}
NAIVE_MOVES = {LOSE: ROCK, DRAW: PAPER, WIN: SCISSORS}


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_total_score_naive(lines))
    print(get_total_score_strategy(lines))


def get_total_score_strategy(lines):
    total = 0

    for line in lines:
        total += get_score_strategy(line)

    return total


def get_score_strategy(line):
    theirs, goal = line.strip().split()
    ours = theirs

    if goal == WIN:
        ours = WINS.get(theirs)
    elif goal == LOSE:
        ours = LOSSES.get(theirs)

    return RESULT_SCORES.get(goal) + MOVE_SCORES.get(ours)


def get_total_score_naive(lines):
    total = 0

    for line in lines:
        total += get_score_naive(line)

    return total


def get_score_naive(line):
    theirs, ours = line.split()
    ours = NAIVE_MOVES[ours]
    result = DRAW

    if WINS[theirs] == ours:
        result = WIN
    elif LOSSES[theirs] == ours:
        result = LOSE

    return MOVE_SCORES[ours] + RESULT_SCORES[result]


if __name__ == '__main__':
    main()
