import os
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(__file__))
dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        costs = []

        for line in lines:
            costs.append([int(n) for n in line])

    return costs


def cheapest_path(costs):
    paths = [(0, 0, 0)]
    total_costs = defaultdict(lambda: 10000000000000000)
    max_x = len(costs[0])
    max_y = len(costs)

    while len(paths) > 0:
        paths.sort(key=lambda p: p[2])
        new_paths = []
        for x, y, cost in paths:
            for dx, dy in dirs:
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= max_x:
                    continue
                if ny < 0 or ny >= max_y:
                    continue

                new_cost = cost + costs[ny][nx]
                if total_costs[(nx, ny)] <= new_cost:
                    continue

                total_costs[(nx, ny)] = new_cost
                new_paths.append((nx, ny, new_cost))

        paths = new_paths

    return total_costs[(max_x - 1, max_y - 1)]


def part1(filename):
    costs = parse_input(filename)

    return cheapest_path(costs)


def extend(costs, times):
    # extend in x direction
    for line in costs:
        line.extend([(n + d) % 9 + 1 for d in range(times - 1) for n in line])

    # extend in y direction
    costs.extend(
        [[(n + d) % 9 + 1 for n in line] for d in range(times - 1) for line in costs]
    )

    return costs


def part2(filename):
    costs = parse_input(filename)
    costs = extend(costs, 5)
    return cheapest_path(costs)


assert part1(os.path.join(currentdir, "test_input.txt")) == 40

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 315

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
