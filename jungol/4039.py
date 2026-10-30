n = int(input())
arr = list(map(int, input().split()))

suffix_min = [0] * n
suffix_min[n - 1] = arr[n - 1]
for i in range(n -2, -1, -1):
    suffix_min[i] = min(arr[i], suffix_min[i + 1])

total = sum(arr)
result = -1
max_ks = []

for k in range(1, n-1):
    total -= arr[k-1]
    avg_result = (total - suffix_min[k]) / (n - k - 1)

    if avg_result >= result:
        if avg_result > result:
            result = avg_result
            max_ks = []
        max_ks.append(k)

print('\n'.join(map(str, max_ks)))