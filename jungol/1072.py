n, m = map(int, input().split())
items = list(map(int, input().split()))

max_size = -12315132
for i in range(n - m + 1):
    sum_result = sum(items[i:i+m])
    max_size = max(max_size, sum_result)

print(max_size)