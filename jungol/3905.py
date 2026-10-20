import sys
input = sys.stdin.readline

n = int(input())
cp = [list(map(int, input().split())) for _ in range(n)]

def cal_dis(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

non_skip_dis = 0
for i in range(n-1):
    non_skip_dis += cal_dis(cp[i], cp[i+1])

max_saved_dis = 0
for i in range(1, n-1):
    saved_dis = cal_dis(cp[i-1], cp[i]) + cal_dis(cp[i], cp[i+1]) - cal_dis(cp[i-1], cp[i+1])
    max_saved_dis = max(saved_dis, max_saved_dis)

print(non_skip_dis - max_saved_dis)