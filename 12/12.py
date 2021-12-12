import os

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    paths = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            paths.append(tuple(line.split("-")))

    return paths


def part1(filename):
    paths = parse_input(filename)
    routes = []
    frontier = [['start']]
    while len(frontier) > 0:
        new_frontier = []
        for route in frontier:
            node = route[-1]
            nexts = [path[1] for path in paths if path[0] == node]
            nexts.extend(path[0] for path in paths if path[1] == node)

            for next in nexts:
                if next.lower() == next and next in route:
                    continue

                new_route = route.copy()
                new_route.append(next)

                if next == 'end':
                    routes.append(new_route)
                else:
                    new_frontier.append(new_route)

        frontier = new_frontier

    return len(routes)


def part2(filename):
    paths = parse_input(filename)
    routes = []
    frontier = [(['start'], False)]
    while len(frontier) > 0:
        new_frontier = []
        for (route, doublevisit) in frontier:
            node = route[-1]
            nexts = [path[1] for path in paths if path[0] == node]
            nexts.extend(path[0] for path in paths if path[1] == node)

            for next in nexts:
                if next == 'start':
                    continue

                new_doublevisit = doublevisit
                if next.lower() == next and next in route:
                    if new_doublevisit:
                        continue
                    new_doublevisit = True

                new_route = route.copy()
                new_route.append(next)

                if next == 'end':
                    routes.append(new_route)
                else:
                    new_frontier.append((new_route, new_doublevisit))

        frontier = new_frontier

    return len(routes)


assert part1(os.path.join(currentdir, "test_input1.txt")) == 10
assert part1(os.path.join(currentdir, "test_input2.txt")) == 19
assert part1(os.path.join(currentdir, "test_input3.txt")) == 226

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))


assert part2(os.path.join(currentdir, "test_input1.txt")) == 36
assert part2(os.path.join(currentdir, "test_input2.txt")) == 103
assert part2(os.path.join(currentdir, "test_input3.txt")) == 3509

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
