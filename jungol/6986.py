import math

n = int(input())
arr = list(map(int, input().split()))

maxVal = -1425151521
minVal = 12315123211

for i in range(1, n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            cost = math.prod(arr[0:i]) + math.prod(arr[i:j]) + math.prod(arr[j:k]) + math.prod(arr[k:n])
            maxVal = max(maxVal, cost)
            minVal = min(minVal, cost)

print(maxVal)
print(minVal)