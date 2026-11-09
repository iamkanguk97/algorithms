# https://jungol.co.kr/problem/5932?cursor=IjYiLDIsNA==

n = int(input())

for i in range(1, n + 1):
    arr = list(range(1, n + 1))
    if i % 2 == 0:
        arr = sorted(arr, reverse=True)
    print(*arr)