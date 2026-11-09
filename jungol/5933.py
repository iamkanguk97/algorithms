# https://jungol.co.kr/problem/5933?cursor=IjYiLDIsNQ==

n = int(input())

for i in range(1, n+1):
    print(*list(range(i, i * n + 1, i)))