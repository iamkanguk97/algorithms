# https://jungol.co.kr/problem/1329?cursor=IjYiLDQsMg==

n = int(input())

if n <= 0 or n > 100 or n % 2 == 0:
    print("INPUT ERROR!")
else:
    half = n // 2
    for i in range(half + 1):
        print(' ' * i + '*' * (2 * i + 1))
    for j in range(half-1, -1, -1):
        print(' ' * j + '*' * (2 * j + 1))