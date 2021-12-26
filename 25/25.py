import os

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        grid = {}
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                grid[x, y] = lines[y][x]

    return grid, len(lines), len(lines[0])


def simulate(filename):
    grid, max_y, max_x = parse_input(filename)
    steps = 0
    while True:
        steps = steps + 1
        moves = 0
        east = [
            (x, y) for x, y in grid
            if grid[x, y] == ">" and grid[(x + 1) % max_x, y] == "."
        ]
        moves = moves + len(east)
        for x, y in east:
            grid[x, y] = "."
            grid[(x + 1) % max_x, y] = ">"

        south = [
            (x, y) for x, y in grid
            if grid[x, y] == "v" and grid[x, (y + 1) % max_y] == "."
        ]
        moves = moves + len(south)
        for x, y in south:
            grid[x, y] = "."
            grid[x, (y + 1) % max_y] = "v"

        if moves == 0:
            return steps


assert simulate(os.path.join(currentdir, "test_input1.txt")) == 58
print("Part 1: ", simulate(os.path.join(currentdir, "input.txt")))
