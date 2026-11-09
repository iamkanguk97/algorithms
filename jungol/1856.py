# https://jungol.co.kr/problem/1856?cursor=IjYiLDIsMQ==

n, m = map(int, input().split())
arr = []

for i in range(n):
    temp = [i * m + k for k in range(1, m + 1)]
    if i % 2 == 1:
        temp = temp[::-1]
    arr.append(temp)

for i in range(n):
    for j in range(m):
        print(arr[i][j], end=' ')
    print()