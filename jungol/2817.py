# https://jungol.co.kr/problem/2817?cursor=IjYiLDgsMw==

def lotto(start, picked):
    if len(picked) == 6:
        print(*picked)
        return
    for idx in range(start, k):
        picked.append(s[idx])
        lotto(idx + 1, picked)
        picked.pop()

arr = list(map(int, input().split()))
k, s = arr[0], arr[1:]

lotto(0, [])