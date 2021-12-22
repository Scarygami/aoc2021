import os
import numpy as np

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_rule(line):
    state, ranges = line.split(" ")
    ranges = [r[2:] for r in ranges.split(",")]
    ranges = [r.split("..") for r in ranges]
    ranges = [(int(r[0]), int(r[1])) for r in ranges]
    return (ranges, True if state == "on" else False)


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        rules = [parse_rule(line) for line in lines]

    return rules


def initialization_rule(rule):
    [(x1, x2), (y1, y2), (z1, z2)] = rule[0]
    if x1 < -50:
        return False
    if x2 > 50:
        return False
    if y1 < -50:
        return False
    if y2 > 50:
        return False
    if z1 < -50:
        return False
    if z2 > 50:
        return False
    return True


def voxelise(rules):
    xs = set()
    ys = set()
    zs = set()

    for [(x1, x2), (y1, y2), (z1, z2)], _ in rules:
        xs.add(x1)
        xs.add(x2+1)
        ys.add(y1)
        ys.add(y2+1)
        zs.add(z1)
        zs.add(z2+1)

    xs = sorted(xs)
    ys = sorted(ys)
    zs = sorted(zs)

    counts = np.zeros((len(xs) - 1, len(ys) - 1, len(zs) - 1), dtype=np.uint64)
    for x in range(len(xs) - 1):
        for y in range(len(ys) - 1):
            for z in range(len(zs) - 1):
                counts[x, y, z] = (
                    (xs[x+1] - xs[x]) * (ys[y+1] - ys[y]) * (zs[z+1] - zs[z])
                )

    new_rules = []
    for [(x1, x2), (y1, y2), (z1, z2)], state in rules:
        new_rules.append((
            [
                (xs.index(x1), xs.index(x2+1)),
                (ys.index(y1), ys.index(y2+1)),
                (zs.index(z1), zs.index(z2+1))
            ], state
        ))

    return new_rules, counts, (len(xs) - 1, len(ys) - 1, len(zs) - 1)


def reboot(filename, initialize=True):
    rules = parse_input(filename)
    if initialize:
        rules = [rule for rule in rules if initialization_rule(rule)]

    rules, counts, sizes = voxelise(rules)

    grid = np.zeros(sizes, dtype=bool)
    for [(x1, x2), (y1, y2), (z1, z2)], state in rules:
        grid[x1:x2, y1:y2, z1:z2] = state

    return np.sum(grid * counts)


assert reboot(os.path.join(currentdir, "test_input1.txt")) == 39
assert reboot(os.path.join(currentdir, "test_input2.txt")) == 590784
print("Part 1: ", reboot(os.path.join(currentdir, "input.txt")))

assert reboot(os.path.join(currentdir, "test_input3.txt")) == 474140
assert reboot(os.path.join(currentdir, "test_input3.txt"), False) == 2758514936282235
print("Part 2: ", reboot(os.path.join(currentdir, "input.txt"), False))
