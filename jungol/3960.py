n = int(input())
pos = sorted(int(input()) for _ in range(n))
max_explosion_count = 0

for start in range(n):
    # 오른쪽
    right, width_r = start, 1
    while True:
        nxt = right
        while nxt + 1 < n and pos[nxt + 1] - pos[right] <= width_r:
            nxt += 1
        if right == nxt:
            break
        right = nxt
        width_r += 1

    left, width_l = start, 1
    while True:
        nxt = left
        while nxt - 1 >= 0 and pos[left] - pos[nxt - 1] <= width_l:
            nxt -= 1
        if left == nxt:
            break
        left = nxt
        width_l += 1

    max_explosion_count = max(max_explosion_count, right - left + 1)

print(max_explosion_count)