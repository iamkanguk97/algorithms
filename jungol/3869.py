n = int(input())
bong = sorted(int(input()) for _ in range(n))

min_cost = 124151523125123
for a in range(84):
    tmp = 0
    for b in bong:
        if b < a:
            tmp += (a - b) ** 2
        if b > a + 17:
            tmp += (b - (a + 17)) ** 2
    min_cost = min(tmp, min_cost)

print(min_cost)