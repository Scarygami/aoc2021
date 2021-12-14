import os
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        template = lines[0]
        rules = {}
        for line in lines[2:]:
            pair, insert = line.split(" -> ")
            rules[pair] = insert

    return template, rules


def transform1(template, rules):
    new_template = [template[0]]

    for i in range(len(template) - 1):
        insert = rules[template[i:i+2]]
        new_template.append(insert)
        new_template.append(template[i+1])

    return ''.join(new_template)


def part1(filename, steps=10):
    template, rules = parse_input(filename)

    for _ in range(steps):
        template = transform1(template, rules)

    counts = {}
    for char in template:
        if char not in counts:
            counts[char] = template.count(char)

    return max(counts.values()) - min(counts.values())


def transform2(pairs, counts, rules):
    new_pairs = defaultdict(int)
    for pair, count in pairs.items():
        insert = rules[pair]
        new_pairs[pair[0] + insert] += count
        new_pairs[insert + pair[1]] += count
        counts[insert] += count

    return new_pairs, counts


def part2(filename, steps=40):
    template, rules = parse_input(filename)
    pairs = defaultdict(int)
    counts = defaultdict(int)
    for i in range(len(template) - 1):
        pairs[template[i] + template[i+1]] += 1
        counts[template[i]] += 1
    counts[template[-1]] += 1

    for _ in range(steps):
        pairs, counts = transform2(pairs, counts, rules)

    return max(counts.values()) - min(counts.values())


assert part1(os.path.join(currentdir, "test_input.txt")) == 1588

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt"), 10) == 1588
assert part2(os.path.join(currentdir, "test_input.txt"), 40) == 2188189693529

print("Part 2: ", part2(os.path.join(currentdir, "input.txt"), 40))
