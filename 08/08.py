import os

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        displays = []
        for line in lines:
            patterns, output = line.split(' | ')
            displays.append(
                (
                    [set(p) for p in patterns.split(' ')],
                    [set(o) for o in output.split(' ')]
                )
            )

    return displays


def part1(filename):
    displays = parse_input(filename)
    count = 0
    for display in displays:
        for output in display[1]:
            if len(output) in [2, 3, 4, 7]:
                count = count + 1

    return count


def decode_input(patterns):
    zero = None
    one = frozenset([p for p in patterns if len(p) == 2][0])
    two = None
    three = None
    four = frozenset([p for p in patterns if len(p) == 4][0])
    five = None
    six = None
    seven = frozenset([p for p in patterns if len(p) == 3][0])
    eight = frozenset([p for p in patterns if len(p) == 7][0])
    nine = None

    patterns.remove(one)
    patterns.remove(four)
    patterns.remove(seven)
    patterns.remove(eight)

    """
     0000
    1    2
    1    2
     3333
    4    5
    4    5
     6666
    """
    segments = ['', '', '', '', '', '', '']

    # Segment 0 = Seven - One
    segments[0] = list(seven - one)[0]

    # Segment 6 = Nine - Four - Segment 0
    for p in patterns:
        if four.issubset(p) and segments[0] in p and len(p) == 6:
            nine = frozenset(p)
            patterns.remove(nine)
            segments[6] = list(nine - four - set([segments[0]]))[0]
            break

    # Segment 4 = Eight - Nine
    segments[4] = list(eight - nine)[0]

    # Segment 3 = Eight - Zero
    for p in patterns:
        if p.issubset(eight) and one.issubset(p) and len(p) == 6:
            zero = frozenset(p)
            patterns.remove(zero)
            segments[3] = list(eight - zero)[0]
            break

    # Segment 2 = Two - [0,3,4,6]
    tmp = set([segments[0], segments[3], segments[4], segments[6]])
    for p in patterns:
        if tmp.issubset(p) and len(p) == 5:
            two = frozenset(p)
            patterns.remove(two)
            segments[2] = list(two - tmp)[0]
            break

    # Segment 5 = Three - [0,2,3,6]
    tmp = set([segments[0], segments[2], segments[3], segments[6]])
    for p in patterns:
        if tmp.issubset(p) and one.issubset(p) and len(p) == 5:
            three = frozenset(p)
            patterns.remove(three)
            segments[5] = list(three - tmp)[0]
            break

    # Segment 1 = Zero - [0,2,4,5,6]
    tmp = set([segments[0], segments[2], segments[4], segments[5], segments[6]])
    segments[1] = list(zero - tmp)[0]

    five = frozenset([segments[0], segments[1], segments[3], segments[5], segments[6]])
    six = frozenset(eight - set(segments[2]))

    decoder = dict()
    decoder[zero] = 0
    decoder[one] = 1
    decoder[two] = 2
    decoder[three] = 3
    decoder[four] = 4
    decoder[five] = 5
    decoder[six] = 6
    decoder[seven] = 7
    decoder[eight] = 8
    decoder[nine] = 9

    return decoder


def part2(filename):
    displays = parse_input(filename)
    sum = 0
    for display in displays:
        decoder = decode_input(display[0])

        output = [decoder.get(frozenset(o), -1) for o in display[1]]

        sum = sum + output[3] + 10 * output[2] + 100 * output[1] + 1000 * output[0]

    return sum


assert part1(os.path.join(currentdir, "test_input1.txt")) == 26

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input2.txt")) == 5353
assert part2(os.path.join(currentdir, "test_input1.txt")) == 61229

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
