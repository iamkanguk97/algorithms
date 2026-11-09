# https://jungol.co.kr/problem/1307?cursor=IjYiLDIsNg==

n = int(input())

arr, temp = [], []
for i in range(n * n - 1, -1, -1):
    temp.append(chr((ord('A') + i % 26)))
    if i % n == 0:
        arr.append(temp)
        temp = []

for i in range(n):
    for j in range(n):
        print(arr[j][i], end=' ')
    print()