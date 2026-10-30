import sys
input = sys.stdin.readline

###### Claude Code의 풀이.. 깔끔하다!

n, q = map(int, input().split())
prefix = [[0, 0, 0]]

for _ in range(n):
    row = prefix[-1][:]
    row[int(input()) - 1] += 1
    prefix.append(row)

result = []
for _ in range(q):
    a, b = map(int, input().split())
    result.append(' '.join(str(prefix[b][k] - prefix[a - 1][k]) for k in range(3)))

print('\n'.join(result))

###### 나의 X같은 풀이... 그래도 풀었다..

# cow_ids = [int(input()) for _ in range(n)]
#
# prefix_h = [0] * (n + 1)
# prefix_g = [0] * (n + 1)
# prefix_j = [0] * (n + 1)
#
# for i in range(1, n + 1):
#     if cow_ids[i - 1] == 1:
#         prefix_h[i] = prefix_h[i - 1] + 1
#         prefix_g[i] = prefix_g[i - 1]
#         prefix_j[i] = prefix_j[i - 1]
#     elif cow_ids[i - 1] == 2:
#         prefix_g[i] = prefix_g[i - 1] + 1
#         prefix_h[i] = prefix_h[i - 1]
#         prefix_j[i] = prefix_j[i - 1]
#     else:
#         prefix_j[i] = prefix_j[i - 1] + 1
#         prefix_h[i] = prefix_h[i - 1]
#         prefix_g[i] = prefix_g[i - 1]
#
# result = []
# for _ in range(q):
#     a, b = map(int, input().split())
#     result.append([prefix_h[b] - prefix_h[a - 1], prefix_g[b] - prefix_g[a - 1], prefix_j[b] - prefix_j[a - 1]])
#
# for r in result:
#     print(*r, sep=' ')

