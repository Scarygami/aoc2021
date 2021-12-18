import os
from math import floor, ceil

currentdir = os.path.dirname(os.path.abspath(__file__))


class Number:
    def __init__(self, value=None, parent=None):
        self.value = value
        self.parent = parent
        self.children = []

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.children[0]},{self.children[1]}]"

    @property
    def depth(self):
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @property
    def leaves(self):
        if self.value is not None:
            return [self]
        leaves = self.children[0].leaves
        leaves.extend(self.children[1].leaves)
        return leaves

    @property
    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.children[0].magnitude + 2 * self.children[1].magnitude

    def find_explode(self):
        if len(self.children) > 0:
            if self.depth == 4:
                return self
            explode = self.children[0].find_explode()
            if explode is None:
                explode = self.children[1].find_explode()
            return explode

        return None

    def copy(self, parent=None):
        node = Number(self.value, parent)
        if len(self.children) > 0:
            node.children.append(self.children[0].copy(node))
            node.children.append(self.children[1].copy(node))
        return node


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        numbers = [parse_number(line) for line in lines]

    return numbers


def parse_number(input, parent=None):
    if type(input) is str:
        input = eval(input)

    if type(input) is list:
        node = Number(None, parent)
        node.children.append(parse_number(input[0], node))
        node.children.append(parse_number(input[1], node))
        return node

    return Number(input, parent)


def reduce_step(number):
    explode = number.find_explode()
    leaves = number.leaves
    if explode is not None:
        i = leaves.index(explode.children[0])
        if i > 0:
            leaves[i-1].value = leaves[i-1].value + leaves[i].value
        if i + 2 < len(leaves):
            leaves[i+2].value = leaves[i+2].value + leaves[i+1].value
        explode.value = 0
        explode.children = []
        return number

    splits = [leaf for leaf in leaves if leaf.value >= 10]
    if len(splits) > 0:
        split = splits[0]
        s1 = int(floor(split.value / 2))
        s2 = int(ceil(split.value / 2))
        split.value = None
        split.children.append(Number(s1, split))
        split.children.append(Number(s2, split))
        return number

    return number


def reduce(number):
    before = str(number)
    while before != str(reduce_step(number)):
        before = str(number)
    return number


def add(number1, number2):
    root = Number(None, None)
    number1 = number1.copy(root)
    number2 = number2.copy(root)
    root.children = [number1, number2]
    return reduce(root)


def add_all(numbers):
    sum = numbers[0]
    for number in numbers[1:]:
        sum = add(sum, number)
    return sum


def find_maximum_magnitude(numbers):
    max = 0
    for i1 in range(len(numbers)):
        for i2 in range(len(numbers)):
            if i1 != i2:
                sum = add(numbers[i1], numbers[i2])
                if sum.magnitude > max:
                    max = sum.magnitude

    return max


numbers = parse_input(os.path.join(currentdir, "test_input1.txt"))
assert(str(add_all(numbers)) == "[[[[1,1],[2,2]],[3,3]],[4,4]]")

numbers = parse_input(os.path.join(currentdir, "test_input2.txt"))
assert(str(add_all(numbers)) == "[[[[3,0],[5,3]],[4,4]],[5,5]]")

numbers = parse_input(os.path.join(currentdir, "test_input3.txt"))
assert(str(add_all(numbers)) == "[[[[5,0],[7,4]],[5,5]],[6,6]]")

numbers = parse_input(os.path.join(currentdir, "test_input4.txt"))
assert(str(add_all(numbers)) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")

numbers = parse_input(os.path.join(currentdir, "test_input5.txt"))
sum = add_all(numbers)
assert(str(sum) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
assert(sum.magnitude == 4140)
assert(find_maximum_magnitude(numbers) == 3993)

numbers = parse_input(os.path.join(currentdir, "input.txt"))
sum = add_all(numbers)
print("Part 1: ", sum.magnitude)
print("Part 2: ", find_maximum_magnitude(numbers))
