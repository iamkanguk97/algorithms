n, k = map(int, input().split())
temps = list(map(int, input().split()))

# 슬라이딩 윈도우 풀이
window = sum(temps[:k])
best = window

for i in range(k, n):
    window += temps[i] - temps[i - k]
    best = max(best, window)

print(best)

# 누적합 풀이
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + temps[i]

print(max(prefix[i + k] - prefix[i] for i in range(n - k + 1)))


# 망한 나의 풀이
# prefix = [0] * (n - k + 2)
# prefix[1] = sum(temps[:k])
#
# for idx in range(2, n - k + 2):
#     prefix[idx] = prefix[idx - 1] - temps[idx - 2] + temps[idx + k - 2]
#
# # print(prefix)
# print(max(prefix[1:]))