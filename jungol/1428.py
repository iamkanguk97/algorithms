A,B,C,W = map(int, input().split())
result = 123151321412

for x in range(W + 1):
    for y in range(W + 1):
        for z in range(W + 1):
            if A * x + B * y + C * z == W:
                result = min(result, x + y + z)

print(result)