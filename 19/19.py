import os
import numpy as np
from rotations import prepare_rotations

currentdir = os.path.dirname(os.path.abspath(__file__))
ROTATIONS = prepare_rotations()


class Scanner():
    def __init__(self, data):
        self.orientation = None
        self.location = None
        self.beacons = []
        self.aligned = False
        self.checked = False
        for line in data:
            self.beacons.append(np.array(
                [int(c) for c in line.split(',')]
            ))

    @property
    def aligned_beacons(self):
        if not self.aligned:
            return None

        return [
            (self.orientation @ beacon) + self.location for beacon in self.beacons
        ]


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        data = []
        scanners = []
        for line in lines[1:]:
            if line == "":
                scanners.append(Scanner(data))
                data = []
                continue

            if line[:3] == "---":
                continue

            data.append(line)

        if len(data) > 0:
            scanners.append(Scanner(data))

    return scanners


def align(scanner1, scanner2):
    if not scanner1.aligned:
        return False
    if scanner2.aligned:
        return True

    # Quick check via relative distances to skip impossible matches
    base_beacons = scanner1.aligned_beacons
    base_distances = []
    for beacon1 in base_beacons:
        base_distances.extend(
            np.linalg.norm(beacon2-beacon1) for beacon2 in base_beacons
        )

    test_beacons = scanner2.beacons
    test_distances = []
    for beacon1 in test_beacons:
        test_distances.extend(
            np.linalg.norm(beacon2-beacon1) for beacon2 in test_beacons
        )

    matches = [
        distance for distance in base_distances if distance in test_distances
    ]

    if len(matches) < 144:
        return False

    for rotation in ROTATIONS:
        test_beacons = [
            rotation @ beacon for beacon in scanner2.beacons
        ]
        for base_beacon in base_beacons:
            for test_beacon in test_beacons:
                delta = test_beacon - base_beacon
                compare_beacons = [
                    tuple(beacon + delta) for beacon in base_beacons
                ]
                matched_beacons = [
                    beacon for beacon in test_beacons
                    if tuple(beacon) in compare_beacons
                ]
                if len(matched_beacons) >= 12:
                    scanner2.aligned = True
                    scanner2.orientation = rotation
                    scanner2.location = -delta
                    return True

    return False


def max_distance(scanners):
    max = 0
    for scanner1 in scanners:
        for scanner2 in scanners:
            distance = np.sum(np.abs(scanner2.location - scanner1.location))
            if distance > max:
                max = distance

    return max


def align_scanners(filename):
    print("Starting scanner alignment...")
    scanners = parse_input(filename)
    scanners[0].orientation = ROTATIONS[0]
    scanners[0].location = np.array([0, 0, 0])
    scanners[0].aligned = True

    while any([not scanner.aligned for scanner in scanners]):
        base_scanners = [
            scanner for scanner in scanners
            if scanner.aligned and not scanner.checked
        ]
        test_scanners = [
            scanner for scanner in scanners
            if not scanner.aligned
        ]
        print(
            'Aligned: ', len(scanners) - len(test_scanners),
            ' / Unaligned: ', len(test_scanners)
        )
        base_scanner = base_scanners[0]
        for test_scanner in test_scanners:
            align(base_scanner, test_scanner)

        base_scanner.checked = True

    beacons = []
    for scanner in scanners:
        beacons.extend(
            tuple(beacon) for beacon in scanner.aligned_beacons
        )
    beacons = set(beacons)

    return len(beacons), max_distance(scanners)


beacons, distance = align_scanners(os.path.join(currentdir, 'test_input.txt'))
assert beacons == 79
assert distance == 3621

beacons, distance = align_scanners(os.path.join(currentdir, 'input.txt'))
print("Part 1: ", beacons)
print("Part 2: ", distance)
