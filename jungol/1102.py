# https://jungol.co.kr/problem/1102?cursor=IjYiLDcsNA==

n = int(input())

stack = []
for _ in range(n):
    cmd = input().split()

    if cmd[0] == 'i':
        stack.append(cmd[1])
    elif cmd[0] == 'c':
        print(len(stack))
    elif cmd[0] == 'o':
        if len(stack) == 0:
            print("empty")
        else:
            print(stack.pop())