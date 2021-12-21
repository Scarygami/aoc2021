from itertools import product


def practice_game(pos):
    dice = 1
    rolls = 0
    score = [0, 0]
    player = 0

    while score[0] < 1000 and score[1] < 1000:
        moves = 3 * dice + 3
        pos[player] = (pos[player] + moves - 1) % 10 + 1
        score[player] = score[player] + pos[player]
        dice = (dice + 2) % 100 + 1
        player = 1 - player
        rolls = rolls + 3

    return rolls * score[player]


quantum_options = list(product([1, 2, 3], repeat=3))
sums = set([sum(option) for option in quantum_options])
dice_options = dict(zip(
    sums,
    [len([1 for option in quantum_options if sum(option) == s]) for s in sums]
))


def quantum_game(pos, score, player=0):
    if score[0] >= 21:
        return [1, 0]
    if score[1] >= 21:
        return [0, 1]

    wins = [0, 0]
    for dice in dice_options:
        new_pos = pos.copy()
        new_score = score.copy()
        new_pos[player] = (new_pos[player] + dice - 1) % 10 + 1
        new_score[player] = new_score[player] + new_pos[player]
        wins0, wins1 = quantum_game(new_pos, new_score, 1 - player)
        wins[0] = wins[0] + dice_options[dice] * wins0
        wins[1] = wins[1] + dice_options[dice] * wins1

    return wins


assert practice_game([4, 8]) == 739785
print("Part 1: ", practice_game([3, 10]))

assert max(quantum_game([4, 8], [0, 0])) == 444356092776315
print("Part 2: ", max(quantum_game([3, 10], [0, 0])))
