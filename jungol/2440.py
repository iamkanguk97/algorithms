n = int(input())
count = 0
isFinished = False

while n >= 0:
    if n % 5 == 0:
        count += n // 5
        isFinished = True
        break
    n -= 3
    count += 1

if isFinished:
    print(count)
else:
    print(-1)