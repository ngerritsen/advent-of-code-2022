import math
import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    tree_grid = list(map(lambda line: list(map(int, line)), lines))

    print(get_amount_of_trees_visible_from_outside(tree_grid))
    print(get_best_scenic_score(tree_grid))


def get_amount_of_trees_visible_from_outside(grid):
    visible_trees = set()
    height = len(grid)
    width = len(grid[0])

    # Horizontal
    for y in range(height):
        # From left
        max_size = -1
        for x in range(width):
            max_size = add_if_taller(grid, x, y, visible_trees, max_size)

        # From right
        max_size = -1
        for x in range(width - 1, -1, -1):
            max_size = add_if_taller(grid, x, y, visible_trees, max_size)

    # Vertical
    for x in range(width):
        # From top
        max_size = -1
        for y in range(height):
            max_size = add_if_taller(grid, x, y, visible_trees, max_size)

        # From bottom
        max_size = -1
        for y in range(width - 1, -1, -1):
            max_size = add_if_taller(grid, x, y, visible_trees, max_size)

    return len(visible_trees)


def add_if_taller(grid, x, y, visible_trees, max_size):
    val = grid[y][x]
    if val <= max_size:
        return max_size
    visible_trees.add((x, y))
    return val


def get_best_scenic_score(grid):
    height = len(grid)
    width = len(grid[0])
    max_score = -1

    for y in range(height):
        for x in range(width):
            scores = []
            tree_height = grid[y][x]

            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                continue

            # To left
            score = 0
            for nx in range(x - 1, -1, -1):
                score += 1
                if grid[y][nx] >= tree_height:
                    break

            scores.append(score)

            # To right
            score = 0
            for nx in range(x + 1, width):
                score += 1
                if grid[y][nx] >= tree_height:
                    break

            scores.append(score)

            # To top
            score = 0
            for ny in range(y - 1, -1, -1):
                score += 1
                if grid[ny][x] >= tree_height:
                    break

            scores.append(score)

            # To bottom
            score = 0
            for ny in range(y + 1, height):
                score += 1
                if grid[ny][x] >= tree_height:
                    break

            scores.append(score)
            total_score = math.prod(scores)

            if total_score > max_score:
                max_score = total_score

    return max_score


if __name__ == '__main__':
    main()
