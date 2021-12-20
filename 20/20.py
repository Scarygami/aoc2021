import os
import numpy as np

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        rule = [True if c == "#" else False for c in lines[0]]
        size = len(lines[2]) + 2
        grid = np.array([np.zeros(size, dtype=bool)])

        for line in lines[2:]:
            row = [False]
            row.extend([True if c == "#" else False for c in line])
            row.append(False)
            grid = np.append(grid, [row], 0)

        grid = np.append(grid, [np.zeros(size, dtype=bool)], 0)

    return rule, grid


def extend(grid, outside):
    size = grid.shape[0]
    if outside:
        extension = [np.ones(size, dtype=bool)]
    else:
        extension = [np.zeros(size, dtype=bool)]
    grid = np.append(grid, extension, 0)
    grid = np.append(extension, grid, 0)

    size = size + 2
    if outside:
        extension = np.transpose([np.ones(size, dtype=bool)])
    else:
        extension = np.transpose([np.zeros(size, dtype=bool)])

    grid = np.append(grid, extension, 1)
    grid = np.append(extension, grid, 1)

    return grid


def shrink(grid):
    size = grid.shape[0]
    return grid[1:size-1, 1:size-1]


def simulate_step(rule, grid, outside):
    extended = extend(grid, outside)
    size = grid.shape[0]

    for x in range(size):
        for y in range(size):
            data = extended[x:x+3, y:y+3]
            index = 0
            for bit in data.flatten():
                index = index * 2 + (1 if bit else 0)

            grid[x, y] = rule[index]

    if outside:
        outside = rule[511]
    else:
        outside = rule[0]

    grid = extend(grid, outside)

    return grid, outside


def simulate(filename, steps):
    rule, grid = parse_input(filename)
    outside = False

    for _ in range(steps):
        grid, outside = simulate_step(rule, grid, outside)

    return np.count_nonzero(grid)


assert simulate(os.path.join(currentdir, "test_input.txt"), 2) == 35
print("Part 1: ", simulate(os.path.join(currentdir, "input.txt"), 2))

assert simulate(os.path.join(currentdir, "test_input.txt"), 50) == 3351
print("Part 1: ", simulate(os.path.join(currentdir, "input.txt"), 50))
