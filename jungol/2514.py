# https://jungol.co.kr/problem/2514?cursor=IjYiLDUsMQ==

s = input()
koi_count, ioi_count = 0, 0
k_temp, i_temp = [], []

## K_TEMP
### [K]
### [O]

for idx, ch in enumerate(s):
    if ch == 'K':
        k_temp.append(ch)
    elif ch == 'O':
        if len(k_temp) > 0:
            if s[idx - 1] == 'K':
                k_temp.append(ch)
            else:
                k_temp = []

        if len(i_temp) > 0:
            if s[idx - 1] == 'I':
                i_temp.append(ch)
            else:
                i_temp = []
    elif ch == 'I':
        if len(k_temp) > 1:
            if s[idx - 1] == 'O' and s[idx - 2] == 'K':
                koi_count += 1
                k_temp = ['I']
        if len(i_temp) > 1:
            if s[idx - 1] == 'O' and s[idx - 2] == 'I':
                ioi_count += 1
                i_temp = ['I']
        else:
            i_temp.append(ch)
    else:
        k_temp = []
        i_temp = []


print(koi_count)
print(ioi_count)