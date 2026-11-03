def bt(arr):
    if len(arr) == n:
        if sum(arr) == m:
            print(*arr)
        return

    for i in range(1, 7):
        arr.append(i)
        bt(arr)
        arr.pop()

n, m = map(int, input().split())
bt([])