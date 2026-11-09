# https://jungol.co.kr/problem/1314?cursor=IjYiLDIsNw==

n = int(input())
arr = []

for i in range(n):
    temp = [ord('A') + (i * n + k) % 26 for k in range(n)]
    if i % 2 == 1:
        temp = temp[::-1]
    arr.append(temp)

for i in range(n):
    for j in range(n):
        print(chr(arr[j][i]), end=' ')
    print()