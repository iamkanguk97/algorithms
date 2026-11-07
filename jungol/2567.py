# https://jungol.co.kr/problem/2567?cursor=IjYiLDgsNg==

def fn(num):
    result = (num * n) % p

    # 탈출조건
    if result in temp:
        return len(temp) - temp.index(result)

    temp.append(result)
    return fn(result)


n, p = map(int, input().split())
temp = []

print(fn(n))
