# https://jungol.co.kr/problem/1535?cursor=IjYiLDUsNA==

arr = []
isCheck = set()

while True:
    s = input()
    if s == 'END':
        break
    s_arr = s.split()
    for x in s_arr:
        if x not in isCheck:
            isCheck.add(x)
            arr.append(x)
    print(*arr)