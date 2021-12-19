import numpy as np


def prepare_rotations():
    rot_x = np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ])

    rot_y = np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ])

    rot_z = np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])

    rotation_check = set()
    rotations = []
    identity = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    rotations.append(identity)
    rotation_check.add(tuple(identity.flatten()))
    for rot in rotations:
        tmp = rot.copy()
        for _ in range(4):
            tmp = rot_x @ tmp
            flat = tuple(tmp.flatten())
            if flat in rotation_check:
                continue
            rotations.append(tmp)
            rotation_check.add(flat)

        tmp = rot.copy()
        for _ in range(4):
            tmp = rot_y @ tmp
            flat = tuple(tmp.flatten())
            if flat in rotation_check:
                continue
            rotations.append(tmp)
            rotation_check.add(flat)

        tmp = rot.copy()
        for _ in range(4):
            tmp = rot_z @ tmp
            flat = tuple(tmp.flatten())
            if flat in rotation_check:
                continue
            rotations.append(tmp)
            rotation_check.add(flat)

    return rotations
