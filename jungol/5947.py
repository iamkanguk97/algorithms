# https://jungol.co.kr/problem/5947?cursor=IjYiLDQsNQ==

n = int(input())

if n < 1 or n > 50 or n % 2 == 0:
    print("INPUT ERROR!")
    exit(0)

for i in range(1, n + 1):
    count = min(i, n + 1 - i)
    print(' '.join(map(str, list(range(1, count + 1)))))