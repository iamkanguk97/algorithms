# https://jungol.co.kr/problem/1304?cursor=IjYiLDIsMg==

n = int(input())

for i in range(1, n+1):
    print(*list(range(i, n * n + 1, n)))