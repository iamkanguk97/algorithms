# 1번부터 N번까지 N개 맛이 있는 아이스크림
# 서로 두가지 맛 아이스크림 -> 환상조합
# 아이스크림 본래의 맛을 느끼고 싶음..

# 1 2 3 4 5
# 1 2
# 3 4
# 1 3

# 1 4 5
# 2 3 5
# 2 4 5

n, m = map(int, input().split())
flavor = [[False] * (n + 1) for _ in range(n + 1)]

for _ in range(m):
    a, b = map(int, input().split())
    flavor[a][b] = True
    flavor[b][a] = True

count = 0

for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        if flavor[i][j]:
            continue
        for k in range(j + 1, n + 1):
            if flavor[i][k] or flavor[j][k]:
                continue
            count += 1

print(count)