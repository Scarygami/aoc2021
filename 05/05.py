import os
import re
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        vents = []
        for line in lines:
            vents.append([int(n) for n in re.split(",| -> ", line)])

    return vents


def draw_vents_straight(vents, grid=None):
    if grid is None:
        grid = defaultdict(int)
    for vent in vents:
        if vent[0] == vent[2] or vent[1] == vent[3]:
            x1 = min(vent[0], vent[2])
            x2 = max(vent[0], vent[2])
            y1 = min(vent[1], vent[3])
            y2 = max(vent[1], vent[3])
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[(x, y)] = grid[(x, y)] + 1

    return grid


def draw_vents_diagonal(vents, grid=None):
    if grid is None:
        grid = defaultdict(int)
    for vent in vents:
        if vent[0] != vent[2] and vent[1] != vent[3]:
            x1 = vent[0]
            x2 = vent[2]
            y1 = vent[1]
            y2 = vent[3]
            dx = 1 if x1 < x2 else -1
            dy = 1 if y1 < y2 else -1
            x = x1
            y = y1
            for _ in range(abs(x1 - x2) + 1):
                grid[(x, y)] = grid[(x, y)] + 1
                x = x + dx
                y = y + dy

    return grid


def part1(filename):
    vents = parse_input(filename)
    grid = draw_vents_straight(vents)

    crossings = [key for key in grid if grid[key] > 1]

    return len(crossings)


def part2(filename):
    vents = parse_input(filename)
    grid = draw_vents_straight(vents)
    grid = draw_vents_diagonal(vents, grid)

    crossings = [key for key in grid if grid[key] > 1]

    return len(crossings)


assert part1(os.path.join(currentdir, "test_input.txt")) == 5

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 12

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
