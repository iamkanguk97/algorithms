N,M = map(int, input().split())

def bt(picked):
    if len(picked) == M:
        print(*picked)
        return

    for num in range(1, N + 1):
        picked.append(num)
        bt(picked)
        picked.pop()

bt([])