n = int(input())
cow = input().rstrip()

c_count, co_count, cow_count = 0, 0, 0

for c in cow:
    if c == 'C':
        c_count += 1
    elif c == 'O':
        co_count += c_count
    else:
        cow_count += co_count

print(cow_count)