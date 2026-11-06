# https://jungol.co.kr/problem/2857?cursor=IjYiLDUsMg==

arr = []
for _ in range(5):
    chs = input()
    arr.append(list(chs) + [''] * (15 - len(chs)))

for i in range(15):
    for j in range(5):
        print(arr[j][i], end='')