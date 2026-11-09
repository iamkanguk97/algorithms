# https://jungol.co.kr/problem/1339?cursor=IjYiLDIsOQ==

# <n = 11>
# Z (0)
# A Q (1)
# B R J (2)
# C S K E (3)
# D T L F B (4)
# E U M G C A (5 = half)
# F V N H D (6)
# G W O I (7)
# H X P (8)
# I Y (9)
# J (10)

def next_chr(ch):
    return chr(ord('A') + (ord(ch) - ord('A') + 1) % 26)


n = int(input())

if n < 0 or n > 100 or n % 2 == 0:
    print("INPUT ERROR")
    exit(0)

half = n // 2
arr = [['_'] * (half + 1) for _ in range(n)]
ch = 'A'
arr[half][half] = ch

for i in range(half):
    for j in range(i, -1, -1):
        ch = next_chr(ch)
        arr[half-1-j][half-1-i] = ch

    ch = next_chr(ch)
    arr[half][half-i-1] = ch

    for j in range(i+1):
        ch = next_chr(ch)
        arr[half+1+j][half-1-i] = ch

for i in range(n):
    print(*arr[i][:min(i, n-1-i)+1])