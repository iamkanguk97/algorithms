s = input()

result = 0
for idx in range(len(s)):
    if idx == 0:
        result += 10
        continue
    result += 5 if s[idx-1] == s[idx] else 10

print(result)