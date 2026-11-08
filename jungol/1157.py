# https://jungol.co.kr/problem/1157?cursor=IjYiLDcsMg==

n = int(input())
arr = list(map(int, input().split()))

for i in range(n-1):
    for j in range(n-1-i):
        if arr[j] > arr[j+1]:
            temp = arr[j]
            arr[j] = arr[j+1]
            arr[j+1] = temp
    print(*arr)