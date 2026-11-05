# https://jungol.co.kr/problem/5934?cursor=IjYiLDQsMQ==

n = int(input())

if n <= 0 or n > 100 or n % 2 == 0:
    print("INPUT ERROR!")
else:
    for i in range(0, n // 2 + 1):
        print(' ' * i + '*' * (n // 2 + 1 - i))
    for j in range(n // 2 + 1, n):
        print(' ' * (n // 2) + '*' * (j - (n // 2 - 1)))