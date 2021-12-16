import os

currentdir = os.path.dirname(os.path.abspath(__file__))

hex2bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

SUM = 0
PROD = 1
MIN = 2
MAX = 3
LIT = 4
GT = 5
LT = 6
EQ = 7


class Packet:
    def __init__(self, version, type, value, children):
        self.version = version
        self.type = type
        self.value = value
        self.children = children

    def __repr__(self):
        return f"{self.version} - {self.type} - {self.value} - {len(self.children)}"

    @property
    def total_version(self):
        sum = self.version
        for child in self.children:
            sum = sum + child.total_version

        return sum

    @property
    def result(self):
        if self.type == LIT:
            return self.value

        if self.type == SUM:
            return sum(child.result for child in self.children)

        if self.type == PROD:
            prod = 1
            for child in self.children:
                prod = prod * child.result
            return prod

        if self.type == MIN:
            return min(child.result for child in self.children)

        if self.type == MAX:
            return max(child.result for child in self.children)

        if self.type == LT:
            if self.children[0].result < self.children[1].result:
                return 1
            return 0

        if self.type == GT:
            if self.children[0].result > self.children[1].result:
                return 1
            return 0

        if self.type == EQ:
            if self.children[0].result == self.children[1].result:
                return 1
            return 0

        return None


def decode(bin, count=None):
    packets = []
    i = 0

    while i < len(bin) and (not count or len(packets) < count):
        if len(bin[i:]) < 3:
            break
        version = int(bin[i:i+3], 2)
        i = i + 3

        if len(bin[i:]) < 3:
            break
        type = int(bin[i:i+3], 2)
        i = i + 3
        if type == LIT:
            mode = "D"
        else:
            mode = "I"

        if mode == "I":
            if len(bin[i:]) < 1:
                break
            length_type = int(bin[i], 2)
            i = i + 1

            if length_type == 0:
                if len(bin[i:]) < 15:
                    break
                length = int(bin[i:i+15], 2)
                i = i + 15
                children, _ = decode(bin[i:i+length])
                i = i + length
            else:
                if len(bin[i:]) < 11:
                    break
                length = int(bin[i:i+11], 2)
                i = i + 11
                children, new_i = decode(bin[i:], length)
                i = i + new_i

            packets.append(Packet(version, type, 0, children))

        if mode == "D":
            value = 0
            while bin[i] == "1":
                value = value * 16 + int(bin[i+1:i+5], 2)
                i = i + 5
            value = value * 16 + int(bin[i+1:i+5], 2)
            i = i + 5

            packets.append(Packet(version, type, value, []))

    return packets, i


def parse_input(filename):
    with open(filename) as f:
        hex = f.read().splitlines()[0]
        bin = "".join(hex2bin[h] for h in hex)

    calculation, _ = decode(bin)
    return calculation[0]


def part1(filename):
    calculation = parse_input(filename)
    return calculation.total_version


def part2(filename):
    calculation = parse_input(filename)
    return calculation.result


test = parse_input(os.path.join(currentdir, "test_input01.txt"))
assert test.version == 6
assert test.type == 4
assert test.value == 2021

test = parse_input(os.path.join(currentdir, "test_input02.txt"))
assert test.version == 1
assert test.type == 6
assert test.children[0].value == 10
assert test.children[1].value == 20

test = parse_input(os.path.join(currentdir, "test_input03.txt"))
assert test.version == 7
assert test.type == 3
assert test.children[0].value == 1
assert test.children[1].value == 2
assert test.children[2].value == 3

assert part1(os.path.join(currentdir, "test_input04.txt")) == 16
assert part1(os.path.join(currentdir, "test_input05.txt")) == 12
assert part1(os.path.join(currentdir, "test_input06.txt")) == 23
assert part1(os.path.join(currentdir, "test_input07.txt")) == 31

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input08.txt")) == 3
assert part2(os.path.join(currentdir, "test_input09.txt")) == 54
assert part2(os.path.join(currentdir, "test_input10.txt")) == 7
assert part2(os.path.join(currentdir, "test_input11.txt")) == 9
assert part2(os.path.join(currentdir, "test_input12.txt")) == 1
assert part2(os.path.join(currentdir, "test_input13.txt")) == 0
assert part2(os.path.join(currentdir, "test_input14.txt")) == 0
assert part2(os.path.join(currentdir, "test_input15.txt")) == 1

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
