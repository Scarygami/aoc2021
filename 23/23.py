import os
import json

currentdir = os.path.dirname(os.path.abspath(__file__))

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

targets = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9
}


def parse_input(filename, part2=False):
    with open(filename) as f:
        lines = f.read().splitlines()
        grid = {}
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] in ["A", "B", "C", "D", "."]:
                    grid[x, y] = (lines[y][x], "" if lines[y][x] == "." else "start")

    if part2:
        for x in targets.values():
            grid[x, 5] = grid[x, 3]

        grid[3, 3] = ("D", "start")
        grid[3, 4] = ("D", "start")
        grid[5, 3] = ("C", "start")
        grid[5, 4] = ("B", "start")
        grid[7, 3] = ("B", "start")
        grid[7, 4] = ("A", "start")
        grid[9, 3] = ("A", "start")
        grid[9, 4] = ("C", "start")

    y_max = 5 if part2 else 3
    for y in range(y_max, 1, -1):
        for x in targets.values():
            amphipod, _ = grid[x, y]
            if x == targets[amphipod]:
                if y == y_max:
                    grid[x, y] = (amphipod, "end")
                    continue
                if grid[x, y + 1][1] == "end":
                    grid[x, y] = (amphipod, "end")

    return grid


def is_reachable(grid, amphipod_coord, target_coord, part2=False):
    amphipod, state = grid[amphipod_coord]
    xa, ya = amphipod_coord
    xt, yt = target_coord

    if state == "end":
        return False

    y_max = 3
    if part2:
        y_max = 5

    if state == "moved":
        if xt != targets[amphipod] or yt == 1:
            return False

        for y in range(yt + 1, y_max + 1):
            if grid[xt, y][0] != amphipod:
                return False

        for y in range(2, yt + 1):
            if grid[xt, y][0] != ".":
                return False

    if state == "start":
        if yt != 1:
            return False
        if xt in targets.values():
            return False
        for y in range(2, ya):
            if grid[xa, y][0] != ".":
                return False

    if xa < xt:
        x1 = xa + 1
        x2 = xt + 1
    else:
        x1 = xt
        x2 = xa

    for x in range(x1, x2):
        if grid[(x, 1)][0] != ".":
            return False

    return True


def find_moves(grid, part2=False):
    moves = []
    amphipods = [
        coord for coord in grid
        if grid[coord][1] in ["start", "moved"]
    ]
    amphipods.sort(key=lambda a: grid[a][1])
    empty = [
        coord for coord in grid
        if grid[coord][0] == "."
    ]
    for amphipod in amphipods:
        reachable = [
            coord for coord in empty if is_reachable(grid, amphipod, coord, part2)
        ]
        moves.extend(
            (amphipod, coord) for coord in reachable
        )

    return moves


def distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def detect_goal(grid):
    states = [grid[coord][1] for coord in grid]
    if "start" in states or "moved" in states:
        return False
    return True


def heuristic(frontier):
    grid, cost = frontier
    ends = sum([1 for coord in grid if grid[coord][1] == "end"])
    moved = sum([1 for coord in grid if grid[coord][1] == "moved"])

    return (-ends, -moved, cost)


def grid_hash(grid):
    return json.dumps(list(grid.items()), sort_keys=True)


def find_path(filename, part2=False):
    grid = parse_input(filename, part2)

    frontiers = [(grid, 0)]
    state_costs = {}
    state_costs[grid_hash(grid)] = 0
    final_cost = None
    while len(frontiers) > 0:
        frontiers.sort(key=lambda f: heuristic(f))
        (grid, cost) = frontiers.pop(0)
        moves = find_moves(grid, part2)
        for (start, end) in moves:
            new_grid = grid.copy()
            new_grid[start] = (".", "")
            amphipod, state = grid[start]
            if state == "start":
                new_state = "moved"
            if state == "moved":
                new_state = "end"
            new_grid[end] = (amphipod, new_state)
            new_cost = cost + distance(start, end) * costs[amphipod]
            if final_cost is not None and new_cost >= final_cost:
                continue
            if detect_goal(new_grid):
                if final_cost is None or new_cost < final_cost:
                    final_cost = new_cost
                continue
            hash = grid_hash(new_grid)
            if hash in state_costs and state_costs[hash] <= new_cost:
                continue
            state_costs[hash] = new_cost

            frontiers.append((new_grid, new_cost))

    return final_cost


assert find_path(os.path.join(currentdir, "test_input1.txt")) == 12521
print("Part 1: ", find_path(os.path.join(currentdir, "input.txt")))

assert find_path(os.path.join(currentdir, "test_input1.txt"), True) == 44169
print("Part 2: ", find_path(os.path.join(currentdir, "input.txt"), True))
