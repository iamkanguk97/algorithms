def dice1(depth, n):
    if depth == n + 1:
        print(*arr)
        return

    for i in range(1, 7):
        arr.append(i)
        dice1(depth + 1, n)
        arr.pop()

def dice2(depth, n):
    if depth == n + 1:
        print(*arr)
        return

    start = arr[-1] if arr else 1
    for i in range(start, 7):
        arr.append(i)
        dice2(depth + 1, n)
        arr.pop()

def dice3(depth, n):
    if depth == n + 1:
        print(*arr)
        return

    for i in range(1, 7):
        if i in arr:
            continue
        arr.append(i)
        dice3(depth + 1, n)
        arr.pop()

n, m = map(int, input().split())
arr = []

if m == 1:
    dice1(1, n)
elif m == 2:
    dice2(1, n)
else:
    dice3(1, n)