paperCount = int(input())
whitePaper = [[0] * 100 for _ in range(100)]
result = 0

for _ in range(paperCount):
    px, py = map(int, input().split())
    for i in range(px, px + 10):
        for j in range(py, py + 10):
            if whitePaper[i][j] == 0:
                whitePaper[i][j] = 1
                result += 1

print(result)