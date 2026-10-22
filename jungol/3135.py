n = int(input())
arr = list(map(int, input().split()))
nu_hab = [0] * (n + 1)

for i in range(1, n + 1):
    nu_hab[i] = nu_hab[i - 1] + arr[i - 1]

q = int(input())
answer = []

for _ in range(q):
    s, e = map(int, input().split())
    answer.append(nu_hab[e] - nu_hab[s - 1])

for ans in answer:
    print(ans)