# https://jungol.co.kr/problem/5945?cursor=IjYiLDQsMw==

n = int(input())

if n < 1 or n > 50 or n % 2 == 0:
    print("INPUT ERROR!")
    exit(0)

startNumber = 1

for i in range(n):
    startNumber += i
    temp = list(range(startNumber, startNumber + (i + 1)))
    if (i + 1) % 2 == 0:
        temp.reverse()
    print(' '.join(map(str, temp)))