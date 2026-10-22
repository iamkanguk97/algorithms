import sys
input = sys.stdin.readline

t = int(input())
queries = [tuple(map(int, input().split())) for _ in range(t)]
prefix = [0] * 10001

for i in range(1, 10001):
    digits = str(i)
    check_result = len(set(digits)) == len(digits)
    prefix[i] = prefix[i - 1] + check_result

for q in queries:
    n, m = q
    print(prefix[m] - prefix[n - 1])