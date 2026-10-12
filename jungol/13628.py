esc_len = list(map(int, input().split()))
hp = int(input())

result = 13215152131251

for a in range(2):
    for b in range(2):
        for c in range(2):
            walks = [a, b, c]
            time, hp_cost = 0, 0
            for i in range(3):
                if walks[i] == 1:
                    time += esc_len[i] // 2
                    hp_cost += esc_len[i] // 2
                else:
                    time += esc_len[i]

            if hp_cost < hp:
                result = min(result, time)

print(result)