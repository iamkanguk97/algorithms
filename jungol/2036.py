import sys
input = sys.stdin.readline

n, m = map(int, input().split())
pi = sorted(int(input()) for _ in range(m))
profit, selectPi = 0, 0

for idx, p in enumerate(pi):
    curr_profit = p * min(n, m - idx)
    if profit < curr_profit:
        profit, selectPi = curr_profit, p

print(selectPi, profit)