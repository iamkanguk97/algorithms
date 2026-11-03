n, m = map(int, input().split())
arr = list(map(int, input().split()))
used = [False] * n

def bt(seq):
    if len(seq) == m:
        print(*seq)
        return

    for i in range(n):
        if used[i]:
            continue
        used[i] = True
        seq.append(arr[i])
        bt(seq)
        seq.pop()
        used[i] = False

bt([])