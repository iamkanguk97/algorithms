N,M = map(int,input().split())
checked = [False] * (N + 1)

def bt(arr):
    if len(arr) == M:
        print(*arr)
        return

    for num in range(1, N + 1):
        if checked[num]:
            continue
        checked[num] = True
        arr.append(num)
        bt(arr)
        arr.pop()
        checked[num] = False

bt([])