n = int(input())
case = [list(map(int, input().split())) for _ in range(n)]
count = 0

def get_sb(num, target):
    str_num = str(num)
    str_target = str(target)
    s_count, b_count = 0, 0

    for i in range(3):
        for j in range(3):
            if str_num[i] == str_target[j]:
                if i == j:
                    s_count += 1
                    continue
                b_count += 1

    return s_count, b_count


for i in range(123, 988):
    if '0' in str(i) or len(set(str(i))) != 3:
        continue
    isCorrect = True
    for c, s, b in case:
        s_count, b_count = get_sb(i, c)
        if s != s_count or b != b_count:
            isCorrect = False
            break

    if isCorrect:
        count += 1

print(count)
