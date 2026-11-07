# https://jungol.co.kr/problem/1697?cursor=IjYiLDcsNw==

n = int(input())

queue = []
for _ in range(n):
    cmd = input().split()

    if cmd[0] == 'i':
        queue.append(cmd[1])
    elif cmd[0] == 'c':
        print(len(queue))
    else:
        if len(queue) == 0:
            print("empty")
        else:
            print(queue.pop(0))
