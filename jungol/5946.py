# https://jungol.co.kr/problem/5946?cursor=IjYiLDQsNA==

n = int(input())

if n < 0 or n > 50 or n % 2 == 0:
    print("INPUT ERROR!")
    exit(0)

cnt = n * 2 - 1

for i in range(n):
    lst = [i] * cnt
    cnt -= 2
    print(' ' * (i * 2) + (' '.join(map(str, lst))) + ' ' * (i * 2))