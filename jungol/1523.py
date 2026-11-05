# https://jungol.co.kr/problem/1523?cursor=IjYiLDQsMA==

def print_type1():
    for i in range(n):
        for j in range(0, i+1):
            print('*', end='')
        print()

def print_type2():
    for i in range(n):
        for j in range(n-i, 0, -1):
            print('*', end='')
        print()

def print_type3():
    for i in range(n):
        print(' ' * (n-i-1) +  '*' * (2*i + 1))

def render():
    if m == 1:
        print_type1()
    elif m == 2:
        print_type2()
    else:
        print_type3()

n, m = map(int, input().split())

if n < 1 or n > 100 or m < 1 or m > 3:
    print("INPUT ERROR!")
else:
    render()