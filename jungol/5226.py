lr = input().strip()
best = score = lr.count('R')

for c in lr:
    if c == 'L':
        score += 1
    else:
        score -= 1
    best = max(best, score)

print(best)