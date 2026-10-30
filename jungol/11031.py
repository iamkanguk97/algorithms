import sys
input = sys.stdin.readline

n, b, a = map(int, input().split())
arr = sorted(list(map(int, input().split())))

prefix_full = [0] * (n + 1)
prefix_half = [0] * (n + 1)

for i in range(n):
    prefix_full[i + 1] = prefix_full[i] + arr[i]
    prefix_half[i + 1] = prefix_half[i] + arr[i] // 2


answer = 0
for k in range(1, n + 1):
    coupons = min(a, k)
    cost = prefix_full[k - coupons] + (prefix_half[k] - prefix_half[k - coupons])
    if cost > b:
        break
    answer = k

print(answer)