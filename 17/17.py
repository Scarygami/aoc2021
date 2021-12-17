tx1 = 139
tx2 = 187
ty1 = -148
ty2 = -89

min_dx = 17
max_dx = 188
min_dy = -148
max_dy = 147
max_y = 0

solutions = []
for dx in range(min_dx, max_dx + 1):
    for dy in range(min_dy, max_dy + 1):
        x = 0
        y = 0
        ndx = dx
        ndy = dy
        while x <= tx2 and y >= ty1:
            x = x + ndx
            y = y + ndy
            if y > max_y:
                max_y = y
            if ndx > 0:
                ndx = ndx - 1
            ndy = ndy - 1
            if x >= tx1 and x <= tx2 and y >= ty1 and y <= ty2:
                solutions.append((dx, dy))
                break

print("Part 1:", max_y)
print("Part 2:", len(solutions))
