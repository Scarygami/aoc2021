import os

currentdir = os.path.dirname(os.path.abspath(__file__))

BINGOS = [
    [0, 1, 2, 3, 4],
    [5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 21, 23, 24],
    [0, 5, 10, 15, 20],
    [1, 6, 11, 16, 21],
    [2, 7, 12, 17, 22],
    [3, 8, 13, 18, 23],
    [4, 9, 14, 19, 24],
]


class Board:
    def __init__(self, lines):
        board = []
        for line in lines:
            board.extend(line.split(" "))
        self.board = [int(n) for n in board if n != ""]

    def __repr__(self):
        return ",".join(str(n) for n in self.board)

    def update(self, number):
        self.board = [-1 if n == number else n for n in self.board]

    def bingo(self):
        for check in BINGOS:
            count = sum(self.board[i] for i in check)
            if count == -5:
                return True

        return False

    def score(self):
        return sum(n for n in self.board if n > 0)


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        boards = []
        numbers = [int(n) for n in lines[0].split(",")]
        for i in range(2, len(lines), 6):
            boards.append(Board(lines[i : i + 5]))

    return numbers, boards


def part1(filename):
    numbers, boards = parse_input(filename)

    for number in numbers:
        for board in boards:
            board.update(number)
            if board.bingo():
                return number * board.score()


def part2(filename):
    numbers, boards = parse_input(filename)

    for number in numbers:
        for board in boards:
            board.update(number)

        if len(boards) == 1 and boards[0].bingo():
            return number * board.score()

        boards = [board for board in boards if not board.bingo()]


assert part1(os.path.join(currentdir, "test_input.txt")) == 4512

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 1924

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
