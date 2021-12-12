import os

currentdir = os.path.dirname(os.path.abspath(__file__))

neighbours = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        state = []
        for line in lines:
            state.append([int(s) for s in line])

    return state


def find_flashes(state):
    flashes = []
    for y in range(len(state)):
        for x in range(len(state[0])):
            if state[y][x] > 9:
                flashes.append((x, y))

    return flashes


def simulate(state):
    width = len(state[0])
    height = len(state)

    # increase all by 1
    new_state = [[n + 1 for n in line] for line in state]
    flash_count = 0

    flashes = find_flashes(new_state)
    while len(flashes) > 0:
        for xf, yf in flashes:
            for dx, dy in neighbours:
                x = xf + dx
                y = yf + dy
                if x >= 0 and x < width and y >= 0 and y < height:
                    if new_state[y][x] != 0:
                        new_state[y][x] = new_state[y][x] + 1
            new_state[yf][xf] = 0
            flash_count = flash_count + 1

        flashes = find_flashes(new_state)

    return new_state, flash_count


def part1(filename, steps=100):
    state = parse_input(filename)
    all_flashes = 0
    for _ in range(steps):
        state, flashes = simulate(state)
        all_flashes = all_flashes + flashes

    return all_flashes


def part2(filename):
    state = parse_input(filename)
    width = len(state[0])
    height = len(state)
    target = width * height
    steps = 0

    while True:
        steps = steps + 1
        state, flashes = simulate(state)
        if flashes == target:
            return steps


assert part1(os.path.join(currentdir, "test_input1.txt"), 1) == 9
assert part1(os.path.join(currentdir, "test_input2.txt"), 10) == 204
assert part1(os.path.join(currentdir, "test_input2.txt")) == 1656

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))


assert part2(os.path.join(currentdir, "test_input2.txt")) == 195

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
