A, B, C, n = map(int, input().split())

def solution():
    for a in range(0, n // A + 1):
        for b in range(0, n // B + 1):
            for c in range(0, n // C + 1):
                if A * a + B * b + C * c == n:
                    print(1)
                    return

    print(0)

solution()