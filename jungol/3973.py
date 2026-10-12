N, B = map(int, input().split())

cow_pos = []
for _ in range(N):
    cow_pos.append(list(map(int, input().split())))

def solution():
    answer = N

    for a in [cp[0] + 1 for cp in cow_pos]:
        for b in [cp[1] + 1 for cp in cow_pos]:
            c1, c2, c3, c4 = 0, 0, 0, 0
            for cp in cow_pos:
                if cp[0] < a and cp[1] < b:
                    c1 += 1
                elif cp[0] < a and b < cp[1] <= B:
                    c2 += 1
                elif a < cp[0] <= B and cp[1] < b:
                    c3 += 1
                else:
                    c4 += 1

            answer = min(answer, max(c1, c2, c3, c4))

    return answer

print(solution())